#!/usr/bin/env node
/**
 * Test specific pour le mot "dans"
 * Ce test vérifie que la recherche de contenu fonctionne avec un mot français commun
 */

const http = require('http');

console.log('🔍 TEST SPÉCIFIQUE: Recherche du mot "dans"');
console.log('='.repeat(50));

async function testSearchWord(word) {
    return new Promise((resolve) => {
        const searchData = JSON.stringify({ term: word });
        
        const options = {
            hostname: 'localhost',
            port: 3001,
            path: '/search',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Content-Length': Buffer.byteLength(searchData)
            },
            timeout: 10000
        };

        console.log(`🔎 Recherche pour: "${word}"`);
        
        const req = http.request(options, (res) => {
            let data = '';
            
            res.on('data', chunk => {
                data += chunk;
            });
            
            res.on('end', () => {
                try {
                    const result = JSON.parse(data);
                    
                    console.log(`📊 Statut de la réponse: ${res.statusCode}`);
                    console.log(`📈 Nombre de résultats: ${result.results ? result.results.length : 0}`);
                    
                    if (result.results && result.results.length > 0) {
                        console.log('\n📄 RÉSULTATS DÉTAILLÉS:');
                        console.log('-'.repeat(40));
                        
                        result.results.forEach((fileResult, index) => {
                            console.log(`\n${index + 1}. 📁 ${fileResult.category}/${fileResult.filename}`);
                            console.log(`   📅 Date: ${fileResult.date}`);
                            console.log(`   🔢 Correspondances: ${fileResult.match_count}`);
                            
                            if (fileResult.excerpts && fileResult.excerpts.length > 0) {
                                console.log('   📝 Extraits:');
                                fileResult.excerpts.forEach((excerpt, excerptIndex) => {
                                    console.log(`      ${excerptIndex + 1}. Ligne ${excerpt.line_number}: "${excerpt.text.substring(0, 100)}${excerpt.text.length > 100 ? '...' : ''}"`);
                                });
                            }
                        });
                        
                        console.log('\n✅ SUCCÈS: La recherche de contenu fonctionne parfaitement!');
                        console.log(`🎯 Le mot "${word}" a été trouvé dans ${result.results.length} fichier(s)`);
                        
                    } else {
                        console.log(`⚠️  Aucun résultat trouvé pour "${word}"`);
                        console.log('💡 Cela peut signifier que le mot n\'existe pas dans les fichiers');
                    }
                    
                } catch (error) {
                    console.error('❌ Erreur lors du parsing JSON:', error.message);
                    console.log('📄 Réponse brute:', data);
                }
                
                resolve();
            });
        });

        req.on('error', (error) => {
            console.error('❌ Erreur de connexion:', error.message);
            console.log('💡 Assurez-vous que le serveur est démarré avec: node search-server.js');
            resolve();
        });

        req.on('timeout', () => {
            console.error('❌ Timeout de la requête');
            req.destroy();
            resolve();
        });

        req.write(searchData);
        req.end();
    });
}

// Test principal
async function runTest() {
    console.log('🚀 Démarrage du test...\n');
    
    // Test du serveur d'abord
    console.log('1️⃣ Vérification du serveur...');
    const statusOptions = {
        hostname: 'localhost',
        port: 3001,
        path: '/status',
        method: 'GET'
    };

    const statusReq = http.request(statusOptions, (res) => {
        if (res.statusCode === 200) {
            console.log('✅ Serveur actif\n');
            
            // Maintenant tester la recherche
            console.log('2️⃣ Test de recherche...');
            testSearchWord('dans').then(() => {
                console.log('\n' + '='.repeat(50));
                console.log('🏁 Test terminé');
            });
        } else {
            console.log(`❌ Serveur répond avec erreur: ${res.statusCode}`);
        }
    });

    statusReq.on('error', (error) => {
        console.log('❌ Serveur non accessible:', error.message);
        console.log('💡 Démarrez le serveur avec: node search-server.js');
    });

    statusReq.end();
}

runTest();