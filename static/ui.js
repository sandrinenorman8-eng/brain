// UI functions for Deuxième Cerveau
// All DOM manipulation and UI-related functions

/**
 * Display files in the UI
 */
export function displayFiles(files, categories) {
    const container = document.getElementById('file-list');

    if (!container) {
        console.warn('⚠️ Files container not found - file list display skipped');
        return;
    }

    // Clear existing content
    container.innerHTML = '';

    if (files.length === 0) {
        container.innerHTML = '<p>Aucun fichier trouvé</p>';
        return;
    }

    // Create file items
    files.forEach(file => {
        const cat = categories.find(c => c.name === file.category);
        if (!cat) return; // Skip if category not found

        const fileItem = document.createElement('div');
        fileItem.className = 'file-item glass-effect p-4 rounded-lg mb-3';
        fileItem.style.borderLeft = `4px solid ${cat.color}`;

        const dateFormatted = file.date.split('-').reverse().join('/');
        
        // Extract just the filename from path (handle subfolders)
        const displayName = file.filename.split('/').pop();
        const subfolderInfo = file.subfolder ? ` [${file.subfolder}]` : '';

        fileItem.innerHTML = `
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                    <span class="text-2xl">${cat.emoji}</span>
                    <div>
                        <div class="font-medium text-white">${displayName}${subfolderInfo}</div>
                        <div class="text-sm text-primary/70">${cat.name} • ${dateFormatted}</div>
                    </div>
                </div>
                <a href="/read/${cat.name}/${encodeURIComponent(file.filename)}"
                   target="_blank"
                   class="px-3 py-1 bg-primary/20 hover:bg-primary/40 text-primary rounded transition-colors">
                    📖 Lire
                </a>
            </div>
        `;

        container.appendChild(fileItem);
    });
}

/**
 * Update filter buttons based on available categories
 */
export function updateFilterButtons(categories, currentFilter, filterCallback) {
    const filterContainer = document.getElementById('filter-buttons');
    if (!filterContainer) return;

    filterContainer.innerHTML = '';

    // Add "All" button
    const allButton = document.createElement('button');
    allButton.className = `filter-btn px-3 py-2 rounded-lg transition-colors ${
        currentFilter === 'all'
            ? 'bg-primary text-white'
            : 'bg-primary/20 text-primary hover:bg-primary/40'
    }`;
    allButton.textContent = '📂 Tout';
    allButton.onclick = () => filterCallback('all');
    filterContainer.appendChild(allButton);

    // Add category buttons
    categories.forEach(cat => {
        const button = document.createElement('button');
        button.className = `filter-btn px-3 py-2 rounded-lg transition-colors ${
            currentFilter === cat.name
                ? 'bg-primary text-white'
                : 'bg-primary/20 text-primary hover:bg-primary/40'
        }`;
        button.innerHTML = `${cat.emoji} ${cat.name}`;
        button.onclick = () => filterCallback(cat.name);
        filterContainer.appendChild(button);
    });
}

/**
 * Render folder buttons with hierarchy (parent folders with subfolders)
 */
export async function renderFolderButtons(categories, openFolderCallback, deleteCategoryCallback) {
    console.log('🔍 renderFolderButtons called with categories:', categories.map(c => c.name));
    console.log('📊 Total categories received:', categories.length);

    const foldersContainer = document.getElementById('folder-buttons');
    if (!foldersContainer) {
        console.error('❌ folder-buttons container not found');
        return;
    }

    foldersContainer.innerHTML = '';

    if (categories.length === 0) {
        console.log('⚠️ No categories to render');
        foldersContainer.innerHTML = '<div class="no-folders text-primary/70">Aucune catégorie trouvée</div>';
        return;
    }

    // Load folder hierarchy
    let hierarchy = {};
    try {
        const response = await fetch('/folder_hierarchy');
        if (response.ok) {
            hierarchy = await response.json();
            console.log('📁 Hierarchy loaded:', Object.keys(hierarchy));
        }
    } catch (error) {
        console.error('Error loading hierarchy:', error);
    }

    // Group categories by parent folder
    const parentFolders = {};
    const standaloneCategories = [];

    categories.forEach(cat => {
        let foundParent = false;
        for (const [parentName, parentData] of Object.entries(hierarchy)) {
            if (parentData.subfolders && parentData.subfolders.includes(cat.name)) {
                if (!parentFolders[parentName]) {
                    parentFolders[parentName] = {
                        ...parentData,
                        name: parentName,
                        children: []
                    };
                }
                parentFolders[parentName].children.push(cat);
                foundParent = true;
                break;
            }
        }
        if (!foundParent) {
            standaloneCategories.push(cat);
        }
    });

    console.log('📂 Parent folders:', Object.keys(parentFolders));
    console.log('📄 Standalone categories:', standaloneCategories.map(c => c.name));

    // Render parent folders with subfolders
    Object.entries(parentFolders).sort((a, b) => a[0].localeCompare(b[0])).forEach(([parentName, parentData]) => {
        renderParentFolder(parentName, parentData, foldersContainer, openFolderCallback, deleteCategoryCallback);
    });

    // Render standalone categories
    const sortedCategories = [...standaloneCategories].sort((a, b) => a.name.localeCompare(b.name));
    console.log('🔤 Standalone categories sorted:', sortedCategories.map(c => c.name));

    sortedCategories.forEach((cat, index) => {
        const folderDiv = document.createElement('div');
        folderDiv.className = 'folder-item glass-effect p-4 rounded-lg mb-3';

        folderDiv.innerHTML = `
            <div class="folder-content">
                <div class="folder-info">
                    <span class="category-emoji">${cat.emoji}</span>
                    <span class="category-name">${cat.name}</span>
                </div>
                <div class="folder-actions">
                    <button class="action-btn open-btn"
                            data-category-name="${cat.name}"
                            onclick="handleFolderOpen(event, '${cat.name}')"
                            title="Ouvrir le dossier">
                        📁
                    </button>
                    <button class="action-btn fusion-btn"
                            data-category-name="${cat.name}"
                            onclick="handleFolderFusionBackend(event, '${cat.name}')"
                            title="Fusionner les fichiers (Backend)">
                        🔗
                    </button>
                    <button class="erase-btn"
                            data-category-name="${cat.name}"
                            data-category-color="${cat.color}"
                            data-category-emoji="${cat.emoji}"
                            onclick="handleFolderDelete(event, '${cat.name}', '${cat.color}', '${cat.emoji}')"
                            title="Supprimer la catégorie">
                        🗑️
                    </button>
                </div>
            </div>
        `;
        foldersContainer.appendChild(folderDiv);
    });
}

/**
 * Render folder buttons with hierarchical structure (NEW VERSION)
 */
export function renderFolderButtonsStructured(structured, openFolderCallback, deleteCategoryCallback) {
    console.log('🔍 renderFolderButtonsStructured called');
    console.log('📂 Parents:', structured.parents.length, 'Standalone:', structured.standalone.length);

    const foldersContainer = document.getElementById('folder-buttons');
    if (!foldersContainer) {
        console.error('❌ folder-buttons container not found');
        return;
    }

    foldersContainer.innerHTML = '';

    // Render parent folders with collapsible children
    structured.parents.forEach(parent => {
        const parentDiv = document.createElement('div');
        parentDiv.className = 'parent-folder mb-4';
        
        const parentId = `parent-${parent.name.replace(/\s+/g, '-')}`;
        const isExpanded = localStorage.getItem(parentId) !== 'collapsed';

        parentDiv.innerHTML = `
            <div class="parent-folder-header glass-effect p-3 rounded-lg cursor-pointer hover:bg-primary/10 transition-colors"
                 onclick="toggleParentFolder('${parentId}')"
                 style="border-left: 4px solid ${parent.color}">
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                        <span class="collapse-icon transition-transform duration-300 ${isExpanded ? '' : 'rotate-[-90deg]'}">▼</span>
                        <span class="text-2xl">${parent.emoji}</span>
                        <span class="text-white font-medium">${parent.name}</span>
                        <span class="text-primary/70 text-sm">(${parent.children.length} sous-catégories)</span>
                    </div>
                </div>
            </div>
            <div class="parent-folder-children ml-8 mt-2 space-y-2 ${isExpanded ? '' : 'hidden'}" id="${parentId}">
                ${parent.children.map(child => `
                    <div class="folder-item glass-effect p-3 rounded-lg" style="border-left: 3px solid ${child.color}">
                        <div class="folder-content">
                            <div class="folder-info">
                                <span class="category-emoji text-xl">${child.emoji}</span>
                                <span class="category-name text-sm">${child.name}</span>
                            </div>
                            <div class="folder-actions">
                                <button class="action-btn open-btn"
                                        onclick="handleFolderOpen(event, '${child.name}')"
                                        title="Ouvrir le dossier">
                                    📁
                                </button>
                                <button class="action-btn fusion-btn"
                                        onclick="handleFolderFusionBackend(event, '${child.name}')"
                                        title="Fusionner les fichiers">
                                    🔗
                                </button>
                                <button class="erase-btn"
                                        onclick="handleFolderDelete(event, '${child.name}', '${child.color}', '${child.emoji}')"
                                        title="Supprimer la catégorie">
                                    🗑️
                                </button>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        foldersContainer.appendChild(parentDiv);
    });

    // Render standalone categories
    if (structured.standalone.length > 0) {
        const standaloneSection = document.createElement('div');
        standaloneSection.className = 'standalone-categories mt-4';
        
        structured.standalone.forEach(cat => {
            const folderDiv = document.createElement('div');
            folderDiv.className = 'folder-item glass-effect p-4 rounded-lg mb-3';
            folderDiv.style.borderLeft = `4px solid ${cat.color}`;

            folderDiv.innerHTML = `
                <div class="folder-content">
                    <div class="folder-info">
                        <span class="category-emoji">${cat.emoji}</span>
                        <span class="category-name">${cat.name}</span>
                    </div>
                    <div class="folder-actions">
                        <button class="action-btn open-btn"
                                onclick="handleFolderOpen(event, '${cat.name}')"
                                title="Ouvrir le dossier">
                            📁
                        </button>
                        <button class="action-btn fusion-btn"
                                onclick="handleFolderFusionBackend(event, '${cat.name}')"
                                title="Fusionner les fichiers">
                            🔗
                        </button>
                        <button class="erase-btn"
                                onclick="handleFolderDelete(event, '${cat.name}', '${cat.color}', '${cat.emoji}')"
                                title="Supprimer la catégorie">
                            🗑️
                        </button>
                    </div>
                </div>
            `;
            standaloneSection.appendChild(folderDiv);
        });
        
        foldersContainer.appendChild(standaloneSection);
    }
}

/**
 * Render categories in the main section
 */
export async function renderCategories(categories, saveCallback, deleteCallback) {
    console.log('🔍 renderCategories called - loading structured data');

    const container = document.getElementById('categories-container');
    if (!container) {
        console.error('❌ categories-container not found');
        return;
    }

    container.innerHTML = '';

    try {
        // Load structured categories
        const response = await fetch('/categories_structured');
        const structured = await response.json();
        
        console.log('📂 Structured data loaded for main section:', structured);

        // Render parent folders
        if (structured.parents && structured.parents.length > 0) {
            structured.parents.forEach(parent => {
                const parentEl = document.createElement('div');
                parentEl.className = 'parent-folder mb-3';
                parentEl.style.borderLeft = `4px solid ${parent.color}`;
                
                const parentId = `main-parent-${parent.name.replace(/\s+/g, '-')}`;
                
                parentEl.innerHTML = `
                    <div class="parent-header glass-effect p-3 rounded-lg cursor-pointer flex items-center justify-between hover:scale-105 transition-all"
                         onclick="toggleParentFolder('${parentId}')">
                        <div class="flex items-center space-x-2">
                            <span class="toggle-icon">▼</span>
                            <span class="text-xl">${parent.emoji}</span>
                            <span class="text-white font-medium">${parent.name}</span>
                            <span class="text-primary/60 text-sm">(${parent.children.length} sous-catégories)</span>
                        </div>
                    </div>
                    <div class="children-container pl-6 mt-2" id="${parentId}">
                        ${parent.children.map(child => `
                            <div class="child-category glass-effect p-3 rounded-lg mb-2 cursor-pointer transition-all hover:scale-105"
                                 style="border-left: 3px solid ${child.color}"
                                 onclick="handleCategoryClick(event, '${child.name}', '${child.emoji}', '${child.color}')">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center space-x-2">
                                        <span class="text-lg">${child.emoji}</span>
                                        <span class="text-white">${child.name}</span>
                                    </div>
                                    <button class="delete-btn text-red-400 hover:text-red-300"
                                            onclick="event.stopPropagation(); handleCategoryDelete(event, '${child.name}', '${child.color}', '${child.emoji}')"
                                            title="Supprimer la catégorie">
                                        🗑️
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `;
                
                container.appendChild(parentEl);
            });
        }

        // Render standalone categories
        if (structured.standalone && structured.standalone.length > 0) {
            structured.standalone.forEach(cat => {
                const categoryEl = document.createElement('div');
                categoryEl.className = 'category-item glass-effect p-4 rounded-lg mb-3 cursor-pointer transition-all hover:scale-105';
                categoryEl.style.borderLeft = `4px solid ${cat.color}`;

                categoryEl.innerHTML = `
                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-3">
                            <span class="text-2xl">${cat.emoji}</span>
                            <span class="text-white font-medium">${cat.name}</span>
                        </div>
                        <button class="delete-btn"
                                onclick="event.stopPropagation(); handleCategoryDelete(event, '${cat.name}', '${cat.color}', '${cat.emoji}')"
                                title="Supprimer la catégorie">
                            🗑️
                        </button>
                    </div>
                `;

                categoryEl.onclick = () => saveCallback(cat);
                container.appendChild(categoryEl);
            });
        }

        // Setup click handler for child categories
        window.handleCategoryClick = function(event, name, emoji, color) {
            event.stopPropagation();
            saveCallback({ name, emoji, color });
        };

    } catch (error) {
        console.error('❌ Error loading structured categories:', error);
        // Fallback to flat display
        const sortedCategories = [...categories].sort((a, b) => a.name.localeCompare(b.name));
        sortedCategories.forEach(cat => {
            const categoryEl = document.createElement('div');
            categoryEl.className = 'category-item glass-effect p-4 rounded-lg mb-3 cursor-pointer transition-all hover:scale-105';
            categoryEl.style.borderLeft = `4px solid ${cat.color}`;
            categoryEl.innerHTML = `
                <div class="flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                        <span class="text-2xl">${cat.emoji}</span>
                        <span class="text-white font-medium">${cat.name}</span>
                    </div>
                    <button class="delete-btn"
                            onclick="handleCategoryDelete(event, '${cat.name}', '${cat.color}', '${cat.emoji}')"
                            title="Supprimer la catégorie">
                        🗑️
                    </button>
                </div>
            `;
            categoryEl.onclick = () => saveCallback(cat);
            container.appendChild(categoryEl);
        });
    }
}

/**
 * Show notification
 */
export function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm ${
        type === 'success' ? 'bg-green-500' :
        type === 'error' ? 'bg-red-500' :
        'bg-blue-500'
    } text-white`;
    notification.innerHTML = `
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-2">
                <span class="text-xl">
                    ${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}
                </span>
                <span>${message}</span>
            </div>
            <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;

    document.body.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

/**
 * Update character counter for input fields
 */
export function updateCharCounter(input) {
    const counter = input.parentElement.querySelector('.char-counter');
    if (counter) {
        const remaining = 19 - input.value.length;
        counter.textContent = `${remaining}/19`;
        counter.style.color = remaining < 0 ? '#dc3545' : remaining < 5 ? '#ffc107' : '#6c757d';
    }
}

/**
 * Show erase confirmation dialog
 */
export function showEraseConfirmation(name, color, emoji, confirmCallback) {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50';
    modal.innerHTML = `
        <div class="glass-effect rounded-xl w-full max-w-md p-6">
            <h3 class="text-xl font-display text-primary text-glow mb-4">⚠️ Confirmer la suppression</h3>
            <p class="text-white mb-2">Êtes-vous sûr de vouloir supprimer la catégorie <strong style="color: ${color}">${emoji} ${name}</strong> ?</p>
            <p class="text-red-400 text-sm mb-4">Cette action est irréversible et supprimera tous les fichiers de cette catégorie.</p>
            <div class="flex space-x-3 justify-end">
                <button class="px-4 py-2 bg-gray-500/20 hover:bg-gray-500/40 text-white rounded transition-colors"
                        onclick="this.closest('.fixed').remove()">Annuler</button>
                <button class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded transition-colors"
                        onclick="this.closest('.fixed').remove(); window.confirmDeleteCategory('${name}')">Supprimer</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

/**
 * Show fusion modal
 */
export function showFusionModal(type, categories, globalFusionCallback, categoryFusionCallback) {
    const modal = document.getElementById('fusionModal');

    if (type === 'global') {
        document.getElementById('fusionModalTitle').textContent = '🔗 Fusion Globale';
        document.getElementById('fusionModalContent').innerHTML = `
            <p class="text-white mb-4">Fusionner toutes les notes de toutes les catégories en un seul fichier ?</p>
            <div class="flex space-x-3 justify-end">
                <button class="modal-btn cancel-btn"
                        onclick="ui.closeFusionModal()">Annuler</button>
                <button class="modal-btn confirm-btn"
                        onclick="ui.closeFusionModal(); window.handleGlobalFusion()">Fusionner</button>
            </div>
        `;
    } else if (type === 'category') {
        document.getElementById('fusionModalTitle').textContent = '🔗 Fusion par Catégories';
        document.getElementById('fusionModalContent').innerHTML = `
            <p class="text-white mb-4">Sélectionnez les catégories à fusionner :</p>
            <div class="space-y-2 mb-4">
                ${categories.map(cat => `
                    <label class="category-checkbox flex items-center space-x-2 cursor-pointer">
                        <input type="checkbox" value="${cat.name}" class="rounded">
                        <span style="color: ${cat.color}">${cat.emoji} ${cat.name}</span>
                    </label>
                `).join('')}
            </div>
            <div class="flex space-x-3 justify-end">
                <button class="modal-btn cancel-btn"
                        onclick="ui.closeFusionModal()">Annuler</button>
                <button class="modal-btn confirm-btn"
                        onclick="ui.closeFusionModal(); window.handleCategoryFusion()">Fusionner</button>
            </div>
        `;
    }

    modal.classList.remove('hidden');
}

/**
 * Close fusion modal
 */
export function closeFusionModal() {
    document.getElementById('fusionModal').classList.add('hidden');
}

/**
 * Handle folder fusion button click
 */
export function handleFolderFusion(event, categoryName) {
    event.stopPropagation(); // Prevent triggering folder actions

    console.log('🔗 Opening fusion for category:', categoryName);

    // Open the fusion page in a new tab
    const fusionUrl = `/fusionner?dossier=${encodeURIComponent(categoryName)}`;
    window.open(fusionUrl, '_blank');

    // Show notification
    showNotification(`🔗 Fusion de la catégorie "${categoryName}" ouverte`, 'success');
}


/**
 * Render a parent folder with its subfolders (collapsible)
 */
function renderParentFolder(parentName, parentData, container, openFolderCallback, deleteCategoryCallback) {
    const parentDiv = document.createElement('div');
    parentDiv.className = 'parent-folder-item mb-4';
    
    const parentId = `parent-${parentName.replace(/\s+/g, '-')}`;
    
    parentDiv.innerHTML = `
        <div class="parent-folder-header glass-effect p-4 rounded-lg cursor-pointer hover:bg-primary/10 transition-colors"
             onclick="toggleSubfolders('${parentId}')">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                    <span class="text-2xl">${parentData.emoji}</span>
                    <span class="font-bold text-white text-lg">${parentName}</span>
                    <span class="text-sm text-primary/70">(${parentData.children.length} sous-dossiers)</span>
                </div>
                <span class="toggle-icon transition-transform duration-300" id="icon-${parentId}">▼</span>
            </div>
        </div>
        <div class="subfolders-container hidden mt-2 ml-8 space-y-2" id="${parentId}">
            ${parentData.children.map(cat => `
                <div class="subfolder-item glass-effect p-3 rounded-lg">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <span class="text-xl">${cat.emoji}</span>
                            <span class="text-white">${cat.name}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <button class="action-btn text-sm px-2 py-1"
                                    onclick="handleFolderOpen(event, '${cat.name}')"
                                    title="Ouvrir">
                                📁
                            </button>
                            <button class="action-btn text-sm px-2 py-1"
                                    onclick="handleFolderFusionBackend(event, '${cat.name}')"
                                    title="Fusionner">
                                🔗
                            </button>
                            <button class="erase-btn text-sm px-2 py-1"
                                    onclick="handleFolderDelete(event, '${cat.name}', '${cat.color}', '${cat.emoji}')"
                                    title="Supprimer">
                                🗑️
                            </button>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    
    container.appendChild(parentDiv);
}

/**
 * Toggle subfolders visibility
 */
window.toggleSubfolders = function(folderId) {
    const subfoldersContainer = document.getElementById(folderId);
    const icon = document.getElementById(`icon-${folderId}`);
    
    if (subfoldersContainer && icon) {
        subfoldersContainer.classList.toggle('hidden');
        icon.style.transform = subfoldersContainer.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(180deg)';
    }
};
