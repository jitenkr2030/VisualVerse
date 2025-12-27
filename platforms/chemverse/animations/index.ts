/**
 * ChemVerse Animation Module
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

// Organic Chemistry Animations
export { 
  animateHydrocarbon, 
  animateFunctionalGroup, 
  animateOrganicReaction 
} from './organic';

// Inorganic Chemistry Animations
export { 
  animatePeriodicTable, 
  animateBonding, 
  animateCoordination 
} from './inorganic';

// Physical Chemistry Animations
export { 
  animateThermodynamics, 
  animateKinetics, 
  animateEquilibrium 
} from './physical';

// Types
export type { 
  HydrocarbonOptions,
  FunctionalGroupOptions,
  ReactionOptions,
  PeriodicTableOptions,
  BondingOptions,
  CoordinationOptions,
  ThermodynamicsOptions,
  KineticsOptions,
  EquilibriumOptions 
} from './types';

// Index file for all exports
export * from './types';
