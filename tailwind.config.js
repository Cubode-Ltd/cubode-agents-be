/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./cubode_agent/assets/html/**/*.{html,js}", // Ensure all relevant HTML files are included
    "./cubode_agent/assets/html/home.html",
    "./cubode_agent/assets/html/login.html",
    "./cubode_agent/assets/html/register.html"
  ],
  theme: {
    colors: {
      custom_Black: "#2D2D2A",
      dark_Blue:'#1e395cff',
      custom_Gray:'#C1C1CA',
      blastoiser: "#aabbcc"
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
