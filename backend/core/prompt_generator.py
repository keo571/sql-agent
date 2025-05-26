# sql_agent/core/prompt_generator.py
from ..utils.logger import get_logger

logger = get_logger(__name__)

class DynamicPromptGenerator:
    def __init__(self, schema_manager, relevance_analyzer):
        self.schema_manager = schema_manager
        self.relevance_analyzer = relevance_analyzer
    
    def _generate_schema_section(self, schemas, relevant_tables):
        """Generate the schema section of the prompt"""
        schema_lines = ["Database Schema:\n"]
        
        for table_name, schema in schemas.items():
            if table_name in relevant_tables:
                schema_lines.extend([
                    f"Table: {table_name}",
                    "Columns:"
                ])
                
                for column in schema['columns']:
                    nullable = "NULL" if column['nullable'] else "NOT NULL"
                    primary_key = "PRIMARY KEY" if column['primary_key'] else ""
                    schema_lines.append(f"- {column['name']}: {column['type']} {primary_key} {nullable}")
                schema_lines.append("")
        
        return "\n".join(schema_lines)
    
    def _generate_relationships_section(self, schemas, relevant_tables):
        """Generate the relationships section of the prompt"""
        relationship_lines = ["Table Relationships:\n"]
        
        for table_name, schema in schemas.items():
            if table_name in relevant_tables and schema.get('foreign_keys'):
                relationship_lines.append(f"{table_name} relationships:")
                for fk in schema['foreign_keys']:
                    relationship_lines.append(f"- {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
                relationship_lines.append("")
        
        return "\n".join(relationship_lines)
    
    def _generate_instructions_section(self):
        """Generate the instructions section of the prompt"""
        return """IMPORTANT: You must respond with ONLY a valid SQL SELECT query. Do not include any explanations, markdown formatting, or other text.

Rules:
1. The response must be a single SQL SELECT query
2. The query must start with SELECT and end with a semicolon
3. Only use tables and columns that exist in the schema above
4. Do not include any text before or after the query
5. Do not use markdown code blocks or backticks

Example of correct response:
SELECT name FROM customers WHERE id = 1;

Example of incorrect responses:
❌ Here's the query: SELECT name FROM customers WHERE id = 1;
❌ ```sql
SELECT name FROM customers WHERE id = 1;
```
❌ The query to get the customer name is: SELECT name FROM customers WHERE id = 1;"""
    
    def generate_prompt(self, query):
        """Generate a prompt with relevant schema information"""
        # Get all available schemas
        schemas = self.schema_manager.get_all_schemas()
        
        # Analyze which tables are relevant to the query
        relevant_tables = self.relevance_analyzer.analyze_query(query)
        
        # Build the prompt sections
        prompt_sections = [
            "You are a SQL expert assistant. You have access to the following database schema:\n",
            self._generate_schema_section(schemas, relevant_tables),
            self._generate_relationships_section(schemas, relevant_tables),
            self._generate_instructions_section()
        ]
        
        return "\n".join(prompt_sections)