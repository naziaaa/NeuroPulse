import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables
load_dotenv()

# Neo4j connection details from .env file
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

class Neo4jDemo:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_data(self):
        with self.driver.session() as session:
            session.run("CREATE (s:Student {name:'Alice'})")
            session.run("CREATE (s:Student {name:'Bob'})")
            session.run("CREATE (c:Course {name:'Math'})")
            session.run("CREATE (c:Course {name:'Physics'})")
            session.run("""
                MATCH (s:Student {name:'Alice'}), (c:Course {name:'Math'})
                CREATE (s)-[:ENROLLED_IN]->(c)
            """)
            session.run("""
                MATCH (s:Student {name:'Bob'}), (c:Course {name:'Physics'})
                CREATE (s)-[:ENROLLED_IN]->(c)
            """)

    def fetch_data(self):
        with self.driver.session() as session:
            result = session.run("MATCH (s:Student)-[:ENROLLED_IN]->(c:Course) RETURN s.name, c.name")
            for record in result:
                print(f"{record['s.name']} is enrolled in {record['c.name']}")

# Run the demo
neo4j_demo = Neo4jDemo(URI, USERNAME, PASSWORD)
neo4j_demo.create_data()
neo4j_demo.fetch_data()
neo4j_demo.close()
