// State management for Deuxième Cerveau
// Centralized application state management

const state = {
    allFiles: [],
    categories: [],
    currentFilter: 'all',
    currentLetter: 'all',
    partitioningState: {
        sections: {
            'main-section': { collapsed: false, size: 'auto', order: 1 },
            'notes-section': { collapsed: false, size: 'auto', order: 2 },
            'folders-section': { collapsed: false, size: 'auto', order: 3 }
        },
        isResizing: false,
        resizeData: null,
        autoExpansion: true,
        contentObservers: new Map()
    }
};

/**
 * Get filtered files based on current filter and letter
 */
export function getFilteredFiles() {
    let filteredFiles = state.allFiles;
    
    // Apply category filter
    if (state.currentFilter !== 'all') {
        filteredFiles = filteredFiles.filter(file => file.category === state.currentFilter);
    }
    
    // Apply letter filter
    if (state.currentLetter !== 'all') {
        filteredFiles = filteredFiles.filter(file => {
            const firstChar = file.filename.charAt(0).toUpperCase();
            return firstChar === state.currentLetter;
        });
    }
    
    return filteredFiles;
}

/**
 * Get all files
 */
export function getAllFiles() {
    return state.allFiles;
}

/**
 * Set all files
 */
export function setAllFiles(files) {
    state.allFiles = files;
}

/**
 * Get categories
 */
export function getCategories() {
    return state.categories;
}

/**
 * Set categories
 */
export function setCategories(categories) {
    state.categories = categories;
}

/**
 * Add a category
 */
export function addCategory(category) {
    state.categories.push(category);
}

/**
 * Remove a category
 */
export function removeCategory(categoryName) {
    state.categories = state.categories.filter(c => c.name !== categoryName);
}

/**
 * Get current filter
 */
export function getCurrentFilter() {
    return state.currentFilter;
}

/**
 * Set current filter
 */
export function setCurrentFilter(filter) {
    state.currentFilter = filter;
}

/**
 * Get current letter filter
 */
export function getCurrentLetter() {
    return state.currentLetter;
}

/**
 * Set current letter filter
 */
export function setCurrentLetter(letter) {
    state.currentLetter = letter;
}

/**
 * Get partitioning state
 */
export function getPartitioningState() {
    return state.partitioningState;
}

/**
 * Update partitioning state section
 */
export function updatePartitioningSection(sectionId, updates) {
    if (state.partitioningState.sections[sectionId]) {
        state.partitioningState.sections[sectionId] = {
            ...state.partitioningState.sections[sectionId],
            ...updates
        };
    }
}

/**
 * Save partitioning state to localStorage
 */
export function savePartitioningState() {
    try {
        localStorage.setItem('partitioningState', JSON.stringify(state.partitioningState));
    } catch (error) {
        console.warn('⚠️ Could not save partitioning state:', error);
    }
}

/**
 * Load partitioning state from localStorage
 */
export function loadPartitioningState() {
    try {
        const saved = localStorage.getItem('partitioningState');
        if (saved) {
            const parsedState = JSON.parse(saved);
            // Merge with default state to handle new properties
            state.partitioningState = { ...state.partitioningState, ...parsedState };
        }
    } catch (error) {
        console.warn('⚠️ Could not load partitioning state:', error);
    }
}
