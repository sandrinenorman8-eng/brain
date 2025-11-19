import importlib
import sys

sys.path.insert(0, '.')

try:
    import app as myapp
    importlib.reload(myapp)
    print('Imported app OK')

    # Direct call of the view function
    with myapp.app.test_request_context('/'):
        try:
            result = myapp.index()
            if isinstance(result, tuple):
                print('index() returned tuple:', result[1])
            else:
                print('index() returned type:', type(result).__name__)
        except Exception as e:
            print('index() raised exception:', repr(e))

    # Test via test client
    myapp.app.testing = True
    with myapp.app.test_client() as client:
        rv = client.get('/')
        print('GET / status:', rv.status_code)
        if rv.status_code != 200:
            print('GET / body (first 300 chars):', rv.data.decode('utf-8', errors='ignore')[:300])

        rv2 = client.get('/all_notes')
        print('GET /all_notes status:', rv2.status_code)
        if rv2.status_code != 200:
            print('GET /all_notes body (first 300 chars):', rv2.data.decode('utf-8', errors='ignore')[:300])

except Exception as e:
    print('Top-level error:', repr(e))











