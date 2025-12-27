"""
Animation Metadata Service for VisualVerse Content Metadata Layer

This service manages the relationship between concept knowledge and visual
animation assets, enabling searchable visual content and intelligent
content reuse across subject domains.

Licensed under the Apache License, Version 2.0
"""

from typing import List, Optional, Dict, Any, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
import os
import re
from collections import defaultdict
import json

from ..models.visual_meta import (
    AnimationAsset,
    ConceptVisualMapping,
    VisualLearningPath,
    AssetFormat,
    AssetType,
    RelevanceType,
    AssetComplexity,
    AssetStatus,
    AssetSearchRequest,
    AssetSearchResult,
    AssetGenerationRequest,
    parse_asset_path,
    extract_keywords_from_description
)


logger = logging.getLogger(__name__)


class AnimationServiceStats:
    """Statistics for animation service operations"""
    
    def __init__(self):
        self.total_assets: int = 0
        self.total_mappings: int = 0
        self.total_paths: int = 0
        self.assets_by_format: Dict[str, int] = defaultdict(int)
        self.assets_by_subject: Dict[str, int] = defaultdict(int)
        self.concepts_with_visuals: int = 0
        self.last_scan_time: Optional[datetime] = None
        self.last_scan_assets: int = 0
        self.auto_tagged_count: int = 0
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'total_assets': self.total_assets,
            'total_mappings': self.total_mappings,
            'total_paths': self.total_paths,
            'assets_by_format': dict(self.assets_by_format),
            'assets_by_subject': dict(self.assets_by_subject),
            'concepts_with_visuals': self.concepts_with_visuals,
            'last_scan_time': self.last_scan_time.isoformat() if self.last_scan_time else None,
            'last_scan_assets': self.last_scan_assets,
            'auto_tagged_count': self.auto_tagged_count
        }


class AnimationMetadataService:
    """
    Service for managing animation assets and their relationship to concepts.
    
    This service provides functionality for:
    - Indexing animation assets from the file system
    - Managing concept-to-animation mappings
    - Searching assets by various criteria
    - Generating visual learning paths
    """
    
    def __init__(
        self,
        assets_root: str = "/workspace/visualverse/engine/animation-engine/assets",
        storage_path: str = "/tmp/visualverse/visual-meta"
    ):
        """
        Initialize the animation metadata service.
        
        Args:
            assets_root: Root directory of animation assets
            storage_path: Path for storing metadata
        """
        self.assets_root = assets_root
        self.storage_path = storage_path
        self._assets: Dict[str, AnimationAsset] = {}
        self._mappings: Dict[str, ConceptVisualMapping] = {}
        self._paths: Dict[str, VisualLearningPath] = {}
        self._concept_to_assets: Dict[str, List[str]] = defaultdict(list)  # concept_id -> asset_ids
        self._stats = AnimationServiceStats()
        
        # Ensure storage directory exists
        os.makedirs(storage_path, exist_ok=True)
        
        # Load existing data
        self._load_from_storage()
    
    # =========================================================================
    # Asset Management
    # =========================================================================
    
    def scan_and_index_assets(
        self,
        directory: Optional[str] = None,
        recursive: bool = True,
        file_extensions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Scan directory and index animation assets.
        
        Args:
            directory: Directory to scan (defaults to assets_root)
            recursive: Whether to scan subdirectories
            file_extensions: Specific extensions to look for
            
        Returns:
            Scan results dictionary
        """
        scan_dir = directory or self.assets_root
        
        if file_extensions is None:
            file_extensions = ['.mp4', '.gif', '.webp', '.svg', '.json', '.html']
        
        start_time = datetime.now()
        results = {
            'scanned': 0,
            'new': 0,
            'updated': 0,
            'errors': [],
            'skipped': []
        }
        
        # Supported format mapping
        format_map = {
            '.mp4': AssetFormat.MP4,
            '.gif': AssetFormat.GIF,
            '.webp': AssetFormat.WEBP,
            '.svg': AssetFormat.SVG,
            '.json': AssetFormat.LOTTIE,
            '.html': AssetFormat.HTML5
        }
        
        try:
            for root, dirs, files in os.walk(scan_dir):
                for filename in files:
                    file_ext = os.path.splitext(filename)[1].lower()
                    
                    if file_ext not in file_extensions:
                        continue
                    
                    results['scanned'] += 1
                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, self.assets_root)
                    
                    # Parse asset metadata
                    parsed = parse_asset_path(relative_path, self.assets_root)
                    
                    # Get file size
                    file_size = os.path.getsize(file_path)
                    
                    # Generate asset key
                    asset_key = parsed['asset_key']
                    
                    # Check if asset already exists
                    existing = self._find_asset_by_key(asset_key)
                    
                    # Determine asset type from path and format
                    asset_type = self._determine_asset_type(asset_key, parsed['format'])
                    
                    # Create asset
                    asset = AnimationAsset(
                        asset_key=asset_key,
                        file_name=parsed['file_name'],
                        display_name=self._generate_display_name(filename),
                        description=self._generate_description(asset_key),
                        file_path=relative_path,
                        file_size_bytes=file_size,
                        format=AssetFormat(parsed['format']),
                        asset_type=asset_type,
                        status=AssetStatus.DRAFT
                    )
                    
                    if existing:
                        # Update existing
                        asset.id = existing.id
                        asset.status = existing.status
                        asset.concept_ids = existing.concept_ids
                        asset.tags = existing.tags
                        asset.keywords = existing.keywords
                        self._assets[asset.id] = asset
                        results['updated'] += 1
                    else:
                        # Create new
                        self._assets[asset.id] = asset
                        results['new'] += 1
                
                if not recursive:
                    break
        
        except Exception as e:
            results['errors'].append(f"Scan error: {str(e)}")
            logger.error(f"Error scanning assets: {e}")
        
        # Update statistics
        self._stats.total_assets = len(self._assets)
        self._stats.last_scan_time = start_time
        self._stats.last_scan_assets = results['scanned']
        
        # Update format and subject counts
        for asset in self._assets.values():
            self._stats.assets_by_format[asset.format.value] += 1
            for subj in asset.subject_ids:
                self._stats.assets_by_subject[subj] += 1
        
        # Save to storage
        self._save_to_storage()
        
        logger.info(
            f"Asset scan complete: {results['scanned']} scanned, "
            f"{results['new']} new, {results['updated']} updated"
        )
        
        return results
    
    def _find_asset_by_key(self, asset_key: str) -> Optional[AnimationAsset]:
        """Find an asset by its key"""
        for asset in self._assets.values():
            if asset.asset_key == asset_key:
                return asset
        return None
    
    def _determine_asset_type(self, asset_key: str, format_type: str) -> AssetType:
        """Determine asset type from path and format"""
        key_lower = asset_key.lower()
        
        if 'diagram' in key_lower:
            return AssetType.DIAGRAM
        elif 'chart' in key_lower:
            return AssetType.CHART
        elif 'interactive' in key_lower:
            return AssetType.INTERACTIVE
        elif 'simulation' in key_lower:
            return AssetType.SIMULATION
        elif format_type == 'lottie':
            return AssetType.INTERACTIVE
        elif format_type == 'svg':
            return AssetType.DIAGRAM
        
        return AssetType.ANIMATION
    
    def _generate_display_name(self, filename: str) -> str:
        """Generate a display name from filename"""
        name = os.path.splitext(filename)[0]
        # Convert kebab-case to Title Case
        name = ' '.join(word.capitalize() for word in name.replace('-', ' ').split())
        return name
    
    def _generate_description(self, asset_key: str) -> str:
        """Generate a description from asset key"""
        parts = asset_key.split('/')
        if len >= 2:
            subject = parts[0].title()
            topic = ' '.join(p.title() for p in parts[1].split('-')[:3])
            return f"{subject} animation about {topic}"
        return f"Animation: {asset_key}"
    
    def get_asset(self, asset_id: str) -> Optional[AnimationAsset]:
        """Get an asset by ID"""
        return self._assets.get(asset_id)
    
    def list_assets(
        self,
        subject_id: Optional[str] = None,
        format_type: Optional[AssetFormat] = None,
        status: Optional[AssetStatus] = None,
        page: int = 1,
        page_size: int = 20
    ) -> List[AnimationAsset]:
        """List assets with optional filtering"""
        results = list(self._assets.values())
        
        if subject_id:
            results = [a for a in results if subject_id in a.subject_ids]
        
        if format_type:
            results = [a for a in results if a.format == format_type]
        
        if status:
            results = [a for a in results if a.status == status]
        
        # Paginate
        start = (page - 1) * page_size
        return results[start:start + page_size]
    
    def update_asset(self, asset_id: str, updates: Dict[str, Any]) -> Optional[AnimationAsset]:
        """Update an asset's metadata"""
        asset = self._assets.get(asset_id)
        if not asset:
            return None
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(asset, key):
                setattr(asset, key, value)
        
        asset.updated_at = datetime.now()
        
        # Save changes
        self._save_to_storage()
        
        return asset
    
    def delete_asset(self, asset_id: str) -> bool:
        """Delete an asset"""
        if asset_id not in self._assets:
            return False
        
        asset = self._assets[asset_id]
        
        # Remove from mappings
        for mapping_id in list(self._mappings.keys()):
            mapping = self._mappings[mapping_id]
            if mapping.asset_id == asset_id:
                del self._mappings[mapping_id]
        
        # Remove from concept index
        for cid in list(self._concept_to_assets.keys()):
            if asset_id in self._concept_to_assets[cid]:
                self._concept_to_assets[cid].remove(asset_id)
        
        del self._assets[asset_id]
        self._save_to_storage()
        
        return True
    
    # =========================================================================
    # Concept-Asset Mapping
    # =========================================================================
    
    def create_mapping(
        self,
        concept_id: str,
        asset_id: str,
        relevance_type: RelevanceType,
        relevance_score: float = 1.0,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        is_automatic: bool = False,
        confidence_score: float = 0.5
    ) -> ConceptVisualMapping:
        """
        Create a mapping between a concept and an asset.
        
        Args:
            concept_id: Concept ID
            asset_id: Asset ID
            relevance_type: How the asset relates to the concept
            relevance_score: Strength of relevance (0-1)
            start_time: Optional start time for segment
            end_time: Optional end time for segment
            is_automatic: Whether this was auto-generated
            confidence_score: Confidence in auto-generated mapping
            
        Returns:
            Created mapping
        """
        # Validate IDs exist
        if concept_id not in self._concept_to_assets:
            logger.warning(f"Concept {concept_id} may not exist in knowledge graph")
        
        if asset_id not in self._assets:
            raise ValueError(f"Asset {asset_id} not found")
        
        # Check for existing mapping
        existing = self._find_existing_mapping(concept_id, asset_id)
        if existing:
            # Update existing
            existing.relevance_type = relevance_type
            existing.relevance_score = relevance_score
            existing.start_time = start_time
            existing.end_time = end_time
            existing.is_automatic = is_automatic
            existing.confidence_score = confidence_score
            existing.updated_at = datetime.now()
            mapping = existing
        else:
            # Create new
            mapping = ConceptVisualMapping(
                concept_id=concept_id,
                asset_id=asset_id,
                relevance_type=relevance_type,
                relevance_score=relevance_score,
                start_time=start_time,
                end_time=end_time,
                is_automatic=is_automatic,
                confidence_score=confidence_score
            )
            self._mappings[mapping.id] = mapping
        
        # Update indexes
        self._concept_to_assets[concept_id].append(asset_id)
        self._concept_to_assets[concept_id] = list(set(self._concept_to_assets[concept_id]))
        
        # Update asset concept list
        asset = self._assets[asset_id]
        if concept_id not in asset.concept_ids:
            asset.concept_ids.append(concept_id)
            if asset.primary_concept_id is None:
                asset.primary_concept_id = concept_id
        
        # Update statistics
        self._stats.total_mappings = len(self._mappings)
        self._stats.concepts_with_visuals = len(self._concept_to_assets)
        
        # Save
        self._save_to_storage()
        
        logger.info(f"Created mapping: {concept_id} <-> {asset_id} ({relevance_type.value})")
        
        return mapping
    
    def _find_existing_mapping(
        self,
        concept_id: str,
        asset_id: str
    ) -> Optional[ConceptVisualMapping]:
        """Find existing mapping between concept and asset"""
        for mapping in self._mappings.values():
            if mapping.concept_id == concept_id and mapping.asset_id == asset_id:
                return mapping
        return None
    
    def get_mappings_for_concept(
        self,
        concept_id: str,
        relevance_types: Optional[List[RelevanceType]] = None,
        approved_only: bool = False
    ) -> List[ConceptVisualMapping]:
        """Get all mappings for a concept"""
        results = [
            m for m in self._mappings.values()
            if m.concept_id == concept_id
        ]
        
        if relevance_types:
            results = [m for m in results if m.relevance_type in relevance_types]
        
        if approved_only:
            results = [m for m in results if m.is_approved]
        
        return results
    
    def get_mappings_for_asset(
        self,
        asset_id: str
    ) -> List[ConceptVisualMapping]:
        """Get all mappings for an asset"""
        return [
            m for m in self._mappings.values()
            if m.asset_id == asset_id
        ]
    
    def approve_mapping(
        self,
        mapping_id: str,
        notes: Optional[str] = None
    ) -> Optional[ConceptVisualMapping]:
        """Approve a mapping"""
        mapping = self._mappings.get(mapping_id)
        if not mapping:
            return None
        
        mapping.is_approved = True
        mapping.approval_notes = notes
        mapping.updated_at = datetime.now()
        
        self._save_to_storage()
        
        return mapping
    
    def delete_mapping(self, mapping_id: str) -> bool:
        """Delete a mapping"""
        if mapping_id not in self._mappings:
            return False
        
        mapping = self._mappings[mapping_id]
        
        # Remove from concept index
        if mapping.concept_id in self._concept_to_assets:
            if mapping.asset_id in self._concept_to_assets[mapping.concept_id]:
                self._concept_to_assets[mapping.concept_id].remove(mapping.asset_id)
        
        del self._mappings[mapping_id]
        self._stats.total_mappings = len(self._mappings)
        
        self._save_to_storage()
        
        return True
    
    # =========================================================================
    # Asset Search
    # =========================================================================
    
    def search_assets(self, request: AssetSearchRequest) -> AssetSearchResult:
        """
        Search for animation assets.
        
        Args:
            request: Search request with criteria
            
        Returns:
            Search results with pagination
        """
        results = list(self._assets.values())
        
        # Filter by query
        if request.query:
            query_lower = request.query.lower()
            results = [
                a for a in results
                if (query_lower in a.display_name.lower() or
                    query_lower in a.description.lower() or
                    any(query_lower in t for t in a.tags) or
                    any(query_lower in k for k in a.keywords))
            ]
        
        # Filter by concept
        if request.concept_ids:
            results = [
                a for a in results
                if any(cid in a.concept_ids for cid in request.concept_ids)
            ]
        
        # Filter by subject
        if request.subject_ids:
            results = [
                a for a in results
                if any(sid in a.subject_ids for sid in request.subject_ids)
            ]
        
        # Filter by format
        if request.format:
            results = [a for a in results if a.format == request.format]
        
        # Filter by asset type
        if request.asset_type:
            results = [a for a in results if a.asset_type == request.asset_type]
        
        # Filter by relevance types (via mappings)
        if request.relevance_types:
            relevant_asset_ids = set()
            for mapping in self._mappings.values():
                if mapping.relevance_type in request.relevance_types:
                    relevant_asset_ids.add(mapping.asset_id)
            results = [a for a in results if a.id in relevant_asset_ids]
        
        # Filter by quality
        results = [a for a in results if a.quality_score >= request.min_quality]
        
        # Filter by duration
        if request.min_duration is not None:
            results = [a for a in results if a.duration_seconds and a.duration_seconds >= request.min_duration]
        if request.max_duration is not None:
            results = [a for a in results if a.duration_seconds and a.duration_seconds <= request.max_duration]
        
        # Filter by tags
        if request.tags:
            results = [
                a for a in results
                if any(t in a.tags for t in request.tags)
            ]
        
        # Filter by audio
        if request.has_audio is not None:
            results = [a for a in results if a.has_audio == request.has_audio]
        
        # Sort results
        if request.sort_by == 'relevance':
            results.sort(key=lambda a: a.quality_score, reverse=True)
        elif request.sort_by == 'date':
            results.sort(key=lambda a: a.created_at, reverse=(request.sort_order == 'desc'))
        elif request.sort_by == 'duration':
            results.sort(
                key=lambda a: a.duration_seconds or 0,
                reverse=(request.sort_order == 'desc')
            )
        elif request.sort_by == 'quality':
            results.sort(key=lambda a: a.quality_score, reverse=(request.sort_order == 'desc'))
        
        # Calculate facets
        facets = self._calculate_facets(results)
        
        # Paginate
        total = len(results)
        start = (request.page - 1) * request.page_size
        paginated_results = results[start:start + request.page_size]
        
        # Convert to response format
        assets_data = [
            {
                'id': a.id,
                'asset_key': a.asset_key,
                'display_name': a.display_name,
                'description': a.description,
                'format': a.format.value,
                'asset_type': a.asset_type.value,
                'duration_seconds': a.duration_seconds,
                'quality_score': a.quality_score,
                'concepts': a.concept_ids,
                'subjects': a.subject_ids,
                'tags': a.tags,
                'has_audio': a.has_audio,
                'thumbnail_url': f"/api/v1/animations/{a.id}/thumbnail",
                'view_url': f"/api/v1/animations/{a.id}/view"
            }
            for a in paginated_results
        ]
        
        return AssetSearchResult(
            assets=assets_data,
            total_count=total,
            page=request.page,
            page_size=request.page_size,
            has_next=(start + request.page_size) < total,
            facets=facets
        )
    
    def _calculate_facets(self, assets: List[AnimationAsset]) -> Dict[str, Dict[str, int]]:
        """Calculate search facets from results"""
        facets = {
            'formats': {},
            'subjects': {},
            'types': {},
            'tags': {}
        }
        
        for asset in assets:
            # Format facets
            fmt = asset.format.value
            facets['formats'][fmt] = facets['formats'].get(fmt, 0) + 1
            
            # Subject facets
            for subj in asset.subject_ids:
                facets['subjects'][subj] = facets['subjects'].get(subj, 0) + 1
            
            # Type facets
            atype = asset.asset_type.value
            facets['types'][atype] = facets['types'].get(atype, 0) + 1
            
            # Tag facets (top 10)
            for tag in asset.tags[:10]:
                facets['tags'][tag] = facets['tags'].get(tag, 0) + 1
        
        return facets
    
    # =========================================================================
    # Auto-Tagging
    # =========================================================================
    
    def auto_tag_asset(
        self,
        asset_id: str,
        concept_names: Optional[Dict[str, str]] = None
    ) -> AnimationAsset:
        """
        Automatically tag an asset based on its metadata and concept mappings.
        
        Args:
            asset_id: Asset to tag
            concept_names: Optional mapping of concept_id -> name
            
        Returns:
            Updated asset
        """
        asset = self._assets.get(asset_id)
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")
        
        new_tags = set(asset.tags)
        new_keywords = set(asset.keywords)
        
        # Extract keywords from display name and description
        new_keywords.update(extract_keywords_from_description(asset.display_name))
        if asset.description:
            new_keywords.update(extract_keywords_from_description(asset.description))
        
        # Add tags from asset key
        key_parts = asset.asset_key.replace('/', ' ').replace('-', ' ').split()
        for part in key_parts:
            if len(part) > 2:
                new_tags.add(part.lower())
        
        # Add tags from concept mappings
        for mapping in self.get_mappings_for_asset(asset_id):
            concept_id = mapping.concept_id
            
            # Get concept name
            concept_name = concept_names.get(concept_id, '') if concept_names else ''
            
            # Add concept name as tag
            if concept_name:
                new_tags.add(concept_name.lower().replace(' ', '-'))
            
            # Add relevance type as tag
            new_tags.add(mapping.relevance_type.value)
        
        # Update asset
        asset.tags = list(new_tags)
        asset.keywords = list(new_keywords)
        asset.updated_at = datetime.now()
        
        self._stats.auto_tagged_count += 1
        self._save_to_storage()
        
        logger.info(f"Auto-tagged asset {asset_id} with {len(new_tags)} tags")
        
        return asset
    
    def suggest_concepts_for_asset(
        self,
        asset_id: str,
        known_concepts: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Suggest concepts that might be related to an asset.
        
        Args:
            asset_id: Asset to analyze
            known_concepts: Known concepts with their metadata
            
        Returns:
            List of suggested concepts with confidence scores
        """
        asset = self._assets.get(asset_id)
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")
        
        suggestions = []
        
        # Create keyword set from asset
        asset_keywords = set(asset.keywords)
        asset_keywords.update(extract_keywords_from_description(asset.display_name))
        asset_keywords.update(extract_keywords_from_description(asset.description or ''))
        
        if not known_concepts:
            return suggestions
        
        # Compare with known concepts
        for concept_id, concept_data in known_concepts.items():
            concept_keywords = set(concept_data.get('keywords', []))
            concept_keywords.update(concept_data.get('tags', []))
            concept_keywords.update(extract_keywords_from_description(concept_data.get('name', '')))
            
            # Calculate overlap
            overlap = asset_keywords & concept_keywords
            if overlap:
                score = len(overlap) / len(asset_keywords | concept_keywords)
                
                suggestions.append({
                    'concept_id': concept_id,
                    'concept_name': concept_data.get('name', concept_id),
                    'confidence': score,
                    'matched_keywords': list(overlap)
                })
        
        # Sort by confidence
        suggestions.sort(key=lambda x: x['confidence'], reverse=True)
        
        return suggestions[:10]
    
    # =========================================================================
    # Visual Learning Paths
    # =========================================================================
    
    def generate_visual_path(
        self,
        concept_ids: List[str],
        path_name: str,
        path_description: Optional[str] = None,
        subject_id: str = "unknown"
    ) -> VisualLearningPath:
        """
        Generate a visual learning path from concept IDs.
        
        Args:
            concept_ids: Ordered list of concept IDs
            path_name: Name for the path
            path_description: Optional description
            subject_id: Primary subject ID
            
        Returns:
            Generated visual learning path
        """
        visual_assets = []
        total_duration = 0.0
        total_quality = 0.0
        covered_concepts = 0
        
        for concept_id in concept_ids:
            mappings = self.get_mappings_for_concept(
                concept_id,
                relevance_types=[
                    RelevanceType.PRIMARY_EXPLANATION,
                    RelevanceType.VISUAL_EXAMPLE,
                    RelevanceType.SUMMARY
                ],
                approved_only=True
            )
            
            for mapping in mappings[:2]:  # Max 2 assets per concept
                asset = self._assets.get(mapping.asset_id)
                if asset:
                    duration = mapping.end_time or asset.duration_seconds or 30.0
                    total_duration += duration
                    total_quality += asset.quality_score
                    
                    visual_assets.append({
                        'concept_id': concept_id,
                        'asset_id': mapping.asset_id,
                        'relevance_type': mapping.relevance_type.value,
                        'relevance_score': mapping.relevance_score,
                        'start_time': mapping.start_time,
                        'end_time': mapping.end_time
                    })
            
            if visual_assets and visual_assets[-1]['concept_id'] == concept_id:
                covered_concepts += 1
        
        # Calculate metrics
        asset_coverage = covered_concepts / len(concept_ids) if concept_ids else 0
        avg_quality = total_quality / len(visual_assets) if visual_assets else 0.8
        
        path = VisualLearningPath(
            name=path_name,
            description=path_description or f"Visual learning path with {len(concept_ids)} concepts",
            concept_ids=concept_ids,
            visual_assets=visual_assets,
            total_duration_seconds=total_duration,
            total_assets=len(visual_assets),
            asset_coverage=asset_coverage,
            average_asset_quality=avg_quality,
            subject_id=subject_id
        )
        
        self._paths[path.id] = path
        self._stats.total_paths += 1
        
        self._save_to_storage()
        
        logger.info(f"Generated visual path {path.id} with {len(visual_assets)} assets")
        
        return path
    
    def get_visual_path(self, path_id: str) -> Optional[VisualLearningPath]:
        """Get a visual learning path"""
        return self._paths.get(path_id)
    
    def list_visual_paths(
        self,
        subject_id: Optional[str] = None,
        published_only: bool = False
    ) -> List[VisualLearningPath]:
        """List visual learning paths"""
        results = list(self._paths.values())
        
        if subject_id:
            results = [p for p in results if p.subject_id == subject_id]
        
        if published_only:
            results = [p for p in results if p.is_published]
        
        return results
    
    def enrich_learning_path(
        self,
        path_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Enrich a text-based learning path with visual assets.
        
        Args:
            path_id: ID of the learning path
            
        Returns:
            Enriched path data with visual URLs
        """
        path = self._paths.get(path_id)
        if not path:
            return None
        
        return path.to_enriched_response()
    
    # =========================================================================
    # Storage
    # =========================================================================
    
    def _save_to_storage(self) -> None:
        """Save all data to storage"""
        try:
            # Save assets
            assets_data = {
                aid: asset.dict()
                for aid, asset in self._assets.items()
            }
            with open(os.path.join(self.storage_path, 'assets.json'), 'w') as f:
                json.dump(assets_data, f, indent=2, default=str)
            
            # Save mappings
            mappings_data = {
                mid: mapping.to_dict()
                for mid, mapping in self._mappings.items()
            }
            with open(os.path.join(self.storage_path, 'mappings.json'), 'w') as f:
                json.dump(mappings_data, f, indent=2, default=str)
            
            # Save paths
            paths_data = {
                pid: path.dict()
                for pid, path in self._paths.items()
            }
            with open(os.path.join(self.storage_path, 'paths.json'), 'w') as f:
                json.dump(paths_data, f, indent=2, default=str)
            
        except Exception as e:
            logger.error(f"Error saving to storage: {e}")
    
    def _load_from_storage(self) -> None:
        """Load data from storage"""
        try:
            # Load assets
            assets_path = os.path.join(self.storage_path, 'assets.json')
            if os.path.exists(assets_path):
                with open(assets_path, 'r') as f:
                    assets_data = json.load(f)
                    for aid, data in assets_data.items():
                        self._assets[aid] = AnimationAsset(**data)
            
            # Load mappings
            mappings_path = os.path.join(self.storage_path, 'mappings.json')
            if os.path.exists(mappings_path):
                with open(mappings_path, 'r') as f:
                    mappings_data = json.load(f)
                    for mid, data in mappings_data.items():
                        self._mappings[mid] = ConceptVisualMapping(**data)
                        self._concept_to_assets[data['concept_id']].append(data['asset_id'])
            
            # Load paths
            paths_path = os.path.join(self.storage_path, 'paths.json')
            if os.path.exists(paths_path):
                with open(paths_path, 'r') as f:
                    paths_data = json.load(f)
                    for pid, data in paths_data.items():
                        self._paths[pid] = VisualLearningPath(**data)
            
            # Update statistics
            self._stats.total_assets = len(self._assets)
            self._stats.total_mappings = len(self._mappings)
            self._stats.total_paths = len(self._paths)
            self._stats.concepts_with_visuals = len(self._concept_to_assets)
            
            logger.info(
                f"Loaded {self._stats.total_assets} assets, "
                f"{self._stats.total_mappings} mappings, "
                f"{self._stats.total_paths} paths"
            )
            
        except Exception as e:
            logger.warning(f"Error loading from storage: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get service statistics"""
        return self._stats.to_dict()
    
    def clear_cache(self) -> None:
        """Clear all cached data"""
        self._assets.clear()
        self._mappings.clear()
        self._paths.clear()
        self._concept_to_assets.clear()
        self._stats = AnimationServiceStats()
        logger.info("Cleared all animation service data")
