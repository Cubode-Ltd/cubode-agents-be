const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: {
    login: './cubode_agent/assets/js/login.js',
    register: './cubode_agent/assets/js/register.js',
    home: './cubode_agent/assets/js/home.js',
  },
  output: {
    path: path.resolve(__dirname, './cubode_agent/static/bundle/'),
    filename: '[name].bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      },
    ],
  },
  plugins: [
    new BundleTracker({
        path: path.resolve(__dirname, 'cubode_agent'),
        filename: 'webpack-stats.json'
    }),
    new HtmlWebpackPlugin({
      filename: 'login.html',
      template: './cubode_agent/assets/html/login.html',
      chunks: ['login'],
    }),
    new HtmlWebpackPlugin({
      filename: 'register.html',
      template: './cubode_agent/assets/html/register.html',
      chunks: ['register'],
    }),
    new HtmlWebpackPlugin({
      filename: 'home.html',
      template: './cubode_agent/assets/html/home.html',
      chunks: ['home'],
    }),
    new webpack.WatchIgnorePlugin({
      paths: [/node_modules/],
    }),
],
  mode: 'development',
};
