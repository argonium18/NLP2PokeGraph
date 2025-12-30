from app.infrastructure.client.neo4j_client import Neo4jClient
from app.pipeline.enumerate_entities.entity_enumerator import EntityEnumerator
from app.pipeline.classify_meaning.llm_input_builder import LLMInputBuilder
from app.shared.config.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from app.shared.logging.logger import logger

def main():
    # Neo4j からエンティティ取得
    neo4j_client = Neo4jClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    entity_list = neo4j_client.get_all_entities()
    neo4j_client.close()
    logger.info(f"Loaded {len(entity_list)} entities from Neo4j")

    # 文ブロックサンプル
    text_block = "Hex can be used on sets packing Will-O-Wisp to deal massive damage to burned foes, notably letting Skeledirge OHKO Slowking."
    subject = "Skeledirge"

    # 候補エンティティ列挙
    enumerator = EntityEnumerator(entity_list)
    candidates = enumerator.enumerate_candidates(text_block)
    logger.info(f"Candidates: {[e.name for e in candidates]}")

    # LLM入力生成
    llm_input = LLMInputBuilder.build_input(subject, text_block, candidates)
    print(llm_input)

if __name__ == "__main__":
    main()
