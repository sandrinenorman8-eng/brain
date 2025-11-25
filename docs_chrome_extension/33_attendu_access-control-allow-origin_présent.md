# Attendu: access-control-allow-origin présent

# Test 3: Authentification
curl -X POST https://your-backend.vercel.app/api/auth/google \
  -H "Content-Type: application/json" \
  -d '{"googleToken":"test"}'