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

async function analyzeFusionIA() {
  console.log('Creating Browserbase session...');
  const session = await createSession();
  console.log('Session:', session.id);
  console.log('View: https://www.browserbase.com/sessions/' + session.id);

  const browser = await chromium.connectOverCDP(session.connectUrl);
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  try {
    console.log('\n=== ANALYSE FUSION IA ===\n');
    
    console.log('1. Navigation vers ngrok...');
    await page.goto('https://volitionary-prince-springily.ngrok-free.dev', {
      waitUntil: 'networkidle',
      timeout: 30000
    });
    
    console.log('2. Bypass ngrok warning...');
    await page.click('button:has-text("Visit Site")');
    await page.waitForLoadState('networkidle');
    console.log('   URL:', page.url());
    
    console.log('\n3. Recherche du bouton Fusion IA...');
    const fusionButton = await page.locator('button:has-text("Fusion IA")').first();
    const fusionButtonExists = await fusionButton.count() > 0;
    console.log('   Bouton trouvé:', fusionButtonExists);
    
    if (fusionButtonExists) {
      const buttonText = await fusionButton.textContent();
      console.log('   Texte:', buttonText);
      
      console.log('\n4. Clic sur Fusion IA...');
      await fusionButton.click();
      await page.waitForTimeout(2000);
      
      const pages = context.pages();
      console.log('   Nombre de pages:', pages.length);
      
      let fusionPage = page;
      if (pages.length > 1) {
        fusionPage = pages[pages.length - 1];
        console.log('   Nouvelle page détectée');
      }
      
      await fusionPage.waitForLoadState('networkidle', { timeout: 10000 });
      console.log('   URL Fusion IA:', fusionPage.url());
      
      console.log('\n5. Analyse de la page Fusion IA...');
      await fusionPage.screenshot({ path: 'fusion_ia_page.png', fullPage: true });
      console.log('   Screenshot: fusion_ia_page.png');
      
      const title = await fusionPage.title();
      console.log('   Titre:', title);
      
      const h1 = await fusionPage.locator('h1').first().textContent().catch(() => 'N/A');
      console.log('   H1:', h1);
      
      console.log('\n6. Vérification du statut API...');
      const apiStatus = await fusionPage.locator('text=/API|statut|connexion/i').allTextContents();
      console.log('   Statuts trouvés:', apiStatus.length);
      if (apiStatus.length > 0) {
        console.log('   Premiers statuts:', apiStatus.slice(0, 3));
      }
      
      console.log('\n7. Recherche des fusions disponibles...');
      const fusionCards = await fusionPage.locator('[class*="fusion"], [class*="card"]').count();
      console.log('   Cartes de fusion:', fusionCards);
      
      const noFusionMsg = await fusionPage.locator('text=/aucune fusion/i').count();
      console.log('   Message "Aucune fusion":', noFusionMsg > 0 ? 'OUI' : 'NON');
      
      console.log('\n8. Extraction du contenu complet...');
      const bodyText = await fusionPage.locator('body').textContent();
      const lines = bodyText.split('\n').filter(l => l.trim()).slice(0, 20);
      console.log('   Premières lignes:');
      lines.forEach((line, i) => console.log(`   ${i+1}. ${line.trim().substring(0, 80)}`));
      
      console.log('\n9. Vérification des erreurs console...');
      const consoleLogs = [];
      fusionPage.on('console', msg => {
        consoleLogs.push(`[${msg.type()}] ${msg.text()}`);
      });
      
      await fusionPage.waitForTimeout(2000);
      
      if (consoleLogs.length > 0) {
        console.log('   Logs console:', consoleLogs.length);
        consoleLogs.slice(0, 5).forEach(log => console.log('   ' + log));
      }
      
      console.log('\n10. Test de l\'API /ai/test...');
      const response = await fusionPage.evaluate(async () => {
        try {
          const res = await fetch('/ai/test');
          const data = await res.json();
          return { status: res.status, data };
        } catch (error) {
          return { error: error.message };
        }
      });
      console.log('   Réponse API:', JSON.stringify(response, null, 2));
      
      console.log('\n11. Screenshot final...');
      await fusionPage.screenshot({ path: 'fusion_ia_final.png', fullPage: true });
      console.log('   Screenshot: fusion_ia_final.png');
      
    } else {
      console.log('   ❌ BOUTON FUSION IA NON TROUVÉ');
      await page.screenshot({ path: 'no_fusion_button.png', fullPage: true });
    }
    
    console.log('\n=== ANALYSE TERMINÉE ===');
    console.log('Session replay:', `https://www.browserbase.com/sessions/${session.id}`);
    
  } catch (error) {
    console.error('\n=== ERREUR ===');
    console.error('Message:', error.message);
    console.error('Stack:', error.stack);
    await page.screenshot({ path: 'fusion_ia_error.png', fullPage: true });
  } finally {
    await browser.close();
  }
}

analyzeFusionIA().catch(console.error);
