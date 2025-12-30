# smogon_fetch.py
import requests
import re
from typing import Any, Dict, Optional

BASE = "https://pkmn.github.io/smogon/data"  # data.pkmn.cc -> pkmn.github.io にリダイレクトされます

def _get_json(path: str) -> Any:
    url = f"{BASE}/{path}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.json()

def fetch_sets(format_id: str) -> Dict[str, Any]:
    """
    例: format_id = "gen9ou" または "gen9"（世代全体）
    戻り値: species -> { set_name -> set_data }
    """
    return _get_json(f"sets/{format_id}.json")

def fetch_analyses(format_id: str) -> Dict[str, Any]:
    """
    Smogon の解説（analysis）を取得。各 species に対して文章／セクションが入っている。
    """
    return _get_json(f"analyses/{format_id}.json")

def fetch_stats(format_id: str) -> Dict[str, Any]:
    """
    使用率統計（usage stats）の要約データ。
    """
    return _get_json(f"stats/{format_id}.json")

def normalize_name(name: str) -> str:
    """
    keys がどのように正規化されているかはソースによるが、一般的な変換を試みるユーティリティ。
    - 空白を取り、ハイフンの扱いを調整するなど。
    """
    n = name.strip().lower()
    n = n.replace(" ", "").replace(".", "").replace(":", "").replace("’", "'")
    # species のキーは Showdown 準拠のものが多い（例: 'greattusk', 'iron-moth' 等）
    # ハイフンが入っている場合はそのまま or 削る場合があるので両方試す実装にするのが安全
    return n

def get_pokemon_sets(format_id: str, species: str) -> Optional[Dict[str, Any]]:
    """
    指定フォーマットの該当ポケモンの推奨型（複数セット）を返す。
    """
    sets = fetch_sets(format_id)
    # keys は表示名/スラッグ混在するので直当て -> 正規化マッチの順で探す
    if species in sets:
        return sets[species]
    # 試しに正規化して探す
    norm = normalize_name(species)
    # 直接一致するキーが無いときは走査
    for key in sets.keys():
        if normalize_name(key) == norm:
            return sets[key]
    return None

def extract_set_fields(set_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    set_data の中から Moves / Nature / Ability / Item / EVs / Role を穏当に抜き出す。
    Smogon側の JSON フィールド名は一貫していない（Display Name を使っていることがある）ため
    .get を多めに使い、存在するものを拾う実装にしてある。
    """
    out = {}
    # 多くの set のキー例: "moves", "Moves", "ability", "Ability" ... を想定して安全に取り出す
    def first_get(d, *keys, default=None):
        for k in keys:
            if k in d:
                return d[k]
        return default

    out["name"] = first_get(set_data, "title", "name", "Set")  # セット名
    out["moves"] = first_get(set_data, "moves", "Moves", [])
    out["nature"] = first_get(set_data, "nature", "Nature", None)
    out["ability"] = first_get(set_data, "ability", "Ability", None)
    out["item"] = first_get(set_data, "item", "Item", None)
    out["evs"] = first_get(set_data, "ev", "evs", "EVs", None)
    out["role"] = first_get(set_data, "role", "Role", None)
    # そのほか raw data を丸ごと渡す場合は下に格納
    out["_raw"] = set_data
    return out

def check_json_format(format_id: str, species: str):
    """
    指定フォーマットの該当ポケモンの推奨型（複数セット）を返す。
    """
    sets = fetch_sets(format_id)
    # keys は表示名/スラッグ混在するので直当て -> 正規化マッチの順で探す
    if species in sets:
        print(sets[species])


if __name__ == "__main__":

    fmt = "gen9ou"
    mon = "Great Tusk"  # 取得したいポケモン名（表示名で良い）
    check_json_format(fmt, mon)

# if __name__ == "__main__":
#     # 使い方例
#     fmt = "gen9ou"
#     mon = "Great Tusk"  # 取得したいポケモン名（表示名で良い）
#     print(f"Fetching sets for {mon} in {fmt} ...")
#     ps = get_pokemon_sets(fmt, mon)
#     if not ps:
#         print("Not found in sets for that format.")
#     else:
#         # ps は set名 -> set データ の dict
#         for set_name, data in ps.items():
#             parsed = extract_set_fields(data)
#             print("== Set:", set_name)
#             print("Moves:", parsed["moves"])
#             print("Nature:", parsed["nature"])
#             print("Ability:", parsed["ability"])
#             print("Item:", parsed["item"])
#             print("EVs:", parsed["evs"])
#             print("Role:", parsed["role"])
#             print()
