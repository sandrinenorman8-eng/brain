const fs = require('fs');
const path = require('path');
const http = require('http');
const url = require('url');

// Configuration
const PORT = 3008;
const SEARCH_EXTENSIONS = ['.txt', '.md', '.html'];

// Load categories
let categories = [];
try {
    console.log('🔍 Chargement des catégories...');
    console.log('📁 Répertoire actuel:', process.cwd());
    const categoriesData = fs.readFileSync('categories.json', 'utf8');
    console.log('📄 Taille du fichier categories.json:', categoriesData.length);
    categories = JSON.parse(categoriesData);
    console.log(`✅ ${categories.length} catégories chargées`);
    categories.forEach(cat => console.log(`  - ${cat.name} (${cat.emoji})`));
} catch (error) {
    console.error('❌ Erreur chargement catégories:', error.message);
    console.error('📁 Répertoire actuel:', process.cwd());
    console.error('🔍 Vérification du fichier:');
    try {
        const stats = fs.statSync('categories.json');
        console.log('📊 Taille:', stats.size);
        console.log('📅 Dernière modification:', stats.mtime);
    } catch (statError) {
        console.error('❌ Impossible d\'accéder au fichier categories.json:', statError.message);
    }
}

async function searchInFile(filePath, searchTerm) {
    try {
        const content = await fs.promises.readFile(filePath, 'utf8');
        const lines = content.split('\n');
        const matches = [];

        lines.forEach((line, index) => {
            const lowerLine = line.toLowerCase();
            const lowerTerm = searchTerm.toLowerCase();

            if (lowerLine.includes(lowerTerm)) {
                const startIndex = Math.max(0, lowerLine.indexOf(lowerTerm) - 50);
                const endIndex = Math.min(line.length, lowerLine.indexOf(lowerTerm) + searchTerm.length + 50);
                let excerpt = line.substring(startIndex, endIndex);

                if (startIndex > 0) excerpt = '...' + excerpt;
                if (endIndex < line.length) excerpt = excerpt + '...';

                matches.push({
                    line_number: index + 1,
                    text: excerpt,
                    match_number: matches.length + 1
                });
            }
        });

        return matches;
    } catch (error) {
        console.error(`❌ Erreur lecture ${filePath}:`, error.message);
        return [];
    }
}

async function searchInCategory(categoryName, searchTerm) {
    const categoryPath = path.join(process.cwd(), 'data', categoryName);
    
    console.log(`🔍 Recherche dans: ${categoryPath}`);

    // Vérifier que le dossier existe
    if (!fs.existsSync(categoryPath)) {
        console.log(`⚠️ Dossier non trouvé: ${categoryPath}`);
        return [];
    }

    const results = [];

    try {
        const files = fs.readdirSync(categoryPath);
        console.log(`📂 ${files.length} fichiers dans ${categoryName}`);

        for (const fileName of files) {
            const filePath = path.join(categoryPath, fileName);
            const fileExt = path.extname(fileName);

            if (SEARCH_EXTENSIONS.includes(fileExt)) {
                const matches = await searchInFile(filePath, searchTerm);

                if (matches.length > 0) {
                    console.log(`✅ ${matches.length} correspondances dans ${fileName}`);
                    
                    const dateMatch = fileName.match(/(\d{4}-\d{2}-\d{2})/);
                    const fileDate = dateMatch ? dateMatch[1] : new Date().toISOString().split('T')[0];

                    results.push({
                        category: categoryName,
                        filename: fileName,
                        date: fileDate,
                        match_count: matches.length,
                        excerpts: matches.slice(0, 3)
                    });
                }
            }
        }
    } catch (error) {
        console.error(`❌ Erreur recherche dans ${categoryName}:`, error.message);
    }

    return results;
}

async function performSearch(searchTerm) {
    console.log(`\n🔍 RECHERCHE: "${searchTerm}"`);
    console.log(`📁 Catégories à scanner: ${categories.length}`);

    if (!searchTerm || searchTerm.length < 2) {
        console.log('⚠️ Terme trop court');
        return { results: [], message: 'Terme de recherche trop court' };
    }

    const allResults = [];
    
    // Recherche séquentielle avec logs détaillés
    for (const category of categories) {
        console.log(`\n📂 Scan de: ${category.name}`);
        const categoryResults = await searchInCategory(category.name, searchTerm);
        allResults.push(...categoryResults);
    }

    console.log(`\n✅ TOTAL: ${allResults.length} résultats trouvés\n`);

    return {
        results: allResults,
        message: `${allResults.length} fichier(s) trouvé(s)`
    };
}

// Serveur HTTP
const server = http.createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    const parsedUrl = url.parse(req.url, true);
    
    if (req.method === 'POST' && parsedUrl.pathname === '/search') {
        let body = '';

        req.on('data', chunk => {
            body += chunk.toString();
        });

        req.on('end', async () => {
            try {
                const { term } = JSON.parse(body);
                console.log(`\n📨 Requête de recherche reçue: "${term}"`);
                
                const searchResults = await performSearch(term);

                res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
                res.end(JSON.stringify(searchResults));
                
                console.log(`📤 Réponse envoyée: ${searchResults.results.length} résultats`);
            } catch (error) {
                console.error('❌ Erreur recherche:', error);
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: error.message }));
            }
        });
    } else if (req.method === 'GET' && parsedUrl.pathname === '/status') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ 
            status: 'running', 
            categories: categories.length,
            message: 'Serveur de recherche actif'
        }));
    } else {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Endpoint non trouvé' }));
    }
});

server.listen(PORT, () => {
    console.log('\n========================================');
    console.log(`🎉 Serveur de recherche démarré`);
    console.log(`🌐 URL: http://localhost:${PORT}`);
    console.log(`📂 ${categories.length} catégories disponibles`);
    console.log(`🔍 Extensions: ${SEARCH_EXTENSIONS.join(', ')}`);
    console.log('========================================');
    console.log('\nEndpoints:');
    console.log(`  POST /search - Recherche de contenu`);
    console.log(`  GET  /status - Statut du serveur`);
    console.log('\nAppuyez sur Ctrl+C pour arrêter\n');
});

process.on('SIGINT', () => {
    console.log('\n\n🛑 Arrêt du serveur...');
    server.close(() => {
        console.log('✅ Serveur arrêté\n');
        process.exit(0);
    });
});
