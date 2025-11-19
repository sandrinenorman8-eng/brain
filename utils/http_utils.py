import requests
import time

def post_json(url, data, timeout=10, max_retries=2):
    for attempt in range(max_retries + 1):
        try:
            response = requests.post(url, json=data, timeout=timeout)
            return response
        except requests.exceptions.ConnectionError as e:
            if attempt < max_retries:
                time.sleep(1)
                continue
            raise ConnectionError(f"Failed to connect to {url} after {max_retries + 1} attempts") from e
        except requests.exceptions.Timeout as e:
            if attempt < max_retries:
                time.sleep(1)
                continue
            raise TimeoutError(f"Request to {url} timed out after {timeout}s") from e
        except Exception as e:
            raise Exception(f"Unexpected error calling {url}: {str(e)}") from e
    
    raise Exception(f"Failed to complete request to {url}")
