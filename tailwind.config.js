/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  purge: [
    './cubode_agent/assets/**/*.html',
    './cubode_agent/assets/**/*.js',
    './cubode_agent/assets/**/*.jsx',
    './cubode_agent/assets/**/*.ts',
    './cubode_agent/assets/**/*.tsx',
    './cubode_agent/assets/**/*.vue',
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
