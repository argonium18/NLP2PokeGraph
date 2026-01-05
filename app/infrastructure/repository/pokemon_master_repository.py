import json
from pathlib import Path


class PokemonMasterRepository:
    BASE_PATH = Path(
        r"C:\EngineersData\01_Projects\09_NLP2PokeGraph"
        r"\app\tools\showdown\data\raw\showdown"
    )

    def load_all(self) -> dict:
        return {
            "pokedex": self._load_json("pokedex.json"),
            "moves": self._load_json("moves.json"),
            "abilities": self._load_json("abilities.json"),
            "items": self._load_json("items.json"),
            "typechart": self._load_json("typechart.json"),
        }

    def _load_json(self, filename: str) -> dict:
        path = self.BASE_PATH / filename
        with open(path, encoding="utf-8") as f:
            return json.load(f)
