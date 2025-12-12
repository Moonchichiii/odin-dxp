/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./apps/**/*.py",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Satoshi', 'system-ui', 'sans-serif'],
        display: ['ClashDisplay', 'system-ui', 'sans-serif'],
      },
      colors: {
        odin: {
          bg: "#020617", // slate-950
          accent: "#22c55e", // emerald-500
          accentSoft: "#4ade80", // emerald-400
        },
      },
    },
  },
  plugins: [],
};
