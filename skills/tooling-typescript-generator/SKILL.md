---
name: "TypeScript Tooling Specialist"
slug: "tooling-typescript-generator"
description: "Generate TypeScript/JavaScript project scaffolding with npm/pnpm/yarn, Jest/Vitest, ESLint/Prettier, and bundling (Vite/Rollup/esbuild)."
capabilities:
  - Project structure generation (library, CLI, API, React/Vue frontend)
  - Package manager setup (npm, pnpm, yarn with workspaces)
  - Testing framework configuration (Jest, Vitest, Playwright)
  - TypeScript configuration (strict mode, paths, decorators)
  - Linting and formatting (ESLint, Prettier, Biome)
  - Bundling and build tools (Vite, Rollup, esbuild, tsup)
  - Monorepo setup (Turborepo, Nx)
inputs:
  - project_type: "library | cli | api | react | vue | monorepo (string)"
  - package_manager: "npm | pnpm | yarn (string)"
  - typescript_version: "5.3 | 5.4 | 5.5 (string)"
  - project_name: "Name of the project (string)"
outputs:
  - project_structure: "Directory layout with all config files (JSON)"
  - package_json: "Complete package.json configuration"
  - tsconfig_json: "TypeScript configuration"
  - build_config: "Vite/Rollup/esbuild configuration"
keywords:
  - typescript
  - javascript
  - tooling
  - npm
  - jest
  - vitest
  - eslint
  - vite
  - node
  - react
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://www.typescriptlang.org/docs/
  - https://docs.npmjs.com/
  - https://vitejs.dev/guide/
  - https://jestjs.io/docs/getting-started
  - https://eslint.org/docs/latest/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Starting a new TypeScript/JavaScript project requiring modern tooling
- Migrating legacy JavaScript projects to TypeScript
- Setting up React/Vue applications with type safety
- Creating CLI tools with Node.js
- Building monorepo workspaces with shared packages

**Not for:**
- Next.js/Nuxt projects (use framework CLIs)
- React Native/Expo (use `mobile-cicd-generator`)
- Simple scripts without build requirements

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601)
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `project_type` must be one of: library, cli, api, react, vue, monorepo
- `package_manager` must be one of: npm, pnpm, yarn
- `typescript_version` must be one of: 5.3, 5.4, 5.5
- `project_name` must be valid npm package name (lowercase, hyphens allowed)

**Source freshness:**
- TypeScript docs must be accessible [accessed 2025-10-26](https://www.typescriptlang.org/docs/)
- npm docs must be accessible [accessed 2025-10-26](https://docs.npmjs.com/)
- Vite docs must be accessible [accessed 2025-10-26](https://vitejs.dev/guide/)
- Jest docs must be accessible [accessed 2025-10-26](https://jestjs.io/docs/getting-started)

---

## Procedure

### T1: Basic Project Structure (≤2k tokens)

**Fast path for common cases:**

1. **Directory Layout Generation**
   ```
   project-name/
     src/
       index.ts
     tests/
       index.test.ts
     package.json
     tsconfig.json
     .gitignore
     README.md
   ```

2. **Core package.json** [accessed 2025-10-26](https://docs.npmjs.com/cli/v10/configuring-npm/package-json)
   ```json
   {
     "name": "project-name",
     "version": "0.1.0",
     "type": "module",
     "main": "./dist/index.js",
     "types": "./dist/index.d.ts",
     "scripts": {
       "build": "tsc",
       "test": "jest",
       "lint": "eslint src"
     },
     "devDependencies": {
       "typescript": "^5.5.0",
       "@types/node": "^20.0.0"
     }
   }
   ```

3. **TypeScript Configuration** [accessed 2025-10-26](https://www.typescriptlang.org/tsconfig)
   ```json
   {
     "compilerOptions": {
       "target": "ES2022",
       "module": "ESNext",
       "moduleResolution": "bundler",
       "strict": true,
       "esModuleInterop": true,
       "skipLibCheck": true,
       "declaration": true,
       "outDir": "./dist"
     },
     "include": ["src"],
     "exclude": ["node_modules", "dist"]
   }
   ```

**Decision:** If only basic scaffolding needed → STOP at T1; otherwise proceed to T2.

---

### T2: Full Tooling Setup (≤6k tokens)

**Extended configuration with testing and build tools:**

1. **Testing Framework Configuration**

   **Jest** [accessed 2025-10-26](https://jestjs.io/docs/getting-started)
   ```json
   {
     "devDependencies": {
       "jest": "^29.7.0",
       "@types/jest": "^29.5.0",
       "ts-jest": "^29.1.0"
     },
     "scripts": {
       "test": "jest",
       "test:watch": "jest --watch",
       "test:coverage": "jest --coverage"
     }
   }
   ```

   jest.config.js:
   ```javascript
   export default {
     preset: 'ts-jest',
     testEnvironment: 'node',
     roots: ['<rootDir>/tests'],
     testMatch: ['**/*.test.ts'],
     collectCoverageFrom: ['src/**/*.ts'],
     coverageThreshold: {
       global: { branches: 80, functions: 80, lines: 80 }
     }
   };
   ```

   **Vitest** (alternative, faster) [accessed 2025-10-26](https://vitest.dev/guide/)
   ```json
   {
     "devDependencies": {
       "vitest": "^1.6.0"
     },
     "scripts": {
       "test": "vitest run",
       "test:watch": "vitest"
     }
   }
   ```

2. **Linting and Formatting**

   **ESLint + Prettier** [accessed 2025-10-26](https://eslint.org/docs/latest/use/getting-started)
   ```json
   {
     "devDependencies": {
       "eslint": "^8.57.0",
       "@typescript-eslint/parser": "^7.0.0",
       "@typescript-eslint/eslint-plugin": "^7.0.0",
       "prettier": "^3.2.0",
       "eslint-config-prettier": "^9.1.0"
     }
   }
   ```

   .eslintrc.json:
   ```json
   {
     "parser": "@typescript-eslint/parser",
     "plugins": ["@typescript-eslint"],
     "extends": [
       "eslint:recommended",
       "plugin:@typescript-eslint/recommended",
       "prettier"
     ],
     "rules": {
       "@typescript-eslint/no-unused-vars": "error",
       "@typescript-eslint/explicit-function-return-type": "warn"
     }
   }
   ```

3. **Build Tools**

   **Vite** (for libraries and apps) [accessed 2025-10-26](https://vitejs.dev/config/)
   ```javascript
   // vite.config.ts
   import { defineConfig } from 'vite';
   import { resolve } from 'path';

   export default defineConfig({
     build: {
       lib: {
         entry: resolve(__dirname, 'src/index.ts'),
         name: 'MyLib',
         fileName: 'index'
       }
     }
   });
   ```

   **tsup** (zero-config bundler) [accessed 2025-10-26](https://tsup.egoist.dev/)
   ```json
   {
     "scripts": {
       "build": "tsup src/index.ts --format cjs,esm --dts"
     }
   }
   ```

4. **React/Vue Project Setup**

   **React with Vite**:
   ```json
   {
     "dependencies": {
       "react": "^18.3.0",
       "react-dom": "^18.3.0"
     },
     "devDependencies": {
       "@vitejs/plugin-react": "^4.3.0",
       "@types/react": "^18.3.0",
       "@types/react-dom": "^18.3.0"
     }
   }
   ```

   **Vue with Vite**:
   ```json
   {
     "dependencies": {
       "vue": "^3.4.0"
     },
     "devDependencies": {
       "@vitejs/plugin-vue": "^5.0.0"
     }
   }
   ```

---

### T3: Advanced Configuration (≤12k tokens)

**Deep configuration for monorepos and production:**

1. **Monorepo Setup** [accessed 2025-10-26](https://pnpm.io/workspaces)

   **pnpm Workspaces**:
   ```yaml
   # pnpm-workspace.yaml
   packages:
     - 'packages/*'
     - 'apps/*'
   ```

   Root package.json:
   ```json
   {
     "name": "monorepo",
     "private": true,
     "scripts": {
       "build": "pnpm -r build",
       "test": "pnpm -r test",
       "lint": "pnpm -r lint"
     }
   }
   ```

   **Turborepo** [accessed 2025-10-26](https://turbo.build/repo/docs)
   ```json
   {
     "devDependencies": {
       "turbo": "^2.0.0"
     }
   }
   ```

   turbo.json:
   ```json
   {
     "pipeline": {
       "build": {
         "dependsOn": ["^build"],
         "outputs": ["dist/**"]
       },
       "test": {
         "dependsOn": ["build"]
       }
     }
   }
   ```

2. **TypeScript Path Mapping**
   ```json
   {
     "compilerOptions": {
       "baseUrl": ".",
       "paths": {
         "@/*": ["src/*"],
         "@utils/*": ["src/utils/*"],
         "@components/*": ["src/components/*"]
       }
     }
   }
   ```

3. **CI/CD Pipeline** (GitHub Actions)
   ```.github/workflows/ci.yml
   name: CI
   on: [push, pull_request]
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: pnpm/action-setup@v4
         - uses: actions/setup-node@v4
           with:
             node-version: 20
             cache: 'pnpm'
         - run: pnpm install --frozen-lockfile
         - run: pnpm test
         - run: pnpm build
   ```

4. **Package Publishing** [accessed 2025-10-26](https://docs.npmjs.com/cli/v10/commands/npm-publish)
   ```json
   {
     "files": ["dist"],
     "exports": {
       ".": {
         "import": "./dist/index.js",
         "require": "./dist/index.cjs",
         "types": "./dist/index.d.ts"
       }
     },
     "publishConfig": {
       "access": "public"
     }
   }
   ```

5. **Playwright E2E Testing** (for React/Vue)
   ```json
   {
     "devDependencies": {
       "@playwright/test": "^1.45.0"
     },
     "scripts": {
       "test:e2e": "playwright test"
     }
   }
   ```

---

## Decision Rules

**Package Manager Selection:**
- **pnpm:** Monorepos, disk space efficiency, strict dependency resolution
- **yarn:** Existing Yarn projects, plug'n'play mode
- **npm:** Default choice, ubiquitous, simple projects

**Project Type Structure:**
- **library:** Dual ESM/CJS output, type declarations, no bundled dependencies
- **cli:** Shebang, executable permissions, bundled dependencies
- **api:** Express/Fastify setup, middleware, error handling
- **react/vue:** Component structure, routing, state management
- **monorepo:** Workspace configuration, shared packages, build orchestration

**Abort Conditions:**
- Invalid `project_name` (uppercase, special chars) → error
- Conflicting configuration (React + Vue) → error
- Unsupported TypeScript version → error

**Tool Version Selection:**
- Use latest stable TypeScript 5.x
- Pin dev dependencies, use caret ranges for prod
- ESM-first module strategy

---

## Output Contract

**Schema (JSON):**

```json
{
  "project_name": "string",
  "project_type": "library | cli | api | react | vue | monorepo",
  "typescript_version": "string",
  "package_manager": "npm | pnpm | yarn",
  "structure": {
    "directories": ["string"],
    "files": {
      "path/to/file": "file content (string)"
    }
  },
  "commands": {
    "install": "string",
    "dev": "string",
    "build": "string",
    "test": "string",
    "lint": "string"
  },
  "next_steps": ["string"],
  "timestamp": "ISO-8601 string (NOW_ET)"
}
```

**Required Fields:**
- All fields mandatory
- File contents must be syntactically valid (JSON, TypeScript)
- Include inline comments explaining configuration choices

---

## Examples

**Example: React Application with Vite**

```yaml
INPUT: {project_type: "react", package_manager: "pnpm", typescript_version: "5.5"}
OUTPUT:
structure:
  - src/{App.tsx, main.tsx, vite-env.d.ts}
  - public/
  - index.html, vite.config.ts, tsconfig.json
vite.config.ts:
  import { defineConfig } from 'vite';
  import react from '@vitejs/plugin-react';
  export default defineConfig({ plugins: [react()] });
tsconfig.json:
  {
    "compilerOptions": {
      "target": "ES2020", "module": "ESNext",
      "lib": ["ES2020", "DOM"],
      "jsx": "react-jsx", "strict": true,
      "moduleResolution": "bundler"
    }
  }
commands:
  install: "pnpm install"
  dev: "pnpm vite"
  build: "pnpm vite build"
  test: "pnpm vitest"
```

---

## Quality Gates

**Token Budgets:**
- **T1:** ≤2k tokens (basic structure + package.json + tsconfig)
- **T2:** ≤6k tokens (testing, linting, build tools, React/Vue)
- **T3:** ≤12k tokens (monorepos, CI/CD, publishing, E2E)

**Safety:**
- No hardcoded API keys or secrets
- .gitignore includes node_modules, dist, .env
- ESLint configured to catch security issues

**Auditability:**
- All configurations cite official documentation
- Version constraints explicit
- Generation timestamp included

**Determinism:**
- Same inputs → identical structure
- Versions pinned where appropriate
- No randomness in generation

**Performance:**
- T1 generation: <1 second
- T2 generation: <3 seconds
- T3 generation: <5 seconds

---

## Resources

**Official Documentation (accessed 2025-10-26):**
1. [TypeScript Handbook](https://www.typescriptlang.org/docs/) - Language reference
2. [npm Documentation](https://docs.npmjs.com/) - Package management
3. [Vite Guide](https://vitejs.dev/guide/) - Build tool and dev server
4. [Jest Getting Started](https://jestjs.io/docs/getting-started) - Testing framework
5. [ESLint User Guide](https://eslint.org/docs/latest/) - Linting
6. [pnpm Workspaces](https://pnpm.io/workspaces) - Monorepo management
7. [Turborepo Docs](https://turbo.build/repo/docs) - Build orchestration

**Build Tools:**
- [Rollup](https://rollupjs.org/) - Module bundler
- [esbuild](https://esbuild.github.io/) - Extremely fast bundler
- [tsup](https://tsup.egoist.dev/) - Zero-config TypeScript bundler

**Testing:**
- [Vitest](https://vitest.dev/) - Vite-native test framework
- [Playwright](https://playwright.dev/) - E2E testing

**Best Practices:**
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/) - Best practices
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/) - Patterns
