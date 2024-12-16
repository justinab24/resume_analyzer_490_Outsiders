module.exports = {
    setupFilesAfterEnv: ['/src/setupTests.js'],
    moduleNameMapper: {
      '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    },
    testEnvironment: 'jsdom',
    transform: {
      '^.+\\.(js|jsx)$': 'babel-jest',
    },
    transformIgnorePatterns: [
      '/node_modules/(?!reactjs-popup)',
      '/node_modules/(?!axios|react-router-dom)',
    ],
  };