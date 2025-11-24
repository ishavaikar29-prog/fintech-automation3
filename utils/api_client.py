# api_client.py

from typing import Any, Dict, List, Optional
import requests
from error_handler import log_error

def fetch_api_data(url: str, headers: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
    """
    Fetch data from a given API URL.
    Returns a list of dicts; on failure, returns an empty list.
    """
    try:
        print(f"Calling API: {url}")
        res = requests.get(url, headers=headers, timeout=20)
        res.raise_for_status()
        data = res.json()

        # Ensure list format
        if isinstance(data, list):
            return data
        return [data]

    except Exception as e:
        log_error(f"API failed for URL: {url}", e)
        print(f"ERROR calling {url}. See error.log.")
        return []
