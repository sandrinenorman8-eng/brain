// Test rapide du serveur de recherche
const http = require('http');

console.log('🧪 Test du serveur de recherche');

// Test 1: Vérifier le statut
const statusOptions = {
    hostname: 'localhost',
    port: 3001,
    path: '/status',
    method: 'GET',
    headers: {
        'Accept': 'application/json'
    }
};

const statusReq = http.request(statusOptions, (res) => {
    console.log(`✅ Statut: ${res.statusCode}`);
    
    let data = '';
    res.on('data', (chunk) => {
        data += chunk;
    });
    
    res.on('end', () => {
        try {
            const result = JSON.parse(data);
            console.log('📊 Réponse statut:', result);
            
            // Test 2: Recherche
            testSearch();
        } catch (error) {
            console.error('❌ Erreur parsing statut:', error);
        }
    });
});

statusReq.on('error', (error) => {
    console.error('❌ Erreur connexion statut:', error.message);
});

statusReq.end();

function testSearch() {
    const searchData = JSON.stringify({ term: 'test' });
    
    const searchOptions = {
        hostname: 'localhost',
        port: 3001,
        path: '/search',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Content-Length': Buffer.byteLength(searchData)
        }
    };

    const searchReq = http.request(searchOptions, (res) => {
        console.log(`✅ Recherche: ${res.statusCode}`);
        
        let data = '';
        res.on('data', (chunk) => {
            data += chunk;
        });
        
        res.on('end', () => {
            try {
                const result = JSON.parse(data);
                console.log('🔍 Résultats recherche:', result);
                console.log(`📊 ${result.results ? result.results.length : 0} résultats trouvés`);
            } catch (error) {
                console.error('❌ Erreur parsing recherche:', error);
            }
        });
    });

    searchReq.on('error', (error) => {
        console.error('❌ Erreur connexion recherche:', error.message);
    });

    searchReq.write(searchData);
    searchReq.end();
}