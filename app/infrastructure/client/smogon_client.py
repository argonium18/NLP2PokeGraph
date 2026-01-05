# smogon_client.py
import requests
from typing import Dict, Any

class SmogonClient:
    BASE = "https://pkmn.github.io/smogon/data"

    def _get_json(self, path: str) -> dict:
        url = f"{self.BASE}/{path}"
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()

    # 既存の analyses 取得
    def fetch_analyses(self, format_id: str) -> dict:
        return self._get_json(f"analyses/{format_id}.json")

    # 新規追加: sets 取得
    def fetch_sets(self, format_id: str) -> dict:
        return self._get_json(f"sets/{format_id}.json")
