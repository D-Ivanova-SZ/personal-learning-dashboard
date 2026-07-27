import requests
from typing import Dict, Any, Optional


def get_json(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        raise requests.exceptions.Timeout(
            "Request timed out. The server took too long to respond!"
        )

    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError(
            "Failed to connect. Please check your internet connection!"
        )

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        raise requests.exceptions.HTTPError(
            f"HTTP error {status_code}: {e.response.reason}"
        )

    except ValueError:
        raise ValueError("Invalid JSON response received from server!")

    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(
            f"An error occurred while making the request: {str(e)}"
        )
