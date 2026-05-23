#utils.py
"""
The Alcyoneus DB - Helper Utilities
User-Agent rotation, retry logic, and common helpers
"""

import random
import time
from typing import Optional, Callable
from functools import wraps

# User-Agent list for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 Chrome/120.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edge/120.0.2210.61',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15',
    'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
]

# Mobile user agents (for region-specific scanning)
MOBILE_USER_AGENTS = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 Chrome/120.0.0.0',
    'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 Chrome/120.0.0.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Linux; Android 12; SM-A325F) AppleWebKit/537.36 Chrome/120.0.0.0'
]

def get_user_agent(mobile: bool = False) -> str:
    """Get random user agent"""
    agents = MOBILE_USER_AGENTS if mobile else USER_AGENTS
    return random.choice(agents)

def get_desktop_user_agent() -> str:
    """Get desktop user agent"""
    return random.choice(USER_AGENTS)

def get_mobile_user_agent() -> str:
    """Get mobile user agent"""
    return random.choice(MOBILE_USER_AGENTS)

def retry_request(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator for retrying failed requests"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

def chunk_list(lst: list, chunk_size: int) -> list:
    """Split list into chunks"""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def normalize_username(username: str) -> str:
    """Normalize username for consistent searching"""
    # Remove leading/trailing spaces
    username = username.strip()
    # Remove @ if present
    if username.startswith('@'):
        username = username[1:]
    # Convert to lowercase
    username = username.lower()
    # Replace spaces with underscores (common pattern)
    username = username.replace(' ', '_')
    return username

def extract_domain(email: str) -> Optional[str]:
    """Extract domain from email address"""
    if '@' in email:
        return email.split('@')[1]
    return None

def is_valid_domain(domain: str) -> bool:
    """Check if domain looks valid"""
    if not domain or '.' not in domain:
        return False
    import re
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))

def calculate_entropy(text: str) -> float:
    """Calculate entropy of a string (for password analysis)"""
    if not text:
        return 0.0
    
    from math import log2
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    
    entropy = 0
    for count in freq.values():
        prob = count / len(text)
        entropy -= prob * log2(prob)
    
    return entropy

def format_timestamp(timestamp: float = None) -> str:
    """Format timestamp to readable string"""
    from datetime import datetime
    if timestamp is None:
        timestamp = time.time()
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe saving"""
    import re
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces/dots
    filename = filename.strip('. ')
    # Limit length
    if len(filename) > 200:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = f"{name[:190]}.{ext}" if ext else name[:200]
    return filename
