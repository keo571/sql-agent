# SQL Agent

A natural language to SQL query agent that helps users interact with databases using plain English. The agent understands database schemas and can generate appropriate SQL queries based on user questions.

## Features

- Natural language to SQL query conversion
- Intelligent schema analysis and table selection
- Case-insensitive querying
- Interactive web interface
- Complex SQL queries with JOINs
- Error handling and validation

## Recent Improvements

### Case-Insensitive Query Enhancement
The agent now provides robust case-insensitive querying capabilities:
- **Flexible input handling**: Users can enter queries with any case variation (e.g., "us-east", "US-EAST", "Us-East")
- **Smart value matching**: The system automatically handles case variations in database lookups
- **Improved user experience**: No need to worry about exact case matching when querying data

### Advanced Relevancy Analyzer
Enhanced the query analysis system to make the agent more intelligent:
- **Context-aware table selection**: Automatically identifies which database tables are most relevant to each query
- **Optimized prompt generation**: Includes only necessary schema information, improving response accuracy
- **Better performance**: Reduced token usage while maintaining query accuracy
- **Smarter JOIN detection**: Improved ability to determine when table relationships are needed

These improvements make the agent significantly more robust and user-friendly, allowing for more natural interactions with your database.

## Project Structure

```
sql-agent/
├── README.md           # Project documentation and setup guide
├── CHANGELOG.md        # Detailed change history and version tracking
├── requirements.txt    # Python dependencies
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
├── tests/              # Test files and test questions
│   └── test_questions.md  # Example queries for testing
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

### Basic Queries
- "Show me all load balancers in us-east"
- "List all VIP members with port 8080"
- "What are all the VIP addresses in the system?"
- "What tables do you have?"

### JOIN Operations
- "Show me all load balancers and their VIP addresses"
- "Display load balancer names along with their VIP member addresses"

### Case-Insensitive Filtering
- "Find load balancers in US-EAST" (works with any case)
- "Show me devices with names like lb-prod%" 

### Complex Queries
- "Show me load balancers in us-east that have VIPs on port 80"
- "List all VIP members that are associated with load balancers in us-west"

For more test questions, see [tests/test_questions.md](tests/test_questions.md).

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
