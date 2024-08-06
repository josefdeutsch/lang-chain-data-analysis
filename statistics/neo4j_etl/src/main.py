import logging
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from retry import retry

# Load environment variables from .env file
load_dotenv()

BTCUSD_CSV_PATH = os.getenv("BTCUSD_CSV_PATH")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOGGER = logging.getLogger(__name__)

NODES = ["BTCUSD"]

def _set_uniqueness_constraints(tx, node):
    query = f"""CREATE CONSTRAINT IF NOT EXISTS FOR (n:{node})
        REQUIRE n.date IS UNIQUE;"""
    _ = tx.run(query, {})

@retry(tries=100, delay=10)
def load_btcusd_graph_from_csv() -> None:
    """Load structured BTCUSD CSV data into Neo4j"""
    #uri = "bolt://localhost:7687"
    #driver = GraphDatabase.driver(uri, auth=("neo4j", "Password"))
    driver = GraphDatabase.driver(
        NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    LOGGER.info("Setting uniqueness constraints on nodes")
    with driver.session(database="neo4j") as session:
        for node in NODES:
            session.execute_write(_set_uniqueness_constraints, node)

    LOGGER.info("Loading BTCUSD nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{BTCUSD_CSV_PATH}' AS row
        MERGE (b:BTCUSD {{
            date: row.Date,
            open: toFloat(row.Open),
            high: toFloat(row.High),
            low: toFloat(row.Low),
            close: toFloat(row.Close),
            adj_close: toFloat(row["Adj Close"]),
            volume: toFloat(row.Volume)
        }});
        """
        _ = session.run(query, {})

if __name__ == "__main__":
    load_btcusd_graph_from_csv()
