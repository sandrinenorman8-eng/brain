### 10.5 Edge Cases 2025 Checklist
☐ URLs tunnel dynamiques gérées (reload extension)
☐ ID extension réservé (key dans manifest)
☐ Cache CDN OPTIONS désactivé (Cache-Control: no-store)
☐ CSP vérifiée sans typos
☐ Incohérences extension_pages/content_scripts corrigées
☐ Service worker keep-alive implémenté (si nécessaire)
☐ Exponential backoff sur rate limiting
☐ Network errors retryés automatiquement
☐ Token refresh échoué → force re-login
☐ Backend unreachable → notification utilisateur
☐ Error logging implémenté
☐ Telemetry basique active (optionnel)
