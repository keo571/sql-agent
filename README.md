# SQL Agent

A natural language to SQL query agent that helps users interact with databases using plain English. The agent understands database schemas and can generate appropriate SQL queries based on user questions.

## Features

- Natural language to SQL query conversion
- Dynamic prompt generation based on query context and schema relevance
- Schema-aware query generation
- Interactive web interface
- Support for complex SQL queries with JOINs
- Schema information retrieval
- Error handling and validation

## Project Structure

```
sql-agent/
├── backend/
│   ├── api/            # Flask API endpoints
│   ├── core/           # Core agent logic
│   │   ├── prompt_generator.py  # Dynamic prompt generation
│   │   ├── schema_manager.py    # Schema management
│   │   └── agent.py            # Main agent logic
│   ├── database/       # Database connection and utilities
│   ├── tools/          # SQL execution tools
│   └── utils/          # Utility functions
├── frontend/
│   ├── static/         # Static files (CSS, JS)
│   └── templates/      # HTML templates
├── data/               # Sample data and database files
├── scripts/            # Utility scripts
└── notebooks/          # Jupyter notebooks for development
```

## Prerequisites

- Python 3.8+
- SQLite3
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sql-agent.git
cd sql-agent
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key'  # On Windows: set OPENAI_API_KEY=your-api-key
```

## Usage

1. Start the server:
```bash
python -m backend.api.routes
```

2. Open your browser and navigate to:
```
http://localhost:5001
```

3. Start asking questions! For example:
- "What tables do you have?"
- "What items did Alice buy?"
- "What is the total amount spent by each customer?"
- "Which customers spent more than $30 and left a tip greater than $10?"
- "What are the top 3 most expensive items purchased?"
- "Show me all purchases with customer names and item details"
- "Which customers have made more than 2 purchases?"

## How It Works

The agent uses a dynamic prompt generation system that:
1. Analyzes the user's question to determine relevant database tables
2. Generates a context-aware prompt including only the necessary schema information
3. Adapts the prompt based on query complexity and requirements
4. Ensures efficient and accurate SQL query generation

This dynamic approach allows the agent to:
- Focus on relevant schema information for each query
- Handle complex queries with multiple table joins
- Provide accurate results even with large database schemas
- Optimize token usage by including only necessary context