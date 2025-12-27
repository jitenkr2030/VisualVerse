"""
File Operations Utilities for VisualVerse Engine

Safe wrappers for file system operations, temporary directory management,
and cloud storage upload helpers.
"""

import os
import shutil
import tempfile
import hashlib
import mimetypes
from pathlib import Path
from typing import Optional, List, Dict, Any, Union, BinaryIO, TextIO
from dataclasses import dataclass
from enum import Enum
import logging
import json
import csv
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class FileType(Enum):
    """File type enumeration"""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    ARCHIVE = "archive"
    CODE = "code"
    DATA = "data"
    UNKNOWN = "unknown"

@dataclass
class FileInfo:
    """File information wrapper"""
    path: Path
    size: int
    modified: float
    created: float
    type: FileType
    mime_type: Optional[str]
    hash_md5: Optional[str] = None
    hash_sha256: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "path": str(self.path),
            "size": self.size,
            "modified": self.modified,
            "created": self.created,
            "type": self.type.value,
            "mime_type": self.mime_type,
            "hash_md5": self.hash_md5,
            "hash_sha256": self.hash_sha256
        }

class FileOperations:
    """File operations utility class"""
    
    # Common image extensions
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'}
    
    # Common video extensions
    VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv'}
    
    # Common audio extensions
    AUDIO_EXTENSIONS = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'}
    
    # Common document extensions
    DOCUMENT_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'}
    
    # Common archive extensions
    ARCHIVE_EXTENSIONS = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'}
    
    # Common code extensions
    CODE_EXTENSIONS = {'.py', '.js', '.ts', '.html', '.css', '.java', '.cpp', '.c', '.go', '.rs', '.php'}
    
    # Common data extensions
    DATA_EXTENSIONS = {'.json', '.xml', '.csv', '.yaml', '.yml', '.ini', '.cfg', '.toml'}
    
    @classmethod
    def get_file_type(cls, file_path: Union[str, Path]) -> FileType:
        """Determine file type from extension"""
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension in cls.IMAGE_EXTENSIONS:
            return FileType.IMAGE
        elif extension in cls.VIDEO_EXTENSIONS:
            return FileType.VIDEO
        elif extension in cls.AUDIO_EXTENSIONS:
            return FileType.AUDIO
        elif extension in cls.DOCUMENT_EXTENSIONS:
            return FileType.DOCUMENT
        elif extension in cls.ARCHIVE_EXTENSIONS:
            return FileType.ARCHIVE
        elif extension in cls.CODE_EXTENSIONS:
            return FileType.CODE
        elif extension in cls.DATA_EXTENSIONS:
            return FileType.DATA
        else:
            return FileType.UNKNOWN
    
    @classmethod
    def get_mime_type(cls, file_path: Union[str, Path]) -> Optional[str]:
        """Get MIME type for file"""
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type
    
    @classmethod
    def get_file_info(cls, file_path: Union[str, Path], calculate_hashes: bool = True) -> FileInfo:
        """Get comprehensive file information"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = file_path.stat()
        file_type = cls.get_file_type(file_path)
        mime_type = cls.get_mime_type(file_path)
        
        info = FileInfo(
            path=file_path,
            size=stat.st_size,
            modified=stat.st_mtime,
            created=stat.st_ctime,
            type=file_type,
            mime_type=mime_type
        )
        
        if calculate_hashes and file_path.is_file():
            info.hash_md5 = cls.calculate_md5(file_path)
            info.hash_sha256 = cls.calculate_sha256(file_path)
        
        return info
    
    @classmethod
    def safe_mkdir(cls, directory: Union[str, Path], parents: bool = True, exist_ok: bool = True) -> Path:
        """Safely create directory"""
        directory = Path(directory)
        
        try:
            directory.mkdir(parents=parents, exist_ok=exist_ok)
            logger.debug(f"Created directory: {directory}")
            return directory
        except Exception as e:
            logger.error(f"Failed to create directory {directory}: {e}")
            raise
    
    @classmethod
    def safe_remove(cls, path: Union[str, Path], recursive: bool = False, force: bool = False) -> bool:
        """Safely remove file or directory"""
        path = Path(path)
        
        try:
            if path.is_file() or (path.is_symlink() and not recursive):
                if force or path.exists():
                    path.unlink()
                    logger.debug(f"Removed file: {path}")
                    return True
            elif path.is_dir():
                if recursive:
                    shutil.rmtree(path)
                    logger.debug(f"Removed directory recursively: {path}")
                    return True
                else:
                    path.rmdir()
                    logger.debug(f"Removed empty directory: {path}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to remove {path}: {e}")
            if not force:
                raise
            return False
    
    @classmethod
    def safe_copy(cls, source: Union[str, Path], destination: Union[str, Path], 
                  overwrite: bool = False, preserve_metadata: bool = True) -> Path:
        """Safely copy file or directory"""
        source = Path(source)
        destination = Path(destination)
        
        if not source.exists():
            raise FileNotFoundError(f"Source not found: {source}")
        
        if destination.exists() and not overwrite:
            raise FileExistsError(f"Destination already exists: {destination}")
        
        try:
            if source.is_file():
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination) if preserve_metadata else shutil.copy(source, destination)
            elif source.is_dir():
                if destination.exists():
                    shutil.rmtree(destination)
                shutil.copytree(source, destination, dirs_exist_ok=overwrite)
            else:
                raise ValueError(f"Source is neither file nor directory: {source}")
            
            logger.debug(f"Copied {source} to {destination}")
            return destination
        except Exception as e:
            logger.error(f"Failed to copy {source} to {destination}: {e}")
            raise
    
    @classmethod
    def safe_move(cls, source: Union[str, Path], destination: Union[str, Path]) -> Path:
        """Safely move file or directory"""
        source = Path(source)
        destination = Path(destination)
        
        if not source.exists():
            raise FileNotFoundError(f"Source not found: {source}")
        
        try:
            # Handle cross-filesystem moves
            if destination.parent != source.parent:
                # Copy then remove
                cls.safe_copy(source, destination)
                cls.safe_remove(source)
            else:
                # Simple rename
                source.rename(destination)
            
            logger.debug(f"Moved {source} to {destination}")
            return destination
        except Exception as e:
            logger.error(f"Failed to move {source} to {destination}: {e}")
            raise
    
    @classmethod
    def calculate_md5(cls, file_path: Union[str, Path]) -> str:
        """Calculate MD5 hash of file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        hash_md5 = hashlib.md5()
        
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate MD5 for {file_path}: {e}")
            raise
    
    @classmethod
    def calculate_sha256(cls, file_path: Union[str, Path]) -> str:
        """Calculate SHA256 hash of file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        hash_sha256 = hashlib.sha256()
        
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate SHA256 for {file_path}: {e}")
            raise
    
    @classmethod
    def compare_files(cls, file1: Union[str, Path], file2: Union[str, Path]) -> Dict[str, Any]:
        """Compare two files"""
        file1 = Path(file1)
        file2 = Path(file2)
        
        result = {
            "exists": file1.exists() and file2.exists(),
            "same_size": False,
            "same_hash": False,
            "same_content": False,
            "file1_info": None,
            "file2_info": None
        }
        
        if not (file1.exists() and file2.exists()):
            return result
        
        try:
            info1 = cls.get_file_info(file1)
            info2 = cls.get_file_info(file2)
            
            result["file1_info"] = info1.to_dict()
            result["file2_info"] = info2.to_dict()
            
            result["same_size"] = info1.size == info2.size
            
            if result["same_size"]:
                hash1 = cls.calculate_md5(file1)
                hash2 = cls.calculate_md5(file2)
                result["same_hash"] = hash1 == hash2
                
                if result["same_hash"]:
                    result["same_content"] = True
            
            return result
        except Exception as e:
            logger.error(f"Failed to compare files {file1} and {file2}: {e}")
            result["error"] = str(e)
            return result
    
    @classmethod
    def find_files(cls, directory: Union[str, Path], pattern: str = "*", 
                   recursive: bool = True, file_type: Optional[FileType] = None) -> List[Path]:
        """Find files matching pattern"""
        directory = Path(directory)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        if not directory.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")
        
        try:
            if recursive:
                files = list(directory.rglob(pattern))
            else:
                files = list(directory.glob(pattern))
            
            if file_type:
                files = [f for f in files if f.is_file() and cls.get_file_type(f) == file_type]
            else:
                files = [f for f in files if f.is_file()]
            
            return sorted(files)
        except Exception as e:
            logger.error(f"Failed to find files in {directory} with pattern {pattern}: {e}")
            raise
    
    @classmethod
    def ensure_unique_filename(cls, file_path: Union[str, Path]) -> Path:
        """Ensure filename is unique by adding counter if needed"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return file_path
        
        stem = file_path.stem
        suffix = file_path.suffix
        parent = file_path.parent
        
        counter = 1
        while True:
            new_path = parent / f"{stem}_{counter}{suffix}"
            if not new_path.exists():
                return new_path
            counter += 1
    
    @classmethod
    def get_file_size_human(cls, size_bytes: int) -> str:
        """Get human-readable file size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

@contextmanager
def temporary_directory(prefix: str = "visualverse_", suffix: str = "", delete: bool = True):
    """Context manager for temporary directory"""
    temp_dir = tempfile.mkdtemp(prefix=prefix, suffix=suffix)
    
    try:
        yield Path(temp_dir)
    finally:
        if delete:
            try:
                shutil.rmtree(temp_dir)
                logger.debug(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary directory {temp_dir}: {e}")

@contextmanager
def temporary_file(prefix: str = "visualverse_", suffix: str = "", 
                   delete: bool = True, text: bool = False):
    """Context manager for temporary file"""
    if text:
        temp_file = tempfile.NamedTemporaryFile(mode='w', prefix=prefix, suffix=suffix, delete=False)
        temp_file.close()
        temp_path = Path(temp_file.name)
    else:
        temp_path = Path(tempfile.mktemp(prefix=prefix, suffix=suffix))
    
    try:
        yield temp_path
    finally:
        if delete:
            try:
                if temp_path.exists():
                    temp_path.unlink()
                    logger.debug(f"Cleaned up temporary file: {temp_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary file {temp_path}: {e}")

def safe_read_text(file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
    """Safely read text file with error handling"""
    file_path = Path(file_path)
    
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with different encodings
        for enc in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError(f"Could not decode file with any encoding: {file_path}")
    except Exception as e:
        logger.error(f"Failed to read text file {file_path}: {e}")
        raise

def safe_write_text(file_path: Union[str, Path], content: str, 
                   encoding: str = 'utf-8', create_dirs: bool = True) -> None:
    """Safely write text file with directory creation"""
    file_path = Path(file_path)
    
    try:
        if create_dirs:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        
        logger.debug(f"Wrote text file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to write text file {file_path}: {e}")
        raise

def safe_read_json(file_path: Union[str, Path], encoding: str = 'utf-8') -> Dict[str, Any]:
    """Safely read JSON file"""
    content = safe_read_text(file_path, encoding)
    
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {file_path}: {e}")
        raise

def safe_write_json(file_path: Union[str, Path], data: Dict[str, Any], 
                   indent: int = 2, create_dirs: bool = True) -> None:
    """Safely write JSON file"""
    content = json.dumps(data, indent=indent, ensure_ascii=False)
    safe_write_text(file_path, content, create_dirs=create_dirs)

def safe_read_csv(file_path: Union[str, Path], encoding: str = 'utf-8') -> List[Dict[str, str]]:
    """Safely read CSV file"""
    file_path = Path(file_path)
    
    try:
        with open(file_path, 'r', encoding=encoding, newline='') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        logger.error(f"Failed to read CSV file {file_path}: {e}")
        raise

def safe_write_csv(file_path: Union[str, Path], data: List[Dict[str, Any]], 
                  create_dirs: bool = True) -> None:
    """Safely write CSV file"""
    file_path = Path(file_path)
    
    try:
        if create_dirs:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not data:
            return
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        logger.debug(f"Wrote CSV file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to write CSV file {file_path}: {e}")
        raise

# Cloud storage helpers (placeholder implementations)
class CloudStorageHelper:
    """Placeholder for cloud storage operations"""
    
    def __init__(self, provider: str = "local"):
        self.provider = provider
    
    def upload_file(self, local_path: Union[str, Path], remote_path: str) -> Dict[str, Any]:
        """Upload file to cloud storage"""
        # Placeholder implementation
        return {
            "success": True,
            "provider": self.provider,
            "remote_path": remote_path,
            "local_path": str(local_path)
        }
    
    def download_file(self, remote_path: str, local_path: Union[str, Path]) -> Dict[str, Any]:
        """Download file from cloud storage"""
        # Placeholder implementation
        return {
            "success": True,
            "provider": self.provider,
            "remote_path": remote_path,
            "local_path": str(local_path)
        }
    
    def delete_file(self, remote_path: str) -> Dict[str, Any]:
        """Delete file from cloud storage"""
        # Placeholder implementation
        return {
            "success": True,
            "provider": self.provider,
            "remote_path": remote_path
        }
    
    def generate_presigned_url(self, remote_path: str, expires_in: int = 3600) -> str:
        """Generate presigned URL for file access"""
        # Placeholder implementation
        return f"https://example.com/presigned/{remote_path}?expires={expires_in}"