/**
 * PhysicsVerse Animation Types
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

// Mechanics Animation Types
export interface KinematicsOptions {
  initialVelocity: number;
  angle: number;
  gravity: number;
  showTrajectory?: boolean;
  showVectors?: boolean;
}

export interface ForcesOptions {
  forces: Array<{ magnitude: number; direction: number }>;
  mass?: number;
  showFreeBody?: boolean;
}

export interface EnergyOptions {
  mass: number;
  height: number;
  showKinetic?: boolean;
  showPotential?: boolean;
  showTotal?: boolean;
}

export interface MomentumOptions {
  objects: Array<{ mass: number; velocity: number }>;
  collisionType?: 'elastic' | 'inelastic';
  showBefore?: boolean;
  showAfter?: boolean;
}

// Electromagnetism Animation Types
export interface ElectrostaticsOptions {
  charges: Array<{ position: [number, number]; magnitude: number }>;
  showFieldLines?: boolean;
  showPotential?: boolean;
}

export interface CircuitOptions {
  components: string[];
  voltage: number;
  showCurrent?: boolean;
  showVoltageDrop?: boolean;
}

export interface MagnetismOptions {
  source: 'current' | 'magnet';
  position?: [number, number];
  showFieldLines?: boolean;
}

export interface InductionOptions {
  coilTurns: number;
  magneticField: number;
  showFlux?: boolean;
  showCurrent?: boolean;
}

// Optics Animation Types
export interface ReflectionOptions {
  surface: 'plane' | 'concave' | 'convex';
  incidentAngle: number;
  showNormal?: boolean;
}

export interface RefractionOptions {
  interfacePosition: number;
  n1: number;
  n2: number;
  incidentAngle: number;
  showRayPath?: boolean;
}

export interface LensesOptions {
  type: 'convex' | 'concave';
  focalLength: number;
  objectDistance: number;
  showRayDiagram?: boolean;
}

export interface WavesOptions {
  frequency: number;
  amplitude: number;
  type?: 'sine' | 'square' | 'triangle';
  showInterference?: boolean;
}
