/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        arabic: ['Amiri', 'Traditional Arabic', 'serif'],
        cairo: ['Cairo', 'sans-serif'],
      },
      colors: {
        emerald: {
          950: '#022c22',
        },
      },
    },
  },
  plugins: [],
}
