/**
 * Finance Syllabus - FinVerse Platform
 * 
 * This file defines the comprehensive curriculum structure for finance education,
 * covering financial fundamentals, investment analysis, and risk management.
 * 
 * Licensed under the Apache License, Version 2.0
 */

export interface FinanceUnit {
  id: string;
  name: string;
  description: string;
  concepts: string[];
  duration_hours: number;
  difficulty_level: 'beginner' | 'elementary' | 'intermediate' | 'advanced' | 'expert';
  prerequisites: string[];
  learning_outcomes: string[];
  case_studies: string[];
  calculation_practices: string[];
  standards: string[];
}

export interface FinanceSection {
  id: string;
  name: string;
  description: string;
  units: FinanceUnit[];
  total_duration_hours: number;
  sequence_order: number;
}

export interface FinanceSyllabus {
  subject: 'finance';
  display_name: 'Finance & Investment';
  description: 'Comprehensive finance curriculum from basic concepts through advanced financial analysis';
  total_duration_hours: number;
  sections: FinanceSection[];
  applicable_standards: string[];
  target_audience: string[];
}

// ============================================
// SECTION 1: FINANCIAL FUNDAMENTALS
// ============================================

const section1: FinanceSection = {
  id: 'financial-fundamentals',
  name: 'Financial Fundamentals',
  description: 'Core concepts of finance, time value of money, and financial statements',
  units: [],
  total_duration_hours: 80,
  sequence_order: 1
};

section1.units = [
  {
    id: 'time-value-money',
    name: 'Time Value of Money',
    description: 'Understanding present and future value concepts',
    concepts: ['present-value', 'future-value', 'compounding-frequency', 'annuity-calculations', 'perpetuity', 'effective-annual-rate'],
    duration_hours: 25,
    difficulty_level: 'beginner',
    prerequisites: [],
    learning_outcomes: [
      'Explain the concept of time value of money',
      'Calculate present and future values',
      'Apply annuity and perpetuity formulas',
      'Compare different compounding frequencies'
    ],
    case_studies: ['retirement-planning', 'lump-sum-vs-payments'],
    calculation_practices: ['pv-calculation', 'fv-calculation', 'annuity-valuation', 'effective-rate'],
    standards: ['CFA-Level1', 'CFA-Level2']
  },
  {
    id: 'financial-statements',
    name: 'Financial Statements Analysis',
    description: 'Understanding and analyzing corporate financial statements',
    concepts: ['income-statement', 'balance-sheet', 'cash-flow-statement', 'ratio-analysis', 'horizontal-vertical-analysis', 'working-capital'],
    duration_hours: 30,
    difficulty_level: 'beginner',
    prerequisites: ['time-value-money'],
    learning_outcomes: [
      'Interpret the three main financial statements',
      'Calculate and analyze financial ratios',
      'Perform horizontal and vertical analysis',
      'Assess working capital management'
    ],
    case_studies: ['apple-financial-analysis', 'startup-financials'],
    calculation_practices: ['ratio-calculation', 'common-size-statements', 'cash-flow-analysis'],
    standards: ['CFA-Level1', 'ACCA-F3']
  },
  {
    id: 'valuation-basics',
    name: 'Valuation Fundamentals',
    description: 'Methods for valuing assets and companies',
    concepts: ['dcf-introduction', 'comparable-company-analysis', 'precedent-transactions', 'asset-valuation', 'enterprise-value', 'equity-value'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['financial-statements'],
    learning_outcomes: [
      'Apply discounted cash flow methodology',
      'Use comparables for relative valuation',
      'Calculate enterprise and equity value',
      'Understand limitations of each method'
    ],
    case_studies: ['dcf-valuation-apple', 'comparable-tech-sector'],
    calculation_practices: ['dcf-model-basic', 'multiples-calculation', 'ev-calculations'],
    standards: ['CFA-Level1', 'CFA-Level2', 'CFA-Level3']
  }
];

// ============================================
// SECTION 2: CORPORATE FINANCE
// ============================================

const section2: FinanceSection = {
  id: 'corporate-finance',
  name: 'Corporate Finance',
  description: 'Capital structure, cost of capital, and financial decision making',
  units: [],
  total_duration_hours: 90,
  sequence_order: 2
};

section2.units = [
  {
    id: 'capital-budgeting',
    name: 'Capital Budgeting',
    description: 'Evaluating and selecting investment projects',
    concepts: ['npv-method', 'irr-method', 'payback-period', 'profitability-index', 'incremental-cash-flows', 'capital-rationing'],
    duration_hours: 30,
    difficulty_level: 'intermediate',
    prerequisites: ['valuation-basics'],
    learning_outcomes: [
      'Apply NPV and IRR for project evaluation',
      'Calculate and interpret payback period',
      'Analyze incremental cash flows for projects',
      'Handle capital rationing decisions'
    ],
    case_studies: ['factory-expansion-decision', 'new-product-line-analysis'],
    calculation_practices: ['npv-calculation', 'irr-calculation', 'incremental-cashflow'],
    standards: ['CFA-Level1', 'CFA-Level2', 'FM-Curriculum']
  },
  {
    id: 'cost-capital',
    name: 'Cost of Capital',
    description: 'Calculating weighted average cost of capital',
    concepts: ['cost-of-equity', 'cost-of-debt', 'wacc-calculation', 'capital-structure', 'beta-estimation', 'target-capital-structure'],
    duration_hours: 30,
    difficulty_level: 'advanced',
    prerequisites: ['capital-budgeting'],
    learning_outcomes: [
      'Calculate cost of equity using CAPM and dividend discount',
      'Determine cost of debt and preferred stock',
      'Compute weighted average cost of capital',
      'Analyze optimal capital structure'
    ],
    case_studies: ['wacc-calculation-disney', 'capital-structure-decision'],
    calculation_practices: ['wacc-calculation', 'cost-of-equity', 'beta-calculation'],
    standards: ['CFA-Level1', 'CFA-Level2', 'FM-Curriculum']
  },
  {
    id: 'working-capital',
    name: 'Working Capital Management',
    description: 'Managing short-term assets and liabilities',
    concepts: ['operating-cycle', 'cash-conversion-cycle', 'inventory-management', 'receivables-management', 'payables-management', 'cash-budget'],
    duration_hours: 30,
    difficulty_level: 'intermediate',
    prerequisites: ['financial-statements'],
    learning_outcomes: [
      'Calculate and interpret operating and cash cycles',
      'Apply inventory management techniques',
      'Analyze accounts receivable policies',
      'Create and manage cash budgets'
    ],
    case_studies: ['working-capital-optimization', 'cash-management-amazon'],
    calculation_practices: ['cycle-calculations', 'eoq-calculation', 'cash-budget'],
    standards: ['CFA-Level1', 'ACCA-F9', 'FM-Curriculum']
  }
];

// ============================================
// SECTION 3: INVESTMENT ANALYSIS
// ============================================

const section3: FinanceSection = {
  id: 'investment-analysis',
  name: 'Investment Analysis and Portfolio Management',
  description: 'Security analysis, portfolio theory, and asset allocation',
  units: [],
  total_duration_hours: 110,
  sequence_order: 3
};

section3.units = [
  {
    id: 'equity-analysis',
    name: 'Equity Analysis and Valuation',
    description: 'Analyzing and valuing equity securities',
    concepts: ['fundamental-analysis', 'dividend-discount-model', 'relative-valuation-equity', 'earnings-analysis', 'growth-stocks', 'value-stocks'],
    duration_hours: 35,
    difficulty_level: 'advanced',
    prerequisites: ['valuation-basics'],
    learning_outcomes: [
      'Apply fundamental analysis framework',
      'Use dividend discount and residual income models',
      'Calculate intrinsic value using multiples',
      'Differentiate between growth and value investing'
    ],
    case_studies: ['stock-picking-exercise', 'dcf-apple-vs-google'],
    calculation_practices: ['intrinsic-value', 'dividend-models', 'earnings-forecasting'],
    standards: ['CFA-Level1', 'CFA-Level2', 'CFA-Level3']
  },
  {
    id: 'fixed-income',
    name: 'Fixed Income Analysis',
    description: 'Bond valuation, yield analysis, and interest rate risk',
    concepts: ['bond-pricing', 'yield-to-maturity', 'duration', 'convexity', 'credit-analysis', 'bond-portfolio'],
    duration_hours: 35,
    difficulty_level: 'advanced',
    prerequisites: ['time-value-money'],
    learning_outcomes: [
      'Calculate bond prices and yields',
      'Apply duration and convexity measures',
      'Analyze credit risk in fixed income',
      'Construct and manage bond portfolios'
    ],
    case_studies: ['bond-portfolio-case', 'yield-curve-analysis'],
    calculation_practices: ['bond-pricing', 'ytm-calculation', 'duration-convexity'],
    standards: ['CFA-Level1', 'CFA-Level2', 'CFA-Level3']
  },
  {
    id: 'portfolio-theory',
    name: 'Modern Portfolio Theory',
    description: 'Portfolio construction and optimization',
    concepts: ['efficient-frontier', 'capm', 'beta-risk', 'sharpe-ratio', 'portfolio-optimization', 'asset-allocation'],
    duration_hours: 40,
    difficulty_level: 'expert',
    prerequisites: ['equity-analysis', 'fixed-income'],
    learning_outcomes: [
      'Construct efficient portfolios',
      'Apply CAPM for expected returns',
      'Calculate and interpret risk-return metrics',
      'Develop strategic asset allocation'
    ],
    case_studies: ['portfolio-optimization-case', 'asset-allocation-retirement'],
    calculation_practices: ['portfolio-return', 'portfolio-risk', 'sharpe-ratio', 'capm-expected-return'],
    standards: ['CFA-Level1', 'CFA-Level2', 'CFA-Level3']
  }
];

// ============================================
// SECTION 4: DERIVATIVES AND RISK MANAGEMENT
// ============================================

const section4: FinanceSection = {
  id: 'derivatives-risk',
  name: 'Derivatives and Risk Management',
  description: 'Options, futures, hedging strategies, and risk management',
  units: [],
  total_duration_hours: 90,
  sequence_order: 4
};

section4.units = [
  {
    id: 'options-futures',
    name: 'Options and Futures Markets',
    description: 'Understanding derivative instruments and markets',
    concepts: ['forward-contracts', 'futures-basics', 'call-options', 'put-options', 'put-call-parity', 'option-payoffs', 'margin-requirements'],
    duration_hours: 30,
    difficulty_level: 'advanced',
    prerequisites: ['time-value-money'],
    learning_outcomes: [
      'Differentiate between forwards, futures, and options',
      'Calculate payoffs for option strategies',
      'Apply put-call parity relationships',
      'Understand margin and settlement mechanisms'
    ],
    case_studies: ['options-strategy-case', 'futures-hedging-example'],
    calculation_practices: ['option-payoff', 'put-call-parity', 'futures-pricing'],
    standards: ['CFA-Level1', 'CFA-Level2', 'CFA-Level3']
  },
  {
    id: 'option-pricing',
    name: 'Option Pricing Models',
    description: 'Valuation models for options and derivatives',
    concepts: ['black-scholes', 'binomial-model', 'greeks', 'implied-volatility', 'binomial-pricing', 'risk-neutral-valuation'],
    duration_hours: 35,
    difficulty_level: 'expert',
    prerequisites: ['options-futures'],
    learning_outcomes: [
      'Apply Black-Scholes model for option pricing',
      'Implement binomial option pricing',
      'Calculate and interpret option Greeks',
      'Determine implied volatility from market prices'
    ],
    case_studies: ['black-scholes-calibration', 'option-strategy-hedging'],
    calculation_practices: ['black-scholes-calculation', 'greeks-calculation', 'binomial-pricing'],
    standards: ['CFA-Level2', 'CFA-Level3', 'FRM-Part1']
  },
  {
    id: 'risk-management',
    name: 'Financial Risk Management',
    description: 'Identifying, measuring, and managing financial risks',
    concepts: ['var-calculation', 'stress-testing', 'hedge-effectiveness', 'credit-risk', 'market-risk', 'operational-risk'],
    duration_hours: 25,
    difficulty_level: 'expert',
    prerequisites: ['portfolio-theory'],
    learning_outcomes: [
      'Calculate Value at Risk using different methods',
      'Perform stress testing and scenario analysis',
      'Evaluate hedge effectiveness',
      'Develop risk management frameworks'
    ],
    case_studies: ['var-calculation-case', 'stress-test-portfolio'],
    calculation_practices: ['var-historical', 'var-monte-carlo', 'hedge-ratio'],
    standards: ['FRM-Part1', 'FRM-Part2', 'Basel-Accord']
  }
];

// ============================================
// SECTION 5: ADVANCED FINANCE TOPICS
// ============================================

const section5: FinanceSection = {
  id: 'advanced-finance',
  name: 'Advanced Finance Topics',
  description: 'Alternative investments, behavioral finance, and advanced strategies',
  units: [],
  total_duration_hours: 70,
  sequence_order: 5
};

section5.units = [
  {
    id: 'alternative-investments',
    name: 'Alternative Investments',
    description: 'Non-traditional investment vehicles',
    concepts: ['private-equity', 'hedge-funds', 'real-estate', 'commodities', 'infrastructure', 'alternative-performance'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['portfolio-theory'],
    learning_outcomes: [
      'Analyze private equity investment structures',
      'Understand hedge fund strategies and fees',
      'Evaluate real estate and commodity investments',
      'Measure alternative investment performance'
    ],
    case_studies: ['pe-due-diligence', 'hedge-fund-strategy'],
    calculation_practices: ['irr-calculation', 'hedge-fund-metrics', 'real-estate-cap-rate'],
    standards: ['CFA-Level3', 'CAIA-Curriculum']
  },
  {
    id: 'behavioral-finance',
    name: 'Behavioral Finance',
    description: 'Psychological factors affecting financial decisions',
    concepts: ['market-efficiency', 'behavioral-biases', 'prospect-theory', 'anchoring', 'overconfidence', 'herding'],
    duration_hours: 20,
    difficulty_level: 'intermediate',
    prerequisites: ['portfolio-theory'],
    learning_outcomes: [
      'Evaluate efficient market hypothesis vs behavioral perspectives',
      'Identify common behavioral biases',
      'Apply prospect theory to decision making',
      'Understand implications for investment strategy'
    ],
    case_studies: ['bubble-case-dotcom', 'behavioral-biases-portfolio'],
    calculation_practices: ['bias-identification', 'decision-analysis'],
    standards: ['CFA-Level2', 'CFA-Level3', 'Behavioral-Finance-Standard']
  },
  {
    id: 'international-finance',
    name: 'International Finance',
    description: 'Currency markets and international financial management',
    concepts: ['exchange-rates', 'interest-rate-parity', 'currency-hedging', 'international-portfolio', 'foreign-investment', 'balance-payments'],
    duration_hours: 25,
    difficulty_level: 'advanced',
    prerequisites: ['fixed-income', 'portfolio-theory'],
    learning_outcomes: [
      'Calculate and interpret exchange rates',
      'Apply interest rate parity relationships',
      'Hedge currency risk in international portfolios',
      'Analyze international investment considerations'
    ],
    case_studies: ['currency-hedging-case', 'emerging-market-investment'],
    calculation_practices: ['forward-rate-calculation', 'currency-hedge-ratio', 'exposure-calculation'],
    standards: ['CFA-Level1', 'CFA-Level2', 'FRM-Part1']
  }
];

// ============================================
// SECTION 6: FINANCIAL MODELING AND APPLICATIONS
// ============================================

const section6: FinanceSection = {
  id: 'financial-modeling',
  name: 'Financial Modeling and Practical Applications',
  description: 'Building financial models and applying finance concepts',
  units: [],
  total_duration_hours: 60,
  sequence_order: 6
};

section6.units = [
  {
    id: 'financial-modeling-basics',
    name: 'Financial Modeling Fundamentals',
    description: 'Building three-statement and valuation models',
    concepts: ['three-statement-model', 'scenario-analysis', 'sensitivity-analysis', 'circular-references', 'model-auditing'],
    duration_hours: 25,
    difficulty_level: 'intermediate',
    prerequisites: ['corporate-finance'],
    learning_outcomes: [
      'Build integrated three-statement financial models',
      'Perform scenario and sensitivity analysis',
      'Handle circular references and iteration',
      'Audit and validate financial models'
    ],
    case_studies: ['complete-dcf-model', 'lbo-model-intro'],
    calculation_practices: ['three-statement-linking', 'scenario-building', 'model-audit'],
    standards: ['Wall-Street-Prep', 'Breaking-Into-Wall-Street']
  },
  {
    id: 'mergers-acquisitions',
    name: 'Mergers and Acquisitions',
    description: 'M&A analysis and deal structuring',
    concepts: ['m-and-a-process', 'valuation-m-and-a', 'deal-structuring', 'synergy-analysis', 'lbo-basics', 'm-and-a-accounting'],
    duration_hours: 20,
    difficulty_level: 'expert',
    prerequisites: ['financial-modeling-basics'],
    learning_outcomes: [
      'Analyze strategic rationale for M&A',
      'Value targets using accretion/dilution analysis',
      'Calculate synergies and their realization',
      'Understand LBO basics and returns analysis'
    ],
    case_studies: ['m-and-a-case-study', 'lbo-model-case'],
    calculation_practices: ['accretion-dilution', 'synergy-valuation', 'lbo-returns'],
    standards: ['CFA-Level3', 'Investment-Banking-Standards']
  },
  {
    id: 'quantitative-finance',
    name: 'Quantitative Finance Methods',
    description: 'Mathematical and statistical approaches to finance',
    concepts: ['monte-carlo-simulation', 'statistical-analysis', 'regression-finance', 'time-series-analysis', 'factor-models', 'machine-learning-finance'],
    duration_hours: 15,
    difficulty_level: 'expert',
    prerequisites: ['financial-modeling-basics'],
    learning_outcomes: [
      'Apply Monte Carlo simulation for option pricing',
      'Perform regression analysis on financial data',
      'Implement time series forecasting',
      'Understand factor models and their applications'
    ],
    case_studies: ['monte-carlo-valuation', 'factor-model-portfolio'],
    calculation_practices: ['monte-carlo-implementation', 'regression-analysis', 'var-monte-carlo'],
    standards: ['FRM-Part1', 'Quantitative-Finance-Standards']
  }
];

// ============================================
// COMPLETE SYLLABUS DEFINITION
// ============================================

export const financeSyllabus: FinanceSyllabus = {
  subject: 'finance',
  display_name: 'Finance & Investment',
  description: 'Comprehensive finance curriculum from basic concepts through advanced financial analysis',
  total_duration_hours: 500,
  sections: [section1, section2, section3, section4, section5, section6],
  applicable_standards: [
    'CFA Program Curriculum',
    'FRM Program Curriculum',
    'ACCA Qualifications',
    'Investment Banking Standards',
    'Wall Street Prep',
    'CAIA Alternative Investments'
  ],
  target_audience: ['Undergraduate Finance', 'Graduate Finance', 'CFA Candidates', 'FRM Candidates', 'Investment Professionals']
};

// Export utility functions
export function getFinanceUnitById(syllabus: FinanceSyllabus, unitId: string): FinanceUnit | undefined {
  for (const section of syllabus.sections) {
    const unit = section.units.find(u => u.id === unitId);
    if (unit) return unit;
  }
  return undefined;
}

export function getFinancePrerequisites(syllabus: FinanceSyllabus, unitId: string): FinanceUnit[] {
  const unit = getFinanceUnitById(syllabus, unitId);
  if (!unit) return [];
  return unit.prerequisites
    .map(prereqId => getFinanceUnitById(syllabus, prereqId))
    .filter((u): u is FinanceUnit => u !== undefined);
}

export function generateFinanceLearningPath(
  syllabus: FinanceSyllabus,
  startUnitId: string,
  targetUnitId: string
): FinanceUnit[] {
  const path: FinanceUnit[] = [];
  const visited = new Set<string>();
  
  function addUnitAndPrerequisites(unitId: string) {
    if (visited.has(unitId)) return;
    
    const unit = getFinanceUnitById(syllabus, unitId);
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

export function calculateFinanceTotalDuration(syllabus: FinanceSyllabus, unitIds: string[]): number {
  return unitIds.reduce((total, unitId) => {
    const unit = getFinanceUnitById(syllabus, unitId);
    return total + (unit?.duration_hours || 0);
  }, 0);
}

export function getCaseStudies(syllabus: FinanceSyllabus, unitId: string): string[] {
  const unit = getFinanceUnitById(syllabus, unitId);
  return unit?.case_studies || [];
}
