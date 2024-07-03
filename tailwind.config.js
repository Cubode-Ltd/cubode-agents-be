/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./cubode_agent/assets/**/*.html"
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
