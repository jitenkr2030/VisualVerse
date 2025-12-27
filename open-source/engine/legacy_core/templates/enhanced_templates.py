"""
Enhanced Visual Templates for VisualVerse
Subject-specific animation templates with more variety and sophistication.
"""

from typing import Dict, List, Any
from core.plugin_interface import IVerticalPlugin

class TemplateLibrary:
    """Enhanced template library for all subjects"""
    
    @staticmethod
    def get_math_templates() -> Dict[str, Dict[str, Any]]:
        """Get enhanced mathematics visual templates"""
        return {
            # Basic Concept Templates
            "concept_introduction": {
                "name": "Concept Introduction",
                "description": "Introduce a new mathematical concept with definitions and examples",
                "duration": 60,
                "visual_elements": ["title_text", "definition_box", "example_illustration", "key_points"],
                "animation_sequence": [
                    {"step": "title_reveal", "duration": 5, "action": "fade_in_title"},
                    {"step": "definition_display", "duration": 15, "action": "type_definition"},
                    {"step": "example_showcase", "duration": 25, "action": "animate_example"},
                    {"step": "summary_highlight", "duration": 15, "action": "highlight_key_points"}
                ],
                "manim_components": ["Text", "MathTex", "Box", "Highlight", "FadeIn"]
            },
            
            "equation_solving": {
                "name": "Step-by-Step Equation Solving",
                "description": "Show detailed steps for solving equations",
                "duration": 90,
                "visual_elements": ["equation_display", "step_indicators", "transformation_arrows", "solution_highlight"],
                "animation_sequence": [
                    {"step": "initial_equation", "duration": 10, "action": "show_equation"},
                    {"step": "step_1", "duration": 20, "action": "show_transformation"},
                    {"step": "step_2", "duration": 20, "action": "show_transformation"},
                    {"step": "step_3", "duration": 20, "action": "show_transformation"},
                    {"step": "final_solution", "duration": 20, "action": "highlight_solution"}
                ],
                "manim_components": ["MathTex", "Arrow", "Text", "Transform", "Highlight"]
            },
            
            "function_graphing": {
                "name": "Interactive Function Graphing",
                "description": "Plot functions and show key features",
                "duration": 75,
                "visual_elements": ["coordinate_axes", "function_plot", "key_points", "tangent_lines"],
                "animation_sequence": [
                    {"step": "setup_axes", "duration": 15, "action": "draw_coordinate_system"},
                    {"step": "plot_function", "duration": 30, "action": "animate_function_plot"},
                    {"step": "mark_critical_points", "duration": 20, "action": "highlight_extrema"},
                    {"step": "show_tangents", "duration": 10, "action": "draw_tangent_lines"}
                ],
                "manim_components": ["Axes", "FunctionGraph", "Dot", "Line", "MathTex"]
            },
            
            "geometric_proof": {
                "name": "Visual Geometric Proof",
                "description": "Step-by-step geometric proof with constructions",
                "duration": 120,
                "visual_elements": ["geometric_figures", "construction_lines", "proof_steps", "conclusion"],
                "animation_sequence": [
                    {"step": "initial_figure", "duration": 20, "action": "draw_geometry"},
                    {"step": "construction_1", "duration": 25, "action": "add_construction"},
                    {"step": "construction_2", "duration": 25, "action": "add_construction"},
                    {"step": "proof_reasoning", "duration": 35, "action": "show_logical_steps"},
                    {"step": "conclusion", "duration": 15, "action": "highlight_result"}
                ],
                "manim_components": ["Polygon", "Line", "Circle", "Text", "MathTex"]
            },
            
            "calculus_concept": {
                "name": "Calculus Concept Visualization",
                "description": "Visualize limits, derivatives, and integrals",
                "duration": 150,
                "visual_elements": ["function_graph", "limit_illustration", "derivative_visualization", "area_under_curve"],
                "animation_sequence": [
                    {"step": "function_introduction", "duration": 30, "action": "show_function"},
                    {"step": "limit_concept", "duration": 40, "action": "animate_approaching_limit"},
                    {"step": "derivative_visual", "duration": 40, "action": "show_tangent_slope"},
                    {"step": "integral_visual", "duration": 40, "action": "show_area_accumulation"}
                ],
                "manim_components": ["FunctionGraph", "NumberLine", "MathTex", "Area", "Line"]
            },
            
            "algebra_pattern": {
                "name": "Algebraic Pattern Recognition",
                "description": "Identify and work with algebraic patterns",
                "duration": 80,
                "visual_elements": ["pattern_display", "sequence_illustration", "formula_derivation", "verification"],
                "animation_sequence": [
                    {"step": "pattern_showcase", "duration": 20, "action": "display_patterns"},
                    {"step": "sequence_analysis", "duration": 25, "action": "analyze_sequence"},
                    {"step": "formula_derivation", "duration": 25, "action": "derive_formula"},
                    {"step": "verification", "duration": 10, "action": "verify_with_examples"}
                ],
                "manim_components": ["Text", "MathTex", "NumberLine", "Arrow"]
            },
            
            "statistical_analysis": {
                "name": "Statistical Data Visualization",
                "description": "Analyze and visualize statistical data",
                "duration": 100,
                "visual_elements": ["data_points", "histogram", "statistical_measures", "probability_distribution"],
                "animation_sequence": [
                    {"step": "data_presentation", "duration": 20, "action": "show_data_points"},
                    {"step": "histogram_construction", "duration": 30, "action": "build_histogram"},
                    {"step": "measures_calculation", "duration": 25, "action": "calculate_statistics"},
                    {"step": "distribution_analysis", "duration": 25, "action": "show_distribution"}
                ],
                "manim_components": ["Dot", "Rectangle", "NumberLine", "Text", "MathTex"]
            }
        }
    
    @staticmethod
    def get_physics_templates() -> Dict[str, Dict[str, Any]]:
        """Get enhanced physics visual templates"""
        return {
            "mechanics_simulation": {
                "name": "Classical Mechanics Simulation",
                "description": "Simulate motion, forces, and energy conservation",
                "duration": 90,
                "visual_elements": ["moving_objects", "force_vectors", "trajectory_paths", "energy_bars"],
                "animation_sequence": [
                    {"step": "setup_scene", "duration": 15, "action": "create_environment"},
                    {"step": "apply_forces", "duration": 25, "action": "show_force_vectors"},
                    {"step": "motion_simulation", "duration": 35, "action": "animate_motion"},
                    {"step": "energy_analysis", "duration": 15, "action": "show_energy_conservation"}
                ],
                "manim_components": ["Circle", "Arrow", "Line", "Text", "MathTex"]
            },
            
            "wave_propagation": {
                "name": "Wave Motion and Propagation",
                "description": "Visualize different types of waves and their properties",
                "duration": 80,
                "visual_elements": ["wave_source", "wavefronts", "interference_patterns", "frequency_analysis"],
                "animation_sequence": [
                    {"step": "wave_generation", "duration": 20, "action": "create_wave_source"},
                    {"step": "propagation", "duration": 30, "action": "animate_wave_propagation"},
                    {"step": "interference", "duration": 20, "action": "show_interference"},
                    {"step": "frequency_analysis", "duration": 10, "action": "display_frequency"}
                ],
                "manim_components": ["SineWave", "Line", "Text", "MathTex"]
            },
            
            "electromagnetic_field": {
                "name": "Electric and Magnetic Field Visualization",
                "description": "Show field lines and electromagnetic interactions",
                "duration": 110,
                "visual_elements": ["field_lines", "charge_particles", "field_vectors", "field_strength"],
                "animation_sequence": [
                    {"step": "field_setup", "duration": 25, "action": "create_field_sources"},
                    {"step": "field_lines", "duration": 30, "action": "draw_field_lines"},
                    {"step": "particle_interaction", "duration": 35, "action": "simulate_particle_motion"},
                    {"step": "field_strength", "duration": 20, "action": "show_field_intensity"}
                ],
                "manim_components": ["Arrow", "Circle", "Dot", "Text", "MathTex"]
            },
            
            "thermodynamics_process": {
                "name": "Thermodynamic Process Visualization",
                "description": "Show heat transfer and thermodynamic cycles",
                "duration": 95,
                "visual_elements": ["heat_sources", "temperature_gradient", "molecular_motion", "energy_diagrams"],
                "animation_sequence": [
                    {"step": "system_setup", "duration": 20, "action": "create_thermodynamic_system"},
                    {"step": "heat_transfer", "duration": 25, "action": "show_heat_flow"},
                    {"step": "temperature_change", "duration": 25, "action": "animate_temperature"},
                    {"step": "energy_analysis", "duration": 25, "action": "show_energy_diagram"}
                ],
                "manim_components": ["Rectangle", "Arrow", "Circle", "Text", "MathTex"]
            },
            
            "optics_simulation": {
                "name": "Light Propagation and Optics",
                "description": "Demonstrate reflection, refraction, and optical phenomena",
                "duration": 85,
                "visual_elements": ["light_rays", "optical_surfaces", "focal_points", "image_formation"],
                "animation_sequence": [
                    {"step": "light_source", "duration": 15, "action": "create_light_beam"},
                    {"step": "surface_interaction", "duration": 25, "action": "show_reflection_refraction"},
                    {"step": "focal_analysis", "duration": 25, "action": "find_focal_points"},
                    {"step": "image_formation", "duration": 20, "action": "show_image_formation"}
                ],
                "manim_components": ["Line", "Arrow", "Circle", "Text", "MathTex"]
            },
            
            "quantum_mechanics": {
                "name": "Quantum Phenomena Visualization",
                "description": "Illustrate quantum mechanical concepts and experiments",
                "duration": 120,
                "visual_elements": ["wave_functions", "probability_clouds", "energy_levels", "quantum_states"],
                "animation_sequence": [
                    {"step": "wave_function", "duration": 30, "action": "show_wave_function"},
                    {"step": "probability", "duration": 30, "action": "display_probability_cloud"},
                    {"step": "energy_levels", "duration": 30, "action": "show_energy_diagram"},
                    {"step": "quantum_transition", "duration": 30, "action": "animate_quantum_jump"}
                ],
                "manim_components": ["FunctionGraph", "Dot", "Line", "Text", "MathTex"]
            }
        }
    
    @staticmethod
    def get_computer_science_templates() -> Dict[str, Dict[str, Any]]:
        """Get enhanced computer science visual templates"""
        return {
            "algorithm_visualization": {
                "name": "Algorithm Step-by-Step Execution",
                "description": "Visualize algorithm execution with code and animations",
                "duration": 100,
                "visual_elements": ["code_display", "variable_tracker", "execution_pointer", "data_structures"],
                "animation_sequence": [
                    {"step": "algorithm_intro", "duration": 20, "action": "show_algorithm"},
                    {"step": "initialization", "duration": 15, "action": "initialize_variables"},
                    {"step": "execution_loop", "duration": 45, "action": "step_through_algorithm"},
                    {"step": "result_display", "duration": 20, "action": "show_final_result"}
                ],
                "manim_components": ["Text", "Rectangle", "Arrow", "Highlight"]
            },
            
            "data_structure_operations": {
                "name": "Data Structure Manipulation",
                "description": "Show operations on various data structures",
                "duration": 90,
                "visual_elements": ["structure_display", "operation_arrows", "memory_cells", "pointers"],
                "animation_sequence": [
                    {"step": "structure_creation", "duration": 20, "action": "create_data_structure"},
                    {"step": "insertion_operation", "duration": 25, "action": "show_insertion"},
                    {"step": "deletion_operation", "duration": 25, "action": "show_deletion"},
                    {"step": "traversal", "duration": 20, "action": "traverse_structure"}
                ],
                "manim_components": ["Circle", "Rectangle", "Arrow", "Text"]
            },
            
            "sorting_algorithm": {
                "name": "Sorting Algorithm Comparison",
                "description": "Compare different sorting algorithms visually",
                "duration": 110,
                "visual_elements": ["data_array", "sorting_steps", "comparison_counters", "efficiency_metrics"],
                "animation_sequence": [
                    {"step": "data_preparation", "duration": 15, "action": "create_random_array"},
                    {"step": "sorting_process", "duration": 70, "action": "perform_sorting"},
                    {"step": "comparison", "duration": 15, "action": "compare_algorithms"},
                    {"step": "results", "duration": 10, "action": "show_efficiency"}
                ],
                "manim_components": ["Rectangle", "Text", "Arrow", "MathTex"]
            },
            
            "graph_algorithms": {
                "name": "Graph Traversal and Pathfinding",
                "description": "Visualize graph algorithms and shortest paths",
                "duration": 95,
                "visual_elements": ["graph_nodes", "graph_edges", "traversal_path", "distance_metrics"],
                "animation_sequence": [
                    {"step": "graph_creation", "duration": 20, "action": "create_graph"},
                    {"step": "traversal_start", "duration": 25, "action": "begin_traversal"},
                    {"step": "pathfinding", "duration": 35, "action": "find_shortest_path"},
                    {"step": "optimization", "duration": 15, "action": "show_optimization"}
                ],
                "manim_components": ["Circle", "Line", "Arrow", "Text"]
            },
            
            "recursion_visualization": {
                "name": "Recursive Function Execution",
                "description": "Show recursive function calls and stack behavior",
                "duration": 80,
                "visual_elements": ["call_stack", "function_frames", "return_values", "base_case"],
                "animation_sequence": [
                    {"step": "initial_call", "duration": 15, "action": "create_initial_frame"},
                    {"step": "recursive_calls", "duration": 35, "action": "build_call_stack"},
                    {"step": "base_case", "duration": 15, "action": "reach_base_case"},
                    {"step": "unwinding", "duration": 15, "action": "return_from_recursion"}
                ],
                "manim_components": ["Rectangle", "Text", "Arrow", "MathTex"]
            },
            
            "complexity_analysis": {
                "name": "Algorithm Complexity Visualization",
                "description": "Compare time and space complexity of algorithms",
                "duration": 85,
                "visual_elements": ["complexity_graphs", "growth_curves", "performance_metrics", "comparison_charts"],
                "animation_sequence": [
                    {"step": "complexity_intro", "duration": 20, "action": "introduce_complexity"},
                    {"step": "growth_curves", "duration": 30, "action": "plot_growth_curves"},
                    {"step": "algorithm_comparison", "duration": 25, "action": "compare_algorithms"},
                    {"step": "practical_analysis", "duration": 10, "action": "practical_implications"}
                ],
                "manim_components": ["Axes", "FunctionGraph", "Text", "MathTex"]
            }
        }
    
    @staticmethod
    def get_finance_templates() -> Dict[str, Dict[str, Any]]:
        """Get enhanced finance visual templates"""
        return {
            "portfolio_optimization": {
                "name": "Portfolio Theory and Optimization",
                "description": "Visualize Modern Portfolio Theory and efficient frontier",
                "duration": 120,
                "visual_elements": ["asset_points", "efficient_frontier", "risk_return_axes", "portfolio_composition"],
                "animation_sequence": [
                    {"step": "asset_introduction", "duration": 25, "action": "show_individual_assets"},
                    {"step": "risk_return_plot", "duration": 30, "action": "plot_risk_return_space"},
                    {"step": "efficient_frontier", "duration": 35, "action": "construct_frontier"},
                    {"step": "optimal_portfolio", "duration": 30, "action": "highlight_optimal_portfolio"}
                ],
                "manim_components": ["Dot", "Line", "Text", "MathTex", "Axes"]
            },
            
            "financial_modeling": {
                "name": "Financial Model Construction",
                "description": "Build and analyze financial models and scenarios",
                "duration": 100,
                "visual_elements": ["financial_statements", "cash_flows", "scenario_trees", "sensitivity_analysis"],
                "animation_sequence": [
                    {"step": "model_setup", "duration": 20, "action": "create_financial_model"},
                    {"step": "cash_flows", "duration": 30, "action": "model_cash_flows"},
                    {"step": "scenario_analysis", "duration": 30, "action": "analyze_scenarios"},
                    {"step": "sensitivity", "duration": 20, "action": "sensitivity_analysis"}
                ],
                "manim_components": ["Rectangle", "Text", "Line", "MathTex"]
            },
            
            "derivatives_pricing": {
                "name": "Options and Derivatives Pricing",
                "description": "Visualize option pricing models and payoff diagrams",
                "duration": 110,
                "visual_elements": ["payoff_diagrams", "pricing_curves", "greeks_visualization", "binomial_trees"],
                "animation_sequence": [
                    {"step": "option_introduction", "duration": 25, "action": "introduce_options"},
                    {"step": "payoff_diagrams", "duration": 30, "action": "plot_payoffs"},
                    {"step": "pricing_model", "duration": 30, "action": "show_pricing"},
                    {"step": "greeks", "duration": 25, "action": "visualize_sensitivities"}
                ],
                "manim_components": ["Line", "FunctionGraph", "Text", "MathTex"]
            },
            
            "market_analysis": {
                "name": "Market Dynamics and Analysis",
                "description": "Analyze market behavior and trading patterns",
                "duration": 90,
                "visual_elements": ["price_charts", "volume_analysis", "market_trends", "technical_indicators"],
                "animation_sequence": [
                    {"step": "market_data", "duration": 20, "action": "display_price_data"},
                    {"step": "chart_analysis", "duration": 30, "action": "analyze_charts"},
                    {"step": "technical_indicators", "duration": 25, "action": "add_indicators"},
                    {"step": "trading_signals", "duration": 15, "action": "show_signals"}
                ],
                "manim_components": ["Line", "Text", "MathTex", "Axes"]
            },
            
            "risk_management": {
                "name": "Risk Assessment and Management",
                "description": "Visualize risk metrics and hedging strategies",
                "duration": 95,
                "visual_elements": ["risk_metrics", "distribution_charts", "hedging_strategies", "stress_tests"],
                "animation_sequence": [
                    {"step": "risk_identification", "duration": 20, "action": "identify_risks"},
                    {"step": "measurement", "duration": 25, "action": "measure_risks"},
                    {"step": "hedging", "duration": 30, "action": "implement_hedges"},
                    {"step": "stress_testing", "duration": 20, "action": "stress_test"}
                ],
                "manim_components": ["Rectangle", "Text", "MathTex", "FunctionGraph"]
            },
            
            "corporate_finance": {
                "name": "Corporate Financial Decision Making",
                "description": "Analyze capital budgeting and corporate finance decisions",
                "duration": 105,
                "visual_elements": ["project_cash_flows", "decision_trees", "valuation_models", "financing_options"],
                "animation_sequence": [
                    {"step": "project_analysis", "duration": 25, "action": "analyze_projects"},
                    {"step": "valuation", "duration": 30, "action": "calculate_values"},
                    {"step": "financing", "duration": 25, "action": "analyze_financing"},
                    {"step": "decision", "duration": 25, "action": "make_decision"}
                ],
                "manim_components": ["Text", "MathTex", "Line", "Rectangle"]
            }
        }
    
    @staticmethod
    def get_chemistry_templates() -> Dict[str, Dict[str, Any]]:
        """Get enhanced chemistry visual templates"""
        return {
            "molecular_structure": {
                "name": "3D Molecular Geometry and Bonding",
                "description": "Visualize molecular structures and chemical bonding",
                "duration": 85,
                "visual_elements": ["atom_positions", "bond_visualization", "electron_density", "molecular_orbitals"],
                "animation_sequence": [
                    {"step": "atom_placement", "duration": 20, "action": "position_atoms"},
                    {"step": "bond_formation", "duration": 25, "action": "form_bonds"},
                    {"step": "geometry_optimization", "duration": 25, "action": "optimize_geometry"},
                    {"step": "electronic_structure", "duration": 15, "action": "show_electrons"}
                ],
                "manim_components": ["Circle", "Line", "Text", "MathTex"]
            },
            
            "chemical_reaction": {
                "name": "Chemical Reaction Mechanisms",
                "description": "Show reaction mechanisms and energy profiles",
                "duration": 100,
                "visual_elements": ["reactant_molecules", "transition_state", "product_molecules", "energy_diagram"],
                "animation_sequence": [
                    {"step": "reactants", "duration": 20, "action": "show_reactants"},
                    {"step": "reaction_path", "duration": 30, "action": "animate_reaction"},
                    {"step": "transition_state", "duration": 25, "action": "show_activation_complex"},
                    {"step": "products", "duration": 25, "action": "show_products"}
                ],
                "manim_components": ["Circle", "Arrow", "Line", "Text"]
            },
            
            "periodic_trends": {
                "name": "Periodic Table Trends Visualization",
                "description": "Visualize periodic trends and relationships",
                "duration": 90,
                "visual_elements": ["periodic_table", "trend_arrows", "property_graphs", "atomic_models"],
                "animation_sequence": [
                    {"step": "periodic_table", "duration": 25, "action": "display_table"},
                    {"step": "trend_analysis", "duration": 30, "action": "analyze_trends"},
                    {"step": "property_comparison", "duration": 20, "action": "compare_properties"},
                    {"step": "underlying_cause", "duration": 15, "action": "explain_trends"}
                ],
                "manim_components": ["Rectangle", "Text", "Line", "MathTex"]
            },
            
            "thermodynamics": {
                "name": "Chemical Thermodynamics",
                "description": "Visualize enthalpy, entropy, and Gibbs free energy",
                "duration": 110,
                "visual_elements": ["energy_diagrams", "molecular_motion", "enthalpy_changes", "entropy_visualization"],
                "animation_sequence": [
                    {"step": "system_setup", "duration": 20, "action": "define_system"},
                    {"step": "energy_analysis", "duration": 30, "action": "analyze_energy"},
                    {"step": "entropy_change", "duration": 30, "action": "show_entropy"},
                    {"step": "spontaneity", "duration": 30, "action": "determine_spontaneity"}
                ],
                "manim_components": ["FunctionGraph", "Text", "MathTex", "Arrow"]
            },
            
            "equilibrium_dynamics": {
                "name": "Chemical Equilibrium and Le Chatelier",
                "description": "Show dynamic equilibrium and equilibrium shifts",
                "duration": 95,
                "visual_elements": ["equilibrium_mixture", "concentration_graphs", "disturbance_effects", "reestablishment"],
                "animation_sequence": [
                    {"step": "initial_equilibrium", "duration": 20, "action": "establish_equilibrium"},
                    {"step": "disturbance", "duration": 25, "action": "apply_disturbance"},
                    {"step": "response", "duration": 30, "action": "show_response"},
                    {"step": "new_equilibrium", "duration": 20, "action": "reach_new_equilibrium"}
                ],
                "manim_components": ["Rectangle", "Line", "Text", "MathTex"]
            },
            
            "acid_base_chemistry": {
                "name": "Acid-Base Reactions and pH",
                "description": "Visualize acid-base reactions and pH changes",
                "duration": 85,
                "visual_elements": ["pH_scale", "titration_curve", "buffer_systems", "molecular_structures"],
                "animation_sequence": [
                    {"step": "ph_introduction", "duration": 20, "action": "introduce_ph"},
                    {"step": "acid_base_reaction", "duration": 25, "action": "show_reaction"},
                    {"step": "titration_process", "duration": 25, "action": "perform_titration"},
                    {"step": "buffer_action", "duration": 15, "action": "demonstrate_buffer"}
                ],
                "manim_components": ["Line", "Text", "MathTex", "Rectangle"]
            },
            
            "electrochemistry": {
                "name": "Electrochemical Cells and Reactions",
                "description": "Visualize galvanic and electrolytic cells",
                "duration": 100,
                "visual_elements": ["cell_diagram", "electron_flow", "ion_movement", "potential_diagram"],
                "animation_sequence": [
                    {"step": "cell_setup", "duration": 20, "action": "construct_cell"},
                    {"step": "electron_flow", "duration": 25, "action": "show_electron_flow"},
                    {"step": "ion_migration", "duration": 25, "action": "show_ion_movement"},
                    {"step": "potential_analysis", "duration": 30, "action": "analyze_potential"}
                ],
                "manim_components": ["Rectangle", "Arrow", "Text", "MathTex"]
            }
        }

def get_all_templates() -> Dict[str, Dict[str, Dict[str, Any]]]:
    """Get all enhanced templates for all subjects"""
    return {
        "math": TemplateLibrary.get_math_templates(),
        "physics": TemplateLibrary.get_physics_templates(),
        "algorithms": TemplateLibrary.get_computer_science_templates(),
        "finance": TemplateLibrary.get_finance_templates(),
        "chemistry": TemplateLibrary.get_chemistry_templates()
    }

def get_subject_templates(subject: str) -> Dict[str, Dict[str, Any]]:
    """Get templates for a specific subject"""
    all_templates = get_all_templates()
    return all_templates.get(subject, {})