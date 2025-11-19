let allFiles = [];
        let currentFilter = 'all';
        let categories = [];

        // ===== DYNAMIC PARTITIONING SYSTEM =====
        let partitioningState = {
            sections: {
                'main-section': { collapsed: false, size: 'auto', order: 1 },
                'notes-section': { collapsed: false, size: 'auto', order: 2 },
                'folders-section': { collapsed: false, size: 'auto', order: 3 }
            },
            isResizing: false,
            resizeData: null,
            autoExpansion: true,
            contentObservers: new Map()
        };

        // Initialize dynamic partitioning system
        function initializePartitioning() {
            console.log('🚀 Initializing dynamic partitioning system...');
            
            // Load saved state
            loadPartitioningState();
            
            // Set up content observers for auto-expansion
            setupContentObservers();
            
            // Initialize section interactions
            initializeSectionInteractions();
            
            // Set up responsive behavior
            setupResponsiveBehavior();
            
            console.log('✅ Dynamic partitioning system initialized');
        }

        // Toggle section collapse/expand
        function toggleSection(sectionId) {
            const section = document.getElementById(sectionId);
            const content = section.querySelector('.section-content');
            const icon = section.querySelector('.collapse-icon');
            const state = partitioningState.sections[sectionId];
            
            if (!section || !content || !icon) {
                console.error('❌ Section elements not found:', sectionId);
                return;
            }
            
            state.collapsed = !state.collapsed;
            
            if (state.collapsed) {
                content.classList.add('collapsed');
                icon.style.transform = 'rotate(-90deg)';
                section.style.minHeight = '60px';
            } else {
                content.classList.remove('collapsed');
                icon.style.transform = 'rotate(0deg)';
                section.style.minHeight = '200px';
                // Auto-expand based on content
                if (partitioningState.autoExpansion) {
                    adjustSectionSize(sectionId);
                }
            }
            
            savePartitioningState();
            console.log(`🔄 Section ${sectionId} ${state.collapsed ? 'collapsed' : 'expanded'}`);
        }

        // Start resizing a section
        function startResize(event, sectionId) {
            event.preventDefault();
            event.stopPropagation();
            
            partitioningState.isResizing = true;
            partitioningState.resizeData = {
                sectionId: sectionId,
                startX: event.clientX,
                startY: event.clientY,
                startWidth: event.target.closest('.dynamic-section').offsetWidth,
                startHeight: event.target.closest('.dynamic-section').offsetHeight
            };
            
            document.addEventListener('mousemove', handleResize);
            document.addEventListener('mouseup', stopResize);
            
            // Add visual feedback
            document.body.style.cursor = 'nw-resize';
            document.body.style.userSelect = 'none';
            
            console.log('🔄 Started resizing section:', sectionId);
        }

        // Handle resize operation
        function handleResize(event) {
            if (!partitioningState.isResizing || !partitioningState.resizeData) return;
            
            const { sectionId, startX, startY, startWidth, startHeight } = partitioningState.resizeData;
            const section = document.getElementById(sectionId);
            
            if (!section) return;
            
            const deltaX = event.clientX - startX;
            const deltaY = event.clientY - startY;
            
            const newWidth = Math.max(200, startWidth + deltaX);
            const newHeight = Math.max(150, startHeight + deltaY);
            
            section.style.width = newWidth + 'px';
            section.style.height = newHeight + 'px';
            section.style.flex = 'none';
            
            // Update state
            partitioningState.sections[sectionId].size = {
                width: newWidth,
                height: newHeight
            };
        }

        // Stop resize operation
        function stopResize() {
            if (!partitioningState.isResizing) return;
            
            partitioningState.isResizing = false;
            partitioningState.resizeData = null;
            
            document.removeEventListener('mousemove', handleResize);
            document.removeEventListener('mouseup', stopResize);
            
            // Remove visual feedback
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
            
            savePartitioningState();
            console.log('✅ Resize operation completed');
        }

        // Auto-adjust section size based on content
        function adjustSectionSize(sectionId) {
            const section = document.getElementById(sectionId);
            if (!section) return;
            
            const content = section.querySelector('.section-content');
            if (!content) return;
            
            // Calculate content height
            const contentHeight = content.scrollHeight;
            const headerHeight = section.querySelector('.section-header').offsetHeight;
            const minHeight = Math.max(200, contentHeight + headerHeight + 40);
            
            // Apply new height with smooth transition
            section.style.transition = 'height 0.3s ease';
            section.style.height = minHeight + 'px';
            
            setTimeout(() => {
                section.style.transition = '';
            }, 300);
            
            console.log(`📏 Auto-adjusted ${sectionId} height to ${minHeight}px`);
        }

        // Set up content observers for auto-expansion
        function setupContentObservers() {
            const sections = ['main-section', 'notes-section', 'folders-section'];
            
            sections.forEach(sectionId => {
                const section = document.getElementById(sectionId);
                if (!section) return;
                
                const content = section.querySelector('.section-content');
                if (!content) return;
                
                // Create MutationObserver to watch for content changes
                const observer = new MutationObserver((mutations) => {
                    if (partitioningState.autoExpansion && !partitioningState.sections[sectionId].collapsed) {
                        adjustSectionSize(sectionId);
                    }
                });
                
                observer.observe(content, {
                    childList: true,
                    subtree: true,
                    attributes: true,
                    attributeFilter: ['style', 'class']
                });
                
                partitioningState.contentObservers.set(sectionId, observer);
            });
            
            console.log('👀 Content observers set up for auto-expansion');
        }

        // Initialize section interactions
        function initializeSectionInteractions() {
            // Add drag functionality to section headers
            const headers = document.querySelectorAll('.section-header');
            headers.forEach(header => {
                header.addEventListener('mousedown', (e) => {
                    if (e.target.closest('.control-btn')) return;
                    
                    const section = header.closest('.dynamic-section');
                    if (!section) return;
                    
                    // Add drag visual feedback
                    section.style.opacity = '0.8';
                    section.style.transform = 'rotate(2deg)';
                });
                
                header.addEventListener('mouseup', (e) => {
                    const section = header.closest('.dynamic-section');
                    if (!section) return;
                    
                    // Remove drag visual feedback
                    section.style.opacity = '';
                    section.style.transform = '';
                });
            });
            
            console.log('🎯 Section interactions initialized');
        }

        // Set up responsive behavior
        function setupResponsiveBehavior() {
            const container = document.querySelector('.dynamic-container');
            if (!container) return;
            
            // Handle window resize
            window.addEventListener('resize', debounce(() => {
                adjustLayoutForScreenSize();
            }, 250));
            
            // Initial adjustment
            adjustLayoutForScreenSize();
            
            console.log('📱 Responsive behavior set up');
        }

        // Adjust layout based on screen size
        function adjustLayoutForScreenSize() {
            const container = document.querySelector('.dynamic-container');
            if (!container) return;
            
            const width = window.innerWidth;
            
            if (width < 768) {
                // Mobile layout
                container.style.gridTemplateColumns = '1fr';
                container.style.gridTemplateRows = 'auto auto auto';
            } else if (width < 1200) {
                // Tablet layout
                container.style.gridTemplateColumns = '1fr 1fr';
                container.style.gridTemplateRows = 'auto auto';
            } else {
                // Desktop layout
                container.style.gridTemplateColumns = '1fr 1fr 1fr';
                container.style.gridTemplateRows = 'auto auto';
            }
            
            console.log(`📐 Layout adjusted for screen width: ${width}px`);
        }

        // Save partitioning state to localStorage
        function savePartitioningState() {
            try {
                localStorage.setItem('partitioningState', JSON.stringify(partitioningState.sections));
            } catch (error) {
                console.error('❌ Error saving partitioning state:', error);
            }
        }

        // Load partitioning state from localStorage
        function loadPartitioningState() {
            try {
                const saved = localStorage.getItem('partitioningState');
                if (saved) {
                    const savedState = JSON.parse(saved);
                    Object.assign(partitioningState.sections, savedState);
                    
                    // Apply saved state
                    Object.keys(partitioningState.sections).forEach(sectionId => {
                        const section = document.getElementById(sectionId);
                        if (!section) return;
                        
                        const state = partitioningState.sections[sectionId];
                        
                        if (state.collapsed) {
                            toggleSection(sectionId);
                        }
                        
                        if (state.size && typeof state.size === 'object') {
                            section.style.width = state.size.width + 'px';
                            section.style.height = state.size.height + 'px';
                            section.style.flex = 'none';
                        }
                    });
                    
                    console.log('💾 Partitioning state loaded from localStorage');
                }
            } catch (error) {
                console.error('❌ Error loading partitioning state:', error);
            }
        }

        // Utility function for debouncing
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }

        // Public API for external control
        window.partitioningAPI = {
            toggleSection,
            adjustSectionSize,
            getState: () => partitioningState,
            resetLayout: () => {
                Object.keys(partitioningState.sections).forEach(sectionId => {
                    const section = document.getElementById(sectionId);
                    if (section) {
                        section.style.width = '';
                        section.style.height = '';
                        section.style.flex = '';
                        partitioningState.sections[sectionId].size = 'auto';
                    }
                });
                savePartitioningState();
                console.log('🔄 Layout reset to default');
            }
        };

        document.addEventListener('DOMContentLoaded', () => {
            // Initialize dynamic partitioning system first
            initializePartitioning();
            
            // Load application data
            loadCategories();
            loadAllFiles();

            // Focus automatique sur le textarea
            document.getElementById('note-input').focus();

            // Raccourci clavier : Ctrl+Enter pour sauvegarder dans la dernière catégorie utilisée
            document.getElementById('note-input').addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'Enter' && localStorage.getItem('lastCategory')) {
                    const lastCat = JSON.parse(localStorage.getItem('lastCategory'));
                    quickSave(lastCat);
                }
            });
            
            console.log('🚀 Application fully initialized with dynamic partitioning');
        });

        function loadCategories() {
            console.log('🔄 Loading categories...');
            
            fetch('/categories')
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(cats => {
                    console.log('✅ Categories loaded successfully:', { count: cats.length });
                    
                    // Validate categories data
                    if (!Array.isArray(cats)) {
                        throw new Error('Invalid categories data format');
                    }
                    
                    categories = cats;
                    const container = document.getElementById('categories-container');
                    
                    if (!container) {
                        console.error('❌ Categories container not found!');
                        throw new Error('Categories container not found');
                    }
                    
                    container.innerHTML = '';

                    // Créer les boutons de catégories
                    categories.forEach((cat, index) => {
                        try {
                            if (!cat || !cat.name || !cat.emoji || !cat.color) {
                                console.warn(`⚠️ Invalid category data at index ${index}:`, cat);
                                return;
                            }
                            
                        const categoryEl = document.createElement('div');
                        categoryEl.className = 'glass-effect rounded-xl p-4 shadow-inner-strong transition-all duration-300 hover:shadow-glow-primary cursor-pointer';
                        categoryEl.onclick = () => quickSave(cat);

                        categoryEl.innerHTML = `
                            <div class="flex items-center justify-between">
                                <p class="text-lg text-white font-medium">${cat.emoji} ${cat.name}</p>
                                <button class="text-accent hover:text-white transition-colors z-10" onclick="event.stopPropagation(); showEraseConfirmation('${cat.name}', '${cat.color}', '${cat.emoji}');">
                                    <svg fill="currentColor" height="22" viewBox="0 0 256 256" width="22" xmlns="http://www.w3.org/2000/svg"><path d="M216 48h-36V40a16 16 0 0 0-16-16h-48a16 16 0 0 0-16 16v8H64a16 16 0 0 0-16 16v24h184V64a16 16 0 0 0-16-16ZM96 40a8 8 0 0 1 8-8h48a8 8 0 0 1 8 8v8H96Zm120 48H40v120a16 16 0 0 0 16 16h128a16 16 0 0 0 16-16ZM112 112a8 8 0 0 1 16 0v64a8 8 0 0 1-16 0Zm48 0a8 8 0 0 1 16 0v64a8 8 0 0 1-16 0Z"></path></svg>
                                </button>
                            </div>
                        `;
                        container.appendChild(categoryEl);
                            
                        } catch (error) {
                            console.error(`❌ Error creating category button for ${cat?.name || 'unknown'}:`, error);
                        }
                    });

                    // Créer les filtres
                    try {
                    updateFilterButtons();
                    } catch (error) {
                        console.error('❌ Error updating filter buttons:', error);
                    }
                    
                    // Render folder buttons with enhanced error handling
                    try {
                    renderFolderButtons();
                        console.log('✅ Folder buttons rendered successfully');
                    } catch (error) {
                        console.error('❌ Error rendering folder buttons:', error);
                        // Show user-friendly error message
                        const folderContainer = document.getElementById('folder-buttons');
                        if (folderContainer) {
                            folderContainer.innerHTML = `
                                <div style="text-align: center; color: #dc3545; padding: 20px; background: #f8d7da; border-radius: 8px;">
                                    <strong>⚠️ Erreur de chargement des dossiers</strong><br>
                                    <small>Veuillez recharger la page</small>
                                </div>
                            `;
                        }
                    }
                })
                .catch(error => {
                    console.error('❌ Critical error loading categories:', error);
                    
                    // Show error message to user
                    const container = document.getElementById('categories-container');
                    if (container) {
                        container.innerHTML = `
                            <div style="text-align: center; color: #dc3545; padding: 20px; background: #f8d7da; border-radius: 8px;">
                                <strong>⚠️ Erreur de chargement des catégories</strong><br>
                                <small>Veuillez recharger la page ou vérifier votre connexion</small>
                            </div>
                        `;
                    }
                    
                    // Also show error in folder buttons section
                    const folderContainer = document.getElementById('folder-buttons');
                    if (folderContainer) {
                        folderContainer.innerHTML = `
                            <div style="text-align: center; color: #dc3545; padding: 20px; background: #f8d7da; border-radius: 8px;">
                                <strong>⚠️ Impossible de charger les dossiers</strong><br>
                                <small>Erreur de connexion au serveur</small>
                            </div>
                        `;
                    }
                });
        }

        function quickSave(category) {
            const text = document.getElementById('note-input').value.trim();
            if (!text) {
                // Pas de notification
                document.getElementById('note-input').focus();
                return;
            }

            fetch(`/save/${category.name}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            })
            .then(() => {
                // Vider le champ
                document.getElementById('note-input').value = '';
                // Refocus immédiat
                document.getElementById('note-input').focus();
                // Notification de succès
                // Pas de notification
                // Sauvegarder la dernière catégorie utilisée
                localStorage.setItem('lastCategory', JSON.stringify(category));
                // Recharger la liste
                loadAllFiles();
            });
        }

        function loadAllFiles() {
            fetch('/all_files')
                .then(response => response.json())
                .then(data => {
                    allFiles = data;
                    displayFiles();
                })
                .catch(() => {
                    // Si l'endpoint n'existe pas, on charge catégorie par catégorie
                    loadFilesByCategories();
                });
        }

        function loadFilesByCategories() {
            allFiles = [];
            const promises = categories.map(cat =>
                fetch(`/list/${cat.name}`)
                    .then(response => response.json())
                    .then(files => {
                        files.forEach(file => {
                            allFiles.push({
                                category: cat.name,
                                emoji: cat.emoji,
                                color: cat.color,
                                filename: file,
                                date: file.replace(`${cat.name}_`, '').replace('.txt', '')
                            });
                        });
                    })
            );

            Promise.all(promises).then(() => {
                // Trier par date décroissante
                allFiles.sort((a, b) => b.date.localeCompare(a.date));
                displayFiles();
            });
        }

        function displayFiles() {
            const fileList = document.getElementById('file-list');
            if (!fileList) return;
            fileList.innerHTML = '';

            const filteredFiles = currentFilter === 'all' ? allFiles : allFiles.filter(f => f.category === currentFilter);

            if (filteredFiles.length === 0) {
                fileList.innerHTML = '<p class="text-center text-primary/60">Aucune note à afficher.</p>';
                return;
            }

            filteredFiles.forEach(file => {
                const fileItem = document.createElement('div');
                fileItem.className = 'glass-effect rounded-lg p-3 transition-all duration-300 hover:border-primary/50 border border-transparent cursor-pointer';
                const dateFormatted = new Date(file.date).toLocaleDateString('fr-FR');
                const displayName = file.filename.replace(`${file.category}_`, '').replace('.txt', '');

                fileItem.innerHTML = `
                    <div class="flex items-center justify-between">
                        <span class="text-sm font-bold" style="color: ${file.color}">${file.emoji} ${file.category}</span>
                        <span class="text-xs text-primary/70">${dateFormatted}</span>
                    </div>
                    <p class="mt-1 text-base text-white truncate">${displayName}</p>
                `;
                fileItem.onclick = () => openFile(file.category, file.filename);
                fileList.appendChild(fileItem);
            });
        }

        function filterByCategory(category) {
            currentFilter = category;
            document.querySelectorAll('.filter-btn').forEach(btn => {
                const btnCategory = btn.getAttribute('data-category');
                if (btnCategory === category) {
                    btn.style.backgroundColor = 'var(--primary)';
                    btn.style.color = 'var(--primary-dark)';
                    } else {
                    btn.style.backgroundColor = 'rgba(13, 27, 42, 0.5)';
                    btn.style.color = 'white';
                }
            });
            displayFiles();
        }

        function updateFilterButtons() {
            const container = document.getElementById('filter-buttons');
            if(!container) return;
            container.innerHTML = ''; // Clear previous buttons
            const allBtn = document.createElement('button');
            allBtn.className = 'filter-btn h-8 px-4 text-sm font-bold rounded-full transition-colors';
            allBtn.textContent = 'Tout';
            allBtn.onclick = () => filterByCategory('all');
            allBtn.setAttribute('data-category', 'all');
            container.appendChild(allBtn);

            categories.forEach(cat => {
                const btn = document.createElement('button');
                btn.className = 'filter-btn h-8 px-4 text-sm font-bold text-white rounded-full transition-colors bg-primary-dark/50 hover:bg-primary hover:text-primary-dark';
                btn.setAttribute('data-category', cat.name);
                btn.innerHTML = `${cat.emoji} ${cat.name}`;
                btn.onclick = () => filterByCategory(cat.name);
                container.appendChild(btn);
            });
            // Activate 'all' button by default
            filterByCategory('all');
        }

        function addNewCategory() {
            const input = document.getElementById('new-category-name');
            const name = input.value.trim();
            if (!name) return;

            // Validation de la longueur (19 caractères maximum)
            if (name.length > 19) {
                // Pas de notification
                return;
            }

            fetch('/add_category', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: name })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showNotification('❌ Erreur: ' + data.error, 'error');
                } else {
                    input.value = '';
                    loadCategories();
                    showNotification('✅ Catégorie créée avec succès !', 'success');
                }
            })
            .catch(error => {
                console.error('Erreur lors de la création de la catégorie:', error);
                showNotification('❌ Erreur de connexion lors de la création de la catégorie', 'error');
            });
        }

        function openFile(category, filename) {
            window.open(`/read/${category}/${filename}`, '_blank');
        }

        function openFolder(categoryName) {
            // Utiliser l'endpoint serveur pour ouvrir le dossier
            fetch(`/open_folder/${categoryName}`)
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'opened') {
                        // Pas de notifications - ouverture directe
                    } else {
                        // Pas de notifications d'erreur non plus
                    }
                })
                .catch(error => {
                    console.error('Erreur:', error);
                    // Pas de notifications d'erreur
                });
        }

        function getUsername() {
            // Essayer de récupérer le nom d'utilisateur depuis différentes sources
            try {
                // Valeur par défaut
                return 'VOTRE_NOM';
            } catch (e) {
                return 'VOTRE_NOM';
            }
        }

        // Fonction de notification supprimée - plus de notifications

        // ===== REFACTORED FOLDER BUTTONS SYSTEM =====
        let folderButtonsState = {
            isInitialized: false,
            lastUpdate: null,
            errorCount: 0,
            maxRetries: 3
        };

        function renderFolderButtons() {
            try {
                console.log('🔄 Rendering folder buttons...', { categoriesCount: categories.length });
                
                const container = document.getElementById('folder-buttons');
                if (!container) {
                    console.error('❌ Folder buttons container not found!');
                    throw new Error('Folder buttons container not found');
                }

                // Clear container safely
                container.innerHTML = '';
                
                // Validate categories data
                if (!categories || !Array.isArray(categories) || categories.length === 0) {
                    console.warn('⚠️ No categories available for folder buttons');
                    container.innerHTML = '<div style="text-align: center; color: #666; padding: 20px;">Aucune catégorie disponible</div>';
                    return;
                }

                // Create folder buttons for each category
                categories.forEach((cat, index) => {
                    try {
                        if (!cat || !cat.name || !cat.emoji || !cat.color) {
                            console.warn(`⚠️ Invalid category data at index ${index}:`, cat);
                            return;
                        }

                        const categoryContainer = createCategoryContainer(cat, index);
                        container.appendChild(categoryContainer);
                        
                    } catch (error) {
                        console.error(`❌ Error creating category button for ${cat?.name || 'unknown'}:`, error);
                        folderButtonsState.errorCount++;
                    }
                });

                // Update state
                folderButtonsState.isInitialized = true;
                folderButtonsState.lastUpdate = new Date();
                folderButtonsState.errorCount = 0;
                
                console.log('✅ Folder buttons rendered successfully', { 
                    categoriesRendered: categories.length,
                    timestamp: folderButtonsState.lastUpdate 
                });

            } catch (error) {
                console.error('❌ Critical error in renderFolderButtons:', error);
                folderButtonsState.errorCount++;
                
                // Show error message to user
                const container = document.getElementById('folder-buttons');
                if (container) {
                    container.innerHTML = `
                        <div style="text-align: center; color: #dc3545; padding: 20px; background: #f8d7da; border-radius: 8px; margin: 10px;">
                            <strong>⚠️ Erreur de chargement des dossiers</strong><br>
                            <small>Veuillez recharger la page ou contacter le support</small>
                        </div>
                    `;
                }
                
                // Retry mechanism
                if (folderButtonsState.errorCount < folderButtonsState.maxRetries) {
                    console.log(`🔄 Retrying folder buttons render (attempt ${folderButtonsState.errorCount + 1}/${folderButtonsState.maxRetries})`);
                    setTimeout(() => renderFolderButtons(), 1000 * folderButtonsState.errorCount);
                }
            }
        }

        function createCategoryContainer(cat, index) {
            const button = document.createElement('button');
            button.className = 'h-14 px-4 text-base font-bold text-white rounded-lg hover:brightness-125 transition-all duration-300 flex items-center justify-center gap-2';
            button.style.background = cat.color;
            button.innerHTML = `<span>${cat.emoji}</span><span>${cat.name}</span>`;
            button.onclick = () => openSavedLocation(cat);
            return button;
        }

        function showErrorNotification(message) {
            // Create a temporary error notification
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #dc3545;
                color: white;
                padding: 15px 20px;
                border-radius: 8px;
                z-index: 10000;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                animation: slideInRight 0.3s ease;
            `;
            notification.textContent = message;

            document.body.appendChild(notification);

            // Auto-remove after 5 seconds
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.style.animation = 'slideOutRight 0.3s ease';
                    setTimeout(() => notification.remove(), 300);
                }
            }, 5000);
        }

        function showNotification(message, type = 'info') {
            // Create a temporary notification
            const notification = document.createElement('div');

            let backgroundColor = '#6c757d'; // default gray
            if (type === 'success') {
                backgroundColor = '#28a745'; // green
            } else if (type === 'error') {
                backgroundColor = '#dc3545'; // red
            } else if (type === 'warning') {
                backgroundColor = '#ffc107'; // yellow
            }

            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${backgroundColor};
                color: white;
                padding: 15px 20px;
                border-radius: 8px;
                z-index: 10000;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                animation: slideInRight 0.3s ease;
                max-width: 400px;
                word-wrap: break-word;
            `;
            notification.textContent = message;

            document.body.appendChild(notification);

            // Auto-remove after 3 seconds for success/warning, 5 seconds for error
            const timeout = type === 'error' ? 5000 : 3000;
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.style.animation = 'slideOutRight 0.3s ease';
                    setTimeout(() => notification.remove(), 300);
                }
            }, timeout);
        }

        // Enhanced folder buttons refresh function
        function refreshFolderButtons() {
            console.log('🔄 Refreshing folder buttons...');
            try {
                renderFolderButtons();
            } catch (error) {
                console.error('❌ Error refreshing folder buttons:', error);
            }
        }

        // Monitor folder buttons state
        function getFolderButtonsStatus() {
            return {
                ...folderButtonsState,
                containerExists: !!document.getElementById('folder-buttons'),
                categoriesLoaded: categories && categories.length > 0
            };
        }

        function openSavedLocation(category){
            fetch(`/list/${category.name}`)
              .then(r=>r.json())
              .then(files=>{
                  const sorted = (files||[]).slice().sort().reverse();
                  const latest = sorted[0] || null;

                  // Créer une boîte de dialogue modale avec le chemin du dossier
                  const modal = document.createElement('div');
                  modal.style.cssText = `
                      position: fixed;
                      top: 0;
                      left: 0;
                      width: 100%;
                      height: 100%;
                      background: rgba(0,0,0,0.8);
                      display: flex;
                      align-items: center;
                      justify-content: center;
                      z-index: 2000;
                  `;

                  const content = document.createElement('div');
                  content.style.cssText = `
                      background: #1a1a1a;
                      color: #eaeaea;
                      padding: 30px;
                      border-radius: 12px;
                      max-width: 600px;
                      width: 90%;
                      max-height: 80vh;
                      overflow-y: auto;
                      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                  `;

                  const listItems = sorted.map(f=>{
                      const d = f.replace(`${category.name}_`,'').replace('.txt','').split('-').reverse().join('/');
                      const displayName = f.replace(`${category.name}_`, '').replace('.txt', '');
                      return `<li style="margin: 8px 0; padding: 8px; background: #f8f9fa; border-radius: 6px;">
                          <a href="/read/${category.name}/${f}" target="_blank" style="text-decoration: none; color: #333;">
                              📄 ${displayName} — 📅 ${d}
                          </a>
                      </li>`;
                  }).join('');

                  content.innerHTML = `
                      <div style="border-bottom: 3px solid ${category.color}; padding-bottom: 15px; margin-bottom: 20px;">
                          <h2 style="margin: 0; color: ${category.color};">${category.emoji} ${category.name.charAt(0).toUpperCase() + category.name.slice(1)}</h2>
                      </div>

                      <div style="background: #222; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                          <strong style="color: #ccc;">📂 Ouvrir le dossier automatiquement :</strong><br>
                          <button onclick="openFolder('${category.name}')" style="background: #007bff; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-size: 16px; margin: 10px 0;">
                              🗂️ Ouvrir dans l'Explorateur Windows
                          </button>
                          <br><small style="color: #aaa;">(Le dossier s'ouvrira automatiquement dans une nouvelle fenêtre)</small>
                      </div>

                      ${latest ? `
                          <div style="margin-bottom: 20px;">
                              <a href="/read/${category.name}/${latest}" target="_blank" style="background: ${category.color}; color: white; padding: 12px 20px; text-decoration: none; border-radius: 6px; display: inline-block;">
                                  🚀 Ouvrir le dernier fichier (${latest.replace(`${category.name}_`, '').replace('.txt', '').split('-').reverse().join('/')})
                              </a>
                          </div>
                      ` : '<p style="color: #666; font-style: italic;">Aucun fichier dans cette catégorie</p>'}

                      <h3 style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 15px;">📋 Tous les fichiers (${sorted.length})</h3>
                      <ul style="list-style: none; padding: 0; margin: 0;">
                          ${listItems || '<li style="color: #666; font-style: italic; text-align: center; padding: 20px;">— Aucun fichier —</li>'}
                      </ul>

                      <div style="text-align: right; margin-top: 20px; border-top: 1px solid #333; padding-top: 15px;">
                          <button onclick="this.parentElement.parentElement.parentElement.remove()" style="background: #6c757d; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer;">
                              ❌ Fermer
                          </button>
                      </div>
                  `;

                  modal.appendChild(content);
                  document.body.appendChild(modal);

                  // Fermer en cliquant en dehors
                  modal.addEventListener('click', (e) => {
                      if (e.target === modal) {
                          modal.remove();
                      }
                  });
              })
              .catch((error)=>{
                  console.error('Erreur:', error);
                  // Pas de notification
              });
        }

        function createBackup() {
            const button = document.getElementById('backup-button');
            const originalText = button.innerHTML;
            
            // Désactiver le bouton et afficher le statut
            button.disabled = true;
            button.innerHTML = '⏳ Création du backup...';
            
            fetch('/backup_project', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showNotification('❌ Erreur lors de la création du backup: ' + data.error, 'error');
                } else {
                    showNotification('✅ Backup créé avec succès !', 'success');
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                showNotification('❌ Erreur de connexion lors de la création du backup', 'error');
            })
            .finally(() => {
                // Réactiver le bouton
                button.disabled = false;
                button.innerHTML = originalText;
            });
        }

        function limitInputLength(input, maxLength) {
            const currentLength = input.value.length;
            const counter = document.getElementById('char-counter');

            // Retirer les classes existantes
            input.classList.remove('at-limit', 'over-limit');

            // Mettre à jour le compteur
            if (counter) {
                counter.textContent = `${Math.min(currentLength, maxLength)}/${maxLength}`;
                if (currentLength >= maxLength) {
                    counter.style.color = '#ff6b6b';
                } else if (currentLength >= maxLength * 0.9) {
                    counter.style.color = '#FFA94D';
                } else {
                    counter.style.color = '#666';
                }
            }

            if (currentLength > maxLength) {
                input.value = input.value.substring(0, maxLength);
                input.classList.add('over-limit');
                // Pas de notification
                setTimeout(() => {
                    input.classList.remove('over-limit');
                }, 1000);
            } else if (currentLength === maxLength) {
                input.classList.add('at-limit');
            }
        }

        function handlePaste(input, maxLength) {
            setTimeout(() => {
                const originalLength = input.value.length;
                if (originalLength > maxLength) {
                    input.value = input.value.substring(0, maxLength);
                    input.classList.add('over-limit');
                    // Pas de notification
                    setTimeout(() => {
                        input.classList.remove('over-limit');
                    }, 1000);
                }
                limitInputLength(input, maxLength);
            }, 0);
        }

        function preventOverflow(input, maxLength) {
            // Empêcher la saisie si on atteint la limite
            if (input.value.length >= maxLength && event.key !== 'Backspace' && event.key !== 'Delete' &&
                event.key !== 'ArrowLeft' && event.key !== 'ArrowRight' &&
                event.key !== 'Home' && event.key !== 'End' &&
                event.key !== 'Tab' && !event.ctrlKey && !event.metaKey) {
                event.preventDefault();
                // Feedback visuel avec classe CSS
                input.classList.add('over-limit');
                setTimeout(() => {
                    input.classList.remove('over-limit');
                }, 300);
                return false;
            }
        }

        function showEraseConfirmation(name, color, emoji) {
            // Remove any existing modal first
            const existingModal = document.querySelector('.confirmation-modal-container');
            if(existingModal) existingModal.remove();

            const modal = document.createElement('div');
            modal.className = 'confirmation-modal-container fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50';
            modal.onclick = (e) => { if(e.target === modal) modal.remove(); };

            modal.innerHTML = `
                <div class="glass-effect rounded-xl p-6 text-center w-full max-w-md" onclick="event.stopPropagation()">
                    <div class="text-5xl mb-4">⚠️</div>
                    <h2 class="text-2xl font-display text-accent mb-2">Confirmation</h2>
                    <p class="mb-4">
                        Supprimer la catégorie <strong style="color:${color}">${emoji} ${name}</strong> ?<br>
                        <span class="text-accent font-bold">Cette action est définitive.</span>
                    </p>
                    <div class="flex justify-center gap-4">
                        <button class="h-12 px-6 font-bold text-white bg-primary/80 hover:bg-primary rounded-lg" onclick="this.closest('.confirmation-modal-container').remove()">Annuler</button>
                        <button class="h-12 px-6 font-bold text-white bg-accent hover:brightness-125 rounded-lg" onclick="eraseCategory('${name}'); this.closest('.confirmation-modal-container').remove()">Supprimer</button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }

        function eraseCategory(categoryName) {
            fetch(`/erase_category/${categoryName}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showNotification('❌ Erreur lors de la suppression: ' + data.error, 'error');
                } else {
                    showNotification('✅ Catégorie supprimée avec succès !', 'success');
                    // Recharger les catégories et les fichiers
                    loadCategories();
                    loadAllFiles();
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                showNotification('❌ Erreur de connexion lors de la suppression', 'error');
            });
        }

        // Recharger les fichiers toutes les 30 secondes
        setInterval(loadAllFiles, 30000);

        // ===== COMPREHENSIVE MONITORING SYSTEM =====
        
        // Health check function
        function performHealthCheck() {
            const status = {
                timestamp: new Date().toISOString(),
                categories: {
                    loaded: categories && categories.length > 0,
                    count: categories ? categories.length : 0,
                    valid: categories ? categories.every(cat => cat && cat.name && cat.emoji && cat.color) : false
                },
                dom: {
                    categoriesContainer: !!document.getElementById('categories-container'),
                    folderButtonsContainer: !!document.getElementById('folder-buttons'),
                    noteInput: !!document.getElementById('note-input')
                },
                folderButtons: getFolderButtonsStatus(),
                errors: {
                    count: folderButtonsState.errorCount,
                    maxRetries: folderButtonsState.maxRetries
                }
            };
            
            console.log('🏥 Health Check:', status);
            return status;
        }

        // Auto-recovery system
        function autoRecovery() {
            const status = performHealthCheck();

            // Check if folder buttons need recovery
            if (status.folderButtons && !status.folderButtons.isInitialized && status.categories.loaded) {
                console.log('🔄 Auto-recovery: Reinitializing folder buttons...');
                try {
                    renderFolderButtons();
                } catch (error) {
                    console.error('❌ Auto-recovery failed:', error);
                }
            }
            
            // Check if categories container is empty but categories are loaded
            const categoriesContainer = document.getElementById('categories-container');
            if (categoriesContainer && status.categories.loaded && categoriesContainer.children.length === 0) {
                console.log('🔄 Auto-recovery: Reinitializing categories...');
                try {
                    loadCategories();
                } catch (error) {
                    console.error('❌ Auto-recovery failed:', error);
                }
            }
        }

        // Run health check every 10 seconds
        setInterval(performHealthCheck, 10000);
        
        // Run auto-recovery every 30 seconds
        setInterval(autoRecovery, 30000);

        // Enhanced error handling for global errors
        window.addEventListener('error', function(event) {
            console.error('🚨 Global JavaScript Error:', {
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno,
                error: event.error
            });
            
            // If error is related to folder buttons, try to recover
            if (event.message && event.message.includes('folder')) {
                console.log('🔄 Attempting recovery for folder-related error...');
                setTimeout(() => {
                    try {
                        renderFolderButtons();
                    } catch (recoveryError) {
                        console.error('❌ Recovery failed:', recoveryError);
                    }
                }, 1000);
            }
        });

        // Debug function for manual testing
        window.debugFolderButtons = function() {
            console.log('🔧 Manual Debug Mode');
            console.log('Categories:', categories);
            console.log('Folder Buttons State:', folderButtonsState);
            console.log('Health Check:', performHealthCheck());

            // Force refresh
            refreshFolderButtons();
        };

        // ===== SLIDER TEST SYSTEM =====
        let scenarioSliderActive = false;

        function initializeScenarioSlider() {
            const triggerBtn = document.getElementById('scenario-slider-btn');
            const slider = document.getElementById('scenario-vertical-slider');

            if (!triggerBtn || !slider) {
                console.error('❌ Test slider elements not found');
                return;
            }

            // Ouvrir slider au survol de la souris
            triggerBtn.addEventListener('mouseenter', (e) => {
                e.stopPropagation();
                openScenarioSlider();
            });

            // Fermer slider quand la souris quitte le bouton ET le slider
            triggerBtn.addEventListener('mouseleave', (e) => {
                // Petit délai pour permettre de bouger vers le slider
                setTimeout(() => {
                    if (!slider.matches(':hover') && !triggerBtn.matches(':hover')) {
                        closeScenarioSlider();
                    }
                }, 100);
            });

            // Garder le slider ouvert quand on survole le slider lui-même
            slider.addEventListener('mouseenter', () => {
                // Rien à faire, on garde ouvert
            });

            slider.addEventListener('mouseleave', () => {
                // Petit délai avant de fermer pour éviter les fermetures accidentelles
                setTimeout(() => {
                    if (!slider.matches(':hover') && !triggerBtn.matches(':hover')) {
                        closeScenarioSlider();
                    }
                }, 150);
            });

            // Fermer slider when clicking outside
            document.addEventListener('click', (e) => {
                if (!triggerBtn.contains(e.target) && !slider.contains(e.target)) {
                    closeScenarioSlider();
                }
            });

            // Close slider on Escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && scenarioSliderActive) {
                    closeScenarioSlider();
                }
            });

            console.log('✅ Test slider initialized with hover behavior');
        }

        // Fonction supprimée - plus utilisée avec le comportement hover

        function openScenarioSlider() {
            const triggerBtn = document.getElementById('scenario-slider-btn');
            const slider = document.getElementById('scenario-vertical-slider');

            triggerBtn.classList.add('active');
            slider.classList.add('active');
            scenarioSliderActive = true;

            console.log('🔽 Scenario slider opened');
        }

        function closeScenarioSlider() {
            const triggerBtn = document.getElementById('scenario-slider-btn');
            const slider = document.getElementById('scenario-vertical-slider');

            triggerBtn.classList.remove('active');
            slider.classList.remove('active');
            scenarioSliderActive = false;

            console.log('🔼 Test slider closed');
        }

        // Actions des boutons du slider test
        function changeCategoryColor() {
            console.log('🎨 Changing category color...');

            // Créer une fenêtre modale pour changer la couleur
            const modalContent = document.createElement('div');
            modalContent.className = 'modal-content';
            modalContent.style.cssText = `
                background: #1a1a1a;
                color: #eaeaea;
                padding: 30px;
                border-radius: 12px;
                max-width: 600px;
                width: 90%;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            `;

            modalContent.innerHTML = `
                <div style="border-bottom: 3px solid #FF6B6B; padding-bottom: 15px; margin-bottom: 20px;">
                    <h2 style="margin: 0; color: #FF6B6B;">🎨 Changer la Couleur</h2>
                    <p style="color: #666; margin: 5px 0 0 0;">Choisissez une nouvelle couleur pour vos tests</p>
                </div>

                <div id="color-selector" style="margin-bottom: 20px;">
                    <p style="margin-bottom: 15px; color: #666;">Cliquez sur une couleur :</p>
                    <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px;">
                        <button onclick="selectColor('#FF6B6B')" style="background: #FF6B6B; width: 40px; height: 40px; border: none; border-radius: 8px; cursor: pointer; border: 3px solid #FF6B6B;"></button>
                        <button onclick="selectColor('#4ECDC4')" style="background: #4ECDC4; width: 40px; height: 40px; border: none; border-radius: 8px; cursor: pointer;"></button>
                        <button onclick="selectColor('#45B7D1')" style="background: #45B7D1; width: 40px; height: 40px; border: none; border-radius: 8px; cursor: pointer;"></button>
                        <button onclick="selectColor('#FFA07A')" style="background: #FFA07A; width: 40px; height: 40px; border: none; border-radius: 8px; cursor: pointer;"></button>
                        <button onclick="selectColor('#98D8C8')" style="background: #98D8C8; width: 40px; height: 40px; border: none; border-radius: 8px; cursor: pointer;"></button>
                        <button onclick="selectColor('#F7DC6F')" style="background: #F7DC6F; width: 40px; height: 40px; border: none; border-radius: 8px; cursor: pointer;"></button>
                        <button onclick="selectColor('#BB8FCE')" style="background: #BB8FCE; width: 40px; height: 40px; border: none; border-radius: 8px; cursor: pointer;"></button>
                        <button onclick="selectColor('#85C1E9')" style="background: #85C1E9; width: 40px; height: 40px; border: none; border-radius: 8px; cursor: pointer;"></button>
                        <button onclick="selectColor('#F8C471')" style="background: #F8C471; width: 40px; height: 40px; border: none; border-radius: 8px; cursor: pointer;"></button>
                        <button onclick="selectColor('#82E0AA')" style="background: #82E0AA; width: 40px; height: 40px; border: none; border-radius: 8px; cursor: pointer;"></button>
                        <button onclick="selectColor('#F1948A')" style="background: #F1948A; width: 40px; height: 40px; border: none; border-radius: 8px; cursor: pointer;"></button>
                        <button onclick="selectColor('#AED6F1')" style="background: #AED6F1; width: 40px; height: 40px; border: none; border-radius: 8px; cursor: pointer;"></button>
                    </div>
                </div>

                <div style="text-align: right; border-top: 1px solid #eee; padding-top: 15px;">
                    <button onclick="modalManager.close(this.closest('.modal-content'))" style="background: #6c757d; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; margin-right: 10px;">
                        Annuler
                    </button>
                    <button onclick="applyColorChange()" style="background: #FF6B6B; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer;">
                        ✅ Appliquer
                    </button>
                </div>
            `;

            modalManager.open(modalContent);
            closeScenarioSlider();
        }

        let selectedColor = '#FF6B6B';

        function selectColor(color) {
            selectedColor = color;
            // Mettre à jour la bordure des boutons de couleur
            const colorButtons = document.querySelectorAll('#color-selector button');
            colorButtons.forEach(btn => {
                btn.style.border = 'none';
            });
            event.target.style.border = '3px solid #333';
        }

        function applyColorChange() {
            // Ici on pourrait sauvegarder la nouvelle couleur
            console.log('🎨 Nouvelle couleur appliquée:', selectedColor);
            showNotification('✅ Couleur changée avec succès !', 'success');
            modalManager.close(document.querySelector('.modal-content'));
        }

        function renameCategory() {
            console.log('✏️ Renaming test category...');

            // Créer une fenêtre modale pour renommer la catégorie
            const modalContent = document.createElement('div');
            modalContent.className = 'modal-content';
            modalContent.style.cssText = `
                background: #1a1a1a;
                color: #eaeaea;
                padding: 30px;
                border-radius: 12px;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            `;

            modalContent.innerHTML = `
                <div style="border-bottom: 3px solid #FF6B6B; padding-bottom: 15px; margin-bottom: 20px;">
                    <h2 style="margin: 0; color: #FF6B6B;">✏️ Renommer le Dossier</h2>
                    <p style="color: #666; margin: 5px 0 0 0;">Entrez le nouveau nom pour vos tests</p>
                </div>

                <div style="margin-bottom: 20px;">
                    <label for="new-category-name" style="display: block; margin-bottom: 8px; font-weight: 500; color: #333;">Nouveau nom :</label>
                    <input type="text"
                           id="new-category-name"
                           placeholder="Nouveau nom pour test (max 19 caractères)"
                           maxlength="19"
                           style="width: 100%; padding: 12px; border: 2px solid #e9ecef; border-radius: 8px; font-size: 16px; box-sizing: border-box;"
                           oninput="updateCharCounter(this)">
                    <div id="char-counter" style="text-align: right; font-size: 12px; color: #666; margin-top: 5px;">0/19</div>
                </div>

                <div style="text-align: right; border-top: 1px solid #eee; padding-top: 15px;">
                    <button onclick="modalManager.close(this.closest('.modal-content'))" style="background: #6c757d; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; margin-right: 10px;">
                        Annuler
                    </button>
                    <button onclick="applyRename()" style="background: #FF6B6B; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer;">
                        ✅ Renommer
                    </button>
                </div>
            `;

            modalManager.open(modalContent);
            closeScenarioSlider();

            // Focus sur le champ input après un petit délai
            setTimeout(() => {
                const input = document.getElementById('new-category-name');
                if (input) input.focus();
            }, 100);
        }

        function updateCharCounter(input) {
            const counter = document.getElementById('char-counter');
            const length = input.value.length;
            counter.textContent = `${length}/19`;

            if (length > 17) {
                counter.style.color = '#ff6b6b';
            } else if (length > 15) {
                counter.style.color = '#ffa500';
            } else {
                counter.style.color = '#666';
            }
        }

        function applyRename() {
            const newName = document.getElementById('new-category-name').value.trim();

            if (!newName) {
                showNotification('❌ Veuillez entrer un nom valide', 'error');
                return;
            }

            if (newName.length > 19) {
                showNotification('❌ Le nom ne peut pas dépasser 19 caractères', 'error');
                return;
            }

            // Ici on pourrait envoyer la requête pour renommer la catégorie test
            console.log('✏️ Nouveau nom appliqué pour test:', newName);
            showNotification(`✅ Dossier test renommé en "${newName}" !`, 'success');
            modalManager.close(document.querySelector('.modal-content'));
        }

        function deleteCategory() {
            console.log('🗑️ Deleting test category...');

            // Créer une fenêtre modale de confirmation pour supprimer
            const modalContent = document.createElement('div');
            modalContent.className = 'modal-content';
            modalContent.style.cssText = `
                background: #1a1a1a;
                color: #eaeaea;
                padding: 30px;
                border-radius: 12px;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            `;

            modalContent.innerHTML = `
                <div style="border-bottom: 3px solid #dc3545; padding-bottom: 15px; margin-bottom: 20px;">
                    <h2 style="margin: 0; color: #dc3545;">⚠️ Supprimer le Dossier</h2>
                    <p style="color: #666; margin: 5px 0 0 0;">Cette action est irréversible !</p>
                </div>

                <div style="background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 8px; padding: 15px; margin-bottom: 20px;">
                    <div style="font-size: 48px; text-align: center; margin-bottom: 10px;">🗑️</div>
                    <p style="color: #721c24; margin: 0; text-align: center; font-weight: 500;">
                        Êtes-vous sûr de vouloir supprimer le dossier "Test" ?
                    </p>
                    <p style="color: #721c24; margin: 10px 0 0 0; font-size: 14px; text-align: center;">
                        Tous les fichiers de test seront supprimés définitivement.
                    </p>
                </div>

                <div style="display: flex; gap: 10px; justify-content: flex-end;">
                    <button onclick="modalManager.close(this.closest('.modal-content'))" style="background: #6c757d; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer;">
                        ❌ Annuler
                    </button>
                    <button onclick="confirmDeleteCategory()" style="background: #dc3545; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-weight: 600;">
                        🗑️ Supprimer Définitivement
                    </button>
                </div>
            `;

            modalManager.open(modalContent);
            closeScenarioSlider();
        }

        function confirmDeleteCategory() {
            // Ici on pourrait envoyer la requête pour supprimer la catégorie test
            console.log('🗑️ Catégorie test supprimée');
            showNotification('✅ Dossier test supprimé avec succès !', 'success');
            modalManager.close(document.querySelector('.modal-content'));
        }

        function openScenario(date) {
            // Ouvrir un test spécifique
            const filename = `test_${date}.txt`;
            window.open(`/read/test/${filename}`, '_blank');
            console.log(`📖 Opening test: ${filename}`);
        }

        // Initialize monitoring on page load
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🚀 Application initialized with enhanced monitoring');

            // Initialize scenario slider
            initializeScenarioSlider();

            // Initial health check after 2 seconds
            setTimeout(performHealthCheck, 2000);
        });

        // Button Visual Feedback Functions
        function handleFusionButtonClick(button, type) {
            // Add visual feedback
            addButtonClickFeedback(button);
            
            // Show modal after a short delay for visual feedback
            setTimeout(() => {
                showFusionModal(type);
            }, 150);
        }
        
        function addButtonClickFeedback(button) {
            // Remove any existing states
            button.classList.remove('clicked', 'processing', 'success', 'error');
            
            // Add clicked state
            button.classList.add('clicked');
            
            // Add processing state after a short delay
            setTimeout(() => {
                button.classList.remove('clicked');
                button.classList.add('processing');
            }, 200);
        }
        
        function setButtonState(button, state) {
            // Remove all states
            button.classList.remove('clicked', 'processing', 'success', 'error');
            
            if (state) {
                button.classList.add(state);
                
                // Auto-remove success/error states after animation
                if (state === 'success' || state === 'error') {
                    setTimeout(() => {
                        button.classList.remove(state);
                    }, 2000);
                }
            }
        }
        
        function addCategoryButtonClickFeedback(button) {
            // Remove any existing states except clicked
            button.classList.remove('processing', 'success', 'error');
            
            // Add clicked state and keep it
            button.classList.add('clicked');
        }

        // Fusion Modal Functions
        function showFusionModal(type) {
            const modal = document.getElementById('fusionModal');
            const title = document.getElementById('fusionModalTitle');
            const content = document.getElementById('fusionModalContent');

            if (!modal || !title || !content) {
                console.error('❌ Fusion modal elements not found');
                return;
            }
            
            if (type === 'global') {
                title.textContent = '🔗 Fusion Globale';
                content.innerHTML = `
                    <div class="fusion-options">
                        <div class="fusion-option">
                            <span style="font-size: 2rem;">📚</span>
                            <div>
                                <strong>Fusionner toutes les notes</strong>
                                <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9rem;">
                                    Toutes les notes de toutes les catégories seront fusionnées en un seul fichier dans le dossier "fusion_global"
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="fusion-actions">
                        <button class="fusion-action-btn secondary" onclick="closeFusionModal()">Annuler</button>
                        <button class="fusion-action-btn primary" onclick="executeFusion('global')">🔗 Fusionner Tout</button>
                    </div>
                `;
            } else if (type === 'category') {
                title.textContent = '📁 Fusion par Catégorie';
                content.innerHTML = `
                    <div class="fusion-options" id="categoryOptions">
                        <p style="margin: 0 0 15px 0; color: #666;">Cliquez sur une catégorie pour fusionner tous ses fichiers :</p>
                        <!-- Categories will be loaded dynamically -->
                    </div>
                    <div class="fusion-actions">
                        <button class="fusion-action-btn secondary" onclick="closeFusionModal()">Fermer</button>
                    </div>
                `;
                loadCategoryButtons();
            }
            
            modal.style.display = 'block';
        }

        function closeFusionModal() {
            // Reset all button states when closing modal
            resetAllButtonStates();

            // Close the modal
            const modal = document.getElementById('fusionModal');
            if (modal) {
                modal.style.display = 'none';
            } else {
                console.error('❌ Fusion modal not found for closing');
            }
        }
        
        function resetAllButtonStates() {
            // Reset main fusion buttons
            const mainButtons = document.querySelectorAll('.fusion-btn');
            mainButtons.forEach(button => {
                button.classList.remove('clicked', 'processing', 'success', 'error');
            });
            
            // Reset category buttons in modal
            const categoryButtons = document.querySelectorAll('.fusion-option');
            categoryButtons.forEach(button => {
                button.classList.remove('clicked', 'processing', 'success', 'error');
            });
        }

        function loadCategoryButtons() {
            const container = document.getElementById('categoryOptions');
            if (!categories || categories.length === 0) {
                container.innerHTML = '<p style="color: #666; text-align: center;">Aucune catégorie disponible</p>';
                return;
            }
            
            let buttonsHtml = '<p style="margin: 0 0 15px 0; color: #666;">Cliquez sur une catégorie pour fusionner tous ses fichiers :</p>';
            categories.forEach(cat => {
                buttonsHtml += `
                    <div class="fusion-option" 
                         onclick="handleCategoryButtonClick(this, '${cat.name}')"
                         role="button"
                         tabindex="0"
                         aria-label="Fusionner tous les fichiers de la catégorie ${cat.name}">
                        <span style="font-size: 1.5rem;">${cat.emoji}</span>
                        <div style="flex: 1;">
                            <strong>${cat.name}</strong>
                            <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9rem;">
                                Cliquez pour fusionner tous les fichiers de cette catégorie
                            </p>
                        </div>
                        <span style="color: #6A4C93; font-size: 1.2rem;">→</span>
                    </div>
                `;
            });
            container.innerHTML = buttonsHtml;
        }

        function executeFusion(type) {
            if (type === 'global') {
                // Get the global fusion button for visual feedback
                const globalButton = document.querySelector('.fusion-btn:not(.secondary)');
                
                // Fusion globale
                fetch('/fusion/global', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => {
                    // Check if response is ok (status 200-299)
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        // Keep button blue (clicked state) - don't change to success
                        showNotification('✅ Fusion globale réussie !', 'success');
                        closeFusionModal();
                    } else {
                        // Keep button blue (clicked state) - don't change to error
                        showNotification('❌ Erreur lors de la fusion : ' + data.error, 'error');
                    }
                })
                .catch(error => {
                    console.error('Erreur:', error);
                    // Keep button blue (clicked state) - don't change to error
                    showNotification('❌ Erreur lors de la fusion globale: ' + error.message, 'error');
                });
            }
        }

        function handleCategoryButtonClick(button, categoryName) {
            // Add visual feedback
            addCategoryButtonClickFeedback(button);
            
            // Execute fusion after visual feedback
            setTimeout(() => {
                executeSingleCategoryFusion(categoryName, button);
            }, 300);
        }
        
        function executeSingleCategoryFusion(categoryName, buttonElement = null) {
            // Fusion d'une seule catégorie
            fetch('/fusion/single-category', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ category: categoryName })
            })
            .then(response => {
                // Check if response is ok (status 200-299)
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Keep button blue (clicked state) - don't change to success
                    showNotification(`✅ Fusion de la catégorie "${categoryName}" réussie !`, 'success');
                    // Don't close modal automatically - let user see the blue button
                } else {
                    // Keep button blue (clicked state) - don't change to error
                    showNotification('❌ Erreur lors de la fusion : ' + data.error, 'error');
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                // Keep button blue (clicked state) - don't change to error
                showNotification('❌ Erreur lors de la fusion de la catégorie: ' + error.message, 'error');
            });
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('fusionModal');
            if (event.target === modal) {
                closeFusionModal();
            }
        }
        
        // Debug function to test visual feedback (remove in production)
        function testVisualFeedback() {
            console.log('🧪 Testing visual feedback...');
            const globalButton = document.querySelector('.fusion-btn:not(.secondary)');
            if (globalButton) {
                console.log('Testing global button states...');
                setButtonState(globalButton, 'clicked');
                setTimeout(() => setButtonState(globalButton, 'processing'), 500);
                setTimeout(() => setButtonState(globalButton, 'success'), 1000);
                setTimeout(() => setButtonState(globalButton, 'error'), 2000);
                setTimeout(() => setButtonState(globalButton, null), 3000);
            }
        }
        
        // Make test function available globally for debugging
        window.testVisualFeedback = testVisualFeedback;