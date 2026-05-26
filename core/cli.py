# cli.py
#!/usr/bin/env python3
"""
The Alcyoneus DB - Command Line Interface
Exceeding the average reasonable limits of OSINT databases
"""

import argparse
import sys
import json
from datetime import datetime

from database import AlcyoneusDB
from hunter import UsernameHunter
from validator import AntiFalsePositiveValidator
from exporter import DataExporter

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
C = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_banner():
    """Print The Alcyoneus DB banner"""
    banner = f"""
{C}{BOLD}
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   █████╗ ██╗      ██████╗██╗   ██╗ ██████╗ ███╗   ██╗███████╗██╗   ██╗███████╗
║  ██╔══██╗██║     ██╔════╝██║   ██║██╔═══██╗████╗  ██║██╔════╝██║   ██║██╔════╝
║  ███████║██║     ██║     ██║   ██║██║   ██║██╔██╗ ██║█████╗  ██║   ██║███████╗
║  ██╔══██║██║     ██║     ██║   ██║██║   ██║██║╚██╗██║██╔══╝  ██║   ██║╚════██║
║  ██║  ██║███████╗╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║███████╗╚██████╔╝███████║
║  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚══════╝
║                                                                               ║
║         Exceeding the average reasonable limits of OSINT databases           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
{RESET}
    """
    print(banner)

def main():
    parser = argparse.ArgumentParser(
        description='The Alcyoneus DB - Advanced OSINT Database Framework',
        epilog='Example: alcy -u johndoe --categories social_media,coding --export json'
    )
    
    # Search options
    parser.add_argument('-u', '--username', help='Username to search')
    parser.add_argument('-e', '--email', help='Email to search')
    parser.add_argument('-p', '--phone', help='Phone number to search')
    parser.add_argument('-b', '--batch', help='File containing list of usernames (one per line)')
    
    # Filter options
    parser.add_argument('--categories', help='Comma-separated categories (e.g., social_media,coding)')
    parser.add_argument('--regions', help='Comma-separated regions (e.g., global,asia_pacific)')
    parser.add_argument('--platforms', help='Comma-separated specific platforms')
    parser.add_argument('--min-confidence', type=int, default=60, help='Minimum confidence threshold (0-100)')
    
    # Validation options
    parser.add_argument('--validation-level', choices=['basic', 'strict', 'paranoid'], 
                        default='strict', help='Anti-false-positive validation level')
    parser.add_argument('--no-filter', action='store_true', help='Disable false positive filtering')
    
    # Export options
    parser.add_argument('--export', choices=['json', 'csv', 'html', 'pdf', 'markdown'], 
                        help='Export results to format')
    parser.add_argument('-o', '--output', help='Output filename')
    
    # Database options
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    parser.add_argument('--list-platforms', action='store_true', help='List all platforms')
    parser.add_argument('--list-categories', action='store_true', help='List all categories')
    parser.add_argument('--list-regions', action='store_true', help='List all regions')
    
    # Performance options
    parser.add_argument('--threads', type=int, default=30, help='Number of threads (default: 30)')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout in seconds (default: 10)')
    
    # Other
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='version', version='Alcyoneus DB v1.0.0')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Initialize components
    db = AlcyoneusDB()
    validator = AntiFalsePositiveValidator(
        validation_level=args.validation_level,
        min_confidence=args.min_confidence
    )
    exporter = DataExporter()
    
    # Handle stats
    if args.stats:
        stats = db.get_stats()
        print(f"\n{C}{BOLD}📊 DATABASE STATISTICS{RESET}")
        print(f"{Y}Total Platforms:{RESET} {stats['total_platforms']}")
        print(f"{Y}Total Categories:{RESET} {len(stats['categories'])}")
        print(f"{Y}Total Regions:{RESET} {len(stats['regions'])}")
        print(f"{Y}Total Queries:{RESET} {stats['total_queries']}")
        print(f"{Y}Total Finds:{RESET} {stats['total_finds']}")
        print(f"{Y}DB Version:{RESET} {stats['db_version']}")
        print(f"{Y}Last Updated:{RESET} {stats['last_updated']}")
        return
    
    # Handle list platforms
    if args.list_platforms:
        platforms_data = db.load_platforms()
        platforms = platforms_data.get('platforms', [])
        print(f"\n{C}{BOLD}📋 PLATFORMS ({len(platforms)}){RESET}")
        for p in platforms[:50]:
            print(f"  {Y}- {p.get('name')}{RESET} [{p.get('category')}]")
        if len(platforms) > 50:
            print(f"  ... and {len(platforms)-50} more")
        return
    
    # Handle hunt
    if args.username or args.email or args.phone or args.batch:
        hunter = UsernameHunter(
            db=db,
            validation_level=args.validation_level,
            max_threads=args.threads,
            timeout=args.timeout
        )
        
        # Parse filters
        categories = args.categories.split(',') if args.categories else None
        regions = args.regions.split(',') if args.regions else None
        platforms = args.platforms.split(',') if args.platforms else None
        
        # Batch processing
        if args.batch:
            with open(args.batch, 'r') as f:
                usernames = [line.strip() for line in f if line.strip()]
            print(f"{C}[*] Batch hunting {len(usernames)} usernames...{RESET}")
            
            results = hunter.hunt_batch(
                usernames,
                categories=categories,
                regions=regions,
                platform_filter=platforms,
                min_confidence=args.min_confidence if not args.no_filter else 0
            )
            
            # Export batch results
            if args.export:
                filename = args.output or f"alcy_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                if args.export == 'json':
                    filepath = exporter.export_json(results, f"{filename}.json")
                elif args.export == 'csv':
                    # Flatten results for CSV
                    flat_results = []
                    for username, user_results in results.items():
                        for r in user_results:
                            r['searched_username'] = username
                            flat_results.append(r)
                    filepath = exporter.export_csv(flat_results, f"{filename}.csv")
                elif args.export == 'html':
                    filepath = exporter.export_html(flat_results, query=f"Batch {len(usernames)} users", filename=f"{filename}.html")
                print(f"{G}[+] Results exported to {filepath}{RESET}")
            
            return
        
        # Single hunt
        query = args.username or args.email or args.phone
        query_type = 'username' if args.username else 'email' if args.email else 'phone'
        
        results = hunter.hunt(
            query,
            categories=categories,
            regions=regions,
            platform_filter=platforms,
            min_confidence=args.min_confidence if not args.no_filter else 0
        )
        
        # Display report
        print(hunter.generate_report())
        
        # Export results
        if args.export and results:
            filename = args.output or f"alcy_{query}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            if args.export == 'json':
                filepath = exporter.export_json({
                    'query': query,
                    'query_type': query_type,
                    'timestamp': datetime.now().isoformat(),
                    'results': results
                }, f"{filename}.json")
            elif args.export == 'csv':
                filepath = exporter.export_csv(results, f"{filename}.csv")
            elif args.export == 'html':
                filepath = exporter.export_html(results, query=query, filename=f"{filename}.html")
            elif args.export == 'pdf':
                filepath = exporter.export_pdf(results, f"{filename}.pdf")
            elif args.export == 'markdown':
                filepath = exporter.export_markdown(results, query=query, filename=f"{filename}.md")
            
            if filepath:
                print(f"{G}[+] Results exported to {filepath}{RESET}")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
