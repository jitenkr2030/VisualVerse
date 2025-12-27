"""
Vertical Services Package

This package contains domain-specific service implementations for all verticals:
- math_verse: Mathematical visualization and reasoning services
- physics_verse: Physics simulation services (placeholder)
- chem_verse: Chemistry visualization services (placeholder)
- algo_verse: Algorithm visualization and learning services
- fin_verse: Financial visualization services (placeholder)

Licensed under the Apache License, Version 2.0
"""

# Import available vertical services
try:
    from .math_verse import (
        MathVerseConceptService,
        MathVerseVisualService,
        MathVerseReasoningEngine,
        MathVerseAnimationService,
        create_math_concept_service,
        create_math_visual_service,
        create_math_reasoning_engine,
        create_math_animation_service
    )
    MATH_VERSE_AVAILABLE = True
except ImportError:
    MATH_VERSE_AVAILABLE = False
    MathVerseConceptService = None
    MathVerseVisualService = None
    MathVerseReasoningEngine = None
    MathVerseAnimationService = None
    create_math_concept_service = None
    create_math_visual_service = None
    create_math_reasoning_engine = None
    create_math_animation_service = None

# Import AlgoVerse services
try:
    from .algo_verse import (
        AlgoVerseConceptService,
        AlgoVerseVisualService,
        AlgoVerseAnimationService,
        AlgoVerseReasoningEngine,
        CodeElement,
        CodeElementType,
        ComplexityMetrics,
        ControlFlowGraph,
        VisualStyle,
        VisualizationType,
        NodeStyle,
        EdgeStyle,
        AnimationType,
        SortingAlgorithm,
        GraphTraversalType,
        TreeTraversalType,
        ElementState,
        ComplexityClass,
        AlgorithmCategory,
        CorrectnessStatus,
        create_algo_concept_service,
        create_algo_visual_service,
        create_algo_animation_service,
        create_algo_reasoning_engine
    )
    ALGO_VERSE_AVAILABLE = True
except ImportError:
    ALGO_VERSE_AVAILABLE = False
    AlgoVerseConceptService = None
    AlgoVerseVisualService = None
    AlgoVerseAnimationService = None
    AlgoVerseReasoningEngine = None
    CodeElement = None
    CodeElementType = None
    ComplexityMetrics = None
    ControlFlowGraph = None
    VisualStyle = None
    VisualizationType = None
    NodeStyle = None
    EdgeStyle = None
    AnimationType = None
    SortingAlgorithm = None
    GraphTraversalType = None
    TreeTraversalType = None
    ElementState = None
    ComplexityClass = None
    AlgorithmCategory = None
    CorrectnessStatus = None
    create_algo_concept_service = None
    create_algo_visual_service = None
    create_algo_animation_service = None
    create_algo_reasoning_engine = None

# Placeholder for other verticals (to be implemented in Phase 3)
try:
    from .physics_verse import (
        PhysicsVerseConceptService,
        PhysicsVerseVisualService,
        PhysicsVerseAnimationService,
        PhysicsVerseReasoningEngine,
        Vector2D,
        Vector3D,
        Complex,
        Matrix3x3,
        PhysicsState,
        PhysicsConstants,
        UnitConverter,
        NumericalIntegrator,
        PhysicsFormula,
        PhysicsFormulaRegistry,
        PhysicsVisualConfig,
        calculate_kinematic_motion,
        calculate_projectile_motion,
        calculate_orbit_parameters,
        calculate_shock_parameters,
        calculate_wave_properties,
        calculate_rc_circuit,
        calculate_rlc_circuit,
        VectorOperationType,
        IntegrationMethod,
        PhysicsDomain,
        MechanicsSubdomain,
        OpticsSubdomain,
        ElectromagnetismSubdomain,
        PhysicsConceptType,
        PhysicsParameter,
        PhysicsProblem,
        PhysicsSolution,
        PhysicsConcept,
        PhysicsVisualType,
        VectorDisplayType,
        ColorScheme,
        VectorStyle,
        GraphConfig,
        FieldVisualConfig,
        CircuitVisualConfig,
        OpticalConfig,
        PhysicsVisualization,
        AnimationState,
        AnimationType,
        EasingFunction,
        AnimationKeyframe,
        AnimationFrame,
        MotionAnimationConfig,
        WaveAnimationConfig,
        CircuitAnimationConfig,
        PhysicsAnimation,
        ProblemDifficulty,
        SolutionStatus,
        SolutionStep,
        ConceptualAnalysis,
        DimensionalAnalysis,
        create_physics_concept_service,
        create_physics_visual_service,
        create_physics_animation_service,
        create_physics_reasoning_engine
    )
    PHYSICS_VERSE_AVAILABLE = True
except ImportError:
    PHYSICS_VERSE_AVAILABLE = False
    PhysicsVerseConceptService = None
    PhysicsVerseVisualService = None
    PhysicsVerseAnimationService = None
    PhysicsVerseReasoningEngine = None
    Vector2D = None
    Vector3D = None
    Complex = None
    Matrix3x3 = None
    PhysicsState = None
    PhysicsConstants = None
    UnitConverter = None
    NumericalIntegrator = None
    PhysicsFormula = None
    PhysicsFormulaRegistry = None
    PhysicsVisualConfig = None
    calculate_kinematic_motion = None
    calculate_projectile_motion = None
    calculate_orbit_parameters = None
    calculate_shock_parameters = None
    calculate_wave_properties = None
    calculate_rc_circuit = None
    calculate_rlc_circuit = None
    VectorOperationType = None
    IntegrationMethod = None
    PhysicsDomain = None
    MechanicsSubdomain = None
    OpticsSubdomain = None
    ElectromagnetismSubdomain = None
    PhysicsConceptType = None
    PhysicsParameter = None
    PhysicsProblem = None
    PhysicsSolution = None
    PhysicsConcept = None
    PhysicsVisualType = None
    VectorDisplayType = None
    ColorScheme = None
    VectorStyle = None
    GraphConfig = None
    FieldVisualConfig = None
    CircuitVisualConfig = None
    OpticalConfig = None
    PhysicsVisualization = None
    AnimationState = None
    AnimationType = None
    EasingFunction = None
    AnimationKeyframe = None
    AnimationFrame = None
    MotionAnimationConfig = None
    WaveAnimationConfig = None
    CircuitAnimationConfig = None
    PhysicsAnimation = None
    ProblemDifficulty = None
    SolutionStatus = None
    SolutionStep = None
    ConceptualAnalysis = None
    DimensionalAnalysis = None
    create_physics_concept_service = None
    create_physics_visual_service = None
    create_physics_animation_service = None
    create_physics_reasoning_engine = None

# Import ChemVerse services
try:
    from .chem_verse import (
        ChemVerseConceptService,
        ChemVerseVisualService,
        ChemVerseAnimationService,
        ChemVerseReasoningEngine,
        ElementSymbol,
        BondType,
        HybridizationType,
        ReactionType,
        Phase,
        ElementData,
        Vector3D,
        Atom,
        Bond,
        Molecule,
        ChemicalReaction,
        ChemicalConstants,
        StoichiometryCalculator,
        PHCalculator,
        ElectrochemistryCalculator,
        ReactionAnimationConfig,
        MoleculeVisualConfig,
        ChemDomain,
        DifficultyLevel,
        ChemistryConcept,
        LessonContent,
        PracticeProblem,
        PeriodicTable,
        ConceptRepository,
        RenderStyle,
        ColorScheme,
        VectorDisplayStyle,
        AtomVisual,
        BondVisual,
        MoleculeVisual,
        VectorField,
        ElectronOrbital,
        ReactionCoordinateDiagram,
        MoleculeRenderer,
        StructureComparator,
        AnimationState,
        AnimationEasing,
        ParticleEffectType,
        AnimationKeyframe,
        AnimationFrame,
        TransitionState,
        ReactionAnimation,
        MolecularMotion,
        ParticleEffect,
        EasingFunction,
        ReactionAnimator,
        MolecularDynamics,
        ProblemDifficulty,
        SolutionStatus,
        SolutionStep,
        ConceptualAnalysis,
        DimensionalAnalysis,
        ChemistrySolution,
        EquationBalancer,
        StoichiometrySolver,
        AcidBaseSolver,
        ElectrochemistrySolver,
        ThermodynamicsSolver,
        create_chem_concept_service,
        create_chem_visual_service,
        create_chem_animation_service,
        create_chem_reasoning_engine
    )
    CHEM_VERSE_AVAILABLE = True
except ImportError:
    CHEM_VERSE_AVAILABLE = False
    ChemVerseConceptService = None
    ChemVerseVisualService = None
    ChemVerseAnimationService = None
    ChemVerseReasoningEngine = None
    ElementSymbol = None
    BondType = None
    HybridizationType = None
    ReactionType = None
    Phase = None
    ElementData = None
    Vector3D = None
    Atom = None
    Bond = None
    Molecule = None
    ChemicalReaction = None
    ChemicalConstants = None
    StoichiometryCalculator = None
    PHCalculator = None
    ElectrochemistryCalculator = None
    ReactionAnimationConfig = None
    MoleculeVisualConfig = None
    ChemDomain = None
    DifficultyLevel = None
    ChemistryConcept = None
    LessonContent = None
    PracticeProblem = None
    PeriodicTable = None
    ConceptRepository = None
    RenderStyle = None
    ColorScheme = None
    VectorDisplayStyle = None
    AtomVisual = None
    BondVisual = None
    MoleculeVisual = None
    VectorField = None
    ElectronOrbital = None
    ReactionCoordinateDiagram = None
    MoleculeRenderer = None
    StructureComparator = None
    AnimationState = None
    AnimationEasing = None
    ParticleEffectType = None
    AnimationKeyframe = None
    AnimationFrame = None
    TransitionState = None
    ReactionAnimation = None
    MolecularMotion = None
    ParticleEffect = None
    EasingFunction = None
    ReactionAnimator = None
    MolecularDynamics = None
    ProblemDifficulty = None
    SolutionStatus = None
    SolutionStep = None
    ConceptualAnalysis = None
    DimensionalAnalysis = None
    ChemistrySolution = None
    EquationBalancer = None
    StoichiometrySolver = None
    AcidBaseSolver = None
    ElectrochemistrySolver = None
    ThermodynamicsSolver = None
    create_chem_concept_service = None
    create_chem_visual_service = None
    create_chem_animation_service = None
    create_chem_reasoning_engine = None

# Import FinVerse services
try:
    from .fin_verse import (
        FinVerseConceptService,
        FinVerseVisualService,
        FinVerseAnimationService,
        FinVerseReasoningEngine,
        AssetClass,
        TransactionType,
        ChartType,
        TimeFrame,
        IndicatorType,
        PriceQuote,
        OHLCV,
        Security,
        Position,
        Transaction,
        Portfolio,
        CashFlow,
        AmortizationSchedule,
        FinancialCalculator,
        RiskAnalyzer,
        TechnicalIndicator,
        ScenarioInputs,
        ScenarioResult,
        ScenarioPlanner,
        ChartConfig,
        PortfolioVisualConfig,
        FinanceDomain,
        DifficultyLevel,
        FormulaDefinition,
        FinanceConcept,
        LessonContent,
        MarketTerm,
        FormulaRepository,
        ConceptRepository,
        ChartStyle,
        ColorPalette,
        DataPoint,
        ChartSeries,
        CandlestickData,
        AxisConfig,
        LegendConfig,
        TooltipConfig,
        FinancialChart,
        PortfolioAllocation,
        PerformanceData,
        RiskMetricsDisplay,
        TechnicalIndicatorDisplay,
        ChartFactory,
        PortfolioVisualizer,
        CorrelationHeatmap,
        AnimationState,
        AnimationEasing,
        AnimationType,
        AnimationFrame,
        Keyframe,
        AnimationConfig,
        PriceAnimation,
        PortfolioAnimation,
        ScenarioAnimation,
        TransitionState,
        EasingFunctions,
        PriceAnimator,
        PortfolioAnimator,
        ScenarioAnimator,
        MarketTickerAnimator,
        ProblemDifficulty,
        SolutionStatus,
        SolutionStep,
        ConceptualAnalysis,
        FinancialSolution,
        TimeValueSolver,
        RiskAnalysisSolver,
        TechnicalAnalysisSolver,
        ScenarioPlanningSolver,
        create_fin_concept_service,
        create_fin_visual_service,
        create_fin_animation_service,
        create_fin_reasoning_engine
    )
    FIN_VERSE_AVAILABLE = True
except ImportError:
    FIN_VERSE_AVAILABLE = False
    FinVerseConceptService = None
    FinVerseVisualService = None
    FinVerseAnimationService = None
    FinVerseReasoningEngine = None
    AssetClass = None
    TransactionType = None
    ChartType = None
    TimeFrame = None
    IndicatorType = None
    PriceQuote = None
    OHLCV = None
    Security = None
    Position = None
    Transaction = None
    Portfolio = None
    CashFlow = None
    AmortizationSchedule = None
    FinancialCalculator = None
    RiskAnalyzer = None
    TechnicalIndicator = None
    ScenarioInputs = None
    ScenarioResult = None
    ScenarioPlanner = None
    ChartConfig = None
    PortfolioVisualConfig = None
    FinanceDomain = None
    DifficultyLevel = None
    FormulaDefinition = None
    FinanceConcept = None
    LessonContent = None
    MarketTerm = None
    FormulaRepository = None
    ConceptRepository = None
    ChartStyle = None
    ColorPalette = None
    DataPoint = None
    ChartSeries = None
    CandlestickData = None
    AxisConfig = None
    LegendConfig = None
    TooltipConfig = None
    FinancialChart = None
    PortfolioAllocation = None
    PerformanceData = None
    RiskMetricsDisplay = None
    TechnicalIndicatorDisplay = None
    ChartFactory = None
    PortfolioVisualizer = None
    CorrelationHeatmap = None
    AnimationState = None
    AnimationEasing = None
    AnimationType = None
    AnimationFrame = None
    Keyframe = None
    AnimationConfig = None
    PriceAnimation = None
    PortfolioAnimation = None
    ScenarioAnimation = None
    TransitionState = None
    EasingFunctions = None
    PriceAnimator = None
    PortfolioAnimator = None
    ScenarioAnimator = None
    MarketTickerAnimator = None
    ProblemDifficulty = None
    SolutionStatus = None
    SolutionStep = None
    ConceptualAnalysis = None
    FinancialSolution = None
    TimeValueSolver = None
    RiskAnalysisSolver = None
    TechnicalAnalysisSolver = None
    ScenarioPlanningSolver = None
    create_fin_concept_service = None
    create_fin_visual_service = None
    create_fin_animation_service = None
    create_fin_reasoning_engine = None


def get_vertical_service(vertical_id: str, service_type: str):
    """
    Get a service instance for a specific vertical.
    
    Args:
        vertical_id: The vertical identifier
        service_type: Type of service ('concept', 'visual', 'reasoning', 'animation')
        
    Returns:
        Service instance or None if not available
    """
    service_map = {
        'math-verse': {
            'concept': create_math_concept_service,
            'visual': create_math_visual_service,
            'reasoning': create_math_reasoning_engine,
            'animation': create_math_animation_service,
        },
        'algo-verse': {
            'concept': create_algo_concept_service,
            'visual': create_algo_visual_service,
            'reasoning': create_algo_reasoning_engine,
            'animation': create_algo_animation_service,
        },
        'physics-verse': {
            'concept': create_physics_concept_service,
            'visual': create_physics_visual_service,
            'reasoning': create_physics_reasoning_engine,
            'animation': create_physics_animation_service,
        },
        'chem-verse': {
            'concept': create_chem_concept_service,
            'visual': create_chem_visual_service,
            'reasoning': create_chem_reasoning_engine,
            'animation': create_chem_animation_service,
        },
        'fin-verse': {
            'concept': create_fin_concept_service,
            'visual': create_fin_visual_service,
            'reasoning': create_fin_reasoning_engine,
            'animation': create_fin_animation_service,
        }
    }
    
    vertical_services = service_map.get(vertical_id, {})
    factory = vertical_services.get(service_type)
    
    if factory:
        return factory()
    
    return None


def list_available_verticals() -> list:
    """
    List verticals with available service implementations.
    
    Returns:
        List of vertical identifiers
    """
    available = []
    if MATH_VERSE_AVAILABLE:
        available.append('math-verse')
    if PHYSICS_VERSE_AVAILABLE:
        available.append('physics-verse')
    if CHEM_VERSE_AVAILABLE:
        available.append('chem-verse')
    if ALGO_VERSE_AVAILABLE:
        available.append('algo-verse')
    if FIN_VERSE_AVAILABLE:
        available.append('fin-verse')
    return available


def get_service_types_for_vertical(vertical_id: str) -> list:
    """
    Get available service types for a vertical.
    
    Args:
        vertical_id: The vertical identifier
        
    Returns:
        List of available service types
    """
    services = {
        'math-verse': ['concept', 'visual', 'reasoning', 'animation'],
        'physics-verse': ['concept', 'visual', 'reasoning', 'animation'],
        'chem-verse': ['concept', 'visual', 'reasoning', 'animation'],
        'algo-verse': ['concept', 'visual', 'reasoning', 'animation'],
        'fin-verse': ['concept', 'visual', 'reasoning', 'animation']
    }
    return services.get(vertical_id, [])


def create_vertical_service(vertical_id: str, service_type: str, config: dict = None):
    """
    Create a vertical service with optional configuration.
    
    Args:
        vertical_id: The vertical identifier
        service_type: Type of service
        config: Optional configuration dictionary
        
    Returns:
        Configured service instance or None
    """
    service = get_vertical_service(vertical_id, service_type)
    
    if service and config:
        # Apply configuration if the service supports it
        if hasattr(service, 'configure'):
            service.configure(config)
    
    return service


__all__ = [
    # Service availability flags
    'MATH_VERSE_AVAILABLE',
    'PHYSICS_VERSE_AVAILABLE',
    'CHEM_VERSE_AVAILABLE',
    'ALGO_VERSE_AVAILABLE',
    'FIN_VERSE_AVAILABLE',
    
    # Math Verse classes
    'MathVerseConceptService',
    'MathVerseVisualService',
    'MathVerseReasoningEngine',
    'MathVerseAnimationService',
    'create_math_concept_service',
    'create_math_visual_service',
    'create_math_reasoning_engine',
    'create_math_animation_service',
    
    # Physics Verse classes
    'PhysicsVerseConceptService',
    'PhysicsVerseVisualService',
    'PhysicsVerseAnimationService',
    'PhysicsVerseReasoningEngine',
    'Vector2D',
    'Vector3D',
    'Complex',
    'Matrix3x3',
    'PhysicsState',
    'PhysicsConstants',
    'UnitConverter',
    'NumericalIntegrator',
    'PhysicsFormula',
    'PhysicsFormulaRegistry',
    'PhysicsVisualConfig',
    'calculate_kinematic_motion',
    'calculate_projectile_motion',
    'calculate_orbit_parameters',
    'calculate_shock_parameters',
    'calculate_wave_properties',
    'calculate_rc_circuit',
    'calculate_rlc_circuit',
    'VectorOperationType',
    'IntegrationMethod',
    'PhysicsDomain',
    'MechanicsSubdomain',
    'OpticsSubdomain',
    'ElectromagnetismSubdomain',
    'PhysicsConceptType',
    'PhysicsParameter',
    'PhysicsProblem',
    'PhysicsSolution',
    'PhysicsConcept',
    'PhysicsVisualType',
    'VectorDisplayType',
    'ColorScheme',
    'VectorStyle',
    'GraphConfig',
    'FieldVisualConfig',
    'CircuitVisualConfig',
    'OpticalConfig',
    'PhysicsVisualization',
    'AnimationState',
    'AnimationType',
    'EasingFunction',
    'AnimationKeyframe',
    'AnimationFrame',
    'MotionAnimationConfig',
    'WaveAnimationConfig',
    'CircuitAnimationConfig',
    'PhysicsAnimation',
    'ProblemDifficulty',
    'SolutionStatus',
    'SolutionStep',
    'ConceptualAnalysis',
    'DimensionalAnalysis',
    'create_physics_concept_service',
    'create_physics_visual_service',
    'create_physics_animation_service',
    'create_physics_reasoning_engine',
    
    # Chem Verse classes
    'ChemVerseConceptService',
    'ChemVerseVisualService',
    'ChemVerseAnimationService',
    'ChemVerseReasoningEngine',
    'ElementSymbol',
    'BondType',
    'HybridizationType',
    'ReactionType',
    'Phase',
    'ElementData',
    'Vector3D',
    'Atom',
    'Bond',
    'Molecule',
    'ChemicalReaction',
    'ChemicalConstants',
    'StoichiometryCalculator',
    'PHCalculator',
    'ElectrochemistryCalculator',
    'ReactionAnimationConfig',
    'MoleculeVisualConfig',
    'ChemDomain',
    'DifficultyLevel',
    'ChemistryConcept',
    'LessonContent',
    'PracticeProblem',
    'PeriodicTable',
    'ConceptRepository',
    'RenderStyle',
    'ColorScheme',
    'VectorDisplayStyle',
    'AtomVisual',
    'BondVisual',
    'MoleculeVisual',
    'VectorField',
    'ElectronOrbital',
    'ReactionCoordinateDiagram',
    'MoleculeRenderer',
    'StructureComparator',
    'AnimationState',
    'AnimationEasing',
    'ParticleEffectType',
    'AnimationKeyframe',
    'AnimationFrame',
    'TransitionState',
    'ReactionAnimation',
    'MolecularMotion',
    'ParticleEffect',
    'EasingFunction',
    'ReactionAnimator',
    'MolecularDynamics',
    'ProblemDifficulty',
    'SolutionStatus',
    'SolutionStep',
    'ConceptualAnalysis',
    'DimensionalAnalysis',
    'ChemistrySolution',
    'EquationBalancer',
    'StoichiometrySolver',
    'AcidBaseSolver',
    'ElectrochemistrySolver',
    'ThermodynamicsSolver',
    'create_chem_concept_service',
    'create_chem_visual_service',
    'create_chem_animation_service',
    'create_chem_reasoning_engine',
    
    # Algo Verse classes
    'AlgoVerseConceptService',
    'AlgoVerseVisualService',
    'AlgoVerseAnimationService',
    'AlgoVerseReasoningEngine',
    'CodeElement',
    'CodeElementType',
    'ComplexityMetrics',
    'ControlFlowGraph',
    'VisualStyle',
    'VisualizationType',
    'NodeStyle',
    'EdgeStyle',
    'AnimationType',
    'SortingAlgorithm',
    'GraphTraversalType',
    'TreeTraversalType',
    'ElementState',
    'ComplexityClass',
    'AlgorithmCategory',
    'CorrectnessStatus',
    'create_algo_concept_service',
    'create_algo_visual_service',
    'create_algo_animation_service',
    'create_algo_reasoning_engine',
    
    # Fin Verse classes
    'FinVerseConceptService',
    'FinVerseVisualService',
    'FinVerseAnimationService',
    'FinVerseReasoningEngine',
    'AssetClass',
    'TransactionType',
    'ChartType',
    'TimeFrame',
    'IndicatorType',
    'PriceQuote',
    'OHLCV',
    'Security',
    'Position',
    'Transaction',
    'Portfolio',
    'CashFlow',
    'AmortizationSchedule',
    'FinancialCalculator',
    'RiskAnalyzer',
    'TechnicalIndicator',
    'ScenarioInputs',
    'ScenarioResult',
    'ScenarioPlanner',
    'ChartConfig',
    'PortfolioVisualConfig',
    'FinanceDomain',
    'DifficultyLevel',
    'FormulaDefinition',
    'FinanceConcept',
    'LessonContent',
    'MarketTerm',
    'FormulaRepository',
    'ConceptRepository',
    'ChartStyle',
    'ColorPalette',
    'DataPoint',
    'ChartSeries',
    'CandlestickData',
    'AxisConfig',
    'LegendConfig',
    'TooltipConfig',
    'FinancialChart',
    'PortfolioAllocation',
    'PerformanceData',
    'RiskMetricsDisplay',
    'TechnicalIndicatorDisplay',
    'ChartFactory',
    'PortfolioVisualizer',
    'CorrelationHeatmap',
    'AnimationState',
    'AnimationEasing',
    'AnimationType',
    'AnimationFrame',
    'Keyframe',
    'AnimationConfig',
    'PriceAnimation',
    'PortfolioAnimation',
    'ScenarioAnimation',
    'TransitionState',
    'EasingFunctions',
    'PriceAnimator',
    'PortfolioAnimator',
    'ScenarioAnimator',
    'MarketTickerAnimator',
    'ProblemDifficulty',
    'SolutionStatus',
    'SolutionStep',
    'ConceptualAnalysis',
    'FinancialSolution',
    'TimeValueSolver',
    'RiskAnalysisSolver',
    'TechnicalAnalysisSolver',
    'ScenarioPlanningSolver',
    'create_fin_concept_service',
    'create_fin_visual_service',
    'create_fin_animation_service',
    'create_fin_reasoning_engine',
    
    # Utility functions
    'get_vertical_service',
    'list_available_verticals',
    'get_service_types_for_vertical',
    'create_vertical_service'
]
