"""
VisualVerse Creator Platform - Main Package

This package provides the complete Creator & Educator Platform infrastructure
for the VisualVerse learning system, including:

- VerseScript DSL: Domain-specific language for educational content creation
- Version Control: Git-like functionality for content versioning and collaboration
- Syllabus Tagging: Curriculum alignment and educational standards mapping
- Licensing & Monetization: Payment processing, license management, and revenue distribution

Author: MiniMax Agent
Version: 1.0.0
"""

# Version information
__version__ = "1.0.0"
__author__ = "MiniMax Agent"

# DSL Package
from .packages.verse_dsl import (
    VerseScriptParser,
    DSLCompiler,
    ContentTemplate,
    TemplateRegistry,
    compile_verse_script
)

from .packages.verse_dsl.parser import (
    VerseScriptLexer,
    VerseScriptParser as Parser,
    ParseError,
    parse_verse_script,
    Token,
    TokenType,
    ASTNodeType
)

from .packages.verse_dsl.compiler import (
    DSLCompiler as Compiler,
    MathDSLCompiler,
    PhysicsDSLCompiler,
    AlgorithmDSLCompiler,
    CompilationResult,
    CompilationError
)

# Shared Types
from .packages.shared_types import (
    UserRole,
    ContentDomain,
    ContentStatus,
    LicenseType,
    SubscriptionTier,
    VisibilityLevel,
    User,
    ContentMetadata,
    Project,
    Commit,
    Branch,
    SyllabusTag,
    CurriculumBoard,
    Product,
    Transaction,
    License,
    CreatorStats
)

# Version Control Service
from .services.version_control import (
    VersionControlService,
    Commit,
    Branch,
    DiffResult,
    MergeResult,
    ConflictType,
    create_commit_hash,
    get_version_control_service
)

# Syllabus Tagging Service
from .services.syllabus import (
    SyllabusTaggingService,
    CurriculumBoard,
    SyllabusTag,
    TagSearchResult,
    ContentTagAssociation,
    ContentAlignmentReport,
    EducationLevel,
    SubjectArea,
    DifficultyLevel,
    SUPPORTED_BOARDS,
    create_syllabus_service
)

# Licensing & Monetization Service
from .services.licensing import (
    LicensingService,
    LicenseManager,
    PaymentProcessor,
    RevenueDistributor,
    SubscriptionManager,
    License,
    Product,
    Transaction,
    Subscription,
    RevenueShare,
    PaymentMethod,
    LicenseType,
    TransactionStatus,
    SubscriptionStatus,
    SubscriptionTier,
    PlatformFeeConfig,
    create_licensing_service
)


__all__ = [
    # Version
    "__version__",
    
    # DSL
    "VerseScriptParser",
    "DSLCompiler",
    "ContentTemplate",
    "TemplateRegistry",
    "compile_verse_script",
    "VerseScriptLexer",
    "ParseError",
    "parse_verse_script",
    "Token",
    "TokenType",
    "ASTNodeType",
    "MathDSLCompiler",
    "PhysicsDSLCompiler",
    "AlgorithmDSLCompiler",
    "CompilationResult",
    "CompilationError",
    
    # Shared Types
    "UserRole",
    "ContentDomain",
    "ContentStatus",
    "LicenseType",
    "SubscriptionTier",
    "VisibilityLevel",
    "User",
    "ContentMetadata",
    "Project",
    "Commit",
    "Branch",
    "SyllabusTag",
    "CurriculumBoard",
    "Product",
    "Transaction",
    "License",
    "CreatorStats",
    
    # Version Control
    "VersionControlService",
    "Commit",
    "Branch",
    "DiffResult",
    "MergeResult",
    "ConflictType",
    "create_commit_hash",
    "get_version_control_service",
    
    # Syllabus
    "SyllabusTaggingService",
    "CurriculumBoard",
    "SyllabusTag",
    "TagSearchResult",
    "ContentTagAssociation",
    "ContentAlignmentReport",
    "EducationLevel",
    "SubjectArea",
    "DifficultyLevel",
    "SUPPORTED_BOARDS",
    "create_syllabus_service",
    
    # Licensing
    "LicensingService",
    "LicenseManager",
    "PaymentProcessor",
    "RevenueDistributor",
    "SubscriptionManager",
    "License",
    "Product",
    "Transaction",
    "Subscription",
    "RevenueShare",
    "PaymentMethod",
    "TransactionStatus",
    "SubscriptionStatus",
    "PlatformFeeConfig",
    "create_licensing_service"
]


def get_platform_version() -> str:
    """Get the platform version."""
    return __version__


def initialize_platform(storage_dir: str = None) -> Dict[str, Any]:
    """
    Initialize all platform services.
    
    Args:
        storage_dir: Base directory for storing data
        
    Returns:
        Dictionary of initialized services
    """
    from .services.version_control import get_version_control_service
    from .services.syllabus import create_syllabus_service
    from .services.licensing import create_licensing_service
    
    return {
        "version_control": get_version_control_service(storage_dir),
        "syllabus": create_syllabus_service(storage_dir),
        "licensing": create_licensing_service(storage_dir)
    }


# Example usage documentation
EXAMPLE_SCRIPT = '''
# Example: Creating Math Content with VerseScript

from visualverse.platform import compile_verse_script, ContentDomain

# Write VerseScript code
script = """
@scene(width=800, height=600, type="math")

# Define mathematical entities
graph = Entity.Plot(type="2d", color="#3B82F6")
equation = Equation("y = x^2 + 2x + 1")

# Add animation
animate.plot(
    equation,
    range=(-10, 10),
    duration=2000ms,
    easing="ease-in-out"
)
"""

# Compile to VisualVerse configuration
result = compile_verse_script(script)

if result.success:
    config = result.config
    print("Compiled successfully!")
    print(f"Entities: {len(config['entities'])}")
    print(f"Animations: {len(config['animations'])}")
else:
    print(f"Compilation failed: {result.errors}")
'''

EXAMPLE_VERSION_CONTROL = '''
# Example: Version Control for Content

from visualverse.platform import get_version_control_service, User

# Initialize version control
vcs = get_version_control_service("/data/versions")

# Create a new repository
author = User(
    id="user-123",
    email="creator@example.com",
    name="John Doe",
    role="creator"
)

# Initialize repository
commit = vcs.init_repository(
    project_id="project-math-01",
    author_id=author.id,
    author_name=author.name,
    author_email=author.email
)

# Make changes and commit
content = {
    "script.verse": "# My math content",
    "config.json": '{"title": "My Project"}'
}

vcs.commit(
    project_id="project-math-01",
    author_id=author.id,
    author_name=author.name,
    author_email=author.email,
    message="Initial content",
    content=content
)

# Create a branch for experiments
vcs.create_branch(
    name="experimental-features",
    commit_hash=commit.hash,
    author_id=author.id,
    description="Testing new animation features"
)
'''

EXAMPLE_SYLLABUS = '''
# Example: Syllabus Tagging for Curriculum Alignment

from visualverse.platform import create_syllabus_service

# Initialize syllabus service
syllabus = create_syllabus_service("/data/syllabus")

# Search for physics topics
results = syllabus.search_tags(
    query="Newton's laws",
    board_id="board-cbse",
    subject="physics"
)

print(f"Found {results.total_count} tags")

# Get tag hierarchy for a board
hierarchy = syllabus.get_tag_hierarchy("board-cbse")

# Auto-tag content
content_text = """
This lesson covers Newton's three laws of motion.
We will explore concepts of force, mass, and acceleration.
"""

associations = syllabus.auto_tag_content(
    content_id="content-001",
    content_text=content_text,
    board_id="board-cbse"
)

print(f"Auto-tagged with {len(associations)} tags")
'''

EXAMPLE_LICENSING = '''
# Example: Monetization and Licensing

from visualverse.platform import create_licensing_service

# Initialize licensing service
licensing = create_licensing_service("/data/licensing")

# Create a product for sale
product = licensing.create_product(
    project_id="project-physics-01",
    seller_id="creator-123",
    title="Newton's Laws Interactive Simulation",
    description="Master Newton's laws with interactive visualizations",
    price=29.99,
    license_type="personal",
    features=[
        "Full access to all simulations",
        "Downloadable resources",
        "Certificate of completion"
    ]
)

# Process a purchase
transaction = licensing.create_transaction(
    buyer_id="student-456",
    seller_id="creator-123",
    product_id=product.id,
    amount=product.price,
    payment_method="card"
)

# Complete transaction (after payment confirmation)
completed = licensing.complete_transaction(
    transaction_id=transaction.id,
    stripe_payment_id="pi_123456"
)

# Get creator earnings
earnings = licensing.get_creator_earnings("creator-123")
print(f"Total Earnings: ${earnings['totalEarnings']:.2f}")
'''
