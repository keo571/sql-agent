from transformers import pipeline
import re
from sqlalchemy import inspect
from backend.database.connection import get_database_engine

class SchemaRelevanceAnalyzer:
    def __init__(self):
        # Initialize a zero-shot classification pipeline
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        # Get database engine
        self.engine = get_database_engine()
    
    def analyze_query(self, query):
        """Determine which tables are relevant to the query"""
        # Get all available tables from the database
        inspector = inspect(self.engine)
        available_tables = inspector.get_table_names()
        
        # Extract potential table names from the query
        query_terms = set(re.findall(r'\w+', query.lower()))
        
        # Get table descriptions from schema manager
        relevant_tables = []
        for table in available_tables:
            # Use zero-shot classification to determine relevance
            result = self.classifier(
                query,
                candidate_labels=[f"Information about {table}"],
                hypothesis_template="This query is asking for {}"
            )
            
            if result['scores'][0] > 0.5:  # Threshold for relevance
                relevant_tables.append(table)
        
        return relevant_tables