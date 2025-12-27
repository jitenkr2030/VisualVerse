# FinVerse - Syllabus Module

## Overview
This module defines the curriculum structure and lesson content for FinVerse, covering financial markets, interest calculations, and risk management topics.

## License
**Apache 2.0** - This module is open source under the Apache License 2.0. See `/LICENSE` for terms.

## Directory Structure

```
syllabus/
├── manifest.json          # Curriculum structure
├── content/
│   ├── markets/
│   │   ├── stock-basics.md
│   │   ├── technical-analysis.md
│   │   └── market-indicators.md
│   ├── interest/
│   │   ├── time-value.md
│   │   ├── compound-interest.md
│   │   └── annuities.md
│   └── risk/
│       ├── diversification.md
│       ├── portfolio-theory.md
│       └── risk-metrics.md
├── assessments/
│   ├── quizzes.json
│   └── problems.json
└── README.md
```

## Curriculum Structure (manifest.json)

```json
{
  "title": "FinVerse Curriculum",
  "version": "1.0.0",
  "levels": [
    {
      "id": "financial-basics",
      "title": "Financial Fundamentals",
      "order": 1,
      "duration": "6 weeks",
      "topics": [
        {
          "id": "time-value",
          "title": "Time Value of Money",
          "lessons": ["present-value", "future-value", "discounting"],
          "animations": ["interest/time-value"],
          "assessments": ["quiz-tvm"]
        }
      ]
    }
  ]
}
```

## Content Format

Lessons are written in Markdown with embedded animation references:

```markdown
# Time Value of Money

## Learning Objectives
- Understand why money has time value
- Calculate present and future values
- Apply discounting to investment decisions

## Concept: Why Does Money Have Time Value?

Money available today is worth more than the same amount in the future due to its potential earning capacity.

<animation src="interest/time-value.ts" 
           type="interactive"
           params='{"principal": 10000, "rate": 0.07, "years": 10}' />

## The Math

### Future Value (FV)
FV = PV × (1 + r)ⁿ

Where:
- PV = Present Value
- r = Interest rate per period
- n = Number of periods

### Present Value (PV)
PV = FV / (1 + r)ⁿ

Where we "discount" future value back to today.

<animation src="interest/time-value.ts" 
           type="breakdown"
           params='{"showFormulas": true}' />

## Compound Interest vs Simple Interest

### Simple Interest
- Interest calculated only on principal
- I = P × r × t
- Linear growth

### Compound Interest
- Interest calculated on principal + accumulated interest
- A = P × (1 + r/n)ⁿᵗ
- Exponential growth

<animation src="interest/compound-interest.ts" 
           type="comparison"
           params='{"principal": 10000, "rate": 0.07, "years": 20}' />

## Applications

1. **Investment Growth**: How your savings grow over time
2. **Loan Payments**: Understanding mortgage amortization
3. **Retirement Planning**: Required savings to reach goals
4. **Business Valuation**: Discounted cash flow analysis

## Summary
- Money has time value due to earning potential
- Future value = Present value × (1 + r)ⁿ
- Present value = Future value / (1 + r)ⁿ
- Compound interest grows faster than simple interest
```

## License

Licensed under the Apache License, Version 2.0. See `/LICENSE` for details.
