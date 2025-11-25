// Main script for Deuxième Cerveau - Orchestrator
// This file handles initialization, event listeners, and main application flow

// Import modules
import * as api from './api.js';
import * as ui from './ui.js';
import * as state from './state.js';
import * as alphabet from './alphabet.js';

// ===== PARTITIONING SYSTEM FUNCTIONS =====
// These functions remain in main script as they handle core UI state management

function initializePartitioning() {
    console.log('🚀 Initializing dynamic partitioning system...');

    // Load saved state
    state.loadPartitioningState();

    // Set up content observers for auto-expansion
    setupContentObservers();

    // Initialize section interactions
    initializeSectionInteractions();

    // Set up responsive behavior
    setupResponsiveBehavior();

    console.log('✅ Dynamic partitioning system initialized');
}

function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    const content = section.querySelector('.section-content');
    const icon = section.querySelector('.collapse-icon');
    const sectionState = state.getPartitioningState().sections[sectionId];

    if (!section || !content || !icon) {
        console.error('❌ Section elements not found:', sectionId);
        return;
    }

    const newCollapsed = !sectionState.collapsed;
    state.updatePartitioningSection(sectionId, { collapsed: newCollapsed });

    if (newCollapsed) {
        content.classList.add('collapsed');
        icon.style.transform = 'rotate(-90deg)';
        section.style.minHeight = '60px';
    } else {
        content.classList.remove('collapsed');
        icon.style.transform = 'rotate(0deg)';
        section.style.minHeight = '200px';
        // Auto-expand based on content
        if (state.getPartitioningState().autoExpansion) {
            adjustSectionSize(sectionId);
        }
    }

    state.savePartitioningState();
    console.log(`🔄 Section ${sectionId} ${newCollapsed ? 'collapsed' : 'expanded'}`);
}

// ===== MAIN APPLICATION FUNCTIONS =====

async function initializeApp() {
    console.log('🚀 Initializing Deuxième Cerveau...');

    try {
        // Initialize partitioning system
        initializePartitioning();

        // Load initial data
        console.log('🚀 Loading initial data...');

        // Try to load structured categories first
        let structured = null;
        try {
            structured = await api.loadCategoriesStructured();
            console.log('📂 Structured categories loaded:', structured);
        } catch (error) {
            console.warn('⚠️ Could not load structured categories, falling back to flat');
        }

        // Also load flat categories for backward compatibility
        const categories = await api.loadCategories();
        console.log('📂 Categories loaded from backend:', categories.map(c => c.name));
        console.log('📊 Total categories loaded:', categories.length);
        const allFiles = await api.loadAllFiles();

        state.setCategories(categories);
        state.setAllFiles(allFiles);

        // Initialize UI
        ui.updateFilterButtons(state.getCategories(), state.getCurrentFilter(), filterFiles);

        // Initialize alphabet buttons
        alphabet.initializeAlphabetButtons(filterByLetter);

        // Use structured rendering if available, otherwise fall back to flat
        if (structured && structured.parents.length > 0) {
            console.log('✨ Using hierarchical folder structure');
            ui.renderFolderButtonsStructured(structured, handleOpenFolder, handleDeleteCategory);
        } else {
            console.log('📋 Using flat folder structure');
            ui.renderFolderButtons(state.getCategories(), handleOpenFolder, handleDeleteCategory);
        }

        ui.renderCategories(state.getCategories(), handleSaveNote, handleDeleteCategory);
        ui.displayFiles(state.getFilteredFiles(), state.getCategories());

        // Set up event listeners
        setupEventListeners();

        console.log('✅ Application initialized successfully');
    } catch (error) {
        console.error('❌ Error initializing application:', error);
        ui.showNotification('Erreur lors de l\'initialisation de l\'application', 'error');
    }
}

function setupEventListeners() {
    // Add category functionality
    const addCategoryBtn = document.getElementById('add-category-button');
    const newCategoryInput = document.getElementById('new-category-name');

    if (addCategoryBtn && newCategoryInput) {
        addCategoryBtn.addEventListener('click', handleAddCategory);
        newCategoryInput.addEventListener('input', () => {
            ui.updateCharCounter(newCategoryInput);
        });
    }

    // Backup functionality
    const backupBtn = document.getElementById('backup-button');
    if (backupBtn) {
        backupBtn.addEventListener('click', handleCreateBackup);
    }

    // Fusion buttons
    const globalFusionBtn = document.querySelector('button[onclick*="global"]');
    const categoryFusionBtn = document.querySelector('button[onclick*="category"]');

    if (globalFusionBtn) {
        globalFusionBtn.addEventListener('click', () => handleShowFusionModal('global'));
    }

    if (categoryFusionBtn) {
        categoryFusionBtn.addEventListener('click', () => handleShowFusionModal('category'));
    }

    // Fusion modal background click to close
    const fusionModal = document.getElementById('fusionModal');
    if (fusionModal) {
        fusionModal.addEventListener('click', (e) => {
            // Close modal only if clicking on the background, not on the modal content
            if (e.target === fusionModal) {
                ui.closeFusionModal();
            }
        });
    }
}

// ===== EVENT HANDLERS =====

async function handleSaveNote(category) {
    const text = document.getElementById('note-input').value.trim();
    if (!text) {
        ui.showNotification('Veuillez entrer du texte', 'error');
        return;
    }

    try {
        await api.quickSave(category, text);
        document.getElementById('note-input').value = '';

        // Try to refresh data but don't block if it fails
        try {
            const allFiles = await api.loadAllFiles();
            state.setAllFiles(allFiles);
            ui.displayFiles(state.getFilteredFiles(), state.getCategories());
        } catch (refreshError) {
            console.warn('Could not refresh data after save:', refreshError);
            // Don't show error to user, just log it
        }
    } catch (error) {
        ui.showNotification('Erreur lors de la sauvegarde', 'error');
    }
}

async function handleAddCategory() {
    const input = document.getElementById('new-category-name');
    const name = input.value.trim();

    if (!name) {
        ui.showNotification('Veuillez entrer un nom de catégorie', 'error');
        return;
    }

    try {
        const newCategory = await api.addNewCategory(name);
        state.addCategory(newCategory);
        input.value = '';

        // Refresh UI
        console.log('🔄 Refreshing UI after category addition');
        console.log('📂 Current categories in state:', state.getCategories().map(c => c.name));
        ui.updateFilterButtons(state.getCategories(), state.getCurrentFilter(), filterFiles);
        ui.renderFolderButtons(state.getCategories(), handleOpenFolder, handleDeleteCategory);
        ui.renderCategories(state.getCategories(), handleSaveNote, handleDeleteCategory);
    } catch (error) {
        // Error already handled in API function
    }
}

async function handleCreateBackup() {
    const button = document.getElementById('backup-button');
    const originalText = button.innerHTML;

    // Désactiver le bouton et afficher le statut
    button.disabled = true;
    button.innerHTML = '⏳ Création du backup...';

    try {
        const result = await api.createBackup();
        ui.showNotification(`✅ Backup créé: ${result.filename}`, 'success');
    } catch (error) {
        // Error already handled in API function, but show generic error if needed
        ui.showNotification('❌ Erreur lors de la création du backup', 'error');
    } finally {
        // Réactiver le bouton
        button.disabled = false;
        button.innerHTML = originalText;
    }
}

function filterFiles(filterType) {
    state.setCurrentFilter(filterType);
    ui.displayFiles(state.getFilteredFiles(), state.getCategories());
    ui.updateFilterButtons(state.getCategories(), state.getCurrentFilter(), filterFiles);

    // Update alphabet buttons to reflect current selection
    alphabet.updateAlphabetButtons(state.getCurrentLetter(), filterByLetter);
}

/**
 * Filter files by first letter
 * @param {string} letter - Letter to filter by (or 'all' for no filter)
 */
function filterByLetter(letter) {
    console.log(`🔤 Filtering by letter: ${letter}`);
    state.setCurrentLetter(letter);
    ui.displayFiles(state.getFilteredFiles(), state.getCategories());

    // Update UI to reflect current selections
    alphabet.updateAlphabetButtons(state.getCurrentLetter(), filterByLetter);
    ui.updateFilterButtons(state.getCategories(), state.getCurrentFilter(), filterFiles);
}

async function handleOpenFolder(categoryName) {
    try {
        await api.openFolder(categoryName);
        ui.showNotification(`Dossier ouvert: ${categoryName}`, 'success');
    } catch (error) {
        ui.showNotification('Erreur lors de l\'ouverture du dossier', 'error');
    }
}

async function handleDeleteCategory(category) {
    ui.showEraseConfirmation(category.name, category.color, category.emoji, confirmDeleteCategory);
}

async function confirmDeleteCategory(categoryName) {
    try {
        await api.deleteCategory(categoryName);
        state.removeCategory(categoryName);

        // Refresh data and UI
        const allFiles = await api.loadAllFiles();
        state.setAllFiles(allFiles);

        console.log('🔄 Refreshing UI after category deletion');
        console.log('📂 Remaining categories in state:', state.getCategories().map(c => c.name));
        ui.updateFilterButtons(state.getCategories(), state.getCurrentFilter(), filterFiles);
        ui.renderFolderButtons(state.getCategories(), handleOpenFolder, handleDeleteCategory);
        ui.renderCategories(state.getCategories(), handleSaveNote, handleDeleteCategory);
        ui.displayFiles(state.getFilteredFiles(), state.getCategories());
    } catch (error) {
        // Error already handled in API function
    }
}

function handleShowFusionModal(type) {
    ui.showFusionModal(type, state.getCategories(), handleGlobalFusion, handleCategoryFusion);
}

async function handleGlobalFusion() {
    try {
        const result = await api.performGlobalFusion();
        ui.showNotification(`Fusion globale terminée: ${result.filename}`, 'success');
    } catch (error) {
        ui.showNotification('Erreur lors de la fusion globale', 'error');
    }
}

async function handleCategoryFusion() {
    const selectedCheckboxes = document.querySelectorAll('#fusionModal input[type="checkbox"]:checked');
    const selectedCategories = Array.from(selectedCheckboxes).map(cb => cb.value);

    if (selectedCategories.length === 0) {
        ui.showNotification('Veuillez sélectionner au moins une catégorie', 'error');
        return;
    }

    try {
        const result = await api.performCategoryFusion(selectedCategories);
        ui.showNotification(`Fusion par catégories terminée: ${result.filename}`, 'success');
    } catch (error) {
        ui.showNotification('Erreur lors de la fusion par catégories', 'error');
    }
}

// ===== PARTITIONING HELPER FUNCTIONS =====
// These remain in main script for partitioning logic

function setupContentObservers() {
    // Implementation for content observers
    // This would be the detailed implementation from the original file
}

function initializeSectionInteractions() {
    // Set up click handlers for section headers
    document.querySelectorAll('.section-header').forEach(header => {
        header.addEventListener('click', (e) => {
            // Don't trigger if clicking on buttons within the header
            if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
                return;
            }
            const sectionId = header.closest('.dynamic-section').id;
            toggleSection(sectionId);
        });
    });
}

function setupResponsiveBehavior() {
    // Implementation for responsive behavior
    // This would be the detailed implementation from the original file
}

function adjustSectionSize(sectionId) {
    // Implementation for adjusting section size
    // This would be the detailed implementation from the original file
}

// ===== FUSION FUNCTIONS =====

// Handle fusion button clicks
function handleFusionButtonClick(button, type) {
    console.log('🔗 Handling fusion button click:', type);

    // Add visual feedback
    addButtonClickFeedback(button);

    // Disable button temporarily to prevent double-clicks
    button.disabled = true;
    button.style.opacity = '0.7';

    // Show modal after a short delay for visual feedback
    setTimeout(() => {
        ui.showFusionModal(type, state.getCategories(), handleGlobalFusion, handleCategoryFusion);
        // Re-enable button after modal is shown
        setTimeout(() => {
            button.disabled = false;
            button.style.opacity = '';
        }, 200);
    }, 150);
}

function addButtonClickFeedback(button) {
    // Add visual feedback to button
    button.style.transform = 'scale(0.95)';
    button.style.opacity = '0.8';

    // Reset after animation
    setTimeout(() => {
        button.style.transform = '';
        button.style.opacity = '';
    }, 150);
}

// Global functions for button onclick handlers
function handleCategoryDelete(event, categoryName, categoryColor, categoryEmoji) {
    event.stopPropagation();
    const category = { name: categoryName, color: categoryColor, emoji: categoryEmoji };
    handleDeleteCategory(category);
}

function handleFolderOpen(event, categoryName) {
    event.stopPropagation();
    handleOpenFolder(categoryName);
}

function handleFolderDelete(event, categoryName, categoryColor, categoryEmoji) {
    event.stopPropagation();
    const category = { name: categoryName, color: categoryColor, emoji: categoryEmoji };
    handleDeleteCategory(category);
}

// ===== INPUT VALIDATION FUNCTIONS =====

/**
 * Limit input length and update character counter
 * @param {HTMLInputElement} input - The input element
 * @param {number} maxLength - Maximum allowed length
 */
function limitInputLength(input, maxLength) {
    const currentLength = input.value.length;
    const counter = document.getElementById('char-counter');

    if (counter) {
        counter.textContent = `${currentLength}/${maxLength}`;

        // Visual feedback when approaching limit
        if (currentLength >= maxLength) {
            counter.style.color = '#ef4444'; // Red
        } else if (currentLength >= maxLength * 0.8) {
            counter.style.color = '#f59e0b'; // Orange
        } else {
            counter.style.color = 'rgba(0, 246, 255, 0.6)'; // Primary color
        }
    }

    // Enforce max length
    if (currentLength > maxLength) {
        input.value = input.value.substring(0, maxLength);
    }
}

// ===== PARENT FOLDER TOGGLE =====

/**
 * Toggle parent folder expansion/collapse
 * @param {string} parentId - ID of the parent folder container
 */
function toggleParentFolder(parentId) {
    const container = document.getElementById(parentId);
    const header = container.previousElementSibling;
    const icon = header.querySelector('.collapse-icon');

    if (container.classList.contains('hidden')) {
        // Expand
        container.classList.remove('hidden');
        icon.style.transform = 'rotate(0deg)';
        localStorage.setItem(parentId, 'expanded');
    } else {
        // Collapse
        container.classList.add('hidden');
        icon.style.transform = 'rotate(-90deg)';
        localStorage.setItem(parentId, 'collapsed');
    }
}

// ===== GLOBAL EXPORTS =====
// Expose functions needed by HTML onclick attributes IMMÉDIATEMENT
window.handleFusionButtonClick = handleFusionButtonClick;
window.createBackup = handleCreateBackup;
window.addNewCategory = handleAddCategory;
window.toggleSection = toggleSection;
window.handleCategoryDelete = handleCategoryDelete;
window.handleFolderOpen = handleFolderOpen;
window.handleFolderDelete = handleFolderDelete;
window.filterFiles = filterFiles;
window.filterByLetter = filterByLetter;
window.confirmDeleteCategory = confirmDeleteCategory;
window.handleGlobalFusion = handleGlobalFusion;
window.handleCategoryFusion = handleCategoryFusion;
window.limitInputLength = limitInputLength;
window.toggleParentFolder = toggleParentFolder;

// Expose alphabet filter function globally for direct HTML access if needed
window.filterByAlphabet = (letter) => {
    filterByLetter(letter);
};

// Additional functions needed by HTML onclick handlers
window.handleGlobalFusionClick = (button) => handleFusionButtonClick(button, 'global');
window.handleCategoryFusionClick = (button) => handleFusionButtonClick(button, 'category');
window.openUploadModal = async () => {
    console.log('📤 Opening upload modal');
    const modal = document.getElementById('uploadModal');
    const categorySelect = document.getElementById('categorySelect');
    const uploadStatus = document.getElementById('uploadStatus');

    // Reset modal state
    document.getElementById('fileInput').value = '';
    uploadStatus.classList.add('hidden');
    uploadStatus.textContent = '';

    // Load categories
    try {
        const response = await fetch('/categories');
        if (!response.ok) throw new Error('Failed to load categories');
        const categories = await response.json();

        // Populate category dropdown
        categorySelect.innerHTML = '<option value="">-- Choisir une catégorie --</option>';
        categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.name;
            option.textContent = `${cat.emoji} ${cat.name}`;
            categorySelect.appendChild(option);
        });

        modal.classList.remove('hidden');
    } catch (error) {
        console.error('❌ Error loading categories:', error);
        alert('Erreur lors du chargement des catégories');
    }
};

window.closeUploadModal = () => {
    const modal = document.getElementById('uploadModal');
    if (modal) modal.classList.add('hidden');
};

window.uploadFile = async () => {
    console.log('📤 Starting file upload');
    const fileInput = document.getElementById('fileInput');
    const categorySelect = document.getElementById('categorySelect');
    const uploadStatus = document.getElementById('uploadStatus');
    const uploadBtn = document.getElementById('uploadConfirmBtn');

    // Validation
    if (!fileInput.files || fileInput.files.length === 0) {
        uploadStatus.textContent = '❌ Veuillez sélectionner un fichier';
        uploadStatus.className = 'text-sm text-center text-red-500';
        uploadStatus.classList.remove('hidden');
        return;
    }

    if (!categorySelect.value) {
        uploadStatus.textContent = '❌ Veuillez sélectionner une catégorie';
        uploadStatus.className = 'text-sm text-center text-red-500';
        uploadStatus.classList.remove('hidden');
        return;
    }

    // Disable button during upload
    uploadBtn.disabled = true;
    uploadBtn.textContent = '⏳ Téléchargement...';

    try {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('category', categorySelect.value);

        const response = await fetch('/upload_file', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Upload failed');
        }

        const result = await response.json();
        uploadStatus.textContent = `✅ ${result.message || 'Fichier téléchargé avec succès'}`;
        uploadStatus.className = 'text-sm text-center text-green-500';
        uploadStatus.classList.remove('hidden');

        // Close modal after 2 seconds
        setTimeout(() => {
            window.closeUploadModal();
        }, 2000);

    } catch (error) {
        console.error('❌ Upload error:', error);
        uploadStatus.textContent = `❌ Erreur: ${error.message}`;
        uploadStatus.className = 'text-sm text-center text-red-500';
        uploadStatus.classList.remove('hidden');
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Télécharger';
    }
};
window.openAllNotes = () => {
    window.open('/all_notes', '_blank');
};

// ===== GLOBAL FUNCTIONS FOR ONCLICK HANDLERS =====
// These functions are exposed to window for inline onclick handlers in UI

/**
 * Handle folder fusion backend - opens fusion page in new tab
 */
window.handleFolderFusionBackend = function(event, categoryName) {
    if (event) event.stopPropagation();
    console.log('🔗 Opening fusion for category:', categoryName);
    
    const fusionUrl = `/fusionner?dossier=${encodeURIComponent(categoryName)}`;
    window.open(fusionUrl, '_blank');
    ui.showNotification(`🔗 Fusion de la catégorie "${categoryName}" ouverte`, 'success');
};

/**
 * Handle folder open - opens folder in file explorer
 */
window.handleFolderOpen = async function(event, categoryName) {
    if (event) event.stopPropagation();
    console.log('📁 Opening folder for category:', categoryName);
    
    try {
        await api.openFolder(categoryName);
        ui.showNotification(`📁 Dossier ouvert: ${categoryName}`, 'success');
    } catch (error) {
        console.error('❌ Error opening folder:', error);
        ui.showNotification('❌ Erreur lors de l\'ouverture du dossier', 'error');
    }
};

/**
 * Handle folder delete - shows confirmation dialog
 */
window.handleFolderDelete = function(event, categoryName, color, emoji) {
    if (event) event.stopPropagation();
    console.log('🗑️ Delete requested for category:', categoryName);
    
    const category = { name: categoryName, color: color, emoji: emoji };
    handleDeleteCategory(category);
};

/**
 * Toggle parent folder expansion
 */
window.toggleParentFolder = function(folderId) {
    const container = document.getElementById(folderId);
    const icon = container?.previousElementSibling?.querySelector('.collapse-icon, .toggle-icon');
    
    if (container) {
        const isHidden = container.classList.contains('hidden');
        container.classList.toggle('hidden');
        
        if (icon) {
            icon.style.transform = isHidden ? 'rotate(0deg)' : 'rotate(-90deg)';
        }
        
        // Save state to localStorage
        localStorage.setItem(folderId, isHidden ? 'expanded' : 'collapsed');
    }
};

// ===== SAFETY CHECK =====
// Vérifier que toutes les fonctions critiques sont exposées
function verifyGlobalFunctions() {
    const requiredFunctions = [
        'handleFusionButtonClick', 'createBackup', 'addNewCategory',
        'handleCategoryDelete', 'handleFolderOpen', 'handleFolderDelete',
        'filterFiles', 'filterByLetter', 'toggleSection', 'confirmDeleteCategory',
        'handleGlobalFusion', 'handleCategoryFusion', 'handleFolderFusionBackend',
        'toggleParentFolder'
    ];

    let missingFunctions = [];
    requiredFunctions.forEach(funcName => {
        if (typeof window[funcName] !== 'function') {
            missingFunctions.push(funcName);
            console.error(`❌ Fonction manquante: ${funcName}`);
        }
    });

    if (missingFunctions.length > 0) {
        console.error('🚨 FONCTIONS GLOBALES MANQUANTES:', missingFunctions);
        console.error('🔧 Tentative de correction automatique...');

        // Tentative de correction
        try {
            window.handleFusionButtonClick = handleFusionButtonClick;
            window.createBackup = handleCreateBackup;
            window.addNewCategory = handleAddCategory;
            window.toggleSection = toggleSection;
            window.handleCategoryDelete = handleCategoryDelete;
            window.filterFiles = filterFiles;
            window.filterByLetter = filterByLetter;
            console.log('✅ Correction automatique appliquée');
        } catch (error) {
            console.error('❌ Échec de la correction automatique:', error);
        }
    } else {
        console.log('✅ Toutes les fonctions globales sont disponibles');
    }
}

// Exécuter la vérification immédiatement
verifyGlobalFunctions();

// ===== INITIALIZATION =====

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Petit délai pour s'assurer que toutes les fonctions sont exposées
    setTimeout(() => {
        initializeApp();
    }, 100);
});
