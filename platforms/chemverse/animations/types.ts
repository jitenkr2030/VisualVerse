/**
 * ChemVerse Animation Types
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

// Organic Chemistry Animation Types
export interface HydrocarbonOptions {
  formula: string;
  style?: 'ball-and-stick' | 'space-filling' | 'wireframe';
  showBonds?: boolean;
  showAtoms?: boolean;
}

export interface FunctionalGroupOptions {
  group: 'alcohol' | 'ketone' | 'aldehyde' | 'carboxylic' | 'amine';
  formula?: string;
  showHydrogenBonds?: boolean;
}

export interface ReactionOptions {
  reactants: string[];
  products: string[];
  mechanism: 'addition' | 'substitution' | 'elimination';
  showElectronMovement?: boolean;
}

// Inorganic Chemistry Animation Types
export interface PeriodicTableOptions {
  element: string;
  showElectronConfig?: boolean;
  showPeriodicity?: boolean;
}

export interface BondingOptions {
  type: 'ionic' | 'covalent' | 'metallic';
  atoms: string[];
  showElectronTransfer?: boolean;
  showOrbitalOverlap?: boolean;
}

export interface CoordinationOptions {
  centralAtom: string;
  ligands: string[];
  coordinationNumber: number;
  showGeometry?: boolean;
}

// Physical Chemistry Animation Types
export interface ThermodynamicsOptions {
  system: string;
  process: 'isothermal' | 'adiabatic' | 'isochoric' | 'isobaric';
  showHeatFlow?: boolean;
  showWork?: boolean;
}

export interface KineticsOptions {
  reaction: string;
  activationEnergy: number;
  showEnergyBarrier?: boolean;
  showCatalystEffect?: boolean;
}

export interface EquilibriumOptions {
  reaction: string;
  equilibriumConstant: number;
  showLeChatelier?: boolean;
  perturbation?: { type: string; value: number };
}
