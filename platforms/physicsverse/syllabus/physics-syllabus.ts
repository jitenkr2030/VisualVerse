/**
 * Physics Syllabus - PhysicsVerse Platform
 * 
 * This file defines the comprehensive curriculum structure for physics education,
 * covering mechanics, electromagnetism, optics, and modern physics.
 * 
 * Licensed under the Apache License, Version 2.0
 */

export interface PhysicsUnit {
  id: string;
  name: string;
  description: string;
  concepts: string[];
  duration_hours: number;
  difficulty_level: 'beginner' | 'elementary' | 'intermediate' | 'advanced' | 'expert';
  prerequisites: string[];
  learning_outcomes: string[];
  experimental_components: string[];
  mathematical_prerequisites: string[];
  standards: string[];
}

export interface PhysicsSection {
  id: string;
  name: string;
  description: string;
  units: PhysicsUnit[];
  total_duration_hours: number;
  sequence_order: number;
}

export interface PhysicsSyllabus {
  subject: 'physics';
  display_name: 'Physics';
  description: 'Comprehensive physics curriculum covering classical mechanics through modern physics concepts';
  total_duration_hours: number;
  sections: PhysicsSection[];
  applicable_standards: string[];
  grade_levels: string[];
}

// ============================================
// SECTION 1: CLASSICAL MECHANICS (Part 1)
// ============================================

const section1: PhysicsSection = {
  id: 'mechanics-1',
  name: 'Classical Mechanics - Motion',
  description: 'Fundamental concepts of motion, forces, and energy in mechanical systems',
  units: [],
  total_duration_hours: 90,
  sequence_order: 1
};

section1.units = [
  {
    id: 'units-measurement',
    name: 'Units, Measurement, and Error Analysis',
    description: 'Introduction to physical measurements and scientific notation',
    concepts: ['SI-units', 'dimensional-analysis', 'scientific-notation', 'significant-figures', 'measurement-error', 'uncertainty-propagation'],
    duration_hours: 10,
    difficulty_level: 'beginner',
    prerequisites: [],
    learning_outcomes: [
      'Use SI units and convert between unit systems',
      'Apply dimensional analysis to check equations',
      'Express numbers in scientific notation',
      'Calculate and propagate measurement uncertainties'
    ],
    experimental_components: ['ruler-measurement', 'vernier-caliper', 'micrometer'],
    mathematical_prerequisites: ['basic-arithmetic'],
    standards: ['NGSS.MATH.1', 'NGSS.MATH.2']
  },
  {
    id: 'kinematics-1d',
    name: 'Kinematics in One Dimension',
    description: 'Describing motion along a straight line using kinematics quantities',
    concepts: ['position-displacement', 'velocity-speed', 'acceleration', 'motion-graphs', 'free-fall', 'kinematic-equations'],
    duration_hours: 20,
    difficulty_level: 'beginner',
    prerequisites: ['units-measurement'],
    learning_outcomes: [
      'Distinguish between position, displacement, and distance',
      'Calculate velocity, speed, and acceleration',
      'Interpret motion graphs (position-time, velocity-time)',
      'Apply kinematic equations to free-fall motion'
    ],
    experimental_components: [' ticker-timer', 'motion-sensors', 'video-analysis'],
    mathematical_prerequisites: ['linear-equations'],
    standards: ['NGSS.HS-PS2.A.1', 'NGSS.HS-PS2.A.2']
  },
  {
    id: 'vectors',
    name: 'Vectors and Vector Operations',
    description: 'Introduction to vector quantities and their mathematical operations',
    concepts: ['vector-basics', 'vector-components', 'vector-addition', 'scalar-multiplication', 'dot-product', 'cross-product'],
    duration_hours: 15,
    difficulty_level: 'beginner',
    prerequisites: ['kinematics-1d'],
    learning_outcomes: [
      'Represent and interpret vector quantities',
      'Resolve vectors into components',
      'Perform vector addition and subtraction',
      'Calculate dot and cross products'
    ],
    experimental_components: ['vector-addition-board', 'force-table'],
    mathematical_prerequisites: ['trigonometry-basics'],
    standards: ['NGSS.MATH.3', 'NGSS.MATH.4']
  },
  {
    id: 'kinematics-2d',
    name: 'Kinematics in Two Dimensions',
    description: 'Analyzing motion in a plane using vector quantities',
    concepts: ['projectile-motion', 'relative-velocity', 'circular-motion-basics', 'position-vectors', 'velocity-vectors', 'independent-components'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['vectors', 'kinematics-1d'],
    learning_outcomes: [
      'Analyze projectile motion using kinematics equations',
      'Apply relative velocity concepts',
      'Describe uniform circular motion',
      'Resolve 2D motion into independent components'
    ],
    experimental_components: ['projectile-launcher', 'rotational-motion apparatus'],
    mathematical_prerequisites: ['quadratic-equations', 'trigonometry'],
    standards: ['NGSS.HS-PS2.A.1', 'NGSS.HS-PS2.A.2']
  },
  {
    id: 'newtons-laws',
    name: 'Newton\'s Laws of Motion',
    description: 'Understanding the relationship between forces and motion',
    concepts: ['newton-first-law', 'newton-second-law', 'newton-third-law', 'free-body-diagrams', 'mass-weight', 'equilibrium'],
    duration_hours: 20,
    difficulty_level: 'intermediate',
    prerequisites: ['kinematics-2d', 'vectors'],
    learning_outcomes: [
      'State and apply Newton\'s three laws of motion',
      'Construct accurate free-body diagrams',
      'Calculate net force and acceleration',
      'Analyze forces in equilibrium situations'
    ],
    experimental_components: ['dynamics-cart', ' Atwood-machine', 'force-sensors'],
    mathematical_prerequisites: ['linear-equations'],
    standards: ['NGSS.HS-PS2.A.1', 'NGSS.HS-PS2.A.3']
  }
];

// ============================================
// SECTION 2: CLASSICAL MECHANICS (Part 2)
// ============================================

const section2: PhysicsSection = {
  id: 'mechanics-2',
  name: 'Classical Mechanics - Energy and Momentum',
  description: 'Conservation laws, work, energy, and momentum in physical systems',
  units: [],
  total_duration_hours: 85,
  sequence_order: 2
};

section2.units = [
  {
    id: 'work-energy',
    name: 'Work and Energy',
    description: 'Concepts of work, kinetic energy, and potential energy',
    concepts: ['work-definition', 'work-calculation', 'kinetic-energy', 'potential-energy', 'work-energy-theorem', 'conservative-forces'],
    duration_hours: 20,
    difficulty_level: 'intermediate',
    prerequisites: ['newtons-laws'],
    learning_outcomes: [
      'Calculate work done by constant and variable forces',
      'Apply the work-energy theorem',
      'Distinguish between kinetic and potential energy',
      'Identify and analyze conservative forces'
    ],
    experimental_components: ['work-energy apparatus', 'inclined-plane'],
    mathematical_prerequisites: ['integration-basics'],
    standards: ['NGSS.HS-PS3.A.1', 'NGSS.HS-PS3.A.2']
  },
  {
    id: 'conservation-energy',
    name: 'Conservation of Energy',
    description: 'Energy conservation in isolated and non-isolated systems',
    concepts: ['energy-conservation', 'mechanical-energy', 'power-definition', 'energy-transformation', 'efficiency', 'non-conservative-work'],
    duration_hours: 20,
    difficulty_level: 'intermediate',
    prerequisites: ['work-energy'],
    learning_outcomes: [
      'Apply conservation of mechanical energy',
      'Calculate power in various contexts',
      'Analyze energy transformations and transfers',
      'Calculate efficiency of energy conversion'
    ],
    experimental_components: ['pendulum-experiments', 'energy-conservation demonstration'],
    mathematical_prerequisites: ['work-energy'],
    standards: ['NGSS.HS-PS3.B.1', 'NGSS.HS-PS3.B.2']
  },
  {
    id: 'momentum',
    name: 'Linear Momentum and Collisions',
    description: 'Momentum conservation in interactions and collisions',
    concepts: ['momentum-definition', 'impulse-momentum', 'conservation-momentum', 'elastic-collisions', 'inelastic-collisions', 'center-of-mass'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['newtons-laws', 'work-energy'],
    learning_outcomes: [
      'Define and calculate linear momentum',
      'Apply impulse-momentum theorem',
      'Analyze elastic and inelastic collisions',
      'Locate and track center of mass motion'
    ],
    experimental_components: ['collision apparatus', 'ballistic-pendulum', 'motion-sensors'],
    mathematical_prerequisites: ['vector-operations'],
    standards: ['NGSS.HS-PS2.A.3', 'NGSS.HS-PS2.A.4']
  },
  {
    id: 'rotation',
    name: 'Rotational Motion',
    description: 'Motion of objects rotating about a fixed axis',
    concepts: ['angular-quantities', 'rotational-kinematics', 'torque', 'rotational-inertia', 'rolling-motion', 'angular-momentum'],
    duration_hours: 20,
    difficulty_level: 'advanced',
    prerequisites: ['momentum', 'vectors'],
    learning_outcomes: [
      'Relate linear and angular quantities',
      'Apply rotational kinematics equations',
      'Calculate torque and rotational dynamics',
      'Analyze angular momentum conservation'
    ],
    experimental_components: ['rotational-inertia apparatus', 'gyroscope'],
    mathematical_prerequisites: ['trigonometry', 'integration'],
    standards: ['NGSS.HS-PS2.A.3', 'NGSS.HS-PS2.A.4']
  }
];

// ============================================
// SECTION 3: OSCILLATIONS AND WAVES
// ============================================

const section3: PhysicsSection = {
  id: 'oscillations-waves',
  name: 'Oscillations and Waves',
  description: 'Simple harmonic motion, wave properties, and wave phenomena',
  units: [],
  total_duration_hours: 60,
  sequence_order: 3
};

section3.units = [
  {
    id: 'shm',
    name: 'Simple Harmonic Motion',
    description: 'Periodic motion and its mathematical description',
    concepts: ['shm-characteristics', 'spring-mass-system', 'pendulum', 'energy-shm', 'damped-oscillations', 'driven-resonance'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['rotation', 'conservation-energy'],
    learning_outcomes: [
      'Describe characteristics of simple harmonic motion',
      'Analyze spring-mass and pendulum systems',
      'Apply energy conservation in SHM',
      'Understand resonance and damping phenomena'
    ],
    experimental_components: ['spring-mass system', 'pendulum lab', 'damping apparatus'],
    mathematical_prerequisites: ['trigonometry', 'differential-equations-intro'],
    standards: ['NGSS.HS-PS3.A.2', 'NGSS.HS-PS3.B.1']
  },
  {
    id: 'wave-properties',
    name: 'Wave Properties and Phenomena',
    description: 'Characteristics of mechanical and electromagnetic waves',
    concepts: ['wave-basics', 'transverse-longitudinal', 'wave-speed', 'superposition', 'standing-waves', 'doppler-effect'],
    duration_hours: 20,
    difficulty_level: 'intermediate',
    prerequisites: ['shm'],
    learning_outcomes: [
      'Classify waves by type and characteristics',
      'Calculate wave speed and frequency relationships',
      'Apply superposition and interference principles',
      'Explain Doppler effect and its applications'
    ],
    experimental_components: ['wave-tank', 'string-vibration', 'speaker-experiments'],
    mathematical_prerequisites: ['trigonometry', 'velocity-concepts'],
    standards: ['NGSS.HS-PS4.A.1', 'NGSS.HS-PS4.A.2']
  },
  {
    id: 'sound-waves',
    name: 'Sound Waves and Acoustics',
    description: 'Properties of sound waves and their perception',
    concepts: ['sound-properties', 'intensity-loudness', 'pitch-frequency', 'beats', 'standing-sound-waves', 'acoustics'],
    duration_hours: 15,
    difficulty_level: 'intermediate',
    prerequisites: ['wave-properties'],
    learning_outcomes: [
      'Describe sound as a mechanical wave',
      'Relate sound intensity to loudness perception',
      'Analyze beats and beat frequency',
      'Understand acoustic phenomena in enclosed spaces'
    ],
    experimental_components: ['tuning-fork experiments', 'resonance-tubes', 'oscilloscope'],
    mathematical_prerequisites: ['wave-properties'],
    standards: ['NGSS.HS-PS4.A.1', 'NGSS.HS-PS4.A.3']
  }
];

// ============================================
// SECTION 4: THERMODYNAMICS
// ============================================

const section4: PhysicsSection = {
  id: 'thermodynamics',
  name: 'Thermodynamics',
  description: 'Heat, temperature, and energy transfer in physical systems',
  units: [],
  total_duration_hours: 60,
  sequence_order: 4
};

section4.units = [
  {
    id: 'temperature-heat',
    name: 'Temperature and Heat',
    description: 'Thermal energy, temperature, and heat transfer mechanisms',
    concepts: ['temperature-scales', 'thermal-expansion', 'heat-capacity', 'latent-heat', 'conduction', 'convection', 'radiation'],
    duration_hours: 20,
    difficulty_level: 'beginner',
    prerequisites: [],
    learning_outcomes: [
      'Convert between temperature scales',
      'Explain thermal expansion in solids and liquids',
      'Calculate heat transfer in various processes',
      'Distinguish between conduction, convection, and radiation'
    ],
    experimental_components: ['thermal-expansion demo', 'calorimetry lab', 'insulation experiments'],
    mathematical_prerequisites: ['basic-arithmetic'],
    standards: ['NGSS.HS-PS3.A.2', 'NGSS.HS-PS3.B.1']
  },
  {
    id: 'kinetic-theory',
    name: 'Kinetic Theory of Gases',
    description: 'Molecular explanation of gas properties and behavior',
    concepts: ['gas-laws', 'kinetic-molecular-theory', 'ideal-gas-equation', 'internal-energy', 'molecular-speeds', 'real-gases'],
    duration_hours: 20,
    difficulty_level: 'intermediate',
    prerequisites: ['temperature-heat', 'shm'],
    learning_outcomes: [
      'State and apply the ideal gas law',
      'Explain gas properties using kinetic theory',
      'Relate molecular speeds to temperature',
      'Distinguish ideal and real gas behavior'
    ],
    experimental_components: ['gas-law apparatus', 'pressure-temperature demo'],
    mathematical_prerequisites: ['algebra', 'basic-statistics'],
    standards: ['NGSS.HS-PS3.A.2', 'NGSS.HS-PS3.A.3']
  },
  {
    id: 'thermodynamics-laws',
    name: 'Laws of Thermodynamics',
    description: 'Fundamental laws governing energy transformations',
    concepts: ['zeroth-law', 'first-law', 'second-law', 'entropy', 'heat-engines', 'refrigerators', 'carnot-cycle'],
    duration_hours: 20,
    difficulty_level: 'advanced',
    prerequisites: ['kinetic-theory', 'conservation-energy'],
    learning_outcomes: [
      'State and apply the laws of thermodynamics',
      'Calculate changes in internal energy and entropy',
      'Analyze heat engine efficiency',
      'Understand Carnot cycle and reversible processes'
    ],
    experimental_components: ['heat-engine models', 'entropy demonstrations'],
    mathematical_prerequisites: ['calculus-basics'],
    standards: ['NGSS.HS-PS3.B.1', 'NGSS.HS-PS3.B.2']
  }
];

// ============================================
// SECTION 5: ELECTROMAGNETISM
// ============================================

const section5: PhysicsSection = {
  id: 'electromagnetism',
  name: 'Electromagnetism',
  description: 'Electric and magnetic phenomena and their unified description',
  units: [],
  total_duration_hours: 100,
  sequence_order: 5
};

section5.units = [
  {
    id: 'electrostatics',
    name: 'Electrostatics and Electric Fields',
    description: 'Static electric charges and electric field properties',
    concepts: ['electric-charge', 'coulombs-law', 'electric-field', 'field-lines', 'conductors-insulators', 'electric-potential'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['newtons-laws', 'vectors'],
    learning_outcomes: [
      'Explain the nature of electric charge',
      'Apply Coulomb\'s law to calculate forces',
      'Describe and calculate electric fields',
      'Relate electric field to electric potential'
    ],
    experimental_components: ['electrostatics kits', 'field-mappers', 'capacitors'],
    mathematical_prerequisites: ['vector-inverse-square', 'integration'],
    standards: ['NGSS.HS-PS2.B.1', 'NGSS.HS-PS2.B.2']
  },
  {
    id: 'circuits',
    name: 'Electric Circuits',
    description: 'Current flow and circuit analysis',
    concepts: ['electric-current', 'ohms-law', 'series-circuits', 'parallel-circuits', 'kirchhoffs-laws', 'electrical-power'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['electrostatics'],
    learning_outcomes: [
      'Define and calculate electric current',
      'Apply Ohm\'s law and power formulas',
      'Analyze series and parallel circuits',
      'Use Kirchhoff\'s laws for complex circuits'
    ],
    experimental_components: ['circuit-breadboard', 'multimeters', 'oscilloscopes'],
    mathematical_prerequisites: ['algebra', 'systems-equations'],
    standards: ['NGSS.HS-PS2.B.3', 'NGSS.HS-PS2.B.4']
  },
  {
    id: 'magnetic-fields',
    name: 'Magnetic Fields and Forces',
    description: 'Magnetic field properties and interactions with moving charges',
    concepts: ['magnetic-fields', 'magnetic-force', 'charge-motion-fields', 'current-magnetic-field', 'electromagnetic-induction', 'faraday-law'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['circuits', 'vectors'],
    learning_outcomes: [
      'Describe magnetic field properties',
      'Calculate force on moving charges in magnetic fields',
      'Explain magnetic field from current-carrying wires',
      'Apply Faraday\'s law of electromagnetic induction'
    ],
    experimental_components: ['magnet-battery experiments', 'induction coils', 'galvanometers'],
    mathematical_prerequisites: ['right-hand-rule', 'integration'],
    standards: ['NGSS.HS-PS2.B.1', 'NGSS.HS-PS2.B.5']
  },
  {
    id: 'electromagnetic-waves',
    name: 'Electromagnetic Waves',
    description: 'Nature and properties of electromagnetic radiation',
    concepts: ['em-spectrum', 'em-wave-properties', 'light-speed', 'polarization', 'reflection-refraction', 'electromagnetic-generation'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['magnetic-fields', 'wave-properties'],
    learning_outcomes: [
      'Describe the electromagnetic spectrum',
      'Explain electromagnetic wave generation and propagation',
      'Analyze light behavior at boundaries',
      'Understand polarization and its applications'
    ],
    experimental_components: ['optics bench', 'polarizers', 'spectrum-analysis'],
    mathematical_prerequisites: ['trigonometry', 'wave-equations'],
    standards: ['NGSS.HS-PS4.A.1', 'NGSS.HS-PS4.A.3', 'NGSS.HS-PS4.B.1']
  }
];

// ============================================
// SECTION 6: OPTICS AND MODERN PHYSICS
// ============================================

const section6: PhysicsSection = {
  id: 'optics-modern',
  name: 'Optics and Modern Physics',
  description: 'Light behavior, quantum concepts, and atomic physics',
  units: [],
  total_duration_hours: 70,
  sequence_order: 6
};

section6.units = [
  {
    id: 'geometric-optics',
    name: 'Geometric Optics',
    description: 'Light propagation using ray approximation',
    concepts: ['ray-model', 'reflection-laws', 'refraction-snells-law', 'lenses', 'mirrors', 'optical-instruments', 'total-internal-reflection'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['electromagnetic-waves'],
    learning_outcomes: [
      'Apply the ray model of light',
      'Use laws of reflection and refraction',
      'Analyze image formation by lenses and mirrors',
      'Explain operation of optical instruments'
    ],
    experimental_components: ['optical bench', 'lens-mirror sets', 'telescopes'],
    mathematical_prerequisites: ['trigonometry', 'geometry'],
    standards: ['NGSS.HS-PS4.B.1', 'NGSS.HS-PS4.B.2']
  },
  {
    id: 'wave-optics',
    name: 'Wave Optics',
    description: 'Light behavior demonstrating wave characteristics',
    concepts: ['interference', 'diffraction', 'double-slit', 'diffraction-grating', 'thin-films', 'coherence'],
    duration_hours: 20,
    difficulty_level: 'advanced',
    prerequisites: ['geometric-optics', 'wave-properties'],
    learning_outcomes: [
      'Explain interference and diffraction phenomena',
      'Analyze double-slit and grating patterns',
      'Describe thin-film interference',
      'Understand conditions for coherent light'
    ],
    experimental_components: ['laser-interference', 'diffraction-slits', 'Michelson-interferometer'],
    mathematical_prerequisites: ['trigonometry', 'wave-equations'],
    standards: ['NGSS.HS-PS4.A.2', 'NGSS.HS-PS4.B.1']
  },
  {
    id: 'quantum-intro',
    name: 'Introduction to Quantum Physics',
    description: 'Quantum phenomena and their implications',
    concepts: ['photoelectric-effect', 'photons', 'wave-particle-duality', 'uncertainty-principle', 'atomic-spectra', 'quantum-states'],
    duration_hours: 25,
    difficulty_level: 'expert',
    prerequisites: ['wave-optics', 'electromagnetic-waves'],
    learning_outcomes: [
      'Explain the photoelectric effect',
      'Describe wave-particle duality',
      'Apply Heisenberg uncertainty principle',
      'Analyze atomic spectra using quantum concepts'
    ],
    experimental_components: ['photoelectric apparatus', 'spectrum-tubes'],
    mathematical_prerequisites: ['calculus', 'differential-equations'],
    standards: ['NGSS.HS-PS4.B.3', 'NGSS.HS-PS4.B.4']
  }
];

// ============================================
// COMPLETE SYLLABUS DEFINITION
// ============================================

export const physicsSyllabus: PhysicsSyllabus = {
  subject: 'physics',
  display_name: 'Physics',
  description: 'Comprehensive physics curriculum covering classical mechanics through quantum physics concepts',
  total_duration_hours: 465,
  sections: [section1, section2, section3, section4, section5, section6],
  applicable_standards: [
    'Next Generation Science Standards (NGSS)',
    'CBSE (India)',
    'ICSE (India)',
    'GCSE Physics',
    'AP Physics 1 & 2',
    'AP Physics C',
    'IB Physics'
  ],
  grade_levels: ['9', '10', '11', '12', 'Undergraduate']
};

// Export utility functions
export function getPhysicsUnitById(syllabus: PhysicsSyllabus, unitId: string): PhysicsUnit | undefined {
  for (const section of syllabus.sections) {
    const unit = section.units.find(u => u.id === unitId);
    if (unit) return unit;
  }
  return undefined;
}

export function getPhysicsPrerequisites(syllabus: PhysicsSyllabus, unitId: string): PhysicsUnit[] {
  const unit = getPhysicsUnitById(syllabus, unitId);
  if (!unit) return [];
  return unit.prerequisites
    .map(prereqId => getPhysicsUnitById(syllabus, prereqId))
    .filter((u): u is PhysicsUnit => u !== undefined);
}

export function generatePhysicsLearningPath(
  syllabus: PhysicsSyllabus,
  startUnitId: string,
  targetUnitId: string
): PhysicsUnit[] {
  const path: PhysicsUnit[] = [];
  const visited = new Set<string>();
  
  function addUnitAndPrerequisites(unitId: string) {
    if (visited.has(unitId)) return;
    
    const unit = getPhysicsUnitById(syllabus, unitId);
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

export function calculatePhysicsTotalDuration(syllabus: PhysicsSyllabus, unitIds: string[]): number {
  return unitIds.reduce((total, unitId) => {
    const unit = getPhysicsUnitById(syllabus, unitId);
    return total + (unit?.duration_hours || 0);
  }, 0);
}

export function getExperimentalComponents(syllabus: PhysicsSyllabus, unitId: string): string[] {
  const unit = getPhysicsUnitById(syllabus, unitId);
  return unit?.experimental_components || [];
}
