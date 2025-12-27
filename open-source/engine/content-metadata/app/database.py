"""
Database configuration and connection management for VisualVerse Content Metadata Service.
Uses Neo4j graph database for storing educational content relationships.
"""

import os
import logging
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager
from neo4j import AsyncDriver, AsyncSession
from neo4j.auth_basic import AuthToken

logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Database configuration settings"""
    
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.database = os.getenv("NEO4J_DATABASE", "visualverse")
        self.max_connections = int(os.getenv("NEO4J_MAX_CONNECTIONS", "100"))
        self.connection_timeout = int(os.getenv("NEO4J_CONNECTION_TIMEOUT", "30"))

class DatabaseConnection:
    """Database connection manager"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.driver: Optional[AsyncDriver] = None
    
    async def connect(self):
        """Establish database connection"""
        try:
            self.driver = AsyncDriver(
                uri=self.config.uri,
                auth=AuthToken(self.config.username, self.config.password),
                max_connection_pool_size=self.config.max_connections,
                connection_timeout=self.config.connection_timeout
            )
            
            # Test connection
            await self.driver.verify_connectivity()
            logger.info(f"Connected to Neo4j database: {self.config.database}")
            
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise
    
    async def disconnect(self):
        """Close database connection"""
        if self.driver:
            await self.driver.close()
            logger.info("Database connection closed")
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session with automatic cleanup"""
        if not self.driver:
            await self.connect()
        
        async with self.driver.session(database=self.config.database) as session:
            yield session

# Global database instance
db_config = DatabaseConfig()
db_connection = DatabaseConnection(db_config)

async def init_database():
    """Initialize database and create constraints"""
    try:
        await db_connection.connect()
        
        # Create indexes and constraints
        async with db_connection.get_session() as session:
            await session.run("""
                CREATE CONSTRAINT subject_id IF NOT EXISTS 
                FOR (s:Subject) REQUIRE s.id IS UNIQUE
            """)
            
            await session.run("""
                CREATE CONSTRAINT course_id IF NOT EXISTS 
                FOR (c:Course) REQUIRE c.id IS UNIQUE
            """)
            
            await session.run("""
                CREATE CONSTRAINT concept_id IF NOT EXISTS 
                FOR (k:Concept) REQUIRE k.id IS UNIQUE
            """)
            
            await session.run("""
                CREATE CONSTRAINT syllabus_id IF NOT EXISTS 
                FOR (sy:Syllabus) REQUIRE sy.id IS UNIQUE
            """)
            
            # Create indexes for performance
            await session.run("""
                CREATE INDEX subject_name IF NOT EXISTS 
                FOR (s:Subject) ON (s.name)
            """)
            
            await session.run("""
                CREATE INDEX course_subject IF NOT EXISTS 
                FOR (c:Course)-[:BELONGS_TO]->(s:Subject) ON (s.name)
            """)
            
            await session.run("""
                CREATE INDEX concept_subject IF NOT EXISTS 
                FOR (k:Concept)-[:BELONGS_TO]->(s:Subject) ON (s.name)
            """)
            
            await session.run("""
                CREATE INDEX prerequisite_strength IF NOT EXISTS 
                FOR ()-[r:PREREQUISITE]->() ON (r.strength)
            """)
            
        logger.info("Database initialized with constraints and indexes")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise

async def close_database():
    """Close database connection"""
    await db_connection.disconnect()

@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session"""
    async with db_connection.get_session() as session:
        yield session

class DatabaseHelper:
    """Helper class for common database operations"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_subject(self, subject_data: dict):
        """Create a new subject"""
        query = """
        CREATE (s:Subject {
            id: $id,
            name: $name,
            description: $description,
            created_at: datetime(),
            updated_at: datetime()
        })
        RETURN s
        """
        result = await self.session.run(query, subject_data)
        return await result.single()
    
    async def get_subject(self, subject_id: str):
        """Get subject by ID"""
        query = """
        MATCH (s:Subject {id: $id})
        OPTIONAL MATCH (s)-[:HAS_COURSE]->(c:Course)
        OPTIONAL MATCH (s)-[:HAS_CONCEPT]->(k:Concept)
        RETURN s, collect(c) as courses, collect(k) as concepts
        """
        result = await self.session.run(query, {"id": subject_id})
        return await result.single()
    
    async def create_course(self, course_data: dict):
        """Create a new course"""
        query = """
        MATCH (s:Subject {name: $subject_name})
        CREATE (c:Course {
            id: $id,
            name: $name,
            description: $description,
            level: $level,
            estimated_duration: $estimated_duration,
            created_at: datetime(),
            updated_at: datetime()
        })
        CREATE (c)-[:BELONGS_TO]->(s)
        RETURN c
        """
        result = await self.session.run(query, course_data)
        return await result.single()
    
    async def create_concept(self, concept_data: dict):
        """Create a new concept"""
        query = """
        MATCH (s:Subject {name: $subject_name})
        CREATE (k:Concept {
            id: $id,
            name: $name,
            description: $description,
            difficulty_level: $difficulty_level,
            estimated_duration: $estimated_duration,
            learning_objectives: $learning_objectives,
            created_at: datetime(),
            updated_at: datetime()
        })
        CREATE (k)-[:BELONGS_TO]->(s)
        RETURN k
        """
        result = await self.session.run(query, concept_data)
        return await result.single()
    
    async def create_prerequisite(self, concept_id: str, prerequisite_id: str, strength: float = 1.0):
        """Create prerequisite relationship"""
        query = """
        MATCH (k1:Concept {id: $concept_id})
        MATCH (k2:Concept {id: $prerequisite_id})
        CREATE (k1)-[r:PREREQUISITE {
            strength: $strength,
            created_at: datetime()
        }]->(k2)
        RETURN r
        """
        result = await self.session.run(query, {
            "concept_id": concept_id,
            "prerequisite_id": prerequisite_id,
            "strength": strength
        })
        return await result.single()
    
    async def get_learning_path(self, subject_name: str, start_concept: str = None, target_concept: str = None):
        """Generate learning path using graph algorithms"""
        query = """
        MATCH (s:Subject {name: $subject_name})
        MATCH (s)-[:HAS_CONCEPT]->(k:Concept)
        OPTIONAL MATCH (k)-[:PREREQUISITE]->(p:Concept)
        WITH k, collect(p) as prerequisites
        WHERE $start_concept IS NULL OR k.id = $start_concept
        RETURN k, prerequisites
        ORDER BY size(prerequisites), k.difficulty_level
        """
        result = await self.session.run(query, {
            "subject_name": subject_name,
            "start_concept": start_concept,
            "target_concept": target_concept
        })
        
        path = []
        async for record in result:
            concept = record["k"]
            prerequisites = record["prerequisites"]
            path.append({
                "concept": concept,
                "prerequisites": prerequisites,
                "ready_to_learn": len(prerequisites) == 0
            })
        
        return path
    
    async def search_concepts(self, subject_name: str, query_text: str, limit: int = 10):
        """Search concepts by text"""
        query = """
        MATCH (s:Subject {name: $subject_name})
        MATCH (s)-[:HAS_CONCEPT]->(k:Concept)
        WHERE k.name CONTAINS $query_text OR k.description CONTAINS $query_text
        RETURN k
        ORDER BY k.name
        LIMIT $limit
        """
        result = await self.session.run(query, {
            "subject_name": subject_name,
            "query_text": query_text,
            "limit": limit
        })
        
        concepts = []
        async for record in result:
            concepts.append(record["k"])
        
        return concepts

# Database utility functions
async def run_query(query: str, parameters: dict = None):
    """Execute a raw Cypher query"""
    async with get_db() as session:
        result = await session.run(query, parameters or {})
        return [record.data() for record in result]

async def get_database_stats():
    """Get database statistics"""
    stats_query = """
    MATCH (s:Subject)
    OPTIONAL MATCH (s)-[:HAS_COURSE]->(c:Course)
    OPTIONAL MATCH (s)-[:HAS_CONCEPT]->(k:Concept)
    OPTIONAL MATCH ()-[r:PREREQUISITE]->()
    WITH s, count(DISTINCT c) as course_count, count(DISTINCT k) as concept_count, count(DISTINCT r) as prerequisite_count
    RETURN s.name as subject, course_count, concept_count, prerequisite_count
    ORDER BY s.name
    """
    return await run_query(stats_query)
