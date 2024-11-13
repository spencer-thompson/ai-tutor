const path = require("path");
const dotenv = require("dotenv-webpack");
const CopyWebpackPlugin = require("copy-webpack-plugin");

const commonConfig = {
  entry: {
    background: "./src/background.js",
    content: "./src/content.js",
    // popup: "./src/popup.js",
    // css: "./src/styles.css",
  },
  module: {
    // rules: [
    //   // Add loaders here if needed (e.g., for CSS, images)
    //   {
    //     test: /\.css$/,
    //     use: ["style-loader", "css-loader"],
    //   },
    // ],
  },
  plugins: [
    new dotenv(),
    new CopyWebpackPlugin({
      patterns: [
        { from: "./src/styles.css", to: "./styles.css" },
        { from: "./src/sidepanel.html", to: "./sidepanel.html" },
      ],
    }),
  ],
};

const chromeConfig = {
  ...commonConfig,
  output: {
    path: path.resolve(__dirname, "chrome"),
    filename: "[name].bundle.js",
  },
};

const firefoxConfig = {
  ...commonConfig,
  output: {
    path: path.resolve(__dirname, "firefox"),
    filename: "[name].bundle.js",
  },
};

module.exports = [chromeConfig, firefoxConfig];
