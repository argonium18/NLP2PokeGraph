from app.domain.model.entity import Entity
from typing import List

class EntityEnumerator:
    def __init__(self, entity_list: List[Entity]):
        self.entity_list = entity_list

    def enumerate_candidates(self, text: str) -> List[Entity]:
        candidates = []
        for entity in self.entity_list:
            if entity.name in text:
                candidates.append(entity)
        return candidates
    
