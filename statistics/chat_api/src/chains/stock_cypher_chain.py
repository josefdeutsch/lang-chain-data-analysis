import os
from langchain.chains import GraphCypherQAChain
from langchain.prompts import PromptTemplate
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
# Environment variables for models and database credentials
QA_MODEL = os.getenv("QA_MODEL")
CYPHER_MODEL = os.getenv("CYPHER_MODEL")

# Initialize the Neo4j graph connection
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)

# Refresh the graph schema
graph.refresh_schema()

# Template for generating Cypher queries
cypher_generation_template = """
Task:
Generate Cypher query for a Neo4j graph database.

Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Note:
Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything other than
for you to construct a Cypher statement. Do not include any text except
the generated Cypher statement. Make sure the direction of the relationship is
correct in your queries. Make sure you alias both entities and relationships
properly. Do not run any queries that would add to or delete from
the database. Make sure to alias all statements that follow as with
statement (e.g. WITH v as visit, c.billing_amount as billing_amount)
If you need to divide numbers, make sure to
filter the denominator to be non zero.

Examples:
# What was the highest closing price?
MATCH (s:Stock)
RETURN s.date AS date, s.close AS closing_price
ORDER BY s.close DESC
LIMIT 1

# What is the average volume for a specific period?
MATCH (s:Stock)
WHERE s.date >= '2020-08-01' AND s.date <= '2020-08-12'
RETURN avg(s.volume) AS average_volume

# What was the lowest price for each day?
MATCH (s:Stock)
RETURN s.date AS date, s.low AS lowest_price
ORDER BY s.date

# How much did the closing price change day over day?
MATCH (s1:Stock)-[:NEXT_DAY]->(s2:Stock)
RETURN s1.date AS date, (s2.close - s1.close) AS price_change

# Which day had the highest trading volume?
MATCH (s:Stock)
RETURN s.date AS date, s.volume AS trading_volume
ORDER BY s.volume DESC
LIMIT 1

Stock properties:
Dates are in the format 'YYYY-MM-DD'
Prices are in decimal format
Volumes are in integer format

The question is:
{question}
"""

# Prompt template for Cypher query generation
cypher_generation_prompt = PromptTemplate(
    input_variables=["schema", "question"], template=cypher_generation_template
)

# Template for generating QA responses from Cypher query results
qa_generation_template = """You are an assistant that takes the results
from a Neo4j Cypher query and forms a human-readable response. The
query results section contains the results of a Cypher query that was
generated based on a user's natural language question. The provided
information is authoritative, you must never doubt it or try to use
your internal knowledge to correct it. Make the answer sound like a
response to the question.

Query Results:
{context}

Question:
{question}

If the provided information is empty, say you don't know the answer.
Empty information looks like this: []

If the information is not empty, you must provide an answer using the
results. If the question involves a time duration, assume the query
results are in units of days unless otherwise specified.

When dates are provided in the query results, return them in 'YYYY-MM-DD' format.
Make sure you return any list of dates in a way that isn't ambiguous and allows
someone to tell what the full dates are.

Never say you don't have the right information if there is data in
the query results. Make sure to show all the relevant query results
if you're asked.

Helpful Answer:
"""

# Prompt template for QA response generation
qa_generation_prompt = PromptTemplate(
    input_variables=["context", "question"], template=qa_generation_template
)

# Initialize the GraphCypherQAChain with the specified models and templates
stock_cypher_chain = GraphCypherQAChain.from_llm(
    cypher_llm=ChatOpenAI(model=CYPHER_MODEL, temperature=0),
    qa_llm=ChatOpenAI(model=QA_MODEL, temperature=0),
    graph=graph,
    verbose=True,
    qa_prompt=qa_generation_prompt,
    cypher_prompt=cypher_generation_prompt,
    validate_cypher=True,
    top_k=100,
)


