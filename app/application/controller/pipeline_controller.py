# controller/pipeline_controller.py
from fastapi import APIRouter, HTTPException
from app.application.di.container import search_pokemon_usecase  # DI からインポート

router = APIRouter()

@router.get("/pokemon/{name}")
def get_pokemon(name: str):
    """
    指定したポケモン名で検索
    """
    result = search_pokemon_usecase.execute(name)
    if not result:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return result
