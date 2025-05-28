# backend/core/agent.py
from sqlalchemy import inspect
from ..utils.logger import get_logger
from .schema_manager import SchemaManager
from .schema_relevance_analyzer import SchemaRelevanceAnalyzer
from .prompt_generator import DynamicPromptGenerator
from ..tools.sql_agent_tool import sql_engine
from openai import OpenAI
from ..config.settings import Settings
import re

logger = get_logger(__name__)

class SchemaAwareAgent:
    def __init__(self, engine):
        self.engine = engine
        settings = Settings()
        self.schema_manager = SchemaManager(settings.SCHEMA_DB_URL)
        self.relevance_analyzer = SchemaRelevanceAnalyzer()
        self.prompt_generator = DynamicPromptGenerator(
            self.schema_manager,
            self.relevance_analyzer
        )
        
        # Initialize OpenAI client
        self.client = OpenAI()
        
        # Initialize schema metadata
        self._initialize_schema_metadata()
    
    def _clean_sql_query(self, sql_query):
        """Clean and validate the SQL query"""
        if not sql_query:
            raise ValueError("Empty response received")
        
        # Debug: Log the raw response
        logger.info(f"Raw LLM response: {repr(sql_query)}")
            
        # Remove any markdown code blocks
        sql_query = re.sub(r'```sql\s*|\s*```', '', sql_query)
        
        # Remove any explanatory text before or after the query
        sql_query = sql_query.strip()
        
        # Find the first SELECT statement
        select_match = re.search(r'SELECT.*?;', sql_query, re.IGNORECASE | re.DOTALL)
        if select_match:
            sql_query = select_match.group(0)
        else:
            # If no SELECT statement found, try to find one without semicolon
            select_match = re.search(r'SELECT.*', sql_query, re.IGNORECASE | re.DOTALL)
            if select_match:
                sql_query = select_match.group(0) + ';'
            else:
                # Debug: Log when no SELECT found
                logger.error(f"No SELECT statement found in response: {repr(sql_query)}")
                raise ValueError("No valid SELECT statement found in response")
        
        # Ensure the query starts with SELECT and ends with a semicolon
        if not sql_query.upper().startswith('SELECT'):
            raise ValueError("Query must start with SELECT")
        if not sql_query.strip().endswith(';'):
            sql_query = sql_query.strip() + ';'
        
        return sql_query
    
    def _initialize_schema_metadata(self):
        """Initialize schema metadata from the database"""
        inspector = inspect(self.engine)
        for table_name in inspector.get_table_names():
            columns = []
            for column in inspector.get_columns(table_name):
                col_info = {
                    'name': column['name'],
                    'type': str(column['type']),
                    'nullable': column.get('nullable', True),
                    'primary_key': column.get('primary_key', False)
                }
                columns.append(col_info)
            
            # Update schema in metadata database
            self.schema_manager.update_schema(table_name, columns)
    
    def _is_sql_query_request(self, query):
        """Determine if the query is asking for SQL execution"""
        # Get classification from OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a classifier that determines if a question requires SQL query execution. Respond with 'true' if the question needs SQL execution, 'false' otherwise."},
                {"role": "user", "content": query}
            ],
            temperature=0.1
        )
        
        return response.choices[0].message.content.strip().lower() == 'true'
    
    def _is_schema_request(self, query):
        """Determine if the query is asking for schema information"""
        schema_keywords = ['schema', 'tables', 'columns', 'structure', 'what tables', 'show tables', 'list tables']
        return any(keyword in query.lower() for keyword in schema_keywords)
    
    def _get_schema_info(self):
        """Get formatted schema information for all tables"""
        schemas = self.schema_manager.get_all_schemas()
        formatted_schemas = []
        
        for table_name, schema in schemas.items():
            table_info = [f"Table: {table_name}"]
            table_info.append("Columns:")
            
            for column in schema['columns']:
                nullable = "NULL" if column['nullable'] else "NOT NULL"
                primary_key = "PRIMARY KEY" if column['primary_key'] else ""
                table_info.append(f"- {column['name']}: {column['type']} {primary_key} {nullable}")
            
            formatted_schemas.append('\n'.join(table_info))
        
        return '\n\n'.join(formatted_schemas)
    
    def run(self, query):
        """Run a query and return the result"""
        # Check if this is a schema request
        if self._is_schema_request(query):
            return self._get_schema_info(), None
            
        # Check if this is a SQL query request
        if not self._is_sql_query_request(query):
            # Handle as a general question
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful SQL assistant. Answer questions about SQL and databases in a clear, concise way."},
                    {"role": "user", "content": query}
                ],
                temperature=0.1
            )
            return response.choices[0].message.content.strip(), None
        
        # Generate prompt with relevant schemas
        system_prompt = self.prompt_generator.generate_prompt(query)
        
        # Get SQL query from OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.1
        )
        
        # Get and clean the SQL query
        try:
            sql_query = self._clean_sql_query(response.choices[0].message.content.strip())
        except ValueError as e:
            logger.error(f"Invalid SQL query response: {str(e)}")
            raise ValueError(str(e))
        
        # Execute the SQL query
        try:
            result = sql_engine(sql_query, self.engine)
            return result, sql_query
        except Exception as e:
            logger.error(f"SQL query execution failed: {str(e)}")
            raise ValueError(f"Failed to execute SQL query: {str(e)}")

    def run_with_reasoning(self, query):
        """Run a query and return both the result and the SQL query used"""
        result, sql_query = self.run(query)
        
        if sql_query is None:
            # This was a general question or schema request, return just the answer
            return result
        else:
            # Format the SQL query with proper indentation
            formatted_sql = sql_query.replace('SELECT', '\nSELECT').replace('FROM', '\nFROM').replace('JOIN', '\nJOIN').replace('WHERE', '\nWHERE')
            
            # Format the result in a simple list format
            if isinstance(result, list) and result:
                formatted_result = '\n'.join(str(row) for row in result)
            else:
                formatted_result = str(result)
            
            return f"SQL Query:\n{formatted_sql}\n\nResult:\n{formatted_result}"
