// TypeScript Library Example: math-utils
// Demonstrates: type exports, pure functions, zero dependencies

export interface CalculationResult {
  value: number;
  timestamp: Date;
}

export class Calculator {
  private history: number[] = [];

  add(a: number, b: number): CalculationResult {
    const value = a + b;
    this.history.push(value);
    return { value, timestamp: new Date() };
  }

  multiply(a: number, b: number): CalculationResult {
    const value = a * b;
    this.history.push(value);
    return { value, timestamp: new Date() };
  }

  getHistory(): readonly number[] {
    return Object.freeze([...this.history]);
  }

  clear(): void {
    this.history = [];
  }
}
