/**
 * MathVerse Animation Types
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

// Algebra Animation Types
export interface LinearEquationOptions {
  equation: string;
  steps?: boolean;
  duration?: number;
  showGraph?: boolean;
}

export interface QuadraticOptions {
  vertex?: [number, number];
  a: number;
  showRoots?: boolean;
  showVertex?: boolean;
}

export interface PolynomialOptions {
  coefficients: number[];
  range?: [number, number];
}

export interface SystemOptions {
  equations: string[];
  solution?: [number, number];
  showIntersection?: boolean;
}

// Calculus Animation Types
export interface LimitOptions {
  expression: string;
  approach: number;
  direction?: 'left' | 'right' | 'both';
}

export interface DerivativeOptions {
  function: string;
  point: number;
  showTangent?: boolean;
  showSecantApproach?: boolean;
}

export interface IntegralOptions {
  function: string;
  bounds?: [number, number];
  showArea?: boolean;
  method?: 'riemann' | 'trapezoid' | 'simpson';
}

export interface SeriesOptions {
  terms: number[];
  partialSum?: number;
  showConvergence?: boolean;
}

// Linear Algebra Animation Types
export interface VectorOptions {
  components: number[];
  startPoint?: [number, number, number];
  showComponents?: boolean;
}

export interface MatrixOptions {
  data: number[][];
  operation?: 'multiply' | 'transpose' | 'inverse';
  rowOperation?: { row: number; operation: string };
}

export interface TransformationOptions {
  matrix: number[][];
  vectors: number[][];
  showOriginal?: boolean;
  showTransformed?: boolean;
}

export interface EigenvalueOptions {
  matrix: number[][];
  showEigenvectors?: boolean;
  animate?: boolean;
}
