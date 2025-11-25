const { chromium } = require('playwright');

async function test() {
  const browser = await chromium.connectOverCDP(
    `wss://connect.browserbase.com?apiKey=bb_live_-Q2jqMd3m0I3A3yV7BrCKvl1xAs&projectId=bee5922c-e094-40c2-8279-fe176da275dc`
  );

  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  try {
    console.log('Navigating to ngrok URL...');
    await page.goto('https://volitionary-prince-springily.ngrok-free.dev', {
      waitUntil: 'networkidle'
    });
    
    console.log('Current URL:', page.url());
    
    console.log('Taking screenshot 1...');
    await page.screenshot({ path: 'bb_step1_ngrok_warning.png' });
    
    console.log('Clicking Visit Site button...');
    await page.click('button:has-text("Visit Site")');
    
    await page.waitForLoadState('networkidle');
    console.log('After click URL:', page.url());
    
    console.log('Taking screenshot 2...');
    await page.screenshot({ path: 'bb_step2_after_click.png' });
    
    console.log('Extracting page title...');
    const title = await page.title();
    console.log('Page title:', title);
    
    console.log('SUCCESS - Session URL: https://www.browserbase.com/sessions/');
    
  } catch (error) {
    console.error('ERROR:', error.message);
    await page.screenshot({ path: 'bb_error.png' });
  } finally {
    await browser.close();
  }
}

test();
