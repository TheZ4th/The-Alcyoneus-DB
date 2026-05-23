#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The Alcyoneus DB - Automatic Health Check System
Version: 1.5.0
Feature: Automatic Health Check, Platform Verification, Performance Monitoring
"""

import json
import os
import time
import threading
import requests
import hashlib
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import random

# Color codes
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
C = '\033[96m'
P = '\033[95m'
RESET = '\033[0m'
BOLD = '\033[1m'

class HealthCheckSystem:
    """
    Automatic Health Check untuk The Alcyoneus DB
    Memverifikasi platform, cek response time, uptime, dan confidence score
    """
    
    def __init__(self, db_path: str = '/data/data/com.termux/files/home/Alcy/data/platforms.json', config_path: str = None):
        self.db_path = db_path
        self.config = self._load_config(config_path)
        self.results = {
            "timestamp": None,
            "total_platforms": 0,
            "checked": 0,
            "online": 0,
            "offline": 0,
            "changed": 0,
            "new_discovered": 0,
            "average_response_time": 0,
            "platforms_status": [],
            "statistics": {}
        }
        self.lock = threading.Lock()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load health check configuration"""
        default_config = {
            "health_check": {
                "auto_check_interval_hours": 24,
                "max_threads": 20,
                "timeout_seconds": 10,
                "retry_count": 3,
                "retry_delay": 1,
                "save_results": True,
                "notify_on_change": True,
                "confidence_threshold": 60,
                "response_time_warning_ms": 3000,
                "response_time_critical_ms": 5000,
                "verification_frequency": {
                    "high_priority": 12,    # hours
                    "medium_priority": 24,  # hours
                    "low_priority": 48      # hours
                }
            },
            "alerts": {
                "enabled": True,
                "telegram_bot_token": None,
                "telegram_chat_id": None,
                "discord_webhook": None,
                "slack_webhook": None
            },
            "reporting": {
                "save_format": ["json", "csv", "html"],
                "retention_days": 30,
                "export_path": "health_reports"
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                # Merge configs
                for key in user_config:
                    if key in default_config:
                        default_config[key].update(user_config[key])
                    else:
                        default_config[key] = user_config[key]
        
        return default_config
    
    def load_platforms(self) -> Dict:
        """Load platforms database"""
        with open(self.db_path, '/data/data/com.termux/files/home/Alcy/platform.json') as f:
            return json.load(f)
    
    def save_platforms(self, data: Dict):
        """Save platforms database"""
        with open(self.db_path, '/data/data/com.termux/files/home/Alcy/platform.json') as f:
            json.dump(data, f, indent=2)
    
    def check_platform(self, platform: Dict) -> Dict:
        """
        Check a single platform's health
        Returns status, response time, and changes
        """
        name = platform.get('name', 'unknown')
        url_pattern = platform.get('url_pattern', '')
        
        if not url_pattern or '{username}' not in url_pattern:
            return {
                'name': name,
                'status': 'invalid',
                'response_time': None,
                'error': 'Invalid URL pattern'
            }
        
        # Use test username (random string to avoid false positives)
        test_username = f"testuser_{random.randint(1000, 9999)}"
        test_url = url_pattern.format(username=test_username)
        
        start_time = time.time()
        status_code = None
        error = None
        
        for attempt in range(self.config['health_check']['retry_count']):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }
                
                response = requests.get(
                    test_url, 
                    headers=headers, 
                    timeout=self.config['health_check']['timeout_seconds'],
                    allow_redirects=True
                )
                status_code = response.status_code
                error = None
                break
                
            except requests.exceptions.Timeout:
                error = "Timeout"
                time.sleep(self.config['health_check']['retry_delay'])
            except requests.exceptions.ConnectionError:
                error = "Connection Error"
                time.sleep(self.config['health_check']['retry_delay'])
            except Exception as e:
                error = str(e)
                time.sleep(self.config['health_check']['retry_delay'])
        
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        
        # Determine status
        if status_code and status_code in [200, 201, 202, 204]:
            status = 'online'
        elif status_code and status_code in [301, 302, 307, 308]:
            status = 'redirect'
        elif status_code and status_code in [403, 429]:
            status = 'rate_limited'
        elif status_code and status_code in [404, 410]:
            status = 'offline'
        elif status_code and status_code >= 500:
            status = 'server_error'
        else:
            status = 'unknown'
        
        # Check if platform status changed
        previous_status = platform.get('health_status', 'unknown')
        previous_verified = platform.get('verified', False)
        
        changed = False
        if previous_status != status:
            changed = True
        
        # Calculate new confidence based on health
        confidence = platform.get('confidence', 50)
        if status == 'online':
            confidence = min(100, confidence + 5)
        elif status == 'rate_limited':
            confidence = max(0, confidence - 5)
        elif status in ['offline', 'server_error']:
            confidence = max(0, confidence - 10)
        
        # Update platform data
        platform['health_status'] = status
        platform['last_checked'] = datetime.now().isoformat()
        platform['response_time_ms'] = round(response_time, 2)
        platform['confidence'] = confidence
        platform['verified'] = status == 'online'
        
        return {
            'name': name,
            'url': test_url,
            'status': status,
            'status_code': status_code,
            'response_time_ms': round(response_time, 2),
            'error': error,
            'changed': changed,
            'previous_status': previous_status,
            'new_confidence': confidence
        }
    
    def run_health_check(self, progress_callback=None) -> Dict:
        """
        Run complete health check on all platforms
        """
        print(f"{C}{BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════╗")
        print("║         🔍 THE ALCYONEUS DB - AUTOMATIC HEALTH CHECK             ║")
        print("║                    System Diagnosis in Progress                   ║")
        print("╚═══════════════════════════════════════════════════════════════════╝")
        print(f"{RESET}\n")
        
        start_time = time.time()
        
        # Load platforms
        db_data = self.load_platforms()
        platforms = db_data.get('platforms', [])
        total = len(platforms)
        
        print(f"{Y}[*] Total platforms to check: {total}{RESET}")
        print(f"{Y}[*] Max threads: {self.config['health_check']['max_threads']}{RESET}")
        print(f"{Y}[*] Timeout: {self.config['health_check']['timeout_seconds']}s{RESET}\n")
        
        results = []
        online_count = 0
        offline_count = 0
        changed_count = 0
        total_response_time = 0
        
        # Determine priority-based checking order
        platforms_sorted = sorted(platforms, key=lambda x: x.get('priority', 5))
        
        with ThreadPoolExecutor(max_workers=self.config['health_check']['max_threads']) as executor:
            futures = {executor.submit(self.check_platform, p): p for p in platforms_sorted}
            
            completed = 0
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                completed += 1
                
                # Update counters
                if result['status'] == 'online':
                    online_count += 1
                elif result['status'] in ['offline', 'server_error']:
                    offline_count += 1
                
                if result['changed']:
                    changed_count += 1
                
                if result['response_time_ms']:
                    total_response_time += result['response_time_ms']
                
                # Update progress
                progress = (completed / total) * 100
                bar_length = 40
                filled = int(bar_length * completed // total)
                bar = '█' * filled + '░' * (bar_length - filled)
                
                status_color = G if result['status'] == 'online' else R
                print(f"\r{C}[{bar}] {completed}/{total} ({progress:.1f}%){RESET} "
                      f"| {status_color}{result['status']}{RESET} "
                      f"| {result['name']:<20}", end='')
                
                if progress_callback:
                    progress_callback({
                        'completed': completed,
                        'total': total,
                        'current': result
                    })
        
        print("\n")  # New line after progress bar
        
        # Calculate statistics
        avg_response_time = total_response_time / online_count if online_count > 0 else 0
        uptime_percentage = (online_count / total) * 100 if total > 0 else 0
        
        # Update platform data in database
        for result in results:
            for platform in platforms:
                if platform.get('name') == result['name']:
                    platform['health_status'] = result['status']
                    platform['last_checked'] = datetime.now().isoformat()
                    platform['response_time_ms'] = result['response_time_ms']
                    platform['confidence'] = result.get('new_confidence', platform.get('confidence', 50))
                    platform['verified'] = result['status'] == 'online'
                    break
        
        # Update metadata
        db_data['metadata']['last_health_check'] = datetime.now().isoformat()
        db_data['metadata']['health_stats'] = {
            'total_checked': total,
            'online': online_count,
            'offline': offline_count,
            'changed': changed_count,
            'uptime_percentage': round(uptime_percentage, 2),
            'average_response_time_ms': round(avg_response_time, 2)
        }
        
        # Save updated database
        self.save_platforms(db_data)
        
        # Prepare results
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": round(time.time() - start_time, 2),
            "total_platforms": total,
            "checked": total,
            "online": online_count,
            "offline": offline_count,
            "changed": changed_count,
            "new_discovered": 0,
            "average_response_time_ms": round(avg_response_time, 2),
            "uptime_percentage": round(uptime_percentage, 2),
            "platforms_status": results,
            "statistics": {
                "by_status": defaultdict(int),
                "by_category": defaultdict(lambda: {'online': 0, 'total': 0}),
                "by_region": defaultdict(lambda: {'online': 0, 'total': 0}),
                "slowest_platforms": [],
                "fastest_platforms": []
            }
        }
        
        # Generate statistics
        for result in results:
            self.results['statistics']['by_status'][result['status']] += 1
            
            # Find platform data for category/region
            platform_data = next((p for p in platforms if p.get('name') == result['name']), {})
            category = platform_data.get('category', 'unknown')
            region = platform_data.get('region', 'unknown')
            
            self.results['statistics']['by_category'][category]['total'] += 1
            if result['status'] == 'online':
                self.results['statistics']['by_category'][category]['online'] += 1
            
            self.results['statistics']['by_region'][region]['total'] += 1
            if result['status'] == 'online':
                self.results['statistics']['by_region'][region]['online'] += 1
        
        # Sort slowest and fastest
        valid_results = [r for r in results if r.get('response_time_ms')]
        self.results['statistics']['slowest_platforms'] = sorted(
            valid_results, key=lambda x: x.get('response_time_ms', 0), reverse=True
        )[:10]
        self.results['statistics']['fastest_platforms'] = sorted(
            valid_results, key=lambda x: x.get('response_time_ms', 999999)
        )[:10]
        
        # Print summary
        self._print_summary()
        
        # Save report
        if self.config['health_check']['save_results']:
            self._save_report()
        
        # Send alerts if enabled
        if self.config['alerts']['enabled'] and changed_count > 0:
            self._send_alerts()
        
        return self.results
    
    def _print_summary(self):
        """Print health check summary"""
        print(f"{G}{BOLD}╔═══════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{G}{BOLD}║                    📊 HEALTH CHECK SUMMARY                        ║{RESET}")
        print(f"{G}{BOLD}╚═══════════════════════════════════════════════════════════════════╝{RESET}\n")
        
        print(f"{C}📈 Overall Statistics:{RESET}")
        print(f"  {Y}Total Platforms:{RESET} {self.results['total_platforms']}")
        print(f"  {Y}Checked:{RESET} {self.results['checked']}")
        print(f"  {G}Online:{RESET} {self.results['online']} ({self.results['uptime_percentage']}%)")
        print(f"  {R}Offline/Error:{RESET} {self.results['offline']}")
        print(f"  {Y}Status Changed:{RESET} {self.results['changed']}")
        print(f"  {Y}Average Response Time:{RESET} {self.results['average_response_time_ms']}ms")
        print(f"  {Y}Duration:{RESET} {self.results['duration_seconds']} seconds\n")
        
        print(f"{C}📋 Status Breakdown:{RESET}")
        for status, count in self.results['statistics']['by_status'].items():
            color = G if status == 'online' else Y if status == 'rate_limited' else R
            print(f"  {color}{status}:{RESET} {count}")
        
        print(f"\n{C}🗂️ Top Categories by Uptime:{RESET}")
        category_uptime = []
        for cat, stats in self.results['statistics']['by_category'].items():
            if stats['total'] > 0:
                uptime = (stats['online'] / stats['total']) * 100
                category_uptime.append((cat, uptime, stats['online'], stats['total']))
        
        for cat, uptime, online, total in sorted(category_uptime, key=lambda x: x[1], reverse=True)[:5]:
            color = G if uptime >= 80 else Y if uptime >= 50 else R
            print(f"  {color}{cat}:{RESET} {uptime:.1f}% ({online}/{total})")
        
        print(f"\n{C}🌍 Top Regions by Uptime:{RESET}")
        region_uptime = []
        for reg, stats in self.results['statistics']['by_region'].items():
            if stats['total'] > 0:
                uptime = (stats['online'] / stats['total']) * 100
                region_uptime.append((reg, uptime, stats['online'], stats['total']))
        
        for reg, uptime, online, total in sorted(region_uptime, key=lambda x: x[1], reverse=True)[:5]:
            color = G if uptime >= 80 else Y if uptime >= 50 else R
            print(f"  {color}{reg}:{RESET} {uptime:.1f}% ({online}/{total})")
        
        if self.results['statistics']['slowest_platforms']:
            print(f"\n{R}🐌 Slowest Platforms (High Response Time):{RESET}")
            for p in self.results['statistics']['slowest_platforms'][:5]:
                print(f"  {R}• {p['name']}: {p['response_time_ms']}ms ({p['status']}){RESET}")
        
        if self.results['statistics']['fastest_platforms']:
            print(f"\n{G}⚡ Fastest Platforms:{RESET}")
            for p in self.results['statistics']['fastest_platforms'][:5]:
                print(f"  {G}• {p['name']}: {p['response_time_ms']}ms{RESET}")
        
        if self.results['changed'] > 0:
            print(f"\n{Y}⚠️  Platforms with Status Changes:{RESET}")
            changed_platforms = [r for r in self.results['platforms_status'] if r['changed']]
            for p in changed_platforms[:10]:
                old_color = G if p['previous_status'] == 'online' else R
                new_color = G if p['status'] == 'online' else R
                print(f"  {Y}• {p['name']}: {old_color}{p['previous_status']}{RESET} → {new_color}{p['status']}{RESET}")
            if len(changed_platforms) > 10:
                print(f"  {Y}... and {len(changed_platforms) - 10} more{RESET}")
    
    def _save_report(self):
        """Save health check report"""
        export_path = self.config['reporting']['export_path']
        os.makedirs(export_path, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON
        if 'json' in self.config['reporting']['save_format']:
            json_path = f"{export_path}/health_check_{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"{G}[+] JSON report saved: {json_path}{RESET}")
        
        # Save CSV
        if 'csv' in self.config['reporting']['save_format']:
            import csv
            csv_path = f"{export_path}/health_check_{timestamp}.csv"
            with open(csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Platform', 'Status', 'Response Time (ms)', 'Status Code', 'Changed', 'Previous Status'])
                for p in self.results['platforms_status']:
                    writer.writerow([
                        p['name'], p['status'], p['response_time_ms'], 
                        p['status_code'], p['changed'], p.get('previous_status', 'N/A')
                    ])
            print(f"{G}[+] CSV report saved: {csv_path}{RESET}")
        
        # Save HTML
        if 'html' in self.config['reporting']['save_format']:
            html_path = f"{export_path}/health_check_{timestamp}.html"
            self._save_html_report(html_path)
            print(f"{G}[+] HTML report saved: {html_path}{RESET}")
    
    def _save_html_report(self, path: str):
        """Generate HTML report"""
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alcyoneus DB - Health Check Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a0a0a 100%);
            color: #00ff9d;
            padding: 20px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{
            text-align: center;
            padding: 30px;
            border: 2px solid #ff0000;
            border-radius: 10px;
            margin-bottom: 30px;
            background: rgba(255, 0, 0, 0.1);
        }}
        .header h1 {{
            font-size: 36px;
            color: #ff0000;
            text-shadow: 0 0 10px #ff0000;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #ff0000;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }}
        .stat-card h3 {{ color: #ff6b6b; margin-bottom: 10px; }}
        .stat-number {{ font-size: 32px; font-weight: bold; }}
        .online {{ color: #00ff9d; }}
        .offline {{ color: #ff0000; }}
        .warning {{ color: #ffd93d; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 10px;
            overflow: hidden;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 0, 0, 0.3);
        }}
        th {{
            background: #ff0000;
            color: #0a0a0a;
            font-weight: bold;
        }}
        tr:hover {{ background: rgba(255, 0, 0, 0.1); }}
        .status-badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            margin-top: 30px;
            color: rgba(255, 0, 0, 0.5);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🩸 THE ALCYONEUS DB - HEALTH CHECK REPORT</h1>
            <p>Generated: {self.results['timestamp']}</p>
            <p>Duration: {self.results['duration_seconds']} seconds</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <h3>📊 Total Platforms</h3>
                <div class="stat-number">{self.results['total_platforms']}</div>
            </div>
            <div class="stat-card">
                <h3>🟢 Online</h3>
                <div class="stat-number online">{self.results['online']}</div>
                <div>({self.results['uptime_percentage']}%)</div>
            </div>
            <div class="stat-card">
                <h3>🔴 Offline</h3>
                <div class="stat-number offline">{self.results['offline']}</div>
            </div>
            <div class="stat-card">
                <h3>⚡ Response Time</h3>
                <div class="stat-number">{self.results['average_response_time_ms']}ms</div>
            </div>
            <div class="stat-card">
                <h3>🔄 Status Changed</h3>
                <div class="stat-number warning">{self.results['changed']}</div>
            </div>
        </div>
        
        <h2>📋 Platform Status Details</h2>
         <table>
            <thead>
                <tr>
                    <th>Platform</th>
                    <th>Status</th>
                    <th>Response Time</th>
                    <th>Status Code</th>
                    <th>Changed</th>
                </tr>
            </thead>
            <tbody>
                {self._generate_html_rows()}
            </tbody>
         </table>
        
        <div class="footer">
            <p>The Alcyoneus DB v4.1.0 - Automatic Health Check System</p>
            <p>Prowling for the breach. Hunting in the void. 🩸🖤</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(path, 'w') as f:
            f.write(html_template)
    
    def _generate_html_rows(self) -> str:
        """Generate HTML table rows"""
        rows = []
        for p in self.results['platforms_status'][:100]:  # Limit to 100 for display
            status_color = 'online' if p['status'] == 'online' else 'offline' if p['status'] in ['offline', 'server_error'] else 'warning'
            status_display = p['status'].replace('_', ' ').title()
            
            changed_mark = '✅' if p['changed'] else '❌'
            
            rows.append(f"""
                <tr>
                    <td>{p['name']}</td>
                    <td><span class="status-badge {status_color}">{status_display}</span></td>
                    <td>{p['response_time_ms'] if p['response_time_ms'] else 'N/A'}ms</td>
                    <td>{p['status_code'] if p['status_code'] else 'N/A'}</td>
                    <td>{changed_mark}</td>
                </tr>
            """)
        
        return '\n'.join(rows)
    
    def _send_alerts(self):
        """Send alerts via configured channels"""
        changed_platforms = [r for r in self.results['platforms_status'] if r['changed']]
        
        message = f"""
🚨 ALCYONEUS DB HEALTH ALERT 🚨

📊 Summary:
- Total Checked: {self.results['total_platforms']}
- Online: {self.results['online']} ({self.results['uptime_percentage']}%)
- Offline: {self.results['offline']}
- Status Changed: {self.results['changed']}
- Avg Response: {self.results['average_response_time_ms']}ms

⚠️ Platforms with Status Changes:
{chr(10).join([f"  • {p['name']}: {p['previous_status']} → {p['status']}" for p in changed_platforms[:10]])}

Timestamp: {self.results['timestamp']}
        """
        
        # Telegram alert
        if self.config['alerts'].get('telegram_bot_token') and self.config['alerts'].get('telegram_chat_id'):
            try:
                url = f"https://api.telegram.org/bot{self.config['alerts']['telegram_bot_token']}/sendMessage"
                data = {'chat_id': self.config['alerts']['telegram_chat_id'], 'text': message}
                requests.post(url, data=data, timeout=5)
            except:
                pass
        
        # Discord webhook
        if self.config['alerts'].get('discord_webhook'):
            try:
                data = {'content': message}
                requests.post(self.config['alerts']['discord_webhook'], json=data, timeout=5)
            except:
                pass
    
    def auto_health_check_daemon(self):
        """
        Run health check as a daemon (background thread)
        """
        def daemon_loop():
            while True:
                print(f"{C}[*] Running scheduled health check...{RESET}")
                self.run_health_check()
                
                interval = self.config['health_check']['auto_check_interval_hours']
                print(f"{Y}[*] Next check in {interval} hours{RESET}")
                time.sleep(interval * 3600)
        
        thread = threading.Thread(target=daemon_loop, daemon=True)
        thread.start()
        return thread
    
    def verify_single_platform(self, platform_name: str) -> Dict:
        """
        Verify a single platform by name
        """
        db_data = self.load_platforms()
        platform = next((p for p in db_data['platforms'] if p.get('name') == platform_name), None)
        
        if not platform:
            return {'error': f'Platform {platform_name} not found'}
        
        result = self.check_platform(platform)
        
        # Update platform in database
        for p in db_data['platforms']:
            if p.get('name') == platform_name:
                p['health_status'] = result['status']
                p['last_checked'] = datetime.now().isoformat()
                p['response_time_ms'] = result['response_time_ms']
                break
        
        self.save_platforms(db_data)
        
        return result
    
    def get_health_stats(self) -> Dict:
        """
        Get current health statistics from database
        """
        db_data = self.load_platforms()
        platforms = db_data.get('platforms', [])
        
        stats = {
            'total': len(platforms),
            'online': 0,
            'offline': 0,
            'unknown': 0,
            'last_check': db_data.get('metadata', {}).get('last_health_check'),
            'uptime_percentage': 0,
            'average_response_time': 0,
            'by_priority': defaultdict(int),
            'by_category': defaultdict(int)
        }
        
        response_times = []
        for p in platforms:
            status = p.get('health_status', 'unknown')
            if status == 'online':
                stats['online'] += 1
                if p.get('response_time_ms'):
                    response_times.append(p['response_time_ms'])
            elif status in ['offline', 'server_error']:
                stats['offline'] += 1
            else:
                stats['unknown'] += 1
            
            priority = p.get('priority', 5)
            stats['by_priority'][priority] += 1
            
            category = p.get('category', 'unknown')
            stats['by_category'][category] += 1
        
        if response_times:
            stats['average_response_time'] = sum(response_times) / len(response_times)
        
        stats['uptime_percentage'] = (stats['online'] / stats['total']) * 100 if stats['total'] > 0 else 0
        
        return stats


def main():
    """Command line interface for health check"""
    import argparse
    
    parser = argparse.ArgumentParser(description='The Alcyoneus DB - Automatic Health Check')
    parser.add_argument('--check', action='store_true', help='Run health check')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon (auto-check every 24h)')
    parser.add_argument('--stats', action='store_true', help='Show health statistics')
    parser.add_argument('--verify', type=str, help='Verify a specific platform')
    parser.add_argument('--db', type=str, default='platforms.json', help='Path to platforms.json')
    parser.add_argument('--config', type=str, help='Path to config file')
    
    args = parser.parse_args()
    
    hc = HealthCheckSystem(db_path=args.db, config_path=args.config)
    
    if args.daemon:
        print(f"{C}[*] Starting Alcyoneus DB Health Check Daemon...{RESET}")
        hc.auto_health_check_daemon()
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Y}[!] Daemon stopped{RESET}")
    
    elif args.check:
        hc.run_health_check()
    
    elif args.stats:
        stats = hc.get_health_stats()
        print(f"\n{C}{BOLD}📊 ALCYONEUS DB HEALTH STATISTICS{RESET}\n")
        print(f"{Y}Total Platforms:{RESET} {stats['total']}")
        print(f"{G}Online:{RESET} {stats['online']} ({stats['uptime_percentage']:.1f}%)")
        print(f"{R}Offline:{RESET} {stats['offline']}")
        print(f"{Y}Unknown:{RESET} {stats['unknown']}")
        print(f"{Y}Average Response Time:{RESET} {stats['average_response_time']:.2f}ms")
        print(f"{Y}Last Health Check:{RESET} {stats['last_check']}")
        
        print(f"\n{C}By Priority:{RESET}")
        for priority in sorted(stats['by_priority'].keys()):
            print(f"  Priority {priority}: {stats['by_priority'][priority]} platforms")
    
    elif args.verify:
        result = hc.verify_single_platform(args.verify)
        print(f"\n{C}Verification result for {args.verify}:{RESET}")
        print(json.dumps(result, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
