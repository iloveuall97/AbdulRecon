#!/usr/bin/env python
# Windows compatible database initialization

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.database import init_db
from core.config_loader import ConfigLoader
from core.logger import AegisLogger

def main():
    """Initialize database"""
    # Setup logging
    logger_instance = AegisLogger()
    logger = logger_instance.get_logger()
    
    # Load configuration
    config = ConfigLoader()
    
    logger.info("=" * 50)
    logger.info("AegisRecon Pro - Database Initialization")
    logger.info("=" * 50)
    
    try:
        # Initialize database
        db_type = config.get('database.type', 'sqlite')
        logger.info(f"Initializing {db_type} database...")
        
        init_db(config)
        
        logger.info("Database initialized successfully!")
        logger.info(f"Database Type: {db_type}")
        
        if db_type == 'sqlite':
            db_path = config.get('database.sqlite_path', 'data/scans.db')
            logger.info(f"Database Location: {db_path}")
        
        logger.info("=" * 50)
        logger.info("You can now run: python api/app.py")
        logger.info("=" * 50)
        
        return 0
    
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())