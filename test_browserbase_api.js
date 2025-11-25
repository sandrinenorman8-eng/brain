const https = require('https');
const { chromium } = require('playwright');

const API_KEY = 'bb_live_-Q2jqMd3m0I3A3yV7BrCKvl1xAs';
const PROJECT_ID = 'bee5922c-e094-40c2-8279-fe176da275dc';

function createSession() {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      projectId: PROJECT_ID
    });

    const options = {
      hostname: 'www.browserbase.com',
      port: 443,
      path: '/v1/sessions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-bb-api-key': API_KEY,
        'Content-Length': data.length
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        if (res.statusCode === 200 || res.statusCode === 201) {
          resolve(JSON.parse(body));
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${body}`));
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function test() {
  console.log('Creating Browserbase session...');
  const session = await createSession();
  console.log('Session created:', session.id);
  console.log('Session URL:', `https://www.browserbase.com/sessions/${session.id}`);
  console.log('Connect URL:', session.connectUrl);

  const browser = await chromium.connectOverCDP(session.connectUrl);
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  try {
    console.log('\n=== TEST DEUXIEME CERVEAU ===\n');
    
    console.log('1. Navigating to ngrok URL...');
    await page.goto('https://volitionary-prince-springily.ngrok-free.dev', {
      waitUntil: 'networkidle',
      timeout: 30000
    });
    console.log('   Current URL:', page.url());
    
    console.log('\n2. Taking screenshot of ngrok warning...');
    await page.screenshot({ path: 'bb_step1_ngrok_warning.png', fullPage: true });
    console.log('   Screenshot saved: bb_step1_ngrok_warning.png');
    
    console.log('\n3. Clicking "Visit Site" button...');
    await page.click('button:has-text("Visit Site")');
    await page.waitForLoadState('networkidle', { timeout: 30000 });
    console.log('   After click URL:', page.url());
    
    console.log('\n4. Taking screenshot of main app...');
    await page.screenshot({ path: 'bb_step2_main_app.png', fullPage: true });
    console.log('   Screenshot saved: bb_step2_main_app.png');
    
    console.log('\n5. Extracting page info...');
    const title = await page.title();
    console.log('   Page title:', title);
    
    const h1 = await page.textContent('h1').catch(() => 'N/A');
    console.log('   H1 text:', h1);
    
    console.log('\n6. Looking for categories...');
    const categories = await page.$$eval('[class*="category"]', els => 
      els.slice(0, 5).map(el => el.textContent.trim())
    ).catch(() => []);
    console.log('   Categories found:', categories.length);
    if (categories.length > 0) {
      console.log('   First 5:', categories);
    }
    
    console.log('\n=== SUCCESS ===');
    console.log('View session replay:', `https://www.browserbase.com/sessions/${session.id}`);
    
  } catch (error) {
    console.error('\n=== ERROR ===');
    console.error('Message:', error.message);
    await page.screenshot({ path: 'bb_error.png', fullPage: true });
    console.log('Error screenshot saved: bb_error.png');
  } finally {
    await browser.close();
    console.log('\nBrowser closed.');
  }
}

test().catch(console.error);
