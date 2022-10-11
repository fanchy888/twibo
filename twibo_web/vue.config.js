const localhost = "http://192.168.5.2:5000/";
const prod = "http://101.42.236.38/";
module.exports = {
  publicPath: "/dist",

  // outputDir: 在npm run build 或 yarn build 时 ，生成文件的目录名称（要和baseUrl的生产环境路径一致）
  outputDir: "../twibo_server/dist",

  assetsDir: "assets",
  filenameHashing: false,
  lintOnSave: true,

  productionSourceMap: false,
  pwa: {
    iconPaths: {},
  },
  // 它支持webPack-dev-server的所有选项
  devServer: {
    host: "0.0.0.0",
    port: 8080, // 端口号
    https: false, // https:{type:Boolean}
    // open: true, //配置自动启动浏览器
    // proxy: 'http://localhost:4000' // 配置跨域处理,只有一个代理

    // 配置多个代理
    proxy: {
      "/api": {
        target: localhost, // http://101.42.236.38/
        ws: true, // 是否启用websockets
        changeOrigin: true, //开启代理：在本地会创建一个虚拟服务端，然后发送请求的数据，并同时接收请求的数据，这样服务端和服务端进行数据的交互就不会有跨域问题
        // pathRewrite: {
        //   "^/api": "", //这里理解成用'/api'代替target里面的地址,比如我要调用'http://40.00.100.100:3002/user/add'，直接写'/api/user/add'即可
        // },
      },
      // "/socket.io": {
      //   target: "http://101.42.236.38/twibo", // 要访问的接口域名
      //   ws: true, // 是否启用websockets
      //   changeOrigin: true,
      // },
    },
  },
};
