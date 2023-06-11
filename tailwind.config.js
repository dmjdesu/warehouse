/** @type {import('tailwindcss').Config} */
module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  content: [
    "./assets/js/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  purge: {
    enabled: true,
    content: ['./templates/*.html', './templates/**/*.html', './assets/**/*.js', './assets/**/*.jsx'],
  },
  plugins: [],
}

