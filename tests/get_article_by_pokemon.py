# controller/cli_controller.py
from app.application.di.container import (
    load_and_render_smogon_article_usecase,
)

def main():
    pokemon_name = "Garchomp"
    output = load_and_render_smogon_article_usecase.execute(
        pokemon_name=pokemon_name
    )
    print(output)

if __name__ == "__main__":
    main()
