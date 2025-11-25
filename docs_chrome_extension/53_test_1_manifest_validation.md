# Test 1: Manifest validation
echo "Validating manifest.json..."
node -e "const m = require('./extension/manifest.json'); console.log('✅ Manifest valid');"

# Test 2: Backend accessibility
BACKEND_URL=$(node -e "const m = require('./extension/manifest.json'); console.log(m.host_permissions[0].replace('/*', ''));")
echo "Testing backend at $BACKEND_URL..."

curl -f -s "$BACKEND_URL/api/health" > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend accessible"
else
    echo "❌ Backend unreachable"
    exit 1
fi
