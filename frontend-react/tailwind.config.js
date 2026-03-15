/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#FA6C1A',
          dark: '#E55A15',
        },
        secondary: {
          DEFAULT: '#1A67FA',
          dark: '#1555D8',
        },
        'text-dark': '#1a1a1a',
        'text-light': '#666666',
        'light-bg': '#f8f9fa',
        'section-bg': '#ffffff',
        'accent-bg': '#fafbfc',
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
