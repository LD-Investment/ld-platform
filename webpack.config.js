const HtmlWebpackPlugin = require("html-webpack-plugin");
const InterpolateHtmlPlugin = require("interpolate-html-plugin");
const Dotenv = require('dotenv-webpack');


module.exports = {
  mode: "development",
  entry: "./ld_platform_web/src/index.js",
  output: {
    filename: "bundle.[hash].js"
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.html$/,
        use: [
          {
            loader: "html-loader",
            options: {
              minimize: true
            }
          }
        ]
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/i,
        use: [
          {
            loader: "file-loader"
          }
        ]
      },
      {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          // Creates `style` nodes from JS strings
          "style-loader",
          // Translates CSS into CommonJS
          "css-loader",
          // Compiles Sass to CSS
          "sass-loader",
        ],
      },
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: "ld_platform_web/public/index.html",
      favicon: "ld_platform_web/public/favicon.ico"
    }),
    new InterpolateHtmlPlugin({
      PUBLIC_URL: "ld_platform_web/public" // can modify `static` to another name or get it from `process`
    }),
    new Dotenv()
  ],
  devServer: {
    host: "localhost",
    port: 9000,
    open: true,
    hot: true
  }
};
