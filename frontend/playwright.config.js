// playwright.config.js
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './e2e', // Only look for tests in the e2e directory
  use: {
    baseURL: 'http://localhost:3000', // Adjust the base URL as needed
    headless: true,
  },
});