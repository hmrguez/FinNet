== Conclusions

This thesis explored the development of a financial planner QA system powered by a graph-based Retrieval-Augmented Generation (RAG) system. The research and implementation stages underscored the system’s potential to transform financial planning by combining advanced retrieval techniques with natural language generation. The following conclusions can be drawn from this study:

The use of graph-based RAG systems proved effective for managing the complexities of financial data. Graph structures enabled the representation of nuanced relationships between financial concepts, while embedding-based retrieval ensured semantic flexibility in handling diverse user queries. This hybrid approach addressed domain-specific challenges such as contextual relevance, accurate representation of financial dependencies, and user intent understanding.

The integration of Neo4j for graph storage and MongoDB for embedding-based retrieval allowed for efficient querying and knowledge management. The ability to extract subgraphs relevant to user queries demonstrated the system’s capability to deliver precise and contextually appropriate responses, making it particularly suitable for personal financial planning tasks.

The adoption of zero-shot prompt engineering via the Gemini API enabled the system to generate high-quality natural language responses without extensive training on domain-specific data. This approach not only reduced development costs but also provided adaptability to evolving financial knowledge and user needs.

The system’s performance, as measured by accuracy, factual correctness, efficiency, and robustness, validated the feasibility of graph-based RAG systems for fintech applications. Testing highlighted areas for refinement, particularly in handling ambiguous queries and optimizing retrieval strategies, paving the way for future improvements.

This study contributes to the growing body of research on intelligent fintech solutions by presenting a modular, graph-driven framework for QA system development. Its methodology, which emphasizes scalability, semantic richness, and cost-efficiency, can serve as a foundation for further innovation in this domain.

= Limitations and Future Work

Despite its promising results, this study faced limitations that present opportunities for further exploration:
	-	Scalability Challenges: As the knowledge graph grows, computational efficiency and retrieval speed may need optimization.
	-	Domain Adaptation: While effective in financial planning, the system’s adaptability to other domains remains to be tested.
	-	Enhanced Evaluation Metrics: Incorporating user satisfaction and long-term engagement into the evaluation framework would provide deeper insights into real-world applicability.

Future research could focus on refining subgraph extraction techniques, exploring multi-modal data integration, and enhancing the personalization of financial advice by providing user-aware information. Additionally, extending the system to handle real-time data and transactions would increase its practical utility.

By integrating advanced retrieval and generation techniques, this thesis demonstrates how a graph-based RAG system can deliver tailored financial advice, offering a promising step forward in the evolution of intelligent fintech applications.
