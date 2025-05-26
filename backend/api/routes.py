# backend/api/routes.py
from flask import Flask, request, jsonify, render_template
from ..core.agent import SchemaAwareAgent
from ..database.connection import get_database_engine
from ..utils.logger import get_logger

logger = get_logger(__name__)

app = Flask(__name__, 
    template_folder='../../frontend/templates',
    static_folder='../../frontend/static'
)

# Initialize the agent
engine = get_database_engine()
agent = SchemaAwareAgent(engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        # Get response from agent
        response = agent.run_with_reasoning(query)
        return jsonify({'response': response})
        
    except ValueError as e:
        logger.error(f"Query error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)