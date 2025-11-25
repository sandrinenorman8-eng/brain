const https = require('https');
const { chromium } = require('playwright');

const API_KEY = 'bb_live_-Q2jqMd3m0I3A3yV7BrCKvl1xAs';
const PROJECT_ID = 'bee5922c-e094-40c2-8279-fe176da275dc';

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

async function debug() {
  console.log('=== DEBUG FUSION PAGE ===\n');
  
  const session = await createSession();
  console.log('Session:', session.id);

  const browser = await chromium.connectOverCDP(session.connectUrl);
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  const consoleLogs = [];
  page.on('console', msg => consoleLogs.push(`[${msg.type()}] ${msg.text()}`));

  try {
    await page.goto('https://volitionary-prince-springily.ngrok-free.dev', { waitUntil: 'networkidle' });
    await page.click('button:has-text("Visit Site")');
    await page.waitForLoadState('networkidle');
    await page.click('button:has-text("Fusion IA")');
    await page.waitForTimeout(2000);
    
    const pages = context.pages();
    const fusionPage = pages[pages.length - 1];
    await fusionPage.waitForLoadState('networkidle');
    await fusionPage.waitForTimeout(3000);
    
    console.log('\n1. LOGS CONSOLE:');
    consoleLogs.forEach(log => console.log('  ', log));
    
    console.log('\n2. ÉTAT DES ÉLÉMENTS:');
    const state = await fusionPage.evaluate(() => {
      return {
        noFusions: {
          exists: !!document.getElementById('noFusions'),
          display: document.getElementById('noFusions')?.style.display,
          computedDisplay: document.getElementById('noFusions') ? window.getComputedStyle(document.getElementById('noFusions')).display : null,
          visible: document.getElementById('noFusions')?.offsetParent !== null
        },
        fusionsList: {
          exists: !!document.getElementById('fusionsList'),
          childCount: document.getElementById('fusionsList')?.children.length || 0
        }
      };
    });
    console.log(JSON.stringify(state, null, 2));
    
    console.log('\n3. TEST API DIRECT:');
    const apiResponse = await fusionPage.evaluate(async () => {
      const res = await fetch('/ai/list_fusions?t=' + Date.now());
      return {
        status: res.status,
        data: await res.json()
      };
    });
    console.log('  Status:', apiResponse.status);
    console.log('  Fusions:', apiResponse.data.data?.fusions?.length || 0);
    
    console.log('\n4. VÉRIFICATION JAVASCRIPT:');
    const jsCheck = await fusionPage.evaluate(() => {
      return {
        loadFusionsExists: typeof loadFusions === 'function',
        displayFusionsExists: typeof displayFusions === 'function',
        DOMContentLoadedFired: document.readyState
      };
    });
    console.log(JSON.stringify(jsCheck, null, 2));
    
    await fusionPage.screenshot({ path: 'debug_fusion_final.png', fullPage: true });
    console.log('\nScreenshot: debug_fusion_final.png');
    console.log('Session:', `https://www.browserbase.com/sessions/${session.id}`);
    
  } catch (error) {
    console.error('Erreur:', error.message);
  } finally {
    await browser.close();
  }
}

debug().catch(console.error);
