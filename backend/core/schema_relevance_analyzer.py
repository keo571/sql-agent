from transformers import pipeline
import re
from sqlalchemy import inspect
from backend.database.connection import get_database_engine
from functools import lru_cache

class SchemaRelevanceAnalyzer:
    def __init__(self):
        # Initialize a zero-shot classification pipeline
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        # Get database engine
        self.engine = get_database_engine()
        
        # Cache for table keywords to avoid recomputing
        self._keyword_cache = {}
    
    def _extract_keywords_from_name(self, name):
        """Extract keywords from table or column names"""
        keywords = []
        
        # Split by underscore
        parts = name.split('_')
        keywords.extend([part.lower() for part in parts if part])
        
        # Split camelCase
        camel_parts = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', name)
        keywords.extend([part.lower() for part in camel_parts if part])
        
        # Add the full name
        keywords.append(name.lower())
        
        return list(set(keywords))  # Remove duplicates
    
    def _get_table_keywords(self, table_name):
        """Get keywords for a table based on its name and column names (cached)"""
        if table_name in self._keyword_cache:
            return self._keyword_cache[table_name]
            
        keywords = set()
        
        # Add keywords from table name
        keywords.update(self._extract_keywords_from_name(table_name))
        
        # Add keywords from column names
        inspector = inspect(self.engine)
        try:
            columns = inspector.get_columns(table_name)
            for column in columns:
                column_keywords = self._extract_keywords_from_name(column['name'])
                keywords.update(column_keywords)
        except Exception:
            # If we can't get columns, just use table name
            pass
        
        # Cache the result
        result = list(keywords)
        self._keyword_cache[table_name] = result
        return result
    
    @lru_cache(maxsize=1000)
    def _classify_table_relevance(self, query, table_name):
        """Cached AI classification for table relevance"""
        result = self.classifier(
            query,
            candidate_labels=[f"Information about {table_name}"],
            hypothesis_template="This query is asking for {}"
        )
        return result['scores'][0]
    
    def analyze_query(self, query, max_tables=10):
        """
        Determine which tables are relevant to the query
        
        Args:
            query: The user query
            max_tables: Maximum number of tables to return (for performance)
        """
        # Get all available tables from the database
        inspector = inspect(self.engine)
        available_tables = inspector.get_table_names()
        
        # Extract potential table names from the query
        query_lower = query.lower()
        query_terms = set(re.findall(r'\w+', query_lower))
        
        # Stage 1: Fast keyword matching
        high_confidence_tables = []
        maybe_relevant_tables = []
        
        for table in available_tables:
            # Check for direct table name mentions (highest confidence)
            if table.lower() in query_lower:
                high_confidence_tables.append((table, 1.0))
                continue
            
            # Check dynamic keywords
            table_keywords = self._get_table_keywords(table)
            keyword_matches = sum(1 for keyword in table_keywords if keyword in query_terms)
            
            if keyword_matches > 0:
                # Score based on number of keyword matches
                score = min(keyword_matches / len(table_keywords), 0.9)
                if score > 0.3:
                    high_confidence_tables.append((table, score))
                else:
                    maybe_relevant_tables.append(table)
            else:
                maybe_relevant_tables.append(table)
        
        # Stage 2: AI classification for uncertain cases (limited to avoid performance issues)
        ai_classified_tables = []
        if len(high_confidence_tables) < max_tables and maybe_relevant_tables:
            # Only classify a subset to avoid performance issues
            tables_to_classify = maybe_relevant_tables[:min(20, max_tables * 2)]
            
            for table in tables_to_classify:
                try:
                    ai_score = self._classify_table_relevance(query, table)
                    if ai_score > 0.3:
                        ai_classified_tables.append((table, ai_score))
                except Exception:
                    # If AI classification fails, skip this table
                    continue
        
        # Combine and sort results
        all_relevant = high_confidence_tables + ai_classified_tables
        all_relevant.sort(key=lambda x: x[1], reverse=True)  # Sort by confidence score
        
        # Return top tables, respecting max_tables limit
        relevant_tables = [table for table, score in all_relevant[:max_tables]]
        
        # Fallback: if no tables found, return a few most likely candidates
        if not relevant_tables:
            # Return first few tables as fallback, but limit the number
            relevant_tables = available_tables[:min(5, len(available_tables))]
        
        return relevant_tables