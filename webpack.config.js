var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  context: __dirname,

  mode: 'development', 

  entry: './assets/js/main.js', // これがエントリーポイント

  output: { // コンパイルされたファイルの設定
      path: path.resolve('./static/bundles/'),
      filename: "[name]-[hash].js",
  },
  devtool: 'inline-source-map',
  plugins: [
    new BundleTracker({
        path: path.resolve('./'),
        filename: 'webpack-stats.json'
    }),
  ],

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
}