// API functions for Deuxième Cerveau
// All backend communication functions

/**
 * Load categories from the backend
 */
export async function loadCategories() {
    try {
        const response = await fetch('/categories');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        // Handle wrapped response format {success: true, data: [...]}
        const categories = result.data || result;
        console.log(`📂 Loaded ${categories.length} categories`);
        return categories;
    } catch (error) {
        console.error('❌ Error loading categories:', error);
        throw error;
    }
}

/**
 * Load categories with hierarchical structure (parents/children)
 */
export async function loadCategoriesStructured() {
    try {
        const response = await fetch('/categories_structured');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const structured = await response.json();
        console.log(`📂 Loaded structured categories: ${structured.parents.length} parents, ${structured.standalone.length} standalone`);
        return structured;
    } catch (error) {
        console.error('❌ Error loading structured categories:', error);
        // Fallback to flat categories if structured endpoint fails
        console.warn('⚠️ Falling back to flat categories');
        const categories = await loadCategories();
        return {
            parents: [],
            standalone: categories.map(cat => ({
                name: cat.name,
                emoji: cat.emoji,
                color: cat.color,
                path: cat.name,
                isStandalone: true
            }))
        };
    }
}

/**
 * Load all files from all categories
 */
export async function loadAllFiles() {
    try {
        const response = await fetch('/all_files');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        // Handle wrapped response format {success: true, data: [...]}
        const allFiles = result.data || result;
        console.log(`📄 Loaded ${allFiles.length} total files`);
        return allFiles;
    } catch (error) {
        console.error('❌ Error loading all files:', error);
        throw error;
    }
}

/**
 * Load files by categories (optimized version)
 */
export async function loadFilesByCategories(categories) {
    const categoryPromises = categories.map(async (cat) => {
        try {
            const response = await fetch(`/list/${cat.name}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const result = await response.json();
            // Handle wrapped response format {success: true, data: [...]}
            const files = result.data || result;
            return {
                category: cat.name,
                emoji: cat.emoji,
                color: cat.color,
                files: files
            };
        } catch (error) {
            console.error(`❌ Error loading files for ${cat.name}:`, error);
            return {
                category: cat.name,
                emoji: cat.emoji,
                color: cat.color,
                files: []
            };
        }
    });

    try {
        const results = await Promise.all(categoryPromises);
        console.log(`📂 Loaded files from ${results.length} categories`);
        return results;
    } catch (error) {
        console.error('❌ Error loading files by categories:', error);
        throw error;
    }
}

/**
 * Quick save a note to a category
 */
export async function quickSave(category, text) {
    try {
        const response = await fetch(`/save/${category.name}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log(`💾 Saved to ${category.name}`);
        return result;
    } catch (error) {
        console.error('❌ Error saving note:', error);
        throw error;
    }
}

/**
 * Add a new category
 */
export async function addNewCategory(name) {
    try {
        const response = await fetch('/add_category', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const newCategory = await response.json();
        console.log(`🗂️ Added new category: ${newCategory.name}`);
        return newCategory;
    } catch (error) {
        console.error('❌ Error adding category:', error);
        throw error;
    }
}

/**
 * Open folder for a category
 */
export async function openFolder(categoryName) {
    try {
        const response = await fetch(`/open_folder/${categoryName}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        if (result.status === 'opened') {
            console.log(`📁 Opened folder for ${categoryName}`);
        }
        return result;
    } catch (error) {
        console.error('❌ Error opening folder:', error);
        throw error;
    }
}

/**
 * Create a backup
 */
export async function createBackup() {
    try {
        const response = await fetch('/api/backup_project', {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        const data = result.data || result;
        console.log(`💾 Backup created: ${data.filename}`);
        return data;
    } catch (error) {
        console.error('❌ Error creating backup:', error);
        throw error;
    }
}

/**
 * Delete a category
 */
export async function deleteCategory(categoryName) {
    try {
        const response = await fetch(`/erase_category/${categoryName}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log(`🗑️ Deleted category: ${categoryName}`);
        return result;
    } catch (error) {
        console.error('❌ Error deleting category:', error);
        throw error;
    }
}

/**
 * Perform global fusion
 */
export async function performGlobalFusion() {
    try {
        const response = await fetch('/api/fusion/global', {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        const data = result.data || result;
        console.log(`🔗 Global fusion completed`);
        return data;
    } catch (error) {
        console.error('❌ Error performing global fusion:', error);
        throw error;
    }
}

/**
 * Perform category fusion
 */
export async function performCategoryFusion(selectedCategories) {
    try {
        const response = await fetch('/api/fusion/category', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ categories: selectedCategories })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        const data = result.data || result;
        console.log(`🔗 Category fusion completed`);
        return data;
    } catch (error) {
        console.error('❌ Error performing category fusion:', error);
        throw error;
    }
}

/**
 * Perform single category fusion
 */
export async function performSingleCategoryFusion(categoryName) {
    try {
        const response = await fetch('/api/fusion/single-category', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ category: categoryName })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        const data = result.data || result;
        console.log(`🔗 Single category fusion completed`);
        return data;
    } catch (error) {
        console.error('❌ Error performing single category fusion:', error);
        throw error;
    }
}
