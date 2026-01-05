# smogon_normalize_service.py
import re
from app.domain.model.pokemon_set import PokemonSet  # <- import
from typing import Any

def normalize_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())

class SmogonNormalizeService:

    # -------------------------
    # PokemonSet 正規化
    # -------------------------
    def normalize_sets(
        self,
        sets: dict[str, PokemonSet],
        masters: dict[str, dict[str, Any]],
    ) -> dict[str, PokemonSet]:
        """
        { set_name -> PokemonSet } を正規化して返す
        moves / ability / item をマスタに合わせる
        """
        moves_master = masters["moves"]
        abilities_master = masters["abilities"]
        items_master = masters["items"]

        normalized: dict[str, PokemonSet] = {}

        for set_name, pokemon_set in sets.items():
            print(set_name, pokemon_set)  # デバッグ

            # moves（元からリストだが入れ子リストにも対応）
            normalized_moves = self._normalize_list(pokemon_set.moves, moves_master)

            # item（単一文字列 or リスト対応）
            item_list = [pokemon_set.item] if isinstance(pokemon_set.item, str) else pokemon_set.item
            normalized_item = self._normalize_list(item_list, items_master)

            # ability（単体文字列の場合はリスト化）
            ability_list = [pokemon_set.ability] if isinstance(pokemon_set.ability, str) else pokemon_set.ability
            normalized_ability = self._normalize_list(ability_list, abilities_master)

            normalized[set_name] = PokemonSet(
                name=pokemon_set.name,
                moves=normalized_moves,
                nature=pokemon_set.nature,
                ability=normalized_ability,
                item=normalized_item,
                evs=pokemon_set.evs,
                role=pokemon_set.role,
                raw=pokemon_set.raw
            )

        return normalized

    # --------------- 旧API ---------------
    def _normalize_list(self, names: list | None, master: dict) -> list[str] | None:
        """
        文字列リスト専用の正規化関数
        - マスタに存在する名前だけを返す
        - 入れ子リストも平坦化して処理
        - 全て存在しない場合は None
        """
        if not names:
            return None

        # 平坦化（list の中に list があっても展開）
        flat_names: list[str] = []
        for n in names:
            if isinstance(n, list):
                flat_names.extend(n)
            elif n:  # None や空文字列を除外
                flat_names.append(n)

        result: list[str] = []
        for name in flat_names:
            key = normalize_key(name)
            mapped = master.get(key, {}).get("name")
            if mapped:
                result.append(mapped)

        return result if result else None
