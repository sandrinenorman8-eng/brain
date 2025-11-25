# Test 3: CORS headers
echo "Testing CORS headers..."
CORS_HEADER=$(curl -s -I -H "Origin: chrome-extension://test" "$BACKEND_URL/api/health" | grep -i "access-control-allow-origin")
if [ -n "$CORS_HEADER" ]; then
    echo "✅ CORS configured"
else
    echo "❌ CORS not configured"
    exit 1
fi

echo "✅ All tests passed!"
```
