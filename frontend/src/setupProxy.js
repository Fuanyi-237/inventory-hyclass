const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  app.use(
    ['/api', '/uploads'],
    createProxyMiddleware({
      target: 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
      ws: false,
      logLevel: 'silent',
    })
  );
};
