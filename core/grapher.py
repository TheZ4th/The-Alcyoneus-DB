from data.categories_db import CATEGORIES,PLATFORM_CATEGORIES
from data.provider_db import PROVIDERS
from data.regions_db import REGIONS,REGION_PLATFORMS,REGIONAL_SEARCH_ENGINES
import re

class GrapherSystem:

    @staticmethod
    def get_category_info(category_id: str) -> dict:
        """Get category information by ID"""
        return CATEGORIES.get(category_id, {
            'name': 'Unknown',
            'description': 'Uncategorized',
            'icon': '📁',
            'priority': 5
        })

    @staticmethod
    def get_all_categories() -> list:
        """Get all category IDs"""
        return list(CATEGORIES.keys())

    @staticmethod
    def get_categories_by_priority(priority: int) -> list:
        """Get categories by priority level"""
        return [cat for cat, info in CATEGORIES.items() if info.get('priority') == priority]

    @staticmethod
    def get_region_info(region_id: str) -> dict:
        """Get region information by ID"""
        return REGIONS.get(region_id, REGIONS['global'])

    @staticmethod
    def get_country_region(country_code: str) -> str:
        """Get region for a country code"""
        for region_id, region_info in REGIONS.items():
            if country_code in region_info.get('countries', []):
                return region_id
        return 'global'

    @staticmethod
    def get_region_platforms(region_id: str) -> list:
        """Get platforms popular in a region"""
        return REGION_PLATFORMS.get(region_id, [])

    @staticmethod
    def get_region_search_engines(region_id: str) -> list:
        """Get search engines for a region"""
        return REGIONAL_SEARCH_ENGINES.get(region_id, ['google.com'])

    @staticmethod
    def get_provider_by_number(phone_number: str):
        """
        Deteksi provider berdasarkan nomor telepon
        """
        cleaned = re.sub(r'[\s\-\(\)]', '', phone_number.strip())
        for country_code, data in PROVIDERS.items():
            if re.match(data['regex'], cleaned):
                local_number = cleaned
                if cleaned.startswith(data['code']):
                    local_number = cleaned[len(data['code']):]
                elif cleaned.startswith('0'):
                    local_number = cleaned[1:]

                for prefix_len in [4, 3]:
                    if len(local_number) >= prefix_len:
                        prefix = local_number[:prefix_len]
                        if prefix in data['prefixes']:
                            return {
                                'country': data['name'],
                                'country_code': data['code'],
                                'provider': data['prefixes'][prefix],
                                'cleaned': cleaned
                            }

                if 'mvno' in data:
                    for prefix, provider in data['mvno'].items():
                        if local_number.startswith(prefix):
                            return {
                                'country': data['name'],
                                'country_code': data['code'],
                                'provider': provider,
                                'cleaned': cleaned
                            }

                return {
                    'country': data['name'],
                    'country_code': data['code'],
                    'provider': 'Unknown',
                    'cleaned': cleaned
                }

        return None


