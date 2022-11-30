const host = {
  localhost: "http://192.168.5.2:5000/",
  production: "http://www.twibo.icu/",
};

module.exports = {
  publicPath: "/",
  outputDir: "../twibo_server/dist",
  pages: {
    index: {
      entry: "src/pages/fake/main.js",
      template: "public/index.html",
      filename: "index.html",
    },
    twibo: {
      entry: "src/pages/twibo/main.js",
      template: "public/twibo.html",
      filename: "twibo.html",
    },
  },
  assetsDir: "assets",
  filenameHashing: false,
  lintOnSave: true,

  productionSourceMap: false,

  // 它支持webPack-dev-server的所有选项
  devServer: {
    host: "0.0.0.0",
    port: 8080, // 端口号
    https: false, // https:{type:Boolean}

    // 配置多个代理
    proxy: {
      "/api": {
        target: host.localhost,
        ws: true, // 是否启用websockets
        changeOrigin: true, //开启代理：在本地会创建一个虚拟服务端，然后发送请求的数据，并同时接收请求的数据，这样服务端和服务端进行数据的交互就不会有跨域问题
        // pathRewrite: {
        //   "^/api": "", //这里理解成用'/api'代替target里面的地址,比如我要调用'http://40.00.100.100:3002/user/add'，直接写'/api/user/add'即可
        // },
      },
    },
  },
};
