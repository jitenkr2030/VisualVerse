/**
 * FinVerse Animation Module
 * 
 * Copyright 2024 VisualVerse Contributors
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// Markets Animations
export { 
  animateStockChart, 
  animateTradingVolume, 
  animateMarketIndicator 
} from './markets';

// Interest Animations
export { 
  animateCompoundInterest, 
  animateAnnuity, 
  animateAmortization 
} from './interest';

// Risk Animations
export { 
  animateDiversification, 
  animatePortfolioRisk, 
  animateValueAtRisk 
} from './risk';

// Types
export type { 
  StockChartOptions,
  TradingVolumeOptions,
  IndicatorOptions,
  CompoundInterestOptions,
  AnnuityOptions,
  AmortizationOptions,
  DiversificationOptions,
  PortfolioRiskOptions,
  VaROptions 
} from './types';

// Index file for all exports
export * from './types';
