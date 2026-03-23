import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        // Custom Nexus Colors matching HTML template
        surface: {
          DEFAULT: '#0b1326',
          bright: '#31394d',
          container: '#171f33',
          'container-high': '#222a3d',
          'container-highest': '#2d3449',
          'container-low': '#131b2e',
          'container-lowest': '#060e20',
          dim: '#0b1326',
        },
        primary: {
          DEFAULT: '#3fe56c', // Using the EcoVolt green
          container: '#174f26',
        },
        secondary: {
          DEFAULT: '#ff5c5c', // Example alert red
          container: '#4a1b1b',
        },
        tertiary: {
          DEFAULT: '#ffb142', // Example warning yellow
          container: '#4a3311',
        },
        'on-surface': '#dae2fd',
        'on-surface-variant': '#c3c6d7',
        'outline-variant': '#434655'
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        space: ['Manrope', 'sans-serif'],
      }
    },
  },
  plugins: [],
};
export default config;
