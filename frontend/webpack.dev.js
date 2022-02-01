const { merge } = require("webpack-merge");
const common = require("./webpack.common.js");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const InterpolateHtmlPlugin = require("interpolate-html-plugin");
const Dotenv = require("dotenv-webpack");

module.exports = merge(common, {
  mode: "development",
  devtool: "inline-source-map",
  plugins: [
    new HtmlWebpackPlugin({
      template: "ld_platform_web/public/index.html",
      favicon: "ld_platform_web/public/favicon.ico"
    }),
    new InterpolateHtmlPlugin({
      PUBLIC_URL: "ld_platform_web/public" // can modify `static` to another name or get it from `process`
    }),
    new Dotenv({
      path: ".env.development"
    })
  ],
  devServer: {
    host: "localhost",
    port: 9000,
    open: true,
    hot: true
  }
});
