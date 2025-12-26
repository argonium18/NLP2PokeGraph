import requests

class SmogonClient:

    def fetch_analysis(self, json_url: str) -> dict:
        response = requests.get(json_url)
        response.raise_for_status()
        return response.json()
