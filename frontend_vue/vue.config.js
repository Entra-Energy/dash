module.exports = {
    publicPath: '/',
    transpileDependencies: [
      'v-calendar',
      'vue3-pdf',
      '@fawmi/vue-google-maps'
    ],
    configureWebpack: {
      optimization: {
        splitChunks: {
            chunks: 'async',
            minSize: 150000,
            maxSize: 300000
        }
      }
    }
    //...
  };