const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const config = require('./zrc')

console.log(config.mode)

const mainConfig = {

    // mode: config.mode,
    mode: "production",
    // mode: "development",
    entry: './src/index.js',
    devtool: 'inline-source-map',
    target: 'web',
    output: {
        filename: "app.js",
        path: path.resolve('../FlaskApp/static/react')
    },
    module: {
        rules: [{
            test: /\.js$/,
            exclude: /node_modules/,
            use: {
                loader: 'babel-loader',
                options: {
                    presets: [[
                        '@babel/preset-env', {
                            targets: {
                                esmodules: true
                            }
                        }],
                        '@babel/preset-react'],
                    plugins: ['babel-plugin-styled-components']

                }
            }
        },
            {
                test: /\.css$/i,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.ttf$/i,
                type: "asset/resource"
            },
            {
                test: /\.(png|jpeg|gif|svg)$/i,
                type: "asset/resource"
            }]
    },
    resolve: {
        extensions: ['.js']
    },
    plugins : [
        new CopyWebpackPlugin({
            patterns : [
                {from : "public/index.html", to : "index.html"},
            ],
        }),
    ],
}

module.exports = [mainConfig,]