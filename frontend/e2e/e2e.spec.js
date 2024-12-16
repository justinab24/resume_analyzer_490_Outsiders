const { test, expect } = require('@playwright/test');
const path = require('path');

let validToken;

test.describe('End-to-End Tests', () => {
    test.beforeAll(async ({ browser }) => {
        const page = await browser.newPage();
        await page.goto('http://host.docker.internal:3000/register');
        await page.fill('input[placeholder="Email"]', 'test@example.com');
        await page.fill('input[placeholder="Username"]', 'testuser');
        await page.fill('input[placeholder="Password"]', 'password');
        await page.click('button:has-text("Sign Up")');
        await page.waitForURL('http://host.docker.internal:3000/dashboard');
        validToken = await page.evaluate(() => localStorage.getItem('token'));
        await page.close();
    });

    test.beforeEach(async ({ page }) => {
        // Set the valid token in localStorage before each test
        await page.goto('http://host.docker.internal:3000');
        await page.evaluate((token) => {
            localStorage.setItem('token', token);
        }, validToken);
    });

    test('User Registration', async ({ page }) => {
        await page.goto('http://host.docker.internal:3000/register');
        await page.fill('input[placeholder="Email"]', 'newuser@example.com');
        await page.fill('input[placeholder="Username"]', 'newuser');
        await page.fill('input[placeholder="Password"]', 'password');
        await page.click('button:has-text("Sign Up")');
        await expect(page).toHaveURL('http://host.docker.internal:3000/dashboard');
    });

    test('User Login', async ({ page }) => {
        await page.goto('http://host.docker.internal:3000/login');
        await page.fill('input[placeholder="Email"]', 'test@example.com');
        await page.fill('input[placeholder="Password"]', 'password');
        await page.click('button:has-text("Login")');
        await expect(page).toHaveURL('http://host.docker.internal:3000/dashboard');
    });

    test('Resume Upload and Job Description Submission', async ({ page }) => {
        await page.goto('http://host.docker.internal:3000/dashboard');
        await expect(page).toHaveURL('http://host.docker.internal:3000/dashboard');
        const resumePath = path.resolve(__dirname, 'valid_resume.pdf');
        await page.setInputFiles('input[type="file"]', resumePath);
        await page.waitForSelector('#jobDescription');
        await page.fill('#jobDescription', 'Job description text');
        await page.click('button:has-text("Submit")');
    });

    test('Fit Score and Feedback Display', async ({ page }) => {
        await page.goto('http://host.docker.internal:3000/dashboard');
        const resumePath = path.resolve(__dirname, 'valid_resume.pdf');
        await page.setInputFiles('input[type="file"]', resumePath);
        await page.fill('#jobDescription', 'Job description text');
        await page.click('button:has-text("Submit")');
        await page.waitForSelector('#pieChart', { timeout: 60000 }); // Wait for 6000ms (6 seconds)
    });

    test('Report Download', async ({ page }) => {
        await page.goto('http://host.docker.internal:3000/dashboard');
        const resumePath = path.resolve(__dirname, 'valid_resume.pdf');
        await page.setInputFiles('input[type="file"]', resumePath);
        await page.fill('#jobDescription', 'Job description text');
        await page.click('button:has-text("Submit")');
        await page.click('button:has-text("Download PDF Report")');
        const [download] = await Promise.all([
            page.waitForEvent('download'),
            page.click('button:has-text("Download PDF Report")'),
        ]);
        const downloadPath = await download.path();
        expect(downloadPath).toBeTruthy();
    });

    test('Invalid File Type Upload', async ({ page }) => {
        await page.goto('http://host.docker.internal:3000/dashboard');
        const invalidResumePath = path.resolve(__dirname, 'invalid_resume.txt');
        await page.setInputFiles('input[type="file"]', invalidResumePath);
        await page.click('button:has-text("Submit")');
        await expect(page.locator('text=Only PDF and DOCX files are allowed')).toBeVisible();
    });

    test('Oversized File Upload', async ({ page }) => {
        await page.goto('http://host.docker.internal:3000/dashboard');
        const largeResumePath = path.resolve(__dirname, 'large_resume.pdf');
        await page.setInputFiles('input[type="file"]', largeResumePath);
        await page.click('button:has-text("Submit")');
        const resumeError = await page.evaluate(() => window.resumeError);
        expect(resumeError).not.toBeNull();
    });

    test('Unauthorized Access to Dashboard', async ({ page }) => {
        await page.goto('http://host.docker.internal:3000');
        await page.evaluate(() => localStorage.clear());
        await page.goto('http://host.docker.internal:3000/dashboard');
        await expect(page).toHaveURL('http://host.docker.internal:3000/register');
    });
});