from abc import ABC, abstractmethod
from typing import Dict, List, Any

class BaseVulnerabilityDetector(ABC):
    """Base class for all vulnerability detectors"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.module_name = self.__class__.__name__
    
    @abstractmethod
    async def detect(self, url: str, parameters: Dict[str, str]) -> List[Dict[str, Any]]:
        """Detect vulnerabilities
        
        Args:
            url: Target URL
            parameters: Parameters to test
        
        Returns:
            List of detected vulnerabilities
        """
        pass
    
    def get_payloads(self) -> List[str]:
        """Get list of payloads for this detector"""
        return []
    
    def log_finding(self, url: str, parameter: str, severity: str, description: str):
        """Log a vulnerability finding"""
        self.logger.info(f"[{self.module_name}] {severity}: {url} - {parameter}")