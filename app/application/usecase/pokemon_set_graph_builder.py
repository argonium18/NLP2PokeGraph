from app.domain.model.pokemon_set import PokemonSet
from app.infrastructure.model.pokemon_set_graph import PokemonSetGraph, MoveGraph
from typing import List

class PokemonSetGraphBuilder:

    @staticmethod
    def build_from_domain(s: PokemonSet) -> PokemonSetGraph:
        set_id = f"{s.pokemon_name}|{s.set_name}"

        # moves を Graph 用に変換
        moves_graph: List[MoveGraph] = []
        for idx, m in enumerate(s.moves, start=1):
            if isinstance(m, list):
                for move in m:
                    moves_graph.append(MoveGraph(name=move, slot=idx, candidate=True))
            else:
                moves_graph.append(MoveGraph(name=m, slot=idx, candidate=False))

        # Evs が None の場合は None にする
        evs = s.evs
        hp = evs.hp if evs else None
        atk = evs.atk if evs else None
        def_ = evs.def_ if evs else None
        spa = evs.spa if evs else None
        spd = evs.spd if evs else None
        spe = evs.spe if evs else None

        return PokemonSetGraph(
            set_id=set_id,
            pokemon_name=s.pokemon_name,
            set_name=s.set_name,
            nature=s.nature,
            role=s.role,
            hp=hp,
            atk=atk,
            def_=def_,
            spa=spa,
            spd=spd,
            spe=spe,
            moves=moves_graph,
            items=s.item or [],
            abilities=s.ability or [],
        )
