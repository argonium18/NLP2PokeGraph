# controller/pipeline_controller.py
from fastapi import APIRouter, HTTPException
from app.application.di.container import (
    search_pokemon_usecase,
    load_and_render_smogon_article_usecase,  # 既存
    build_graph_usecase,                      # 追加
)

router = APIRouter()

# -----------------------
# Pokemon Graph 検索
# -----------------------
@router.get("/pokemon/{name}")
def get_pokemon(name: str):
    """
    指定したポケモン名で検索
    """
    result = search_pokemon_usecase.execute(name)
    if not result:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return result


# -----------------------
# Smogon 記事取得
# -----------------------
@router.get("/smogon/{pokemon_name}")
def get_smogon_article(pokemon_name: str):
    """
    指定したポケモン名の Smogon 記事を取得して CLI 用文字列で返す
    """
    try:
        output = load_and_render_smogon_article_usecase.execute(
            pokemon_name=pokemon_name
        )
        return {"article": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------
# Graph 作成（Neo4j への登録）
# -----------------------
@router.post("/graph/build/{pokemon_name}")
def build_pokemon_graph(pokemon_name: str):
    """
    指定したポケモン名のデータを取得して Neo4j に登録
    """
    try:
        build_graph_usecase.execute(pokemon_name)
        return {"status": "success", "message": f"Graph built for {pokemon_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))