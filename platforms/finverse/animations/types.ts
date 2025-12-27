/**
 * FinVerse Animation Types
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

// Markets Animation Types
export interface StockChartOptions {
  symbol: string;
  period: '1D' | '1W' | '1M' | '3M' | '1Y' | '5Y';
  showVolume?: boolean;
  chartType?: 'line' | 'candlestick' | 'bar';
  indicators?: string[];
}

export interface TradingVolumeOptions {
  symbol: string;
  period: string;
  showBuySellRatio?: boolean;
  showVolumeProfile?: boolean;
}

export interface IndicatorOptions {
  type: 'SMA' | 'EMA' | 'RSI' | 'MACD' | 'Bollinger';
  parameters?: Record<string, number>;
  showDivergence?: boolean;
}

// Interest Animation Types
export interface CompoundInterestOptions {
  principal: number;
  rate: number;
  years: number;
  compounding: 'daily' | 'monthly' | 'quarterly' | 'annually';
  showGrowth?: boolean;
  compareToSimple?: boolean;
}

export interface AnnuityOptions {
  payment: number;
  rate: number;
  periods: number;
  type: 'ordinary' | 'annuity-due';
  showPaymentSchedule?: boolean;
}

export interface AmortizationOptions {
  principal: number;
  rate: number;
  termYears: number;
  showPrincipalInterest?: boolean;
  showRemainingBalance?: boolean;
}

// Risk Animation Types
export interface DiversificationOptions {
  assets: string[];
  correlations?: number[][];
  showCorrelationMatrix?: boolean;
  portfolioCount?: number;
}

export interface PortfolioRiskOptions {
  assets: string[];
  weights: number[];
  expectedReturns?: number[];
  showEfficientFrontier?: boolean;
  riskFreeRate?: number;
}

export interface VaROptions {
  portfolio: { mean: number; stdDev: number };
  confidenceLevel: number;
  timeHorizon: number;
  method: 'historical' | 'variance-covariance' | 'monte-carlo';
  showDistribution?: boolean;
}
