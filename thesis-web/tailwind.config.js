// thesis-web/tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  darkMode: 'class', // or 'media' for OS-level preference
  theme: {
    extend: {
      colors: {
        'thicker-purple': '#6b21a8', // Define a thicker purple color
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: []
}