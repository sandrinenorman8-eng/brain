const https = require('https');
const { chromium } = require('playwright');

const API_KEY = 'bb_live_-Q2jqMd3m0I3A3yV7BrCKvl1xAs';
const PROJECT_ID = 'bee5922c-e094-40c2-8279-fe176da275dc';
const NGROK_URL = 'https://volitionary-prince-springily.ngrok-free.dev';

function createSession() {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({ projectId: PROJECT_ID });
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

async function testConsole() {
  console.log('Creating Browserbase session...');
  const session = await createSession();
  console.log('Session:', session.id);

  const browser = await chromium.connectOverCDP(session.connectUrl);
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  try {
    // Capturer les logs console
    const consoleLogs = [];
    page.on('console', msg => {
      consoleLogs.push(`[${msg.type()}] ${msg.text()}`);
    });

    console.log('\n1. Navigation...');
    await page.goto(NGROK_URL, { waitUntil: 'networkidle' });
    await page.click('button:has-text("Visit Site")');
    await page.waitForLoadState('networkidle');
    
    console.log('2. Clic Fusion IA...');
    await page.click('button:has-text("Fusion IA")');
    await page.waitForTimeout(2000);
    
    const pages = context.pages();
    const fusionPage = pages[pages.length - 1];
    await fusionPage.waitForLoadState('networkidle');
    await fusionPage.waitForTimeout(3000);
    
    console.log('\n3. Logs Console:');
    consoleLogs.forEach(log => console.log('   ' + log));
    
    console.log('\n4. État des éléments:');
    const noFusionsVisible = await fusionPage.evaluate(() => {
      const el = document.getElementById('noFusions');
      return {
        exists: !!el,
        classList: el ? Array.from(el.classList) : [],
        display: el ? window.getComputedStyle(el).display : null,
        visible: el ? el.offsetParent !== null : false
      };
    });
    console.log('   noFusions:', JSON.stringify(noFusionsVisible, null, 2));
    
    const fusionsListContent = await fusionPage.evaluate(() => {
      const el = document.getElementById('fusionsList');
      return {
        exists: !!el,
        childCount: el ? el.children.length : 0,
        innerHTML: el ? el.innerHTML.substring(0, 200) : null
      };
    });
    console.log('   fusionsList:', JSON.stringify(fusionsListContent, null, 2));
    
    await fusionPage.screenshot({ path: 'fusion_debug.png', fullPage: true });
    console.log('\nScreenshot: fusion_debug.png');
    console.log('Session:', `https://www.browserbase.com/sessions/${session.id}`);
    
  } catch (error) {
    console.error('Erreur:', error.message);
  } finally {
    await browser.close();
  }
}

testConsole().catch(console.error);
