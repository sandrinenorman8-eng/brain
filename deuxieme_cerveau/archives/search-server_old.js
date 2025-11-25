const fs = require('fs').promises;
const path = require('path');
const http = require('http');
const url = require('url');

// Configuration
const PORT = 3008;
const SEARCH_EXTENSIONS = ['.txt', '.md', '.html'];

// Load categories
let categories = [];
try {
    const categoriesData = fs.readFileSync('categories.json', 'utf8');
    categories = JSON.parse(categoriesData);
} catch (error) {
    console.error('❌ Erreur lors du chargement des catégories:', error.message);
}

async function searchInFile(filePath, searchTerm) {
    try {
        const content = await fs.readFile(filePath, 'utf8');
        const lines = content.split('\n');
        const matches = [];

        lines.forEach((line, index) => {
            const lowerLine = line.toLowerCase();
            const lowerTerm = searchTerm.toLowerCase();

            if (lowerLine.includes(lowerTerm)) {
                // Créer un extrait avec contexte
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
        console.error(`Erreur lors de la lecture du fichier ${filePath}:`, error.message);
        return [];
    }
}

async function searchInCategory(categoryName, searchTerm) {
    const categoryPath = path.join(__dirname, categoryName);

    try {
        await fs.access(categoryPath); // Asynchronously check if directory exists
    } catch (error) {
        return []; // Directory does not exist
    }

    const results = [];

    try {
        const files = await fs.readdir(categoryPath);

        for (const fileName of files) {
            const filePath = path.join(categoryPath, fileName);
            const fileExt = path.extname(fileName);

            if (SEARCH_EXTENSIONS.includes(fileExt)) {
                const matches = await searchInFile(filePath, searchTerm);

                if (matches.length > 0) {
                    // Extraire la date du nom de fichier
                    const dateMatch = fileName.match(/(\d{4}-\d{2}-\d{2})/);
                    const fileDate = dateMatch ? dateMatch[1] : new Date().toISOString().split('T')[0];

                    results.push({
                        category: categoryName,
                        filename: fileName,
                        date: fileDate,
                        match_count: matches.length,
                        excerpts: matches.slice(0, 3) // Limiter à 3 extraits par fichier
                    });
                }
            }
        }
    } catch (error) {
        console.error(`Erreur lors de la recherche dans ${categoryName}:`, error.message);
    }

    return results;
}

async function performSearch(searchTerm) {
    console.log(`🔍 Recherche pour: "${searchTerm}"`);

    if (!searchTerm || searchTerm.length < 2) {
        return { results: [], message: 'Terme de recherche trop court' };
    }

    // Run all category searches in parallel for maximum efficiency
    const categoryPromises = categories.map(category => searchInCategory(category.name, searchTerm));
    const nestedResults = await Promise.all(categoryPromises);
    const allResults = nestedResults.flat(); // Flatten the array of arrays

    console.log(`✅ ${allResults.length} résultats trouvés`);

    return {
        results: allResults,
        message: `${allResults.length} fichier(s) trouvé(s)`
    };
}

// Serveur HTTP
const server = http.createServer((req, res) => {
    // CORS headers
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

        req.on('end', async () => { // Make the handler async
            try {
                const { term } = JSON.parse(body);
                const searchResults = await performSearch(term); // Await the async function

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify(searchResults));
            } catch (error) {
                console.error('❌ Erreur lors de la recherche:', error);
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
    console.log(`🚀 Serveur de recherche démarré sur http://localhost:${PORT}`);
    console.log(`📁 ${categories.length} catégories chargées`);
    console.log(`🔍 Extensions supportées: ${SEARCH_EXTENSIONS.join(', ')}`);
    console.log('');
    console.log('Endpoints disponibles:');
    console.log(`  POST http://localhost:${PORT}/search - Recherche de contenu`);
    console.log(`  GET  http://localhost:${PORT}/status - Statut du serveur`);
});

// Gestion propre de l'arrêt
process.on('SIGINT', () => {
    console.log('\n🛑 Arrêt du serveur de recherche...');
    server.close(() => {
        console.log('✅ Serveur arrêté proprement');
        process.exit(0);
    });
});