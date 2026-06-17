import defaultTheme from 'tailwindcss/defaultTheme'

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans:   ['Google Sans', ...defaultTheme.fontFamily.sans],
        arabic: ['Al Majeed Quranic', 'Traditional Arabic', 'serif'],
        cairo:  ['Cairo', 'sans-serif'],
      },
      transitionDuration: {
        '400': '400ms',
      },
      colors: {
        emerald: {
          950: '#022c22',
        },
        brand: {
          DEFAULT: '#234ecc',
          dark:    '#1a3ba8',
          light:   '#3d65e8',
          muted:   '#e8edfb',
        },
      },
    },
  },
  plugins: [],
}
