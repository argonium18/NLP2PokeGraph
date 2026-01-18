import requests


class SmogonClient:
    BASE = "https://pkmn.github.io/smogon/data"

    def _get_json(self, path: str) -> dict:
        url = f"{self.BASE}/{path}"
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def fetch_sets(self, format_id: str) -> dict:
        return self._get_json(f"sets/{format_id}.json")

    def fetch_analyses(self, format_id: str) -> dict:
        return self._get_json(f"analyses/{format_id}.json")

    def fetch_stats(self, format_id: str) -> dict:
        return self._get_json(f"stats/{format_id}.json")

