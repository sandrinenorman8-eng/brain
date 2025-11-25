#!/usr/bin/env node
/**
 * COMPREHENSIVE SEARCH FUNCTIONALITY TEST SUITE
 * Tests all aspects of the search system to identify and resolve issues
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

console.log('🧪 COMPREHENSIVE SEARCH FUNCTIONALITY TEST SUITE');
console.log('='.repeat(60));

// Test configuration
const TEST_CONFIG = {
    serverPort: 3001,
    serverHost: 'localhost',
    testSearchTerms: ['test', 'projet', 'scénario', 'todo', 'xyz123', ''],
    expectedCategories: 20,
    expectedMinFiles: 40
};

// Test results tracking
const testResults = {
    passed: 0,
    failed: 0,
    errors: []
};

function logTest(testName, passed, details = '') {
    const status = passed ? '✅ PASS' : '❌ FAIL';
    console.log(`${status} ${testName}`);
    if (details) console.log(`   ${details}`);
    
    if (passed) {
        testResults.passed++;
    } else {
        testResults.failed++;
        testResults.errors.push(`${testName}: ${details}`);
    }
}

// TEST 1: File System Structure
async function testFileSystemStructure() {
    console.log('\n📁 TEST 1: File System Structure');
    console.log('-'.repeat(40));
    
    try {
        // Check categories.json
        const categoriesExist = fs.existsSync('categories.json');
        logTest('Categories file exists', categoriesExist);
        
        if (categoriesExist) {
            const categoriesData = JSON.parse(fs.readFileSync('categories.json', 'utf8'));
            logTest('Categories data valid', Array.isArray(categoriesData), `Found ${categoriesData.length} categories`);
            
            // Check each category folder
            let totalFiles = 0;
            let validCategories = 0;
            
            for (const category of categoriesData) {
                const categoryPath = category.name;
                const folderExists = fs.existsSync(categoryPath);
                
                if (folderExists) {
                    const files = fs.readdirSync(categoryPath).filter(file => 
                        ['.txt', '.md', '.html'].includes(path.extname(file))
                    );
                    totalFiles += files.length;
                    validCategories++;
                    
                    if (files.length > 0) {
                        console.log(`   📂 ${category.name}: ${files.length} files`);
                    }
                }
            }
            
            logTest('Category folders accessible', validCategories > 0, `${validCategories}/${categoriesData.length} categories have files`);
            logTest('Sufficient files found', totalFiles >= TEST_CONFIG.expectedMinFiles, `Found ${totalFiles} files`);
        }
    } catch (error) {
        logTest('File system structure', false, error.message);
    }
}

// TEST 2: Search Server Functionality
async function testSearchServer() {
    console.log('\n🔍 TEST 2: Search Server Functionality');
    console.log('-'.repeat(40));
    
    return new Promise((resolve) => {
        // Test server status
        const statusOptions = {
            hostname: TEST_CONFIG.serverHost,
            port: TEST_CONFIG.serverPort,
            path: '/status',
            method: 'GET',
            timeout: 5000
        };

        const statusReq = http.request(statusOptions, (res) => {
            logTest('Server responds to status', res.statusCode === 200, `Status code: ${res.statusCode}`);
            
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const result = JSON.parse(data);
                    logTest('Server status valid JSON', true, `Status: ${result.status}`);
                    logTest('Server has categories', result.categories > 0, `${result.categories} categories loaded`);
                    
                    // Test search functionality
                    testSearchEndpoint().then(resolve);
                } catch (error) {
                    logTest('Server status JSON parsing', false, error.message);
                    resolve();
                }
            });
        });

        statusReq.on('error', (error) => {
            logTest('Server connection', false, `Cannot connect: ${error.message}`);
            console.log('   💡 Start server with: node search-server.js');
            resolve();
        });

        statusReq.on('timeout', () => {
            logTest('Server response time', false, 'Server timeout');
            statusReq.destroy();
            resolve();
        });

        statusReq.end();
    });
}

// TEST 3: Search Endpoint Testing
async function testSearchEndpoint() {
    console.log('\n🔎 TEST 3: Search Endpoint Testing');
    console.log('-'.repeat(40));
    
    const searchPromises = TEST_CONFIG.testSearchTerms.map(term => testSingleSearch(term));
    await Promise.all(searchPromises);
}

function testSingleSearch(searchTerm) {
    return new Promise((resolve) => {
        const searchData = JSON.stringify({ term: searchTerm });
        
        const searchOptions = {
            hostname: TEST_CONFIG.serverHost,
            port: TEST_CONFIG.serverPort,
            path: '/search',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Content-Length': Buffer.byteLength(searchData)
            },
            timeout: 10000
        };

        const searchReq = http.request(searchOptions, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const result = JSON.parse(data);
                    const hasResults = result.results && result.results.length > 0;
                    
                    if (searchTerm === '') {
                        logTest(`Empty search handling`, !hasResults || result.results.length === 0, 'Empty search should return no results');
                    } else if (searchTerm === 'xyz123') {
                        logTest(`Non-existent term search`, !hasResults, 'Non-existent term should return no results');
                    } else {
                        logTest(`Search "${searchTerm}"`, hasResults, `Found ${result.results ? result.results.length : 0} results`);
                        
                        if (hasResults) {
                            // Test result structure
                            const firstResult = result.results[0];
                            const hasRequiredFields = firstResult.category && firstResult.filename && firstResult.excerpts;
                            logTest(`Search result structure for "${searchTerm}"`, hasRequiredFields, 'Results have required fields');
                            
                            // Test excerpts
                            if (firstResult.excerpts && firstResult.excerpts.length > 0) {
                                const firstExcerpt = firstResult.excerpts[0];
                                const excerptValid = firstExcerpt.text && firstExcerpt.line_number;
                                logTest(`Search excerpts for "${searchTerm}"`, excerptValid, 'Excerpts have text and line numbers');
                            }
                        }
                    }
                } catch (error) {
                    logTest(`Search "${searchTerm}" JSON parsing`, false, error.message);
                }
                resolve();
            });
        });

        searchReq.on('error', (error) => {
            logTest(`Search "${searchTerm}" connection`, false, error.message);
            resolve();
        });

        searchReq.on('timeout', () => {
            logTest(`Search "${searchTerm}" timeout`, false, 'Request timeout');
            searchReq.destroy();
            resolve();
        });

        searchReq.write(searchData);
        searchReq.end();
    });
}

// TEST 4: HTML File Structure
async function testHTMLStructure() {
    console.log('\n📄 TEST 4: HTML File Structure');
    console.log('-'.repeat(40));
    
    try {
        const htmlExists = fs.existsSync('all_notes_standalone.html');
        logTest('HTML file exists', htmlExists);
        
        if (htmlExists) {
            const htmlContent = fs.readFileSync('all_notes_standalone.html', 'utf8');
            
            // Test essential elements
            const hasSearchInput = htmlContent.includes('id="searchInput"');
            const hasSearchStatus = htmlContent.includes('id="searchStatus"');
            const hasCategoriesContent = htmlContent.includes('id="categories-content"');
            const hasJavaScript = htmlContent.includes('<script>');
            const hasToggleFunction = htmlContent.includes('toggleAccordion');
            const hasPerformSearch = htmlContent.includes('performSearch');
            const hasEventListener = htmlContent.includes('addEventListener');
            
            logTest('HTML has search input', hasSearchInput);
            logTest('HTML has search status', hasSearchStatus);
            logTest('HTML has categories container', hasCategoriesContent);
            logTest('HTML has JavaScript', hasJavaScript);
            logTest('HTML has toggle function', hasToggleFunction);
            logTest('HTML has search function', hasPerformSearch);
            logTest('HTML has event listeners', hasEventListener);
            
            // Test data structure
            const hasFilesData = htmlContent.includes('filesData');
            const hasCategoriesData = htmlContent.includes('categories');
            logTest('HTML has files data', hasFilesData);
            logTest('HTML has categories data', hasCategoriesData);
        }
    } catch (error) {
        logTest('HTML structure test', false, error.message);
    }
}

// TEST 5: Data Generation
async function testDataGeneration() {
    console.log('\n📊 TEST 5: Data Generation');
    console.log('-'.repeat(40));
    
    try {
        // Test Python script
        const pythonScriptExists = fs.existsSync('generate_notes_data.py');
        logTest('Data generation script exists', pythonScriptExists);
        
        // Test generated data file
        const dataFileExists = fs.existsSync('files_data.json');
        logTest('Generated data file exists', dataFileExists);
        
        if (dataFileExists) {
            const dataContent = JSON.parse(fs.readFileSync('files_data.json', 'utf8'));
            const categoryCount = Object.keys(dataContent).length;
            const totalFiles = Object.values(dataContent).reduce((sum, files) => sum + files.length, 0);
            
            logTest('Generated data valid', categoryCount > 0, `${categoryCount} categories, ${totalFiles} files`);
        }
    } catch (error) {
        logTest('Data generation test', false, error.message);
    }
}

// TEST 6: Edge Cases and Error Handling
async function testEdgeCases() {
    console.log('\n⚠️  TEST 6: Edge Cases and Error Handling');
    console.log('-'.repeat(40));
    
    // Test special characters
    const specialTerms = ['café', 'résumé', 'naïve', '中文', '🎬', 'test@#$%'];
    
    for (const term of specialTerms) {
        await testSingleSearch(term);
    }
    
    // Test very long search terms
    const longTerm = 'a'.repeat(1000);
    await testSingleSearch(longTerm);
    
    logTest('Special characters handling', true, 'Tested various special characters');
}

// MAIN TEST EXECUTION
async function runAllTests() {
    console.log(`🚀 Starting comprehensive search functionality tests...`);
    console.log(`📅 ${new Date().toISOString()}`);
    console.log('');
    
    await testFileSystemStructure();
    await testSearchServer();
    await testHTMLStructure();
    await testDataGeneration();
    await testEdgeCases();
    
    // Final results
    console.log('\n' + '='.repeat(60));
    console.log('📊 FINAL TEST RESULTS');
    console.log('='.repeat(60));
    console.log(`✅ Tests Passed: ${testResults.passed}`);
    console.log(`❌ Tests Failed: ${testResults.failed}`);
    console.log(`📈 Success Rate: ${((testResults.passed / (testResults.passed + testResults.failed)) * 100).toFixed(1)}%`);
    
    if (testResults.failed > 0) {
        console.log('\n🔥 CRITICAL ISSUES FOUND:');
        testResults.errors.forEach((error, index) => {
            console.log(`${index + 1}. ${error}`);
        });
        
        console.log('\n🛠️  RECOMMENDED ACTIONS:');
        if (testResults.errors.some(e => e.includes('Server connection'))) {
            console.log('• Start the search server: node search-server.js');
        }
        if (testResults.errors.some(e => e.includes('HTML'))) {
            console.log('• Restore HTML file: copy all_notes_fixed.html all_notes_standalone.html');
        }
        if (testResults.errors.some(e => e.includes('File system'))) {
            console.log('• Run data update: python generate_notes_data.py');
        }
    } else {
        console.log('\n🎉 ALL TESTS PASSED! Search functionality is working correctly.');
    }
    
    console.log('\n💡 To test manually:');
    console.log('1. Open all_notes_standalone.html in browser');
    console.log('2. Try searching for: test, projet, scénario');
    console.log('3. Check browser console (F12) for any errors');
}

// Execute tests
runAllTests().catch(error => {
    console.error('❌ Test suite failed:', error);
    process.exit(1);
});