/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
  
    "./cubode_agent/templates/*.html",
    "./cubode_agent/static/src/*.js",
    "./cubode_agent/static/src/*.css",
    "./cubode_agent/static/src/**/**/*.{html,js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

