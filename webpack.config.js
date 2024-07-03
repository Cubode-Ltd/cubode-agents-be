const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const webpack = require('webpack');
const WebpackShellPluginNext = require('webpack-shell-plugin-next');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

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
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'postcss-loader',
        ],
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
      paths: [
        path.resolve(__dirname, 'node_modules'),
      ],
    }),
    new WebpackShellPluginNext({
      onBuildEnd: {
        scripts: ['docker exec agent_cubode_development python manage.py collectstatic --no-input'],
        blocking: false,
        parallel: true,
      },
    }),
    new CopyWebpackPlugin({
      patterns: [
        { from: 'cubode_agent/assets/svg', to: 'svg' },
      ],
    }),
    new MiniCssExtractPlugin({
      filename: '[name].css',
    }),
],
watchOptions: {
  poll: 1000, // Check for changes every second
  ignored: /node_modules/,
},
mode: 'development',
};
