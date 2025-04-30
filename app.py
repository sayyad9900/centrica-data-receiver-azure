from flask import Flask, request, jsonify
import logging
from datetime import datetime
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store received data in memory (for demo purposes)
# In production, you'd want to use a database
received_data = []

@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data received"}), 400
            
        logger.info(f"Received data: {data}")
        
        # Add timestamp and store
        data_with_timestamp = {
            "received_at": datetime.utcnow().isoformat(),
            "data": data
        }
        received_data.append(data_with_timestamp)
        
        # In production, you'd save to a database here
        
        return jsonify({"status": "success", "message": "Data received"}), 200
        
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"data": received_data}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
