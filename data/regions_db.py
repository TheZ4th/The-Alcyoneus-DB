# regions.py
"""
The Alcyoneus DB - Regional Data
Hyper-local intelligence for region-specific platforms
"""

REGIONS = {
    'global': {
        'name': 'Global',
        'description': 'Worldwide platforms',
        'icon': '🌍',
        'priority': 1
    },
    'north_america': {
        'name': 'North America',
        'description': 'USA, Canada, Mexico',
        'icon': '🌎',
        'priority': 2,
        'countries': ['US', 'CA', 'MX']
    },
    'europe': {
        'name': 'Europe',
        'description': 'European Union and UK',
        'icon': '🌍',
        'priority': 2,
        'countries': ['UK', 'DE', 'FR', 'ES', 'IT', 'NL', 'PL', 'SE', 'NO', 'DK']
    },
    'asia_pacific': {
        'name': 'Asia Pacific',
        'description': 'China, Japan, Korea, Southeast Asia',
        'icon': '🌏',
        'priority': 2,
        'countries': ['CN', 'JP', 'KR', 'IN', 'ID', 'TH', 'VN', 'PH', 'MY', 'SG', 'AU', 'NZ']
    },
    'latin_america': {
        'name': 'Latin America',
        'description': 'South and Central America',
        'icon': '🌎',
        'priority': 3,
        'countries': ['BR', 'AR', 'CO', 'CL', 'PE', 'VE', 'EC', 'GT', 'BO']
    },
    'middle_east': {
        'name': 'Middle East',
        'description': 'GCC countries and Middle East',
        'icon': '🌍',
        'priority': 3,
        'countries': ['SA', 'AE', 'QA', 'KW', 'BH', 'OM', 'JO', 'EG', 'IR', 'IQ', 'IL']
    },
    'africa': {
        'name': 'Africa',
        'description': 'African continent platforms',
        'icon': '🌍',
        'priority': 3,
        'countries': ['ZA', 'NG', 'EG', 'KE', 'MA', 'GH', 'TN', 'DZ']
    }
}

# Region-specific platforms
REGION_PLATFORMS = {
    'north_america': [
        'facebook', 'twitter', 'instagram', 'linkedin', 'reddit', 'tumblr',
        'snapchat', 'pinterest', 'quora', 'yelp', 'craigslist', 'nextdoor'
    ],
    'europe': [
        'xing', 'viadeo', 'skyrock', 'copainsdavant', 'marktplaats',
        'subito', 'olx', 'allegro', 'leboncoin', 'gumtree'
    ],
    'asia_pacific': [
        'weibo', 'wechat', 'qq', 'douyin', 'xiaohongshu', 'baidu_tieba',
        'renren', 'line', 'kakao_talk', 'cyworld', 'mixi', 'rakuten',
        'tokopedia', 'shopee', 'lazada', 'gojek', 'grab'
    ],
    'latin_america': [
        'mercadolivre', 'mercadolibre', 'taringa', 'vakinha', 'getninjas'
    ],
    'middle_east': [
        'telegram', 'clubhouse', 'yalla', 'tango', 'imo', 'viber'
    ],
    'africa': [
        'bubble', '2go', 'mxiti', 'ayoba', 'talk360', 'truelife'
    ]
}

# Regional search engines (for hyper-local OSINT)
REGIONAL_SEARCH_ENGINES = {
    'north_america': ['google.com', 'bing.com', 'yahoo.com'],
    'europe': ['google.de', 'google.fr', 'google.co.uk', 'qwant.com', 'yandex.ru', 'seznam.cz'],
    'asia_pacific': ['google.co.jp', 'naver.com', 'baidu.com', 'yandex.ru', 'yahoo.co.jp'],
    'latin_america': ['google.com.br', 'google.com.mx', 'mercadolibre.com'],
    'middle_east': ['google.ae', 'yandex.ru', 'google.sa'],
    'africa': ['google.co.za', 'google.co.ke']
}
