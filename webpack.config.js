const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  mode: "development",
  entry: "./ld_platform_web/src/index.js",
  output: {
    filename: "bundle.[hash].js",
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.html$/,
        use: [
          {
            loader: "html-loader",
            options: {
              minimize: true,
            },
          },
        ],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "ld_platform_web/public/index.html",
    }),
  ],
  devServer: {
    host: "localhost",
    port: 9000,
    open: true,
    hot: true,
  },
};
