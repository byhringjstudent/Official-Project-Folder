React + Vite + Tailwind CSS

This template sets up React using Vite along with Tailwind CSS for utility-first styling. It's a minimal and fast setup ideal for modern frontend development.
🔧 Included Features

    Vite for lightning-fast bundling and hot module replacement (HMR)

    React for building UI components

    Tailwind CSS for utility-first styling

    Optional: Styles in index.css

# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

Create React-Vite App

1. npm create vite@latest

2. Proceed

3. Select Framework: React

4. Select Variant: JavaScript

5. To run the dev server: npm run dev

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript and enable type-aware lint rules. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

# Tailwind CSS & FlowBite

https://tailwindcss.com/docs/installation/using-vite

npm install tailwindcss @tailwindcss/vite

npm install flowbite

Add TailwindCSS to Vite:
1. Add "import tailwindcss from '@tailwindcss/vite' to the top of the vite.config.js

2. Add tailwindcss() next to react() in plugins.

3. Import TailwindCSS into your index.css file: "@import "tailwindcss";
