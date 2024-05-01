// const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],

  productionSourceMap: false,

  configureWebpack: {
    //plugins: [new BundleAnalyzerPlugin()],
    //mode: 'production',
    resolve:{
      alias: {
        'moment': 'moment/src/moment',

      }
    }
  },

  // publicPath: '/static/yt_dashboard/',
  publicPath: process.env.NODE_ENV === 'production'
    ? 'https://cdn.yourtickets.nl/yt_dashboard/'
    : '/',
    // : 'https://cdn.yourtickets.nl/yt_dashboard/', // was '/'

  outputDir: 'static/yt_dashboard/',

  //assetDir: '', //relative to outputdir
  //relative to outputdir
  indexPath: '../../templates/yt_dashboard/index.html',

  // css: {
  //   loaderOptions: {
  //       scss: {
  //           prependData: '@import "~@/scss/override.scss";'
  //       }
  //   }
  // }
  devServer: {
      proxy: {
          "**": {
            target: "http://localhost:8000",
            ws: true,
            changeOrigin: true
          }
        }
  },

  pluginOptions: {
    i18n: {
      locale: 'en',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: true,
      enableBridge: false
    }
  }
}
