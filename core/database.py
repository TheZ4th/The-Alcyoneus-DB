# database.py
"""
The Alcyoneus DB Core Engine
Load, save, query, and manage the OSINT database
"""

import json
import os
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from collections import defaultdict
import hashlib

class AlcyoneusDB:
    """Core database engine for The Alcyoneus DB"""
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.dirname(os.path.abspath(__file__))
        self.platforms_file = os.path.normpath(os.path.join(self.data_dir, '../data/platform.json'))
        self.results_file = os.path.normpath(os.path.join(self.data_dir, '../reports/hunts/results.json'))
        self.lock = threading.Lock()
        
        # In-memory cache
        self._platforms_cache = None
        self._results_cache = None
        self._stats = {
            'total_queries': 0,
            'total_finds': 0,
            'last_update': None,
            'db_size': 0
        }
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize database files if not exist"""
        if not os.path.exists(self.platforms_file):
            self._create_default_platforms()
        
        if not os.path.exists(self.results_file):
            with open(self.results_file, 'w') as f:
                json.dump([], f, indent=2)
    
    def _create_default_platforms(self):
        """Create default platforms database"""
        default_platforms = {
            "metadata": {
                "version": "1.5.0",
                "name": "The Alcyoneus DB",
                "description": "Exceeding the average reasonable limits of databases",
                "total_platforms": 0,
                "last_updated": datetime.now().isoformat(),
                "categories": 20,
                "regions": 7
            },
            "platforms": []
        }
        
        with open(self.platforms_file, 'w') as f:
            json.dump(default_platforms, f, indent=2)
    
    def load_platforms(self) -> Dict:
        """Load platforms database"""
        if self._platforms_cache is None:
            with self.lock:
                with open(self.platforms_file, 'r') as f:
                    self._platforms_cache = json.load(f)
                    self._stats['db_size'] = os.path.getsize(self.platforms_file)
        return self._platforms_cache
    
    def save_platforms(self, data: Dict):
        """Save platforms database"""
        with self.lock:
            data['metadata']['last_updated'] = datetime.now().isoformat()
            data['metadata']['total_platforms'] = len(data.get('platforms', []))
            with open(self.platforms_file, 'w') as f:
                json.dump(data, f, indent=2)
            self._platforms_cache = data
    
    def add_platform(self, platform_data: Dict):
        """Add a new platform to database"""
        platforms_data = self.load_platforms()
        
        # Check if platform already exists
        existing = [p for p in platforms_data['platforms'] if p.get('name') == platform_data.get('name')]
        if existing:
            return False
        
        # Add required fields if missing
        required_fields = ['name', 'url_pattern', 'category', 'region', 'priority']
        for field in required_fields:
            if field not in platform_data:
                platform_data[field] = 'unknown'
        
        # Add metadata
        platform_data['added_at'] = datetime.now().isoformat()
        platform_data['verified'] = False
        platform_data['confidence'] = 50
        
        platforms_data['platforms'].append(platform_data)
        self.save_platforms(platforms_data)
        return True
    
    def search_platforms(self, query: str, field: str = 'name') -> List:
        """Search platforms by field"""
        platforms_data = self.load_platforms()
        query_lower = query.lower()
        
        results = []
        for platform in platforms_data['platforms']:
            value = platform.get(field, '')
            if query_lower in value.lower():
                results.append(platform)
        
        return results
    
    def get_platforms_by_category(self, category: str) -> List:
        """Get all platforms in a category"""
        platforms_data = self.load_platforms()
        return [p for p in platforms_data['platforms'] if p.get('category') == category]
    
    def get_platforms_by_region(self, region: str) -> List:
        """Get all platforms in a region"""
        platforms_data = self.load_platforms()
        return [p for p in platforms_data['platforms'] if p.get('region') == region]
    
    def save_results(self, query: str, results: List[Dict], query_type: str = 'username'):
        """Save search results to database"""
        with self.lock:
            # Load existing results
            if os.path.exists(self.results_file):
                with open(self.results_file, 'r') as f:
                    all_results = json.load(f)
            else:
                all_results = []
            
            # Create result entry
            result_entry = {
                'query': query,
                'query_type': query_type,
                'timestamp': datetime.now().isoformat(),
                'total_found': len(results),
                'results': results,
                'query_hash': hashlib.md5(f"{query}:{query_type}".encode()).hexdigest()
            }
            
            # Check if query already exists
            existing_idx = None
            for idx, r in enumerate(all_results):
                if r.get('query_hash') == result_entry['query_hash']:
                    existing_idx = idx
                    break
            
            if existing_idx is not None:
                all_results[existing_idx] = result_entry
            else:
                all_results.append(result_entry)
            
            # Save
            with open(self.results_file, 'w') as f:
                json.dump(all_results, f, indent=2)
            
            # Update stats
            self._stats['total_queries'] += 1
            self._stats['total_finds'] += len(results)
    
    def get_query_history(self, limit: int = 100) -> List:
        """Get query history"""
        if not os.path.exists(self.results_file):
            return []
        
        with open(self.results_file, 'r') as f:
            results = json.load(f)
        
        # Sort by timestamp descending
        results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return results[:limit]
    
    def get_query_result(self, query: str, query_type: str = 'username') -> Optional[Dict]:
        """Get specific query result"""
        query_hash = hashlib.md5(f"{query}:{query_type}".encode()).hexdigest()
        
        if not os.path.exists(self.results_file):
            return None
        
        with open(self.results_file, 'r') as f:
            results = json.load(f)
        
        for result in results:
            if result.get('query_hash') == query_hash:
                return result
        
        return None
    
    def delete_query_result(self, query: str, query_type: str = 'username') -> bool:
        """Delete specific query result"""
        query_hash = hashlib.md5(f"{query}:{query_type}".encode()).hexdigest()
        
        if not os.path.exists(self.results_file):
            return False
        
        with open(self.results_file, 'r') as f:
            results = json.load(f)
        
        new_results = [r for r in results if r.get('query_hash') != query_hash]
        
        if len(new_results) == len(results):
            return False
        
        with open(self.results_file, 'w') as f:
            json.dump(new_results, f, indent=2)
        
        return True
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        platforms_data = self.load_platforms()
        
        # Count by category
        category_counts = defaultdict(int)
        for platform in platforms_data.get('platforms', []):
            category = platform.get('category', 'unknown')
            category_counts[category] += 1
        
        # Count by region
        region_counts = defaultdict(int)
        for platform in platforms_data.get('platforms', []):
            region = platform.get('region', 'global')
            region_counts[region] += 1
        
        return {
            'total_platforms': len(platforms_data.get('platforms', [])),
            'categories': dict(category_counts),
            'regions': dict(region_counts),
            'total_queries': self._stats['total_queries'],
            'total_finds': self._stats['total_finds'],
            'db_version': platforms_data.get('metadata', {}).get('version', '1.5.0'),
            'last_updated': platforms_data.get('metadata', {}).get('last_updated'),
            'db_size_bytes': self._stats['db_size']
        }
    
    def export_platforms_json(self, filename: str = 'alcy_export.json'):
        """Export platforms to JSON file"""
        platforms_data = self.load_platforms()
        with open(filename, 'w') as f:
            json.dump(platforms_data, f, indent=2)
        return filename
    
    def import_platforms_json(self, filename: str):
        """Import platforms from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        if 'platforms' in data:
            self.save_platforms(data)
            return True
        return False
