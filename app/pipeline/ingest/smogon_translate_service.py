# pipeline/ingest/smogon_translate_service.py
from app.domain.model.pokemon_set import PokemonSet
from app.domain.value.evs import Evs
from app.infrastructure.repository.smogon_dto import SmogonSetDTO
from typing import Mapping, Any

class SmogonTranslateService:

    def to_pokemon_set(
        self,
        pokemon_name: str,
        set_name: str,
        dto: SmogonSetDTO,
    ) -> PokemonSet:
        raw = dto.raw

        return PokemonSet(
            pokemon_name=pokemon_name,
            set_name=set_name,
            moves=raw.get("moves") or [],
            nature=raw.get("nature"),
            ability=raw.get("ability") or [],
            item=raw.get("item") or [],
            evs=self._to_evs(raw.get("evs")),
            role=raw.get("role"),
        )

    def _to_evs(self, raw: Mapping[str, Any] | None) -> Evs | None:
        if not raw:
            return None

        return Evs(
            hp=raw.get("hp"),
            atk=raw.get("atk"),
            def_=raw.get("def"),
            spa=raw.get("spa"),
            spd=raw.get("spd"),
            spe=raw.get("spe"),
        )
