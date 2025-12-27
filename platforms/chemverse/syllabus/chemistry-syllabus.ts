/**
 * Chemistry Syllabus - ChemVerse Platform
 * 
 * This file defines the comprehensive curriculum structure for chemistry education,
 * covering physical, organic, and inorganic chemistry.
 * 
 * Licensed under the Apache License, Version 2.0
 */

export interface ChemistryUnit {
  id: string;
  name: string;
  description: string;
  concepts: string[];
  duration_hours: number;
  difficulty_level: 'beginner' | 'elementary' | 'intermediate' | 'advanced' | 'expert';
  prerequisites: string[];
  learning_outcomes: string[];
  lab_components: string[];
  molecular_visualizations: string[];
  standards: string[];
}

export interface ChemistrySection {
  id: string;
  name: string;
  description: string;
  units: ChemistryUnit[];
  total_duration_hours: number;
  sequence_order: number;
}

export interface ChemistrySyllabus {
  subject: 'chemistry';
  display_name: 'Chemistry';
  description: 'Comprehensive chemistry curriculum from atomic structure through organic synthesis';
  total_duration_hours: number;
  sections: ChemistrySection[];
  applicable_standards: string[];
  grade_levels: string[];
}

// ============================================
// SECTION 1: FUNDAMENTAL CONCEPTS
// ============================================

const section1: ChemistrySection = {
  id: 'fundamental-chemistry',
  name: 'Fundamental Chemistry Concepts',
  description: 'Basic principles of matter, atomic structure, and chemical bonding',
  units: [],
  total_duration_hours: 80,
  sequence_order: 1
};

section1.units = [
  {
    id: 'matter-classification',
    name: 'Matter and Its Classification',
    description: 'States of matter, mixtures, and pure substances',
    concepts: ['states-matter', 'physical-chemical-changes', 'mixtures-pure-substances', 'elements-compounds', 'homogeneous-heterogeneous', 'separation-techniques'],
    duration_hours: 15,
    difficulty_level: 'beginner',
    prerequisites: [],
    learning_outcomes: [
      'Classify matter by state and composition',
      'Distinguish physical and chemical changes',
      'Identify homogeneous and heterogeneous mixtures',
      'Apply appropriate separation techniques'
    ],
    lab_components: ['filtration', 'distillation', 'chromatography'],
    molecular_visualizations: ['matter-states', 'mixture-types'],
    standards: ['NGSS.MS-PS1.A', 'NGSS.HS-PS1.A']
  },
  {
    id: 'atomic-structure',
    name: 'Atomic Structure and Electron Configuration',
    description: 'Understanding the structure of atoms and electron arrangements',
    concepts: ['atomic-structure', 'subatomic-particles', 'isotopes', 'atomic-mass', 'electron-shells', 'electron-configuration', 'quantum-numbers', 'orbital-diagrams'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['matter-classification'],
    learning_outcomes: [
      'Describe the structure of atoms and subatomic particles',
      'Calculate atomic mass from isotope abundances',
      'Write electron configurations for elements',
      'Apply quantum numbers to describe electrons'
    ],
    lab_components: ['mass-spectrometry', 'flame-test'],
    molecular_visualizations: ['atomic-models', 'electron-orbitals'],
    standards: ['NGSS.HS-PS1.A', 'NGSS.HS-PS1.C']
  },
  {
    id: 'periodic-table',
    name: 'Periodic Table and Periodic Trends',
    description: 'Organization of elements and predictable patterns',
    concepts: ['periodic-law', 'period-groups', 'periodic-trends', 'atomic-radius', 'ionization-energy', 'electronegativity', 'metallic-character', 'periodic-table-blocks'],
    duration_hours: 20,
    difficulty_level: 'intermediate',
    prerequisites: ['atomic-structure'],
    learning_outcomes: [
      'Explain the organization of the periodic table',
      'Predict periodic trends from atomic structure',
      'Relate position to properties of elements',
      'Identify element groups and their characteristics'
    ],
    lab_components: ['element-properties-investigation'],
    molecular_visualizations: ['periodic-trends', 'atomic-size-comparison'],
    standards: ['NGSS.HS-PS1.A', 'NGSS.HS-PS1.C']
  },
  {
    id: 'chemical-bonding',
    name: 'Chemical Bonding and Molecular Structure',
    description: 'Types of chemical bonds and molecular geometry',
    concepts: ['ionic-bonding', 'covalent-bonding', 'metallic-bonding', 'lewis-structures', 'molecular-geometry', 'VSEPR-theory', 'bond-polarity', 'intermolecular-forces'],
    duration_hours: 20,
    difficulty_level: 'intermediate',
    prerequisites: ['periodic-table', 'atomic-structure'],
    learning_outcomes: [
      'Explain formation of ionic, covalent, and metallic bonds',
      'Draw Lewis structures for molecules',
      'Predict molecular geometry using VSEPR theory',
      'Analyze bond and molecular polarity'
    ],
    lab_components: ['bond-type-investigation', 'molecular-model-kits'],
    molecular_visualizations: ['bond-formation', 'molecular-shapes', 'electron-density'],
    standards: ['NGSS.HS-PS1.A', 'NGSS.HS-PS1.C']
  }
];

// ============================================
// SECTION 2: STOICHIOMETRY AND REACTIONS
// ============================================

const section2: ChemistrySection = {
  id: 'stoichiometry',
  name: 'Stoichiometry and Chemical Reactions',
  description: 'Quantitative relationships in chemical reactions',
  units: [],
  total_duration_hours: 70,
  sequence_order: 2
};

section2.units = [
  {
    id: 'nomenclature',
    name: 'Chemical Nomenclature and Formulas',
    description: 'Naming compounds and writing chemical formulas',
    concepts: ['ionic-compounds', 'molecular-compounds', 'acids-bases', 'hydrates', 'naming-rules', 'empirical-molecular-formulas'],
    duration_hours: 15,
    difficulty_level: 'beginner',
    prerequisites: ['chemical-bonding'],
    learning_outcomes: [
      'Name ionic and molecular compounds',
      'Write formulas from compound names',
      'Identify and name acids and bases',
      'Calculate empirical and molecular formulas'
    ],
    lab_components: ['formula-determination'],
    molecular_visualizations: ['compound-structures'],
    standards: ['NGSS.HS-PS1.A', 'NGSS.HS-PS1.C']
  },
  {
    id: 'mole-concept',
    name: 'The Mole Concept and Molar Mass',
    description: 'Counting atoms and molecules by weighing',
    concepts: ['mole-definition', 'avogadro-number', 'molar-mass', 'molar-volume', 'molarity', 'percent-composition'],
    duration_hours: 20,
    difficulty_level: 'intermediate',
    prerequisites: ['nomenclature', 'atomic-structure'],
    learning_outcomes: [
      'Relate moles to number of particles',
      'Calculate molar masses of compounds',
      'Convert between mass, moles, and particles',
      'Prepare solutions of known concentration'
    ],
    lab_components: ['molar-mass-determination', 'solution-preparation'],
    molecular_visualizations: ['mole-concept', 'particle-counting'],
    standards: ['NGSS.HS-PS1.B', 'NGSS.HS-PS1.C']
  },
  {
    id: 'balancing-equations',
    name: 'Balancing Chemical Equations',
    description: 'Writing and balancing chemical equations',
    concepts: ['chemical-equations', 'balancing-rules', 'reaction-types', 'synthesis-decomposition', 'single-replacement', 'double-replacement', 'combustion'],
    duration_hours: 15,
    difficulty_level: 'intermediate',
    prerequisites: ['mole-concept'],
    learning_outcomes: [
      'Write balanced chemical equations',
      'Identify types of chemical reactions',
      'Predict products of common reaction types',
      'Apply conservation of mass to reactions'
    ],
    lab_components: ['reaction-types-demonstration'],
    molecular_visualizations: ['reaction-animation', 'conservation-mass'],
    standards: ['NGSS.HS-PS1.B', 'NGSS.HS-PS1.C']
  },
  {
    id: 'stoichiometry-calculations',
    name: 'Stoichiometry Calculations',
    description: 'Quantitative analysis of chemical reactions',
    concepts: ['stoichiometric-ratios', 'limiting-reactants', 'percent-yield', 'theoretical-yield', 'excess-reagents', 'gas-stoichiometry'],
    duration_hours: 20,
    difficulty_level: 'advanced',
    prerequisites: ['balancing-equations'],
    learning_outcomes: [
      'Calculate quantities using stoichiometric ratios',
      'Identify limiting and excess reactants',
      'Calculate theoretical and percent yields',
      'Solve gas stoichiometry problems'
    ],
    lab_components: ['stoichiometry-lab', 'yield-determination'],
    molecular_visualizations: ['reaction-stoichiometry', 'limiting-reactant'],
    standards: ['NGSS.HS-PS1.B', 'NGSS.HS-PS1.C']
  }
];

// ============================================
// SECTION 3: PHYSICAL CHEMISTRY
// ============================================

const section3: ChemistrySection = {
  id: 'physical-chemistry',
  name: 'Physical Chemistry',
  description: 'Thermodynamics, kinetics, and equilibrium in chemical systems',
  units: [],
  total_duration_hours: 85,
  sequence_order: 3
};

section3.units = [
  {
    id: 'thermochemistry',
    name: 'Thermochemistry and Energy Changes',
    description: 'Heat changes in chemical reactions and processes',
    concepts: ['system-surroundings', 'endothermic-exothermic', 'enthalpy', 'heat-capacity', 'calorimetry', 'hess-law', 'bond-energies', 'standard-enthalpy'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['stoichiometry-calculations'],
    learning_outcomes: [
      'Classify reactions as endothermic or exothermic',
      'Calculate enthalpy changes using Hess\'s Law',
      'Perform calorimetry experiments',
      'Use bond energies to estimate reaction enthalpy'
    ],
    lab_components: ['calorimetry-lab', 'heat-reaction-measurement'],
    molecular_visualizations: ['energy-diagrams', 'enthalpy-changes'],
    standards: ['NGSS.HS-PS1.B', 'NGSS.HS-PS3.A']
  },
  {
    id: 'chemical-kinetics',
    name: 'Chemical Kinetics',
    description: 'Rates of chemical reactions and reaction mechanisms',
    concepts: ['reaction-rates', 'rate-laws', 'rate-constants', 'reaction-order', 'arrhenius-equation', 'activation-energy', 'reaction-mechanisms', 'catalysts'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['thermochemistry'],
    learning_outcomes: [
      'Determine reaction rates from experimental data',
      'Write and use rate laws',
      'Calculate activation energy using Arrhenius equation',
      'Analyze reaction mechanisms and catalyst effects'
    ],
    lab_components: ['kinetics-lab', 'clock-reactions'],
    molecular_visualizations: ['reaction-pathway', 'activation-energy', 'catalysis'],
    standards: ['NGSS.HS-PS1.B', 'NGSS.HS-PS1.C']
  },
  {
    id: 'chemical-equilibrium',
    name: 'Chemical Equilibrium',
    description: 'Dynamic equilibrium in reversible reactions',
    concepts: ['equilibrium-concept', 'equilibrium-constant', 'Le-Chatelier-principle', 'equilibrium-shifts', 'homogeneous-equilibrium', 'heterogeneous-equilibrium', 'reaction-quotient'],
    duration_hours: 20,
    difficulty_level: 'advanced',
    prerequisites: ['chemical-kinetics'],
    learning_outcomes: [
      'Write equilibrium constant expressions',
      'Apply Le Chatelier\'s principle to predict shifts',
      'Calculate equilibrium concentrations',
      'Analyze heterogeneous equilibrium systems'
    ],
    lab_components: ['equilibrium-investigation', 'color-change-reactions'],
    molecular_visualizations: ['equilibrium-animation', 'Le-Chatelier-principle'],
    standards: ['NGSS.HS-PS1.B', 'NGSS.HS-PS1.C']
  },
  {
    id: 'acids-bases',
    name: 'Acids, Bases, and Salts',
    description: 'Properties and reactions of acids and bases',
    concepts: ['acid-base-definitions', 'pH-scale', 'strong-weak-acids', 'acid-base-titration', 'buffer-solutions', 'hydrolysis', 'salt-solutions'],
    duration_hours: 15,
    difficulty_level: 'advanced',
    prerequisites: ['chemical-equilibrium'],
    learning_outcomes: [
      'Define acids and bases using multiple theories',
      'Calculate pH from hydrogen ion concentration',
      'Perform and analyze acid-base titrations',
      'Explain buffer action and prepare buffer solutions'
    ],
    lab_components: ['titration-lab', 'pH-measurement', 'buffer-preparation'],
    molecular_visualizations: ['acid-base-dissociation', 'titration-curve'],
    standards: ['NGSS.HS-PS1.B', 'NGSS.HS-PS1.C']
  }
];

// ============================================
// SECTION 4: INORGANIC CHEMISTRY
// ============================================

const section4: ChemistrySection = {
  id: 'inorganic-chemistry',
  name: 'Inorganic Chemistry',
  description: 'Properties and reactions of inorganic compounds and elements',
  units: [],
  total_duration_hours: 70,
  sequence_order: 4
};

section4.units = [
  {
    id: 'redox-reactions',
    name: 'Redox Reactions and Electrochemistry',
    description: 'Electron transfer in chemical reactions',
    concepts: ['oxidation-reduction', 'oxidation-numbers', 'balancing-redox', 'galvanic-cells', 'electrolytic-cells', 'electrode-potentials', 'electrolysis', 'corrosion'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['acids-bases'],
    learning_outcomes: [
      'Identify oxidation and reduction in reactions',
      'Assign oxidation numbers to elements',
      'Balance redox equations using various methods',
      'Analyze electrochemical cell operation'
    ],
    lab_components: ['voltaic-cell-lab', 'electrolysis-demo', 'titration-redox'],
    molecular_visualizations: ['electron-transfer', 'electrochemical-cells'],
    standards: ['NGSS.HS-PS1.B', 'NGSS.HS-PS2.B']
  },
  {
    id: 'main-group',
    name: 'Main Group Elements',
    description: 'Properties and compounds of s-block and p-block elements',
    concepts: ['alkali-metals', 'alkaline-earth-metals', 'halogens', 'noble-gases', 'oxygen-family', 'nitrogen-family', 'carbon-family', 'periodic-trends-main-group'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['periodic-table'],
    learning_outcomes: [
      'Describe properties of main group element groups',
      'Explain periodic trends in main group elements',
      'Compare properties of compounds across groups',
      'Predict reactivity based on position in periodic table'
    ],
    lab_components: ['element-property-investigation', 'compound-synthesis'],
    molecular_visualizations: ['main-group-properties', 'periodic-trends'],
    standards: ['NGSS.HS-PS1.A', 'NGSS.HS-PS1.C']
  },
  {
    id: 'transition-metals',
    name: 'Transition Metals and Coordination Chemistry',
    description: 'Properties of transition metals and their complexes',
    concepts: ['transition-metals', 'coordination-compounds', 'ligands', 'coordination-number', 'coordination-geometry', 'crystal-field-theory', 'color-transition-complexes', 'magnetic-properties'],
    duration_hours: 20,
    difficulty_level: 'expert',
    prerequisites: ['main-group', 'atomic-structure'],
    learning_outcomes: [
      'Describe properties of transition metals',
      'Name and write formulas for coordination compounds',
      'Explain geometry and isomerism in coordination complexes',
      'Apply crystal field theory to explain properties'
    ],
    lab_components: ['coordination-compound-synthesis', 'spectrophotometry'],
    molecular_visualizations: ['coordination-geometries', 'crystal-field-splitting', 'd-orbital-diagrams'],
    standards: ['NGSS.HS-PS1.A', 'NGSS.HS-PS1.C']
  }
];

// ============================================
// SECTION 5: ORGANIC CHEMISTRY
// ============================================

const section5: ChemistrySection = {
  id: 'organic-chemistry',
  name: 'Organic Chemistry',
  description: 'Structure, properties, and reactions of carbon compounds',
  units: [],
  total_duration_hours: 90,
  sequence_order: 5
};

section5.units = [
  {
    id: 'organic-fundamentals',
    name: 'Fundamentals of Organic Chemistry',
    description: 'Basic principles of organic molecules and their classification',
    concepts: ['organic-carbon', 'hydrocarbons', 'functional-groups', 'hydrocarbon-classes', 'structural-isomers', 'nomenclature-alkanes', 'nomenclature-alkenes-alkynes', 'aromatic-compounds'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['chemical-bonding'],
    learning_outcomes: [
      'Explain the uniqueness of carbon in organic chemistry',
      'Identify and classify hydrocarbon types',
      'Name alkanes, alkenes, and alkynes using IUPAC rules',
      'Recognize aromatic compounds and their properties'
    ],
    lab_components: ['molecular-model-building', 'hydrocarbon-properties'],
    molecular_visualizations: ['carbon-bonding', 'isomer-types', 'functional-groups'],
    standards: ['NGSS.HS-PS1.A', 'NGSS.HS-PS1.C']
  },
  {
    id: 'stereochemistry',
    name: 'Stereochemistry and Isomerism',
    description: 'Spatial arrangement of atoms in organic molecules',
    concepts: ['geometric-isomerism', 'optical-isomerism', 'chirality', 'enantiomers', 'diastereomers', 'conformational-analysis', 'CIP-rules', 'racemic-mixtures'],
    duration_hours: 20,
    difficulty_level: 'advanced',
    prerequisites: ['organic-fundamentals'],
    learning_outcomes: [
      'Identify and distinguish types of isomers',
      'Apply Cahn-Ingold-Prelog priority rules',
      'Analyze conformational isomers in alkanes',
      'Explain the significance of chirality in molecules'
    ],
    lab_components: ['chiral-molecule-models', 'polarimetry'],
    molecular_visualizations: ['3d-molecular-structures', 'isomer-animation', 'chirality-visualization'],
    standards: ['NGSS.HS-PS1.A', 'NGSS.HS-PS1.C']
  },
  {
    id: 'organic-reactions',
    name: 'Organic Reaction Mechanisms',
    description: 'Types and mechanisms of organic reactions',
    concepts: ['substitution-reactions', 'elimination-reactions', 'addition-reactions', 'radical-reactions', 'mechanism-arrow-pushing', 'reaction-conditions', 'reaction-selectivity', 'synthesis-strategies'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['stereochemistry', 'redox-reactions'],
    learning_outcomes: [
      'Classify organic reactions by type',
      'Draw reaction mechanisms using arrow pushing',
      'Predict products of common organic reactions',
      'Develop multi-step synthesis strategies'
    ],
    lab_components: ['organic-reaction-lab', 'synthesis-experiments'],
    molecular_visualizations: ['reaction-mechanisms', 'electron-flow', 'transition-states'],
    standards: ['NGSS.HS-PS1.B', 'NGSS.HS-PS1.C']
  },
  {
    id: 'functional-groups',
    name: 'Functional Group Chemistry',
    description: 'Properties and reactions of major functional groups',
    concepts: ['alcohols-ethers', 'aldehydes-ketones', 'carboxylic-acids', 'esters-amides', 'amines', 'carbonyl-chemistry', 'oxidation-reduction-organic', 'polymerization'],
    duration_hours: 20,
    difficulty_level: 'advanced',
    prerequisites: ['organic-reactions'],
    learning_outcomes: [
      'Name and describe properties of each functional group',
      'Predict reactivity based on functional groups',
      'Explain reactions of carbonyl compounds',
      'Understand polymerization and polymer types'
    ],
    lab_components: ['functional-group-reactions', 'polymer-synthesis'],
    molecular_visualizations: ['functional-group-properties', 'carbonyl-reactions', 'polymer-structures'],
    standards: ['NGSS.HS-PS1.B', 'NGSS.HS-PS1.C']
  }
];

// ============================================
// SECTION 6: ANALYTICAL AND INDUSTRIAL CHEMISTRY
// ============================================

const section6: ChemistrySection = {
  id: 'analytical-industrial',
  name: 'Analytical and Industrial Chemistry',
  description: 'Analytical techniques and industrial chemical processes',
  units: [],
  total_duration_hours: 40,
  sequence_order: 6
};

section6.units = [
  {
    id: 'analytical-techniques',
    name: 'Analytical Chemistry Techniques',
    description: 'Modern methods of chemical analysis',
    concepts: ['spectroscopy-basics', 'chromatography', 'mass-spectrometry', 'titration-advanced', 'electrochemical-analysis', 'qualitative-analysis', 'quantitative-analysis'],
    duration_hours: 20,
    difficulty_level: 'advanced',
    prerequisites: ['physical-chemistry'],
    learning_outcomes: [
      'Explain principles of spectroscopic techniques',
      'Apply chromatographic methods for separation',
      'Interpret mass spectra for compound identification',
      'Choose appropriate analytical techniques for problems'
    ],
    lab_components: ['spectroscopy-lab', 'chromatography-practical', 'instrumental-analysis'],
    molecular_visualizations: ['spectra-interpretation', 'chromatography-process'],
    standards: ['NGSS.HS-PS1.A', 'NGSS.HS-PS1.C']
  },
  {
    id: 'industrial-chemistry',
    name: 'Industrial Chemistry and Sustainability',
    description: 'Large-scale chemical production and environmental considerations',
    concepts: ['industrial-processes', 'fertilizer-production', 'petroleum-refining', 'green-chemistry', 'environmental-chemistry', 'chemical-economics', 'process-optimization'],
    duration_hours: 20,
    difficulty_level: 'advanced',
    prerequisites: ['organic-reactions'],
    learning_outcomes: [
      'Describe major industrial chemical processes',
      'Apply green chemistry principles',
      'Analyze environmental impact of chemical production',
      'Optimize industrial processes for efficiency'
    ],
    lab_components: ['industrial-process-models', 'green-chemistry-experiments'],
    molecular_visualizations: ['industrial-flow-diagrams', 'green-chemistry-comparison'],
    standards: ['NGSS.HS-ETS1.A', 'NGSS.HS-ETS1.B']
  }
];

// ============================================
// COMPLETE SYLLABUS DEFINITION
// ============================================

export const chemistrySyllabus: ChemistrySyllabus = {
  subject: 'chemistry',
  display_name: 'Chemistry',
  description: 'Comprehensive chemistry curriculum covering atomic structure through organic synthesis',
  total_duration_hours: 435,
  sections: [section1, section2, section3, section4, section5, section6],
  applicable_standards: [
    'Next Generation Science Standards (NGSS)',
    'CBSE (India)',
    'ICSE (India)',
    'GCSE Chemistry',
    'AP Chemistry',
    'IB Chemistry',
    'A-Level Chemistry'
  ],
  grade_levels: ['9', '10', '11', '12', 'Undergraduate']
};

// Export utility functions
export function getChemistryUnitById(syllabus: ChemistrySyllabus, unitId: string): ChemistryUnit | undefined {
  for (const section of syllabus.sections) {
    const unit = section.units.find(u => u.id === unitId);
    if (unit) return unit;
  }
  return undefined;
}

export function getChemistryPrerequisites(syllabus: ChemistrySyllabus, unitId: string): ChemistryUnit[] {
  const unit = getChemistryUnitById(syllabus, unitId);
  if (!unit) return [];
  return unit.prerequisites
    .map(prereqId => getChemistryUnitById(syllabus, prereqId))
    .filter((u): u is ChemistryUnit => u !== undefined);
}

export function generateChemistryLearningPath(
  syllabus: ChemistrySyllabus,
  startUnitId: string,
  targetUnitId: string
): ChemistryUnit[] {
  const path: ChemistryUnit[] = [];
  const visited = new Set<string>();
  
  function addUnitAndPrerequisites(unitId: string) {
    if (visited.has(unitId)) return;
    
    const unit = getChemistryUnitById(syllabus, unitId);
    if (!unit) return;
    
    // Add prerequisites first
    for (const prereqId of unit.prerequisites) {
      addUnitAndPrerequisites(prereqId);
    }
    
    visited.add(unitId);
    path.push(unit);
  }
  
  // Add all units from start to target
  for (const section of syllabus.sections) {
    for (const unit of section.units) {
      if (unit.id >= startUnitId && unit.id <= targetUnitId) {
        addUnitAndPrerequisites(unit.id);
      }
    }
  }
  
  return path;
}

export function calculateChemistryTotalDuration(syllabus: ChemistrySyllabus, unitIds: string[]): number {
  return unitIds.reduce((total, unitId) => {
    const unit = getChemistryUnitById(syllabus, unitId);
    return total + (unit?.duration_hours || 0);
  }, 0);
}

export function getLabComponents(syllabus: ChemistrySyllabus, unitId: string): string[] {
  const unit = getChemistryUnitById(syllabus, unitId);
  return unit?.lab_components || [];
}
