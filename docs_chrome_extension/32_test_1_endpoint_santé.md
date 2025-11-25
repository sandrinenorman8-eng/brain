# Test 1: Endpoint santé
curl -I https://your-backend.vercel.app/api/health
# Attendu: HTTP/2 200

# Test 2: Headers CORS
curl -I -H "Origin: chrome-extension://abcd1234" \
  https://your-backend.vercel.app/api/health