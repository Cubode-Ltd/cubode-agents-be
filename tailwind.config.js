/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./cubode_agent/templates/*.html",
    "./cubode_agent/static/src/*.js",
    "./cubode_agent/static/src/*.css",
    "./cubode_agent/static/src/**/**/*.{html,js,jsx,ts,tsx}",
  ],
  theme: {
    colors: {
      custom_Black: "#2D2D2A",
      dark_Blue:'#1e395cff',
      custom_Gray:'#C1C1CA',

    },
    extend: {
      fontSize: {
        "custom-base": "14px",
      },
      lineHeight: {
        "custom-7": "30px",
      },
    },
  },
  plugins: [],
};
