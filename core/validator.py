# validator.py
"""
The Alcyoneus DB - Anti-False-Positive Validator
Validates OSINT results to ensure accuracy and reduce noise
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class AntiFalsePositiveValidator:
    """Advanced validation system for OSINT results"""
    
    def __init__(self, validation_level: str = 'strict', min_confidence: int = 60):
        self.validation_level = validation_level
        self.min_confidence = min_confidence
        self.validation_cache = {}
        
        # False positive patterns (will be loaded from JSON)
        self.fp_patterns = {
            'status_codes': {
                'valid': [200, 201, 202, 204],
                'warning': [301, 302, 307, 308, 403, 429, 404],
                'invalid': [400, 401, 500, 502, 503, 504]
            },
            'error_indicators': [
                'not found', 'does not exist', 'no such user', 'user not found',
                'profile not found', 'page not found', '404 error', '500 error',
                'account suspended', 'user deleted', 'account not active',
                'this profile is not available', 'sorry, nothing here'
            ],
            'placeholder_indicators': [
                'under construction', 'coming soon', 'maintenance mode',
                'default page', 'welcome to', 'test page', 'sample page',
                'example domain', 'this domain is for sale'
            ],
            'bot_indicators': [
                'captcha', 'challenge', 'verify you are human', 'robot check',
                'access denied', 'blocked', 'rate limited', 'too many requests',
                'our systems have detected', 'automated request'
            ],
            'valid_indicators': [
                'joined', 'member since', 'followers', 'following', 'posts',
                'profile', 'account', 'user', 'activity', 'dashboard',
                'settings', 'logout', 'sign out', 'edit profile'
            ]
        }
        
        # Confidence weights
        self.weights = {
            'status_code': 30,
            'content_analysis': 40,
            'response_time': 10,
            'url_pattern': 20
        }
    
    def validate_username_result(self, result: Dict) -> Dict:
        """Validate a username search result"""
        url = result.get('url', '')
        status_code = result.get('status_code', 0)
        response_text = result.get('response_text', '').lower()
        response_time = result.get('response_time', 0)
        
        validation_result = {
            'url': url,
            'valid': True,
            'confidence': 100,
            'errors': [],
            'warnings': [],
            'score_breakdown': {}
        }
        
        # 1. Status code validation
        status_score = self._validate_status_code(status_code)
        validation_result['score_breakdown']['status_code'] = status_score
        if status_score < 50:
            validation_result['errors'].append(f"Invalid status code: {status_code}")
        
        # 2. Content analysis
        content_score = self._analyze_content(response_text)
        validation_result['score_breakdown']['content_analysis'] = content_score
        if content_score < 40:
            validation_result['errors'].append("Content indicates this is a false positive")
        
        # 3. Response time check (too fast = may be cached error page)
        if response_time < 0.1:
            validation_result['warnings'].append("Suspiciously fast response (possible cache/error page)")
            validation_result['score_breakdown']['response_time'] = 30
        elif response_time > 3:
            validation_result['score_breakdown']['response_time'] = 80
        else:
            validation_result['score_breakdown']['response_time'] = 70
        
        # 4. URL pattern validation
        url_score = self._validate_url_pattern(url)
        validation_result['score_breakdown']['url_pattern'] = url_score
        
        # Calculate final confidence
        total_weight = sum(self.weights.values())
        weighted_score = sum(
            validation_result['score_breakdown'].get(key, 0) * (self.weights[key] / 100)
            for key in validation_result['score_breakdown']
        )
        
        validation_result['confidence'] = int(weighted_score)
        
        # Apply validation level
        if self.validation_level == 'paranoid':
            validation_result['valid'] = validation_result['confidence'] >= self.min_confidence + 20
        elif self.validation_level == 'strict':
            validation_result['valid'] = validation_result['confidence'] >= self.min_confidence
        else:  # basic
            validation_result['valid'] = validation_result['confidence'] >= self.min_confidence - 20
        
        # Determine confidence level
        if validation_result['confidence'] >= 80:
            validation_result['confidence_level'] = 'HIGH'
        elif validation_result['confidence'] >= 50:
            validation_result['confidence_level'] = 'MEDIUM'
        else:
            validation_result['confidence_level'] = 'LOW'
        
        return validation_result
    
    def _validate_status_code(self, status_code: int) -> int:
        """Validate HTTP status code"""
        if status_code in self.fp_patterns['status_codes']['valid']:
            return 100
        elif status_code in self.fp_patterns['status_codes']['warning']:
            return 50
        else:
            return 0
    
    def _analyze_content(self, text: str) -> int:
        """Analyze response content for indicators"""
        if not text:
            return 0
        
        score = 100
        
        # Check for error indicators
        for indicator in self.fp_patterns['error_indicators']:
            if indicator in text:
                score -= 20
        
        # Check for placeholder indicators
        for indicator in self.fp_patterns['placeholder_indicators']:
            if indicator in text:
                score -= 15
        
        # Check for bot indicators (WAF, captcha)
        for indicator in self.fp_patterns['bot_indicators']:
            if indicator in text:
                score -= 40
                break  # Major deduction
        
        # Check for valid indicators (boost score)
        for indicator in self.fp_patterns['valid_indicators']:
            if indicator in text:
                score = min(100, score + 10)
        
        # Analyze text length (too short = error page)
        if len(text) < 100:
            score -= 30
        elif len(text) > 10000:
            score += 10  # Substantial content = more likely valid
        
        return max(0, min(100, score))
    
    def _validate_url_pattern(self, url: str) -> int:
        """Validate URL pattern for false positives"""
        score = 100
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'\.\.\/', r'%2e%2e', r'%00', r'\\x00',
            r'\/404', r'\/error', r'\/notfound'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, url.lower()):
                score -= 50
                break
        
        # Check for valid profile patterns
        valid_patterns = [
            r'\/user\/', r'\/profile\/', r'\/@', r'\/u\/',
            r'\/member\/', r'\/account\/', r'\/people\/'
        ]
        
        for pattern in valid_patterns:
            if re.search(pattern, url.lower()):
                score = min(100, score + 20)
                break
        
        return max(0, min(100, score))
    
    def validate_email(self, email: str, response_data: Dict) -> Dict:
        """Validate email search results"""
        result = {
            'email': email,
            'valid': True,
            'confidence': 50,
            'findings': []
        }
        
        # Check email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            result['valid'] = False
            result['findings'].append("Invalid email format")
            result['confidence'] = 0
            return result
        
        # Check if exposed in breaches
        if response_data.get('breaches'):
            result['confidence'] += 40
            result['findings'].append(f"Found in {len(response_data['breaches'])} data breaches")
        
        # Check if verified
        if response_data.get('verified'):
            result['confidence'] += 30
            result['findings'].append("Email is verified")
        
        result['confidence'] = min(100, result['confidence'])
        
        if result['confidence'] >= 70:
            result['confidence_level'] = 'HIGH'
        elif result['confidence'] >= 40:
            result['confidence_level'] = 'MEDIUM'
        else:
            result['confidence_level'] = 'LOW'
            result['valid'] = False
        
        return result
    
    def validate_phone(self, phone: str, response_data: Dict) -> Dict:
        """Validate phone number search results"""
        result = {
            'phone': phone,
            'valid': True,
            'confidence': 50,
            'carrier_verified': False,
            'findings': []
        }
        
        # Check phone format (E.164)
        import re
        phone_pattern = r'^\+?[1-9]\d{1,14}$'
        if not re.match(phone_pattern, phone.replace(' ', '')):
            result['valid'] = False
            result['findings'].append("Invalid phone format (use E.164)")
            result['confidence'] = 0
            return result
        
        # Check carrier
        if response_data.get('carrier') and response_data['carrier'] != 'Unknown':
            result['carrier_verified'] = True
            result['confidence'] += 30
            result['findings'].append(f"Carrier: {response_data['carrier']}")
        
        # Check location
        if response_data.get('location') and response_data['location'] != 'Unknown':
            result['confidence'] += 20
            result['findings'].append(f"Location: {response_data['location']}")
        
        # Check if active
        if response_data.get('valid', False):
            result['confidence'] += 20
            result['findings'].append("Number is valid and active")
        
        result['confidence'] = min(100, result['confidence'])
        
        if result['confidence'] >= 70:
            result['confidence_level'] = 'HIGH'
        elif result['confidence'] >= 40:
            result['confidence_level'] = 'MEDIUM'
        else:
            result['confidence_level'] = 'LOW'
            result['valid'] = False
        
        return result
    
    def filter_results(self, results: List[Dict], min_confidence: int = None) -> List[Dict]:
        """Filter results based on confidence score"""
        if min_confidence is None:
            min_confidence = self.min_confidence
        
        filtered = []
        for result in results:
            if result.get('validation', {}).get('confidence', 0) >= min_confidence:
                filtered.append(result)
        
        return filtered
    
    def generate_validation_report(self, results: List[Dict]) -> Dict:
        """Generate validation statistics report"""
        total = len(results)
        if total == 0:
            return {'total': 0, 'valid': 0, 'filtered': 0}
        
        valid = sum(1 for r in results if r.get('validation', {}).get('valid', False))
        high_conf = sum(1 for r in results if r.get('validation', {}).get('confidence', 0) >= 80)
        medium_conf = sum(1 for r in results if 50 <= r.get('validation', {}).get('confidence', 0) < 80)
        low_conf = sum(1 for r in results if r.get('validation', {}).get('confidence', 0) < 50)
        
        return {
            'total': total,
            'valid': valid,
            'filtered': total - valid,
            'high_confidence': high_conf,
            'medium_confidence': medium_conf,
            'low_confidence': low_conf,
            'filter_rate': round((total - valid) / total * 100, 2),
            'validation_level': self.validation_level,
            'min_confidence': self.min_confidence
        }
