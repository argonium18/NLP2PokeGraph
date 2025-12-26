# app/ingest/infrastructure/client/victoryroad_client.py
import requests

class VictoryRoadClient:
    def fetch(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
