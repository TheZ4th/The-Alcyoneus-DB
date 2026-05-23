# hunter.py
"""
The Alcyoneus DB - Username Hunter
Scans 100+ platforms for username existence with validation
"""

import requests
import threading
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Callable
from urllib.parse import urlparse
import random

from .database import AlcyoneusDB
from .validator import AntiFalsePositiveValidator
from .utils import get_user_agent, retry_request

class UsernameHunter:
    """Advanced username hunter with multi-threading and validation"""
    
    def __init__(self, db: AlcyoneusDB = None, validation_level: str = 'strict', 
                 max_threads: int = 30, timeout: int = 10):
        self.db = db or AlcyoneusDB()
        self.validator = AntiFalsePositiveValidator(validation_level=validation_level)
        self.max_threads = max_threads
        self.timeout = timeout
        self.session = requests.Session()
        self.results = []
        self.total_platforms = 0
        self.scanned = 0
        self.found = 0
        
        # Load platforms
        self.platforms = self._load_platforms()
        
    def _load_platforms(self) -> List[Dict]:
        """Load platforms from database"""
        platforms_data = self.db.load_platforms()
        return platforms_data.get('platforms', [])
    
    def _check_platform(self, username: str, platform: Dict) -> Optional[Dict]:
        """Check a single platform for username existence"""
        url_pattern = platform.get('url_pattern', '')
        if not url_pattern:
            return None
        
        url = url_pattern.format(username=username)
        method = platform.get('method', 'GET').upper()
        expected_status = platform.get('expected_status', [200])
        headers = {'User-Agent': get_user_agent()}
        
        start_time = time.time()
        
        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers, timeout=self.timeout, allow_redirects=True)
            elif method == 'HEAD':
                response = self.session.head(url, headers=headers, timeout=self.timeout)
            else:
                return None
            
            response_time = time.time() - start_time
            
            # Determine if username exists
            exists = response.status_code in expected_status
            
            # Additional check for custom patterns
            if platform.get('exists_pattern'):
                import re
                if re.search(platform['exists_pattern'], response.text, re.IGNORECASE):
                    exists = True
                elif re.search(platform.get('not_exists_pattern', ''), response.text, re.IGNORECASE):
                    exists = False
            
            result = {
                'platform': platform.get('name', 'Unknown'),
                'category': platform.get('category', 'unknown'),
                'region': platform.get('region', 'global'),
                'url': url,
                'status_code': response.status_code,
                'exists': exists,
                'response_time': response_time,
                'response_text': response.text[:500] if exists else '',
                'timestamp': time.time()
            }
            
            # Validate result
            if exists:
                validation = self.validator.validate_username_result(result)
                result['validation'] = validation
                result['exists'] = validation.get('valid', False)
                result['confidence'] = validation.get('confidence', 0)
            
            return result
            
        except Exception as e:
            return {
                'platform': platform.get('name', 'Unknown'),
                'category': platform.get('category', 'unknown'),
                'url': url,
                'exists': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def hunt(self, username: str, categories: List[str] = None, 
             regions: List[str] = None, platform_filter: List[str] = None,
             min_confidence: int = 60, callback: Callable = None) -> List[Dict]:
        """
        Hunt username across all platforms
        
        Args:
            username: Username to search
            categories: Filter by categories (e.g., ['social_media', 'coding'])
            regions: Filter by regions (e.g., ['global', 'asia_pacific'])
            platform_filter: Specific platforms to check
            min_confidence: Minimum confidence for results
            callback: Progress callback function
        
        Returns:
            List of results
        """
        print(f"\n{C}{BOLD}🎯 Hunting username: {username}{RESET}")
        
        # Filter platforms
        platforms_to_check = self.platforms
        
        if categories:
            platforms_to_check = [p for p in platforms_to_check if p.get('category') in categories]
        
        if regions:
            platforms_to_check = [p for p in platforms_to_check if p.get('region') in regions]
        
        if platform_filter:
            platforms_to_check = [p for p in platforms_to_check if p.get('name') in platform_filter]
        
        # Sort by priority
        platforms_to_check.sort(key=lambda x: x.get('priority', 5))
        
        self.total_platforms = len(platforms_to_check)
        self.scanned = 0
        self.found = 0
        self.results = []
        
        print(f"{C}[*] Checking {self.total_platforms} platforms...{RESET}")
        
        # Multithreaded scanning
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {
                executor.submit(self._check_platform, username, platform): platform 
                for platform in platforms_to_check
            }
            
            for future in as_completed(futures):
                self.scanned += 1
                result = future.result()
                
                if result and result.get('exists'):
                    if result.get('confidence', 0) >= min_confidence:
                        self.found += 1
                        self.results.append(result)
                        
                        # Print found result
                        confidence_color = G if result.get('confidence', 0) >= 80 else Y
                        print(f"{confidence_color}[+] FOUND: {result['platform']} -> {result['url']} (conf: {result.get('confidence', 0)}%){RESET}")
                
                # Progress callback
                if callback:
                    callback({
                        'scanned': self.scanned,
                        'total': self.total_platforms,
                        'found': self.found,
                        'current': result
                    })
                
                # Progress display
                if self.scanned % 10 == 0:
                    print(f"\r{C}[Progress] {self.scanned}/{self.total_platforms} | Found: {self.found}{RESET}", end='')
        
        print(f"\n\n{G}{BOLD}✅ Hunt completed!{RESET}")
        print(f"{C}[*] Total platforms checked: {self.scanned}{RESET}")
        print(f"{G}[*] Username found on: {self.found} platforms{RESET}")
        
        # Filter by confidence and sort
        self.results = [r for r in self.results if r.get('confidence', 0) >= min_confidence]
        self.results.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        # Save to database
        if self.results:
            self.db.save_results(username, self.results, 'username')
        
        return self.results
    
    def hunt_batch(self, usernames: List[str], **kwargs) -> Dict[str, List[Dict]]:
        """Hunt multiple usernames in batch"""
        results = {}
        
        for username in usernames:
            print(f"\n{Y}{'='*60}{RESET}")
            results[username] = self.hunt(username, **kwargs)
        
        return results
    
    def get_platforms_summary(self) -> Dict:
        """Get platforms summary statistics"""
        platforms_data = self.db.load_platforms()
        platforms = platforms_data.get('platforms', [])
        
        summary = {
            'total': len(platforms),
            'by_category': {},
            'by_region': {},
            'by_priority': {}
        }
        
        for platform in platforms:
            category = platform.get('category', 'unknown')
            summary['by_category'][category] = summary['by_category'].get(category, 0) + 1
            
            region = platform.get('region', 'global')
            summary['by_region'][region] = summary['by_region'].get(region, 0) + 1
            
            priority = platform.get('priority', 5)
            summary['by_priority'][priority] = summary['by_priority'].get(priority, 0) + 1
        
        return summary
    
    def export_results(self, filename: str = 'hunt_results.json', format: str = 'json'):
        """Export hunt results to file"""
        if format == 'json':
            with open(filename, 'w') as f:
                json.dump({
                    'timestamp': time.time(),
                    'total_found': len(self.results),
                    'results': self.results
                }, f, indent=2)
            print(f"{G}[+] Results saved to {filename}{RESET}")
        
        elif format == 'csv':
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Platform', 'Category', 'URL', 'Confidence', 'Status'])
                for r in self.results:
                    writer.writerow([
                        r.get('platform', ''),
                        r.get('category', ''),
                        r.get('url', ''),
                        r.get('confidence', 0),
                        r.get('status_code', 0)
                    ])
            print(f"{G}[+] Results saved to {filename}{RESET}")
    
    def generate_report(self) -> str:
        """Generate human-readable report"""
        report = []
        report.append("\n" + "="*60)
        report.append(f"{BOLD}THE ALCYONEUS DB - HUNT REPORT{RESET}")
        report.append("="*60)
        report.append(f"\n📊 Statistics:")
        report.append(f"   Total platforms checked: {self.scanned}")
        report.append(f"   Username found on: {self.found} platforms")
        report.append(f"   Filter rate: {self.validator.generate_validation_report(self.results).get('filter_rate', 0)}%")
        
        if self.results:
            report.append(f"\n📍 FOUND ON:")
            for i, r in enumerate(self.results[:20], 1):
                conf_color = G if r.get('confidence', 0) >= 80 else Y
                report.append(f"   {i}. {r['platform']} -> {r['url']} {conf_color}({r.get('confidence', 0)}%){RESET}")
            
            if len(self.results) > 20:
                report.append(f"   ... and {len(self.results) - 20} more")
        
        report.append("\n" + "="*60)
        
        return "\n".join(report)
