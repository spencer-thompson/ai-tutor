# CLAUDE.md - Your AI Coding Assistant Guide

## Build/Test/Lint Commands
```bash
# Development
npm run dev        # Run development server
npm run build      # Build for production
npm run preview    # Preview production build

# Testing
npm run test       # Run all tests with vitest
npx vitest run src/index.test.ts  # Run a single test

# Code Quality
npm run lint       # Run prettier check and eslint
npm run format     # Format with prettier
npm run check      # TypeScript checking
```

## Code Style Guidelines
- **Components**: PascalCase for filenames (ChatBox.svelte)
- **Variables/Functions**: camelCase, underscores for derived variables (_ready)
- **TypeScript**: Use strict typing, interfaces for complex structures
- **Formatting**: Tabs, single quotes, 100 char line width
- **Svelte Structure**: <script lang="ts">, component markup, <style>
- **State Management**: Svelte stores, reactive declarations ($:)
- **Error Handling**: Try/catch blocks, fallbacks for undefined values
- **Component Props**: Use export let with proper typing