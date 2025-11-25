# Vérifier headers CORS et cache
curl -I -X OPTIONS \
  -H "Origin: chrome-extension://abcd1234" \
  -H "Access-Control-Request-Method: POST" \
  https://your-backend.vercel.app/api/endpoint
