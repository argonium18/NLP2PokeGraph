# tests/test_search_garchomp.py
import pytest
from app.application.di.container import search_pokemon_usecase

def test_search_garchomp():
    # DI で作った UseCase をそのまま呼び出す
    result = search_pokemon_usecase.execute("Great Tusk")

    print("検索結果:", result)

if __name__  == "__main__":
    test_search_garchomp()