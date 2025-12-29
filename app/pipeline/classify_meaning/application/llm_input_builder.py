from typing import List
from app.domain.model.entity import Entity

class LLMInputBuilder:
    @staticmethod
    def build_input(subject: str, text: str, candidates: List[Entity]) -> str:
        pokemon_list = [e.name for e in candidates if e.type == "Pokemon"]
        move_list = [e.name for e in candidates if e.type == "Move"]
        item_list = [e.name for e in candidates if e.type == "Item"]

        prompt = f"""
Extract all relationships for the subject '{subject}' from the following sentence.
Only consider target entities from candidate lists.

Sentence:
"{text}"

Candidate Pokemon: {pokemon_list}
Candidate Moves: {move_list}
Candidate Items: {item_list}

Output JSON format:
[
  {{"subject": "{subject}", "relation": "<relation_type>", "object": "<target_entity>", "type": "<entity_type>"}}
]
"""
        return prompt
