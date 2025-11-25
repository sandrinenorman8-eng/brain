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

async function testFusionIA() {
  console.log('Creating Browserbase session...');
  const session = await createSession();
  console.log('Session:', session.id);
  console.log('View: https://www.browserbase.com/sessions/' + session.id);

  const browser = await chromium.connectOverCDP(session.connectUrl);
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  try {
    console.log('\n=== TEST FUSION IA - SERVEUR REDÉMARRÉ ===\n');
    
    console.log('1. Navigation vers ngrok...');
    await page.goto(NGROK_URL, { waitUntil: 'networkidle', timeout: 30000 });
    
    console.log('2. Bypass ngrok...');
    await page.click('button:has-text("Visit Site")');
    await page.waitForLoadState('networkidle');
    
    console.log('3. Clic sur Fusion IA...');
    await page.click('button:has-text("Fusion IA")');
    await page.waitForTimeout(2000);
    
    const pages = context.pages();
    const fusionPage = pages[pages.length - 1];
    await fusionPage.waitForLoadState('networkidle');
    
    console.log('\n4. Test API /ai/test...');
    const apiTest = await fusionPage.evaluate(async () => {
      const res = await fetch('/ai/test');
      return { status: res.status, data: await res.json() };
    });
    console.log('   Status:', apiTest.status);
    console.log('   Data:', JSON.stringify(apiTest.data, null, 2));
    
    console.log('\n5. Test API /ai/list_fusions...');
    const fusionsList = await fusionPage.evaluate(async () => {
      const res = await fetch('/ai/list_fusions');
      return { status: res.status, data: await res.json() };
    });
    console.log('   Status:', fusionsList.status);
    console.log('   Fusions:', fusionsList.data.data?.fusions?.length || 0);
    
    if (fusionsList.data.data?.fusions) {
      fusionsList.data.data.fusions.forEach((f, i) => {
        console.log(`   ${i+1}. ${f.display_name}`);
        console.log(`      Path: ${f.path}`);
      });
    }
    
    console.log('\n6. Vérification de l\'affichage...');
    await fusionPage.waitForTimeout(2000);
    await fusionPage.screenshot({ path: 'fusion_ia_after_restart.png', fullPage: true });
    
    const noFusionMsg = await fusionPage.locator('text=/aucune fusion/i').count();
    console.log('   Message "Aucune fusion":', noFusionMsg > 0 ? 'OUI ❌' : 'NON ✅');
    
    const fusionCards = await fusionPage.locator('[class*="fusion"], [data-fusion]').count();
    console.log('   Cartes de fusion visibles:', fusionCards);
    
    console.log('\n=== RÉSULTAT ===');
    if (apiTest.status === 200 && fusionsList.status === 200 && fusionsList.data.data?.fusions?.length > 0) {
      console.log('✅ API fonctionne');
      console.log('✅ Fusions détectées:', fusionsList.data.data.fusions.length);
      if (noFusionMsg > 0) {
        console.log('❌ PROBLÈME: Fusions détectées par API mais pas affichées dans l\'interface');
      } else {
        console.log('✅ Interface affiche les fusions');
      }
    } else {
      console.log('❌ Problème API ou aucune fusion');
    }
    
    console.log('\nSession replay:', `https://www.browserbase.com/sessions/${session.id}`);
    
  } catch (error) {
    console.error('\n=== ERREUR ===');
    console.error(error.message);
    await page.screenshot({ path: 'fusion_ia_error.png' });
  } finally {
    await browser.close();
  }
}

testFusionIA().catch(console.error);
