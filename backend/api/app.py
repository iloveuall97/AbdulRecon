#!/usr/bin/env python
# Main Flask application (Windows compatible)

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, jsonify
from flask_cors import CORS
from core.config_loader import ConfigLoader
from core.logger import AegisLogger

def create_app(config_path='config/local.yaml'):
    """Create Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    config = ConfigLoader(config_path)
    app.config['SECRET_KEY'] = config.get('app.secret_key', 'dev-key')
    
    # Setup logging
    logger_instance = AegisLogger(config_path)
    logger = logger_instance.get_logger()
    
    # Enable CORS
    cors_origins = config.get('security.cors_origins', ['http://localhost:3000'])
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})
    
    # Store logger in app context
    app.logger_instance = logger
    app.config_instance = config
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({
            'status': 'ok',
            'service': 'AegisRecon Pro API',
            'version': '1.0.0'
        })
    
    # API v1 routes
    @app.route('/api/v1/scans', methods=['GET'])
    def get_scans():
        """List all scans"""
        return jsonify({
            'scans': [],
            'total': 0
        })
    
    @app.route('/api/v1/scans', methods=['POST'])
    def create_scan():
        """Create new scan"""
        return jsonify({
            'scan_id': 'test-scan-123',
            'status': 'created'
        }), 201
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Internal error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    
    logger.info(f"Flask app created successfully")
    return app

if __name__ == '__main__':
    # Create app
    app = create_app()
    
    config = ConfigLoader()
    logger = app.logger_instance
    
    host = config.get('app.host', '127.0.0.1')
    port = config.get('app.port', 5000)
    debug = config.get('app.debug', False)
    
    logger.info("="*60)
    logger.info("AegisRecon Pro API")
    logger.info("="*60)
    logger.info(f"Starting server on http://{host}:{port}")
    logger.info(f"Debug mode: {debug}")
    logger.info("="*60)
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        logger.info("\nServer shutdown by user")