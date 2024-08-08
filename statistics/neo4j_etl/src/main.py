import logging
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from retry import retry

# Load environment variables from .env file
load_dotenv()

BTCUSD_CSV_PATH = os.getenv("BTCUSD_CSV_PATH")
ETHUSD_CSV_PATH = os.getenv("ETHUSD_CSV_PATH")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOGGER = logging.getLogger(__name__)

NODES = ["BTCUSD", "ETHUSD"]

def _set_uniqueness_constraints(tx, node):
    query = f"""CREATE CONSTRAINT IF NOT EXISTS FOR (n:{node})
        REQUIRE n.date IS UNIQUE;"""
    _ = tx.run(query, {})

@retry(tries=100, delay=10)
def load_graph_from_csv(csv_path, node_label) -> None:
    """Load structured CSV data into Neo4j"""
    driver = GraphDatabase.driver(
        NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    LOGGER.info(f"Setting uniqueness constraints on {node_label} nodes")
    with driver.session(database="neo4j") as session:
        session.execute_write(_set_uniqueness_constraints, node_label)

    LOGGER.info(f"Loading {node_label} nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{csv_path}' AS row
        MERGE (b:{node_label} {{ date: row.Date }})
        ON CREATE SET
            b.open = toFloat(row.Open),
            b.high = toFloat(row.High),
            b.low = toFloat(row.Low),
            b.close = toFloat(row.Close),
            b.adj_close = toFloat(row["Adj Close"]),
            b.volume = toFloat(row.Volume)
        ON MATCH SET
            b = b;  // No operation on match
        """
        _ = session.run(query, {})

if __name__ == "__main__":
    load_graph_from_csv(BTCUSD_CSV_PATH, "BTCUSD")
    load_graph_from_csv(ETHUSD_CSV_PATH, "ETHUSD")
