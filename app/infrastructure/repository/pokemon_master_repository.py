# infrastructure/repository/pokemon_master_repository.py
import json
from pathlib import Path


class PokemonMasterRepository:
    BASE_PATH = Path(
        r"C:\EngineersData\01_Projects\09_NLP2PokeGraph"
        r"\app\tools\showdown\data\raw\showdown"
    )

    def load_all(self) -> dict:
        return {
            "pokedex": self._load("pokedex.json"),
            "moves": self._load("moves.json"),
            "abilities": self._load("abilities.json"),
            "items": self._load("items.json"),
            "typechart": self._load("typechart.json"),
        }

    def _load(self, filename: str) -> dict:
        with open(self.BASE_PATH / filename, encoding="utf-8") as f:
            return json.load(f)
