# FinVerse - Animations Module

## Overview
This module contains finance and business animation modules for VisualVerse. It provides visualizations for financial markets, risk management, and interest calculations using the Animation Engine.

## License
**Apache 2.0** - This module is open source under the Apache License 2.0. See `/LICENSE` for terms.

## Directory Structure

```
animations/
├── markets/
│   ├── stock-charts.ts
│   ├── trading-volumes.ts
│   └── market-indicators.ts
├── interest/
│   ├── compound-interest.ts
│   ├── annuities.ts
│   └── amortization.ts
├── risk/
│   ├── diversification.ts
│   ├── portfolio-risk.ts
│   └── value-at-risk.ts
├── index.ts
└── README.md
```

## Quick Start

```typescript
import { 
  animateStockChart, 
  animateCompoundInterest,
  animatePortfolioRisk 
} from './animations';

const animation = animateStockChart({
  symbol: 'AAPL',
  period: '1Y',
  showVolume: true,
  indicators: ['SMA', 'RSI'],
});
```

## Markets Animations

### Stock Charts
- Line charts for price history
- Candlestick patterns
- Volume histograms

### Trading Volumes
- Volume over time
- Buy/sell volume ratio
- Volume price trends

### Market Indicators
- Moving averages (SMA, EMA)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)

## Interest Animations

### Compound Interest
- Exponential growth visualization
- Interest compounding frequency
- Future value calculations

### Annuities
- Present value of annuities
- Future value of annuities
- Payment schedules

### Amortization
- Loan repayment schedules
- Principal vs. interest over time
- Early payment impact

## Risk Animations

### Diversification
- Correlation visualization
- Portfolio spread
- Risk reduction through diversification

### Portfolio Risk
- Volatility comparison
- Sharpe ratio visualization
- Efficient frontier

### Value at Risk (VaR)
- VaR calculation methods
- Risk exposure visualization
- Scenario analysis

## Usage with Animation Engine

```typescript
import { AnimationEngine } from '@visualverse/engine';

const engine = new AnimationEngine();
const scene = engine.createScene();

const financeAnimations = new FinanceAnimations(scene);
financeAnimations.animateCompoundInterest({
  principal: 10000,
  rate: 0.07,
  years: 30,
  compounding: 'monthly',
});
```

## License

Licensed under the Apache License, Version 2.0. See `/LICENSE` for details.
