from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI

class LangChainNeo4jClient:
    def __init__(
        self,
        uri: str,
        user: str,
        password: str,
        openai_api_key: str,
    ):
        self.graph = Neo4jGraph(
            url=uri,
            username=user,
            password=password,
        )

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=openai_api_key,
        )

        self.chain = GraphCypherQAChain.from_llm(
            llm=self.llm,
            graph=self.graph,
            verbose=True,
            return_intermediate_steps=True,
        )

    def query(self, question: str) -> dict:
        """
        自然文 → Cypher → Neo4j → 結果
        """
        return self.chain.invoke({"query": question})
