/**
 * Mathematics Syllabus - MathVerse Platform
 * 
 * This file defines the comprehensive curriculum structure for mathematics education,
 * covering topics from elementary arithmetic through advanced calculus and linear algebra.
 * 
 * Licensed under the Apache License, Version 2.0
 */

export interface SyllabusUnit {
  id: string;
  name: string;
  description: string;
  concepts: string[];
  duration_hours: number;
  difficulty_level: 'beginner' | 'elementary' | 'intermediate' | 'advanced' | 'expert';
  prerequisites: string[];
  learning_outcomes: string[];
  assessment_types: string[];
  standards: string[];
}

export interface SyllabusSection {
  id: string;
  name: string;
  description: string;
  units: SyllabusUnit[];
  total_duration_hours: number;
  sequence_order: number;
}

export interface MathSyllabus {
  subject: 'mathematics';
  display_name: 'Mathematics';
  description: 'Comprehensive mathematics curriculum from basic arithmetic through advanced calculus';
  total_duration_hours: number;
  sections: SyllabusSection[];
  applicable_standards: string[];
  grade_levels: string[];
}

// ============================================
// SECTION 1: FOUNDATIONAL MATHEMATICS
// ============================================

const section1: SyllabusSection = {
  id: 'foundational-math',
  name: 'Foundational Mathematics',
  description: 'Basic mathematical concepts including arithmetic, number systems, and fundamental operations',
  units: [],
  total_duration_hours: 120,
  sequence_order: 1
};

section1.units = [
  {
    id: 'whole-numbers',
    name: 'Whole Numbers and Operations',
    description: 'Understanding whole numbers, their properties, and basic arithmetic operations',
    concepts: ['counting', 'place-value', 'addition', 'subtraction', 'multiplication', 'division', 'order-of-operations'],
    duration_hours: 20,
    difficulty_level: 'beginner',
    prerequisites: [],
    learning_outcomes: [
      'Read and write whole numbers up to 1,000,000',
      'Perform addition, subtraction, multiplication, and division accurately',
      'Apply order of operations in complex expressions',
      'Estimate results using mental math strategies'
    ],
    assessment_types: ['quiz', 'worksheet', 'oral-assessment'],
    standards: ['CCSS.MATH.CONTENT.3.NBT.A.2', 'CCSS.MATH.CONTENT.4.NBT.B.4']
  },
  {
    id: 'fractions-decimals',
    name: 'Fractions and Decimals',
    description: 'Understanding fractional and decimal representations, operations, and conversions',
    concepts: ['fraction-basics', 'equivalent-fractions', 'comparing-fractions', 'decimal-operations', 'fraction-decimal-conversion', 'percentages'],
    duration_hours: 25,
    difficulty_level: 'elementary',
    prerequisites: ['whole-numbers'],
    learning_outcomes: [
      'Understand the concept of fractions as parts of a whole',
      'Find equivalent fractions and simplify fractions',
      'Compare and order fractions with different denominators',
      'Perform operations with decimals',
      'Convert between fractions, decimals, and percentages'
    ],
    assessment_types: ['quiz', 'practical-exercises', 'project'],
    standards: ['CCSS.MATH.CONTENT.4.NF.A.1', 'CCSS.MATH.CONTENT.5.NBT.B.7']
  },
  {
    id: 'integers-rational',
    name: 'Integers and Rational Numbers',
    description: 'Introduction to negative numbers and operations with rational numbers',
    concepts: ['integers', 'negative-numbers', 'absolute-value', 'integer-operations', 'rational-number-line'],
    duration_hours: 20,
    difficulty_level: 'elementary',
    prerequisites: ['fractions-decimals'],
    learning_outcomes: [
      'Understand the concept of negative numbers',
      'Perform addition, subtraction, multiplication, and division with integers',
      'Calculate absolute values',
      'Plot rational numbers on a number line'
    ],
    assessment_types: ['quiz', ' manipulatives', 'digital-tools'],
    standards: ['CCSS.MATH.CONTENT.6.NS.C.5', 'CCSS.MATH.CONTENT.7.NS.A.1']
  },
  {
    id: 'basic-geometry',
    name: 'Basic Geometry and Measurement',
    description: 'Fundamental geometric concepts including shapes, angles, and measurements',
    concepts: ['lines-rays-segments', 'angles', 'polygons', 'circles', 'perimeter', 'area', 'volume', 'unit-conversion'],
    duration_hours: 30,
    difficulty_level: 'elementary',
    prerequisites: ['whole-numbers', 'fractions-decimals'],
    learning_outcomes: [
      'Identify and classify geometric shapes',
      'Measure and classify angles',
      'Calculate perimeter, area, and volume of common shapes',
      'Convert between different units of measurement'
    ],
    assessment_types: ['hands-on-activities', 'construction-projects', 'quiz'],
    standards: ['CCSS.MATH.CONTENT.4.MD.A.3', 'CCSS.MATH.CONTENT.7.G.B.4']
  },
  {
    id: 'data-statistics',
    name: 'Data Analysis and Statistics',
    description: 'Collecting, organizing, and interpreting data using statistical methods',
    concepts: ['data-collection', 'bar-graphs', 'line-graphs', 'mean-median-mode', 'probability-basics', 'data-interpretation'],
    duration_hours: 25,
    difficulty_level: 'beginner',
    prerequisites: ['whole-numbers'],
    learning_outcomes: [
      'Collect and organize data systematically',
      'Create and interpret various types of graphs',
      'Calculate and interpret measures of central tendency',
      'Understand basic probability concepts'
    ],
    assessment_types: ['data-projects', 'presentations', 'quiz'],
    standards: ['CCSS.MATH.CONTENT.6.SP.A.1', 'CCSS.MATH.CONTENT.7.SP.A.1']
  }
];

// ============================================
// SECTION 2: ALGEBRA FUNDAMENTALS
// ============================================

const section2: SyllabusSection = {
  id: 'algebra-fundamentals',
  name: 'Algebra Fundamentals',
  description: 'Introduction to algebraic thinking, expressions, equations, and functions',
  units: [],
  total_duration_hours: 150,
  sequence_order: 2
};

section2.units = [
  {
    id: 'algebraic-expressions',
    name: 'Algebraic Expressions',
    description: 'Writing, simplifying, and evaluating algebraic expressions',
    concepts: ['variables-exponents', 'terms-coefficients', 'like-terms', 'simplifying-expressions', 'evaluating-expressions', 'pattern-recognition'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['integers-rational', 'basic-geometry'],
    learning_outcomes: [
      'Understand the meaning of variables and exponents',
      'Identify terms and coefficients in expressions',
      'Combine like terms to simplify expressions',
      'Evaluate expressions for given variable values'
    ],
    assessment_types: ['quiz', 'expression-building-activities', 'digital-tools'],
    standards: ['CCSS.MATH.CONTENT.6.EE.A.2', 'CCSS.MATH.CONTENT.7.EE.A.1']
  },
  {
    id: 'linear-equations',
    name: 'Linear Equations',
    description: 'Solving one-variable and two-variable linear equations',
    concepts: ['one-step-equations', 'two-step-equations', 'multi-step-equations', 'literal-equations', 'linear-equations-two-variables', 'slope-intercept-form'],
    duration_hours: 35,
    difficulty_level: 'intermediate',
    prerequisites: ['algebraic-expressions'],
    learning_outcomes: [
      'Solve one-step and multi-step linear equations',
      'Rearrange formulas to solve for specific variables',
      'Graph linear equations in two variables',
      'Write equations from word problems'
    ],
    assessment_types: ['problem-sets', 'real-world-applications', 'quiz'],
    standards: ['CCSS.MATH.CONTENT.8.EE.C.7', 'CCSS.MATH.CONTENT.A.REI.B.3']
  },
  {
    id: 'inequalities',
    name: 'Linear Inequalities',
    description: 'Solving and graphing linear inequalities and systems of inequalities',
    concepts: ['inequality-properties', 'solving-inequalities', 'compound-inequalities', 'graphing-inequalities', 'systems-inequalities'],
    duration_hours: 20,
    difficulty_level: 'intermediate',
    prerequisites: ['linear-equations'],
    learning_outcomes: [
      'Apply inequality properties for solving',
      'Solve and graph single and compound inequalities',
      'Represent solutions on number lines',
      'Solve systems of linear inequalities graphically'
    ],
    assessment_types: ['quiz', 'graphing-activities', 'problem-sets'],
    standards: ['CCSS.MATH.CONTENT.A.REI.D.12']
  },
  {
    id: 'linear-functions',
    name: 'Linear Functions',
    description: 'Understanding linear relationships as functions and their applications',
    concepts: ['functions-relations', 'linear-functions', 'slope', 'rate-of-change', 'direct-variation', 'function-notation'],
    duration_hours: 30,
    difficulty_level: 'intermediate',
    prerequisites: ['linear-equations', 'data-statistics'],
    learning_outcomes: [
      'Distinguish between relations and functions',
      'Identify linear functions from equations and graphs',
      'Calculate and interpret slope and rate of change',
      'Use function notation correctly'
    ],
    assessment_types: ['quiz', 'real-world-modeling', 'function-activities'],
    standards: ['CCSS.MATH.CONTENT.8.F.A.3', 'CCSS.MATH.CONTENT.8.F.B.4']
  },
  {
    id: 'systems-equations',
    name: 'Systems of Linear Equations',
    description: 'Solving and analyzing systems of two linear equations',
    concepts: ['systems-introduction', 'substitution-method', 'elimination-method', 'graphing-method', 'applications-systems', 'special-systems'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['linear-equations', 'linear-functions'],
    learning_outcomes: [
      'Solve systems using substitution, elimination, and graphing',
      'Analyze special cases (parallel, coincident lines)',
      'Model real-world situations with systems of equations',
      'Determine the best method for different problem types'
    ],
    assessment_types: ['problem-sets', 'modeling-projects', 'quiz'],
    standards: ['CCSS.MATH.CONTENT.A.REI.C.5', 'CCSS.MATH.CONTENT.A.REI.D.11']
  },
  {
    id: 'quadratic-equations',
    name: 'Quadratic Equations',
    description: 'Solving quadratic equations using multiple methods',
    concepts: ['quadratic-form', 'factoring-quadratics', 'completing-square', 'quadratic-formula', 'discriminant', 'quadratic-graphs', 'applications-quadratics'],
    duration_hours: 15,
    difficulty_level: 'advanced',
    prerequisites: ['linear-equations', 'polynomials'],
    learning_outcomes: [
      'Identify quadratic equations in standard form',
      'Solve quadratics by factoring and using the quadratic formula',
      'Complete the square for solving and vertex form',
      'Analyze quadratic graphs and their features'
    ],
    assessment_types: ['quiz', 'multiple-methods-practice', 'real-world-problems'],
    standards: ['CCSS.MATH.CONTENT.A.REI.B.4']
  }
];

// ============================================
// SECTION 3: GEOMETRY AND TRIGONOMETRY
// ============================================

const section3: SyllabusSection = {
  id: 'geometry-trigonometry',
  name: 'Geometry and Trigonometry',
  description: '平面几何、立体几何和三角学的系统学习',
  units: [],
  total_duration_hours: 140,
  sequence_order: 3
};

section3.units = [
  {
    id: 'euclidean-geometry',
    name: 'Euclidean Geometry Fundamentals',
    description: '点、线、角、多边形的性质和关系',
    concepts: ['点与线', '角的分类与测量', '平行线与垂线', '三角形性质', '多边形分类', '全等与相似'],
    duration_hours: 35,
    difficulty_level: 'intermediate',
    prerequisites: ['basic-geometry'],
    learning_outcomes: [
      '掌握点和线的基本概念',
      '理解并应用角的性质',
      '证明和应用平行线的性质',
      '分类和证明三角形的全等与相似'
    ],
    assessment_types: ['证明题', '作图题', '实际应用'],
    standards: ['CCSS.MATH.CONTENT.4.G.A.1', 'CCSS.MATH.CONTENT.8.G.A.5']
  },
  {
    id: 'geometric-proofs',
    name: 'Geometric Proofs',
    description: 'Developing logical reasoning through geometric proof writing',
    concepts: ['direct-proof', 'indirect-proof', 'proof-structure', 'angle-proofs', 'triangle-proofs', 'parallelogram-proofs'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['euclidean-geometry'],
    learning_outcomes: [
      'Understand the structure of geometric proofs',
      'Write direct and indirect proofs',
      'Prove angle relationships and triangle properties',
      'Construct parallelogram proofs'
    ],
    assessment_types: ['proof-writing', 'logic-exercises', 'quiz'],
    standards: ['CCSS.MATH.CONTENT.G.CO.C.9']
  },
  {
    id: 'coordinate-geometry',
    name: 'Coordinate Geometry',
    description: 'Using the coordinate plane to analyze geometric figures',
    concepts: ['coordinate-plane', 'distance-formula', 'midpoint-formula', 'slope-review', 'geometric-shapes-coordinates', 'transformations'],
    duration_hours: 20,
    difficulty_level: 'intermediate',
    prerequisites: ['linear-functions', 'euclidean-geometry'],
    learning_outcomes: [
      'Plot points and interpret coordinate geometry',
      'Calculate distances and midpoints',
      'Find equations of lines through geometric figures',
      'Apply transformations on the coordinate plane'
    ],
    assessment_types: ['coordinate-activities', 'problem-sets', 'quiz'],
    standards: ['CCSS.MATH.CONTENT.8.G.A.3', 'CCSS.MATH.CONTENT.G.GPE.B.4']
  },
  {
    id: 'area-volume',
    name: 'Area, Surface Area, and Volume',
    description: 'Calculating measurements of two and three-dimensional figures',
    concepts: ['area-formulas', 'surface-area-formulas', 'volume-formulas', 'composite-figures', 'unit-conversion-3d'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['basic-geometry', 'algebraic-expressions'],
    learning_outcomes: [
      'Derive and apply area formulas for all polygons',
      'Calculate surface area of prisms, cylinders, cones, and spheres',
      'Find volumes of 3D shapes',
      'Solve composite figure problems'
    ],
    assessment_types: ['formulas-quiz', 'practical-measurements', 'problem-sets'],
    standards: ['CCSS.MATH.CONTENT.6.G.A.1', 'CCSS.MATH.CONTENT.8.G.C.9']
  },
  {
    id: 'circle-geometry',
    name: 'Circle Geometry',
    description: 'Properties of circles, arcs, and sectors',
    concepts: ['circle-basics', 'arcs-chords', 'inscribed-angles', 'central-angles', 'tangent-properties', 'circle-equations'],
    duration_hours: 20,
    difficulty_level: 'advanced',
    prerequisites: ['euclidean-geometry', 'coordinate-geometry'],
    learning_outcomes: [
      'Identify circle properties and terminology',
      'Calculate arc measures and chord lengths',
      'Prove inscribed angle theorems',
      'Write equations of circles'
    ],
    assessment_types: ['quiz', 'construction-activities', 'proof-exercises'],
    standards: ['CCSS.MATH.CONTENT.G.C.A.1', 'CCSS.MATH.CONTENT.G.C.A.2']
  },
  {
    id: 'right-triangle-trig',
    name: 'Right Triangle Trigonometry',
    description: 'Trigonometric ratios and their applications',
    concepts: ['similar-right-triangles', 'sine-cosine-tangent', 'inverse-trig', 'solving-right-triangles', 'applications-trig', 'angles-elevation-depression'],
    duration_hours: 15,
    difficulty_level: 'advanced',
    prerequisites: ['euclidean-geometry', 'ratio-proportion'],
    learning_outcomes: [
      'Define sine, cosine, and tangent using similar triangles',
      'Use inverse trig functions to find angle measures',
      'Solve right triangles using trig ratios',
      'Apply trig to real-world measurement problems'
    ],
    assessment_types: ['ratio-practice', 'measurement-problems', 'quiz'],
    standards: ['CCSS.MATH.CONTENT.G.SRT.C.6', 'CCSS.MATH.CONTENT.G.SRT.C.8']
  }
];

// ============================================
// SECTION 4: ADVANCED ALGEBRA
// ============================================

const section4: SyllabusSection = {
  id: 'advanced-algebra',
  name: 'Advanced Algebra',
  description: 'Higher-level algebraic concepts including polynomials, radicals, and rational expressions',
  units: [],
  total_duration_hours: 130,
  sequence_order: 4
};

section4.units = [
  {
    id: 'polynomials',
    name: 'Polynomials and Polynomial Functions',
    description: 'Operations and applications of polynomial expressions and functions',
    concepts: ['polynomial-basics', 'polynomial-operations', 'factoring-polynomials', 'polynomial-functions', 'division-algorithm', 'remainder-theorem'],
    duration_hours: 30,
    difficulty_level: 'intermediate',
    prerequisites: ['quadratic-equations'],
    learning_outcomes: [
      'Classify and perform operations on polynomials',
      'Factor polynomials including special forms',
      'Evaluate polynomial functions',
      'Apply the Remainder Theorem'
    ],
    assessment_types: ['operations-quiz', 'factoring-exercises', 'function-analysis'],
    standards: ['CCSS.MATH.CONTENT.APR.A.1', 'CCSS.MATH.CONTENT.APR.B.2']
  },
  {
    id: 'radicals',
    name: 'Radicals and Rational Exponents',
    description: 'Simplifying and operating with radical expressions',
    concepts: ['radical-basics', 'simplifying-radicals', 'radical-operations', 'rational-exponents', 'radical-equations', 'complex-numbers-intro'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['quadratic-equations', 'integer-operations'],
    learning_outcomes: [
      'Simplify radical expressions',
      'Perform operations with radicals',
      'Convert between radical and exponential forms',
      'Solve radical equations'
    ],
    assessment_types: ['simplification-practice', 'operations-quiz', 'equation-solving'],
    standards: ['CCSS.MATH.CONTENT.N.RN.A.1', 'CCSS.MATH.CONTENT.N.RN.A.2']
  },
  {
    id: 'rational-expressions',
    name: 'Rational Expressions and Equations',
    description: 'Simplifying and solving rational expressions and equations',
    concepts: ['rational-basics', 'simplifying-rationals', 'rational-operations', 'rational-equations', 'rational-functions', 'discontinuities'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['polynomials', 'radicals'],
    learning_outcomes: [
      'Simplify complex rational expressions',
      'Perform operations with rational expressions',
      'Solve rational equations',
      'Analyze rational functions and asymptotes'
    ],
    assessment_types: ['simplification-quiz', 'equation-solving', 'function-analysis'],
    standards: ['CCSS.MATH.CONTENT.APR.A.1', 'CCSS.MATH.CONTENT.CED.A.1']
  },
  {
    id: 'exponential-logarithmic',
    name: 'Exponential and Logarithmic Functions',
    description: 'Growth and decay models using exponential and logarithmic functions',
    concepts: ['exponential-functions', 'exponential-growth-decay', 'logarithmic-basics', 'logarithmic-functions', 'log-properties', 'solving-exponential-equations'],
    duration_hours: 30,
    difficulty_level: 'advanced',
    prerequisites: ['linear-functions', 'inverse-functions'],
    learning_outcomes: [
      'Identify and graph exponential functions',
      'Model real-world growth and decay',
      'Understand logarithms as inverses of exponentials',
      'Apply log properties to solve equations'
    ],
    assessment_types: ['modeling-problems', 'graphing-activities', 'quiz'],
    standards: ['CCSS.MATH.CONTENT.F.LE.A.4', 'CCSS.MATH.CONTENT.F.LE.B.5']
  },
  {
    id: 'conic-sections',
    name: 'Conic Sections',
    description: 'Properties and equations of circles, ellipses, parabolas, and hyperbolas',
    concepts: ['circle-review', 'ellipses', 'parabolas', 'hyperbolas', 'identifying-conics', 'applications-conics'],
    duration_hours: 20,
    difficulty_level: 'expert',
    prerequisites: ['coordinate-geometry', 'quadratic-equations'],
    learning_outcomes: [
      'Derive and graph equations of all conic sections',
      'Identify conic sections from equations',
      'Analyze properties of each conic type',
      'Apply conic sections to real-world situations'
    ],
    assessment_types: ['derivation-exercises', 'graphing-quiz', 'applications'],
    standards: ['CCSS.MATH.CONTENT.G.GPE.A.1', 'CCSS.MATH.CONTENT.G.GPE.A.3']
  }
];

// ============================================
// SECTION 5: PRE-CALCULUS
// ============================================

const section5: SyllabusSection = {
  id: 'precalculus',
  name: 'Pre-Calculus',
  description: 'Advanced mathematical preparation for calculus including sequences, series, and limits',
  units: [],
  total_duration_hours: 100,
  sequence_order: 5
};

section5.units = [
  {
    id: 'sequences-series',
    name: 'Sequences and Series',
    description: 'Arithmetic and geometric sequences and their applications',
    concepts: ['sequences-basics', 'arithmetic-sequences', 'geometric-sequences', 'series-sums', 'sigma-notation', 'infinite-series'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['exponential-logarithmic'],
    learning_outcomes: [
      'Identify and generate arithmetic and geometric sequences',
      'Find sums of finite series',
      'Use sigma notation for series',
      'Determine convergence of infinite series'
    ],
    assessment_types: ['sequence-practice', 'sum-calculation', 'convergence-analysis'],
    standards: ['CCSS.MATH.CONTENT.F.IF.A.3', 'CCSS.MATH.CONTENT.F.BF.A.2']
  },
  {
    id: 'probability-combinatorics',
    name: 'Probability and Combinatorics',
    description: 'Counting techniques and probability theory',
    concepts: ['counting-principle', 'permutations', 'combinations', 'probability-rules', 'conditional-probability', 'binomial-distribution'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['data-statistics'],
    learning_outcomes: [
      'Apply fundamental counting principle',
      'Calculate permutations and combinations',
      'Use probability rules for independent and dependent events',
      'Apply binomial probability'
    ],
    assessment_types: ['counting-exercises', 'probability-problems', 'simulations'],
    standards: ['CCSS.MATH.CONTENT.S.CP.A.1', 'CCSS.MATH.CONTENT.S.MD.A.1']
  },
  {
    id: 'functions-advanced',
    name: 'Advanced Function Analysis',
    description: 'In-depth study of function transformations and compositions',
    concepts: ['function-transformations', 'inverse-functions', 'parent-functions', 'function-composition', 'domain-range-advanced', 'function-analysis'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['linear-functions', 'exponential-logarithmic'],
    learning_outcomes: [
      'Apply all transformations to function families',
      'Find and verify inverse functions',
      'Compose functions and decompose complex functions',
      'Analyze functions for domain, range, and features'
    ],
    assessment_types: ['transformation-quiz', 'inverse-finding', 'composition-exercises'],
    standards: ['CCSS.MATH.CONTENT.F.BF.B.3', 'CCSS.MATH.CONTENT.F.BF.B.4']
  },
  {
    id: 'trigonometry-advanced',
    name: 'Advanced Trigonometry',
    description: 'Extended trigonometric concepts including identities and equations',
    concepts: ['trig-radians', 'unit-circle', 'trig-identities', 'trig-equations', 'law-sines-cosines', 'trig-graphs-advanced'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['right-triangle-trig', 'functions-advanced'],
    learning_outcomes: [
      'Work with angles in radians and degrees',
      'Use the unit circle for trig values',
      'Prove and apply trigonometric identities',
      'Solve trigonometric equations'
    ],
    assessment_types: ['identity-proofs', 'equation-solving', 'graph-analysis'],
    standards: ['CCSS.MATH.CONTENT.F.TF.A.1', 'CCSS.MATH.CONTENT.F.TF.B.7']
  }
];

// ============================================
// SECTION 6: CALCULUS INTRODUCTION
// ============================================

const section6: SyllabusSection = {
  id: 'calculus-intro',
  name: 'Introduction to Calculus',
  description: 'Foundational calculus concepts including limits, derivatives, and integrals',
  units: [],
  total_duration_hours: 80,
  sequence_order: 6
};

section6.units = [
  {
    id: 'limits-continuity',
    name: 'Limits and Continuity',
    description: 'Understanding limits as foundations for calculus',
    concepts: ['limit-basics', 'limit-laws', 'evaluating-limits', 'infinite-limits', 'continuity', 'limits-at-infinity'],
    duration_hours: 20,
    difficulty_level: 'expert',
    prerequisites: ['functions-advanced'],
    learning_outcomes: [
      'Understand limits conceptually and graphically',
      'Apply limit laws to evaluate limits',
      'Identify types of discontinuities',
      'Evaluate limits at infinity'
    ],
    assessment_types: ['limit-calculation', 'graphical-analysis', 'continuity-proofs'],
    standards: ['CCSS.MATH.CONTENT.LIM.1', 'LIM.2']
  },
  {
    id: 'derivatives',
    name: 'Introduction to Derivatives',
    description: 'The derivative as rate of change and slope of tangent lines',
    concepts: ['derivative-definition', 'derivative-rules', 'product-quotient-chain', 'implicit-differentiation', 'derivatives-trig', 'higher-order-derivatives'],
    duration_hours: 35,
    difficulty_level: 'expert',
    prerequisites: ['limits-continuity', 'trigonometry-advanced'],
    learning_outcomes: [
      'Apply the definition of derivative',
      'Differentiate using all rules',
      'Use implicit differentiation',
      'Find higher-order derivatives'
    ],
    assessment_types: ['differentiation-quiz', 'application-problems', 'implicit-differentiation'],
    standards: ['CCSS.MATH.CONTENT.DER.1', 'DER.2', 'DER.3']
  },
  {
    id: 'applications-derivatives',
    name: 'Applications of Derivatives',
    description: 'Using derivatives to analyze functions and solve real-world problems',
    concepts: ['related-rates', 'optimization', 'mean-value-theorem', 'curve-sketching', 'linear-approximation', 'lhopitals-rule'],
    duration_hours: 25,
    difficulty_level: 'expert',
    prerequisites: ['derivatives'],
    learning_outcomes: [
      'Solve related rates problems',
      'Apply optimization techniques',
      'Use derivatives for curve sketching',
      'Apply L\'Hospital\'s Rule for limits'
    ],
    assessment_types: ['related-rates-exercises', 'optimization-problems', 'curve-sketching'],
    standards: ['CCSS.MATH.CONTENT.DER.4', 'DER.5']
  }
];

// ============================================
// COMPLETE SYLLABUS DEFINITION
// ============================================

export const mathSyllabus: MathSyllabus = {
  subject: 'mathematics',
  display_name: 'Mathematics',
  description: 'Comprehensive mathematics curriculum from basic arithmetic through advanced calculus, designed for school through undergraduate levels',
  total_duration_hours: 720,
  sections: [section1, section2, section3, section4, section5, section6],
  applicable_standards: [
    'Common Core State Standards (CCSS)',
    'CBSE (India)',
    'ICSE (India)',
    'GCSE (UK)',
    'AP Mathematics',
    'IB Mathematics'
  ],
  grade_levels: ['5', '6', '7', '8', '9', '10', '11', '12', 'Undergraduate']
};

// Export utility functions
export function getUnitById(syllabus: MathSyllabus, unitId: string): SyllabusUnit | undefined {
  for (const section of syllabus.sections) {
    const unit = section.units.find(u => u.id === unitId);
    if (unit) return unit;
  }
  return undefined;
}

export function getPrerequisites(syllabus: MathSyllabus, unitId: string): SyllabusUnit[] {
  const unit = getUnitById(syllabus, unitId);
  if (!unit) return [];
  return unit.prerequisites
    .map(prereqId => getUnitById(syllabus, prereqId))
    .filter((u): u is SyllabusUnit => u !== undefined);
}

export function generateLearningPath(
  syllabus: MathSyllabus,
  startUnitId: string,
  targetUnitId: string
): SyllabusUnit[] {
  const path: SyllabusUnit[] = [];
  const visited = new Set<string>();
  
  function addUnitAndPrerequisites(unitId: string) {
    if (visited.has(unitId)) return;
    
    const unit = getUnitById(syllabus, unitId);
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

export function calculateTotalDuration(syllabus: MathSyllabus, unitIds: string[]): number {
  return unitIds.reduce((total, unitId) => {
    const unit = getUnitById(syllabus, unitId);
    return total + (unit?.duration_hours || 0);
  }, 0);
}
