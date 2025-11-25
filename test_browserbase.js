const { Stagehand } = require('@browserbasehq/stagehand');

async function test() {
  const stagehand = new Stagehand({
    apiKey: 'bb_live_-Q2jqMd3m0I3A3yV7BrCKvl1xAs',
    projectId: 'bee5922c-e094-40c2-8279-fe176da275dc',
    env: 'BROWSERBASE',
    modelName: 'gemini-2.0-flash-exp',
    modelApiKey: 'AIzaSyBqxLqKdxqJqxqJqxqJqxqJqxqJqxqJqxq',
    verbose: 2,
    debugDom: true
  });

  try {
    console.log('Initializing Stagehand...');
    await stagehand.init();
    
    console.log('Navigating to URL...');
    await stagehand.page.goto('https://volitionary-prince-springily.ngrok-free.dev');
    
    console.log('Current URL:', stagehand.page.url());
    
    console.log('Waiting for page load...');
    await stagehand.page.waitForLoadState('networkidle');
    
    console.log('Taking screenshot...');
    await stagehand.page.screenshot({ path: 'test_ngrok.png' });
    
    console.log('Clicking Visit Site button...');
    await stagehand.page.click('button:has-text("Visit Site")');
    
    await stagehand.page.waitForLoadState('networkidle');
    console.log('After click URL:', stagehand.page.url());
    
    await stagehand.page.screenshot({ path: 'test_after_click.png' });
    
    await stagehand.close();
    console.log('SUCCESS');
  } catch (error) {
    console.error('ERROR:', error.message);
    console.error('Stack:', error.stack);
    await stagehand.close();
  }
}

test();
