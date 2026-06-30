#!/usr/bin/env python
# CLI interface for AegisRecon Pro (Windows compatible)

import sys
import argparse
from pathlib import Path
import asyncio

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.logger import AegisLogger
from core.config_loader import ConfigLoader
from core.scanner import SecurityScanner

def create_parser():
    """Create CLI argument parser"""
    parser = argparse.ArgumentParser(
        description='AegisRecon Pro - Professional Security Testing Platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py scan --target https://example.com --modules sqli,xss
  python cli.py scan --target https://example.com --scope example.com --output reports/scan.pdf
  python cli.py crawl --target https://example.com --depth 3
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Run security scan')
    scan_parser.add_argument('--target', required=True, help='Target URL')
    scan_parser.add_argument('--scope', help='Scope domain(s) (comma-separated)')
    scan_parser.add_argument('--modules', default='sqli,xss,cmdi', help='Modules to run (comma-separated)')
    scan_parser.add_argument('--depth', type=int, default=3, help='Crawl depth (default: 3)')
    scan_parser.add_argument('--output', help='Output report path')
    scan_parser.add_argument('--format', choices=['pdf', 'html', 'json', 'markdown'], default='html', help='Report format')
    scan_parser.add_argument('--proxy', help='Proxy URL')
    scan_parser.add_argument('--threads', type=int, default=10, help='Number of concurrent threads')
    
    # Crawl command
    crawl_parser = subparsers.add_parser('crawl', help='Crawl target')
    crawl_parser.add_argument('--target', required=True, help='Target URL')
    crawl_parser.add_argument('--depth', type=int, default=3, help='Crawl depth')
    crawl_parser.add_argument('--output', help='Output file')
    
    # Version
    parser.add_argument('--version', action='version', version='AegisRecon Pro v1.0.0')
    parser.add_argument('--config', default='config/local.yaml', help='Configuration file path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    return parser

def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    logger_instance = AegisLogger(args.config)
    logger = logger_instance.get_logger()
    
    # Load configuration
    config = ConfigLoader(args.config)
    
    logger.info("="*60)
    logger.info("AegisRecon Pro v1.0.0 - Security Testing Platform")
    logger.info("="*60)
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        if args.command == 'scan':
            return handle_scan(args, config, logger)
        elif args.command == 'crawl':
            return handle_crawl(args, config, logger)
        else:
            logger.error(f"Unknown command: {args.command}")
            return 1
    
    except KeyboardInterrupt:
        logger.warning("\nScan interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

def handle_scan(args, config, logger):
    """Handle scan command"""
    logger.info(f"Target: {args.target}")
    logger.info(f"Modules: {args.modules}")
    logger.info(f"Depth: {args.depth}")
    logger.info(f"Threads: {args.threads}")
    
    # Initialize scanner
    scanner = SecurityScanner(config, logger)
    
    # Parse modules
    modules = [m.strip() for m in args.modules.split(',')]
    
    # Run scan
    logger.info("Starting scan...")
    # TODO: Implement actual scanning
    logger.info("Scan completed")
    
    return 0

def handle_crawl(args, config, logger):
    """Handle crawl command"""
    logger.info(f"Target: {args.target}")
    logger.info(f"Depth: {args.depth}")
    
    # TODO: Implement crawling
    logger.info("Crawling completed")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())