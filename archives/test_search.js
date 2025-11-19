// Test rapide du système de recherche
const fs = require('fs');
const path = require('path');

console.log('🧪 Test du système de recherche');
console.log('================================');

// Test 1: Vérifier les catégories
try {
    const categoriesData = fs.readFileSync('categories.json', 'utf8');
    const categories = JSON.parse(categoriesData);
    console.log(`✅ ${categories.length} catégories chargées`);
} catch (error) {
    console.log('❌ Erreur lors du chargement des catégories:', error.message);
    process.exit(1);
}

// Test 2: Vérifier les dossiers
const categories = JSON.parse(fs.readFileSync('categories.json', 'utf8'));
let totalFiles = 0;

categories.forEach(category => {
    const categoryPath = category.name;
    if (fs.existsSync(categoryPath)) {
        const files = fs.readdirSync(categoryPath).filter(file => 
            ['.txt', '.md', '.html'].includes(path.extname(file))
        );
        console.log(`📁 ${category.name}: ${files.length} fichiers`);
        totalFiles += files.length;
    } else {
        console.log(`⚠️  ${category.name}: dossier non trouvé`);
    }
});

console.log(`📊 Total: ${totalFiles} fichiers trouvés`);

// Test 3: Test de recherche simple
function testSearch(searchTerm) {
    console.log(`\n🔍 Test de recherche: "${searchTerm}"`);
    let results = 0;
    
    categories.forEach(category => {
        const categoryPath = category.name;
        if (fs.existsSync(categoryPath)) {
            const files = fs.readdirSync(categoryPath);
            files.forEach(fileName => {
                const filePath = path.join(categoryPath, fileName);
                const fileExt = path.extname(fileName);
                
                if (['.txt', '.md', '.html'].includes(fileExt)) {
                    try {
                        const content = fs.readFileSync(filePath, 'utf8');
                        if (content.toLowerCase().includes(searchTerm.toLowerCase())) {
                            console.log(`  ✅ Trouvé dans: ${categoryPath}/${fileName}`);
                            results++;
                        }
                    } catch (error) {
                        console.log(`  ❌ Erreur lecture: ${filePath}`);
                    }
                }
            });
        }
    });
    
    console.log(`  📊 ${results} fichiers contiennent "${searchTerm}"`);
}

// Tests de recherche
testSearch('test');
testSearch('projet');

console.log('\n🎉 Tests terminés!');
console.log('💡 Pour démarrer le serveur: node search-server.js');