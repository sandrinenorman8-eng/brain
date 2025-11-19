@echo off
echo ========================================
echo   NETTOYAGE COMPLET DES DUPLICATAS
echo ========================================
echo.
echo Fichiers a supprimer: 36
echo Espace a recuperer: 181.4 KB
echo.
pause

REM Creer le dossier archives
if not exist "archives" mkdir archives

if exist "CLEANUP_SUMMARY.txt" move /Y "CLEANUP_SUMMARY.txt" "archives\" >nul 2>&1
if exist "FILE_USAGE_REPORT.md" move /Y "FILE_USAGE_REPORT.md" "archives\" >nul 2>&1
if exist "LIRE_MOI.txt" move /Y "LIRE_MOI.txt" "archives\" >nul 2>&1
if exist "QUICK_START.txt" move /Y "QUICK_START.txt" "archives\" >nul 2>&1
if exist "SCRIPTS_DISPONIBLES.txt" move /Y "SCRIPTS_DISPONIBLES.txt" "archives\" >nul 2>&1
if exist "TEST_MIGRATION.bat" move /Y "TEST_MIGRATION.bat" "archives\" >nul 2>&1
if exist "analyze_files.py" move /Y "analyze_files.py" "archives\" >nul 2>&1
if exist "category_path_resolver.py" move /Y "category_path_resolver.py" "archives\" >nul 2>&1
if exist "cleanup_all_duplicates.bat" move /Y "cleanup_all_duplicates.bat" "archives\" >nul 2>&1
if exist "cleanup_empty_folders.py" move /Y "cleanup_empty_folders.py" "archives\" >nul 2>&1
if exist "cleanup_unused_files.bat" move /Y "cleanup_unused_files.bat" "archives\" >nul 2>&1
if exist "data_structure.json" del /Q "data_structure.json" >nul 2>&1
if exist "debug_index.py" move /Y "debug_index.py" "archives\" >nul 2>&1
if exist "demarrer_recherche.bat" move /Y "demarrer_recherche.bat" "archives\" >nul 2>&1
if exist "detect_active_files.py" move /Y "detect_active_files.py" "archives\" >nul 2>&1
if exist "ensure_html_consistency.py" move /Y "ensure_html_consistency.py" "archives\" >nul 2>&1
if exist "extract_assets.py" move /Y "extract_assets.py" "archives\" >nul 2>&1
if exist "files_data.json" del /Q "files_data.json" >nul 2>&1
if exist "folder_hierarchy.json" move /Y "folder_hierarchy.json" "archives\" >nul 2>&1
if exist "generate_notes_data.py" move /Y "generate_notes_data.py" "archives\" >nul 2>&1
if exist "html_config.json" del /Q "html_config.json" >nul 2>&1
if exist "html_template_generator.py" move /Y "html_template_generator.py" "archives\" >nul 2>&1
if exist "lancer_deuxieme_cerveau.bat" move /Y "lancer_deuxieme_cerveau.bat" "archives\" >nul 2>&1
if exist "monitor.py" move /Y "monitor.py" "archives\" >nul 2>&1
if exist "notes_launcher.html" move /Y "notes_launcher.html" "archives\" >nul 2>&1
if exist "open_all_notes_test.bat" move /Y "open_all_notes_test.bat" "archives\" >nul 2>&1
if exist "organize_data_folders.py" move /Y "organize_data_folders.py" "archives\" >nul 2>&1
if exist "routes_fusion.py" move /Y "routes_fusion.py" "archives\" >nul 2>&1
if exist "search-server.js" move /Y "search-server.js" "archives\" >nul 2>&1
if exist "start_deuxieme_cerveau.ps1" move /Y "start_deuxieme_cerveau.ps1" "archives\" >nul 2>&1
if exist "start_search_server.bat" move /Y "start_search_server.bat" "archives\" >nul 2>&1
if exist "trace_real_files.py" move /Y "trace_real_files.py" "archives\" >nul 2>&1
if exist "update_notes_data.bat" move /Y "update_notes_data.bat" "archives\" >nul 2>&1
if exist "validate_html_consistency.py" move /Y "validate_html_consistency.py" "archives\" >nul 2>&1
if exist "verify_endpoints.py" move /Y "verify_endpoints.py" "archives\" >nul 2>&1
if exist "verify_upload_implementation.py" move /Y "verify_upload_implementation.py" "archives\" >nul 2>&1

echo.
echo [OK] Nettoyage termine!
pause
