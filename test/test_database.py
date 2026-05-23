# tests/test_database.py
"""
Unit tests for Alcyoneus DB
"""

import unittest
import tempfile
import os
import json
from datetime import datetime

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        from alcy.database import AlcyoneusDB
        self.db = AlcyoneusDB(data_dir=self.temp_dir)
    
    def test_init(self):
        """Test database initialization"""
        self.assertIsNotNone(self.db)
        self.assertTrue(os.path.exists(self.db.platforms_file))
        self.assertTrue(os.path.exists(self.db.results_file))
    
    def test_add_platform(self):
        """Test adding platform"""
        platform = {
            'name': 'test_platform',
            'url_pattern': 'https://test.com/{username}',
            'category': 'test',
            'region': 'global',
            'priority': 1
        }
        result = self.db.add_platform(platform)
        self.assertTrue(result)
        
        # Verify added
        platforms = self.db.load_platforms()
        found = any(p['name'] == 'test_platform' for p in platforms['platforms'])
        self.assertTrue(found)
    
    def test_search_platforms(self):
        """Test searching platforms"""
        platform = {
            'name': 'github_test',
            'url_pattern': 'https://github.com/{username}',
            'category': 'coding',
            'region': 'global',
            'priority': 1
        }
        self.db.add_platform(platform)
        
        results = self.db.search_platforms('github', 'name')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'github_test')
    
    def test_save_and_get_results(self):
        """Test saving and retrieving results"""
        results = [{'platform': 'test', 'exists': True}]
        self.db.save_results('testuser', results, 'username')
        
        saved = self.db.get_query_result('testuser', 'username')
        self.assertIsNotNone(saved)
        self.assertEqual(saved['total_found'], 1)
        self.assertEqual(saved['query'], 'testuser')

if __name__ == '__main__':
    unittest.main()
