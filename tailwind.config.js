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
    extend: {
      gridTemplateColumns: {
        '1': 'repeat(1, minmax(0, 1fr))',
        '2': 'repeat(2, minmax(0, 1fr))',
        '3': 'repeat(3, minmax(0, 1fr))',
        // 必要に応じてさらに追加...
      },
    },
  },
  purge: {
    enabled: true,
    content: ['./templates/*.html', './templates/**/*.html', './assets/**/*.js', './assets/**/*.jsx'],
  },
  plugins: [],
}