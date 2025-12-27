"""Initial schema for VisualVerse Content Metadata Service

Revision ID: 001_initial_schema
Revises: 
Create Date: 2025-12-25 12:50:03.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Enable UUID extension for PostgreSQL
    try:
        op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
    except Exception:
        # If not PostgreSQL or extension already exists, continue
        pass

    # Create subjects table
    op.create_table('subjects',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon_url', sa.String(500), nullable=True),
        sa.Column('color_code', sa.String(7), nullable=True),  # Hex color
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('sort_order', sa.Integer(), nullable=False, default=0),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_subjects_name', 'name'),
        sa.Index('ix_subjects_active', 'is_active')
    )

    # Create concepts table
    op.create_table('concepts',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('subject_id', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),  # Rich content/markdown
        sa.Column('difficulty_level', sa.Integer(), nullable=False, default=1),  # 1-5 scale
        sa.Column('estimated_duration', sa.Integer(), nullable=True),  # in minutes
        sa.Column('tags', sa.JSON(), nullable=True),  # Array of tags
        sa.Column('learning_objectives', sa.JSON(), nullable=True),  # Array of objectives
        sa.Column('prerequisites', sa.JSON(), nullable=True),  # Array of prerequisite concept IDs
        sa.Column('metadata', sa.JSON(), nullable=True),  # Additional metadata
        sa.Column('is_published', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_by', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ondelete='CASCADE'),
        sa.Index('ix_concepts_subject_id', 'subject_id'),
        sa.Index('ix_concepts_name', 'name'),
        sa.Index('ix_concepts_difficulty', 'difficulty_level'),
        sa.Index('ix_concepts_published', 'is_published'),
        sa.Index('ix_concepts_created_by', 'created_by')
    )

    # Create concept relationships table (for many-to-many relationships)
    op.create_table('concept_relationships',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('source_concept_id', sa.String(50), nullable=False),
        sa.Column('target_concept_id', sa.String(50), nullable=False),
        sa.Column('relationship_type', sa.String(50), nullable=False),  # prerequisite, related, builds_upon, etc.
        sa.Column('strength', sa.Float(), nullable=True),  # Relationship strength 0-1
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['source_concept_id'], ['concepts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_concept_id'], ['concepts.id'], ondelete='CASCADE'),
        sa.Index('ix_concept_relationships_source', 'source_concept_id'),
        sa.Index('ix_concept_relationships_target', 'target_concept_id'),
        sa.Index('ix_concept_relationships_type', 'relationship_type'),
        sa.UniqueConstraint('source_concept_id', 'target_concept_id', 'relationship_type', name='uq_relationship')
    )

    # Create users table for content management
    op.create_table('users',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('display_name', sa.String(255), nullable=True),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('role', sa.String(50), nullable=False, default='user'),  # admin, creator, user
        sa.Column('permissions', sa.JSON(), nullable=True),  # Role permissions
        sa.Column('preferences', sa.JSON(), nullable=True),  # User preferences
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_users_username', 'username'),
        sa.Index('ix_users_email', 'email'),
        sa.Index('ix_users_role', 'role'),
        sa.Index('ix_users_active', 'is_active')
    )

    # Create content_items table (videos, animations, documents, etc.)
    op.create_table('content_items',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('concept_id', sa.String(50), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('content_type', sa.String(50), nullable=False),  # video, animation, document, interactive
        sa.Column('file_path', sa.String(500), nullable=True),  # Path to file
        sa.Column('file_size', sa.BigInteger(), nullable=True),  # File size in bytes
        sa.Column('duration', sa.Integer(), nullable=True),  # Duration in seconds
        sa.Column('resolution', sa.String(20), nullable=True),  # e.g., "1920x1080"
        sa.Column('format', sa.String(20), nullable=True),  # mp4, webm, pdf, etc.
        sa.Column('quality', sa.String(20), nullable=True),  # low, medium, high
        sa.Column('language', sa.String(10), nullable=True),  # ISO language code
        sa.Column('thumbnail_url', sa.String(500), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),  # Additional metadata
        sa.Column('view_count', sa.Integer(), nullable=False, default=0),
        sa.Column('like_count', sa.Integer(), nullable=False, default=0),
        sa.Column('rating', sa.Float(), nullable=True),  # Average rating
        sa.Column('is_published', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_by', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['concept_id'], ['concepts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='RESTRICT'),
        sa.Index('ix_content_items_concept_id', 'concept_id'),
        sa.Index('ix_content_items_type', 'content_type'),
        sa.Index('ix_content_items_created_by', 'created_by'),
        sa.Index('ix_content_items_published', 'is_published'),
        sa.Index('ix_content_items_created_at', 'created_at')
    )

    # Create content_ratings table for user ratings
    op.create_table('content_ratings',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('content_id', sa.String(50), nullable=False),
        sa.Column('user_id', sa.String(50), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),  # 1-5 stars
        sa.Column('review', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['content_id'], ['content_items.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.Index('ix_content_ratings_content_id', 'content_id'),
        sa.Index('ix_content_ratings_user_id', 'user_id'),
        sa.UniqueConstraint('content_id', 'user_id', name='uq_content_rating')
    )

    # Create learning_paths table for structured learning sequences
    op.create_table('learning_paths',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('subject_id', sa.String(50), nullable=False),
        sa.Column('difficulty_level', sa.Integer(), nullable=False, default=1),  # 1-5 scale
        sa.Column('estimated_duration', sa.Integer(), nullable=True),  # Total duration in minutes
        sa.Column('is_published', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_by', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='RESTRICT'),
        sa.Index('ix_learning_paths_subject_id', 'subject_id'),
        sa.Index('ix_learning_paths_difficulty', 'difficulty_level'),
        sa.Index('ix_learning_paths_published', 'is_published'),
        sa.Index('ix_learning_paths_created_by', 'created_by')
    )

    # Create learning_path_concepts table (concepts in learning path order)
    op.create_table('learning_path_concepts',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('learning_path_id', sa.String(50), nullable=False),
        sa.Column('concept_id', sa.String(50), nullable=False),
        sa.Column('sequence_order', sa.Integer(), nullable=False),
        sa.Column('is_required', sa.Boolean(), nullable=False, default=True),
        sa.Column('estimated_duration', sa.Integer(), nullable=True),  # Duration for this concept in minutes
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['learning_path_id'], ['learning_paths.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['concept_id'], ['concepts.id'], ondelete='CASCADE'),
        sa.Index('ix_learning_path_concepts_path_id', 'learning_path_id'),
        sa.Index('ix_learning_path_concepts_concept_id', 'concept_id'),
        sa.Index('ix_learning_path_concepts_order', 'sequence_order'),
        sa.UniqueConstraint('learning_path_id', 'sequence_order', name='uq_path_sequence')
    )

    # Create user_progress table for tracking learning progress
    op.create_table('user_progress',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('user_id', sa.String(50), nullable=False),
        sa.Column('concept_id', sa.String(50), nullable=False),
        sa.Column('content_id', sa.String(50), nullable=True),  # Specific content item
        sa.Column('learning_path_id', sa.String(50), nullable=True),  # If part of a learning path
        sa.Column('status', sa.String(50), nullable=False, default='not_started'),  # not_started, in_progress, completed, mastered
        sa.Column('progress_percentage', sa.Float(), nullable=False, default=0.0),  # 0.0 - 100.0
        sa.Column('time_spent', sa.Integer(), nullable=True),  # Time spent in seconds
        sa.Column('attempts', sa.Integer(), nullable=False, default=0),
        sa.Column('score', sa.Float(), nullable=True),  # Score if applicable
        sa.Column('last_accessed', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['concept_id'], ['concepts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['content_id'], ['content_items.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['learning_path_id'], ['learning_paths.id'], ondelete='SET NULL'),
        sa.Index('ix_user_progress_user_id', 'user_id'),
        sa.Index('ix_user_progress_concept_id', 'concept_id'),
        sa.Index('ix_user_progress_status', 'status'),
        sa.Index('ix_user_progress_path_id', 'learning_path_id'),
        sa.UniqueConstraint('user_id', 'concept_id', 'content_id', name='uq_user_concept_content')
    )

    # Create search_index table for full-text search
    op.create_table('search_index',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('entity_type', sa.String(50), nullable=False),  # concept, content_item, learning_path
        sa.Column('entity_id', sa.String(50), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),  # Array of searchable tags
        sa.Column('metadata', sa.JSON(), nullable=True),  # Additional searchable metadata
        sa.Column('language', sa.String(10), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_search_index_entity_type', 'entity_type'),
        sa.Index('ix_search_index_entity_id', 'entity_id'),
        sa.Index('ix_search_index_language', 'language'),
        sa.Index('ix_search_index_created_at', 'created_at'),
        sa.UniqueConstraint('entity_type', 'entity_id', name='uq_search_entity')
    )

    # Create triggers for updated_at columns (PostgreSQL specific)
    try:
        # Function to update updated_at timestamp
        op.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ language 'plpgsql';
        """)
        
        # Apply triggers to relevant tables
        for table_name in ['subjects', 'concepts', 'users', 'content_items', 'content_ratings', 
                          'learning_paths', 'user_progress', 'search_index']:
            op.execute(f"""
                CREATE TRIGGER update_{table_name}_updated_at
                BEFORE UPDATE ON {table_name}
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();
            """)
    except Exception:
        # If not PostgreSQL or trigger creation fails, continue
        pass

    # Create some initial data
    op.bulk_insert(
        sa.table('subjects',
                 sa.column('id', sa.String(50)),
                 sa.column('name', sa.String(255)),
                 sa.column('description', sa.Text()),
                 sa.column('color_code', sa.String(7)),
                 sa.column('sort_order', sa.Integer())
        ),
        [
            {'id': 'mathematics', 'name': 'Mathematics', 'description': 'Mathematical concepts and principles', 'color_code': '#3B82F6', 'sort_order': 1},
            {'id': 'physics', 'name': 'Physics', 'description': 'Physical phenomena and laws', 'color_code': '#10B981', 'sort_order': 2},
            {'id': 'chemistry', 'name': 'Chemistry', 'description': 'Chemical reactions and molecular structures', 'color_code': '#F59E0B', 'sort_order': 3},
            {'id': 'computer_science', 'name': 'Computer Science', 'description': 'Programming and computational thinking', 'color_code': '#8B5CF6', 'sort_order': 4},
            {'id': 'biology', 'name': 'Biology', 'description': 'Life sciences and biological processes', 'color_code': '#EF4444', 'sort_order': 5}
        ]
    )

    # Create default admin user
    op.bulk_insert(
        sa.table('users',
                 sa.column('id', sa.String(50)),
                 sa.column('username', sa.String(50)),
                 sa.column('email', sa.String(255)),
                 sa.column('display_name', sa.String(255)),
                 sa.column('role', sa.String(50))
        ),
        [
            {'id': 'admin', 'username': 'admin', 'email': 'admin@visualverse.com', 'display_name': 'System Administrator', 'role': 'admin'}
        ]
    )

def downgrade() -> None:
    """Drop all tables in reverse order"""
    # Drop tables in reverse order to handle foreign key constraints
    op.drop_table('search_index')
    op.drop_table('user_progress')
    op.drop_table('learning_path_concepts')
    op.drop_table('learning_paths')
    op.drop_table('content_ratings')
    op.drop_table('content_items')
    op.drop_table('users')
    op.drop_table('concept_relationships')
    op.drop_table('concepts')
    op.drop_table('subjects')
    
    # Drop the trigger function if it exists
    try:
        op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")
    except Exception:
        pass