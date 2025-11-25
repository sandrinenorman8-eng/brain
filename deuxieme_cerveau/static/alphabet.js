// Alphabet buttons functionality for Deuxième Cerveau
// This file handles the generation and functionality of alphabet buttons for filtering

/**
 * Generate alphabet buttons (A-Z)
 * @param {string} currentLetter - The currently selected letter filter
 * @param {Function} filterCallback - Callback function for letter filtering
 */
export function updateAlphabetButtons(currentLetter, filterCallback) {
    const alphabetContainer = document.getElementById('alphabet-buttons');
    if (!alphabetContainer) {
        console.error('❌ Alphabet container not found when updating buttons');
        return;
    }

    // Clear existing buttons
    alphabetContainer.innerHTML = '';
    
    console.log(`🔤 Updating alphabet buttons with current letter: ${currentLetter}`);

    // Add title to make it clear what these buttons do
    const title = document.createElement('div');
    title.className = 'text-sm text-primary/70 w-full mb-2';
    title.textContent = 'Filtrer par première lettre:';
    alphabetContainer.appendChild(title);

    // Add "All" button
    const allButton = document.createElement('button');
    allButton.className = `filter-btn alphabet-btn px-3 py-2 rounded-lg transition-colors ${
        currentLetter === 'all'
            ? 'bg-primary text-white'
            : 'bg-primary/20 text-primary hover:bg-primary/40'
    }`;
    allButton.textContent = '🔤 Tout';
    allButton.onclick = () => filterCallback('all');
    allButton.style.fontWeight = 'bold';
    alphabetContainer.appendChild(allButton);

    // Generate A-Z buttons
    for (let i = 65; i <= 90; i++) {
        const letter = String.fromCharCode(i);
        const button = document.createElement('button');
        button.className = `filter-btn alphabet-btn px-3 py-2 rounded-lg transition-colors ${
            currentLetter === letter
                ? 'bg-primary text-white'
                : 'bg-primary/20 text-primary hover:bg-primary/40'
        }`;
        button.textContent = letter;
        button.onclick = () => filterCallback(letter);
        button.style.minWidth = '2.5rem';
        button.style.fontWeight = 'bold';
        alphabetContainer.appendChild(button);
    }
    
    console.log(`✅ Alphabet buttons updated: ${alphabetContainer.children.length} buttons created`);
}

/**
 * Filter files by first letter
 * @param {Array} files - Array of files to filter
 * @param {string} letter - Letter to filter by (or 'all' for no filter)
 * @returns {Array} - Filtered array of files
 */
export function filterFilesByLetter(files, letter) {
    if (letter === 'all') {
        return files;
    }
    
    return files.filter(file => {
        // Get the first character of the filename and convert to uppercase
        const firstChar = file.filename.charAt(0).toUpperCase();
        return firstChar === letter;
    });
}

/**
 * Initialize alphabet buttons functionality
 * @param {Function} filterCallback - Callback function to handle letter filtering
 */
export function initializeAlphabetButtons(filterCallback) {
    console.log('🔤 Initializing alphabet buttons...');
    
    // Make sure the container is visible and properly styled
    const alphabetContainer = document.getElementById('alphabet-buttons');
    if (alphabetContainer) {
        // Ensure the container has proper styling
        alphabetContainer.style.display = 'flex';
        alphabetContainer.style.flexWrap = 'wrap';
        alphabetContainer.style.gap = '0.5rem';
        alphabetContainer.style.marginTop = '1rem';
        alphabetContainer.style.marginBottom = '1rem';
        alphabetContainer.style.padding = '0.5rem';
        alphabetContainer.style.borderRadius = '0.5rem';
        alphabetContainer.style.backgroundColor = 'rgba(0, 246, 255, 0.05)';
        alphabetContainer.style.border = '1px solid rgba(0, 246, 255, 0.2)';
        
        console.log('🔤 Alphabet container styled for visibility');
    } else {
        console.error('❌ Alphabet container not found in the DOM');
    }
    
    // Update the buttons
    updateAlphabetButtons('all', filterCallback);
}