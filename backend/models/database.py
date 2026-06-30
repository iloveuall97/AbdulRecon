from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum
from pathlib import Path

Base = declarative_base()

class VulnerabilitySeverity(enum.Enum):
    """Vulnerability severity levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    INFO = 5

class Scan(Base):
    """Scan history model"""
    __tablename__ = 'scans'
    
    id = Column(Integer, primary_key=True)
    scan_id = Column(String(50), unique=True, nullable=False)
    target_url = Column(String(500), nullable=False)
    scope = Column(String(500))
    modules = Column(Text)  # JSON list of modules
    status = Column(String(50), default='pending')  # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    total_issues = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)

class Vulnerability(Base):
    """Vulnerability findings model"""
    __tablename__ = 'vulnerabilities'
    
    id = Column(Integer, primary_key=True)
    scan_id = Column(String(50), nullable=False)
    type = Column(String(100), nullable=False)  # sqli, xss, cmdi, etc.
    severity = Column(Enum(VulnerabilitySeverity), default=VulnerabilitySeverity.MEDIUM)
    url = Column(String(500), nullable=False)
    parameter = Column(String(200))
    payload = Column(Text)
    response = Column(Text)
    proof_of_concept = Column(Text)
    description = Column(Text)
    remediation = Column(Text)
    cvss_score = Column(Integer)  # 0-10
    detected_at = Column(DateTime, default=datetime.utcnow)

def init_db(config):
    """Initialize database"""
    db_type = config.get('database.type', 'sqlite')
    
    if db_type == 'sqlite':
        db_path = config.get('database.sqlite_path', 'data/scans.db')
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        connection_string = f'sqlite:///{db_path}'
    elif db_type == 'postgresql':
        pg_config = config.get('database.postgresql', {})
        user = pg_config.get('user', 'aegisrecon')
        password = pg_config.get('password', 'password')
        host = pg_config.get('host', 'localhost')
        port = pg_config.get('port', 5432)
        database = pg_config.get('database', 'aegisrecon_db')
        connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """Get database session"""
    Session = sessionmaker(bind=engine)
    return Session()