/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './soyal_portfolio/templates/**/*.html',
    './core/templates/**/*.html',
    './home/templates/**/*.html',
    './about/templates/**/*.html',
    './experience/templates/**/*.html',
    './projects/templates/**/*.html',
    './blog/templates/**/*.html',
    './contact/templates/**/*.html',
    './resume/templates/**/*.html',
    './search/templates/**/*.html',
    './core/templatetags/*.py',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      colors: {
        emerald: {
          50: '#f0fdf4',
          100: '#d1fae5',
          200: '#a7f3d0',
          300: '#6ee7b7',
          400: '#34d399',
          500: '#10b981',
          600: '#059669',
          700: '#047857',
          800: '#065f46',
          900: '#064e3b',
          950: '#022c22',
        },
      },
    },
  },
  plugins: [],
};
