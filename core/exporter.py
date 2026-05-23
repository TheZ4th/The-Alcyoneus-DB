# exporter.py
"""
The Alcyoneus DB - Data Exporter
Export results to JSON, CSV, HTML, PDF formats
"""

import json
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional

class DataExporter:
    """Export OSINT results to various formats"""
    
    def __init__(self):
        self.export_dir = 'exports'
        self._ensure_export_dir()
    
    def _ensure_export_dir(self):
        """Create export directory if not exists"""
        import os
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
    
    def export_json(self, data: Dict, filename: str = None) -> str:
        """Export to JSON format"""
        if not filename:
            filename = f"alcy_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = f"{self.export_dir}/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def export_csv(self, results: List[Dict], filename: str = None) -> str:
        """Export results to CSV format"""
        if not filename:
            filename = f"alcy_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if not results:
            return None
        
        # Get all unique keys
        fieldnames = set()
        for result in results:
            fieldnames.update(result.keys())
        fieldnames = sorted(list(fieldnames))
        
        filepath = f"{self.export_dir}/{filename}"
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                # Flatten nested dicts
                flat_result = {}
                for key, value in result.items():
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            flat_result[f"{key}_{sub_key}"] = sub_value
                    else:
                        flat_result[key] = value
                writer.writerow(flat_result)
        
        return filepath
    
    def export_html(self, results: List[Dict], query: str = None, filename: str = None) -> str:
        """Export results to HTML report"""
        if not filename:
            filename = f"alcy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alcyoneus DB - OSINT Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #00ff9d;
            padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            text-align: center;
            padding: 40px;
            border: 2px solid #00ff9d;
            border-radius: 10px;
            margin-bottom: 30px;
            background: rgba(0, 255, 157, 0.1);
        }}
        .header h1 {{
            font-size: 48px;
            text-shadow: 0 0 10px #00ff9d;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #00ff9d;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }}
        .stat-card h3 {{ color: #ff6b6b; margin-bottom: 10px; }}
        .stat-card .number {{ font-size: 36px; font-weight: bold; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 10px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(0, 255, 157, 0.3);
        }}
        th {{
            background: #00ff9d;
            color: #0a0a0a;
            font-weight: bold;
        }}
        tr:hover {{ background: rgba(0, 255, 157, 0.1); }}
        .high { color: #00ff9d; }
        .medium {{ color: #ffd93d; }}
        .low {{ color: #ff6b6b; }}
        .footer {{
            text-align: center;
            padding: 20px;
            margin-top: 30px;
            color: rgba(0, 255, 157, 0.5);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 THE ALCYONEUS DB 🔥</h1>
            <p>Exceeding the average reasonable limits of OSINT databases</p>
            {f"<p><strong>Query:</strong> {query}</p>" if query else ""}
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Total Results</h3>
                <div class="number">{len(results)}</div>
            </div>
            <div class="stat-card">
                <h3>High Confidence</h3>
                <div class="number high">{sum(1 for r in results if r.get('confidence', 0) >= 80)}</div>
            </div>
            <div class="stat-card">
                <h3>Medium Confidence</h3>
                <div class="number medium">{sum(1 for r in results if 50 <= r.get('confidence', 0) < 80)}</div>
            </div>
            <div class="stat-card">
                <h3>Categories</h3>
                <div class="number">{len(set(r.get('category', 'unknown') for r in results))}</div>
            </div>
        </div>
        
        <h2>📊 Detailed Results</h2>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Platform</th>
                    <th>Category</th>
                    <th>URL</th>
                    <th>Confidence</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {self._generate_table_rows(results)}
            </tbody>
        </table>
        
        <div class="footer">
            <p>The Alcyoneus DB - Power beyond limits | #ZK-Phantom</p>
        </div>
    </div>
</body>
</html>
        """
        
        filepath = f"{self.export_dir}/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        return filepath
    
    def _generate_table_rows(self, results: List[Dict]) -> str:
        """Generate HTML table rows"""
        rows = []
        for i, result in enumerate(results[:100], 1):
            confidence = result.get('confidence', 0)
            if confidence >= 80:
                conf_class = 'high'
            elif confidence >= 50:
                conf_class = 'medium'
            else:
                conf_class = 'low'
            
            url = result.get('url', '#')
            platform = result.get('platform', 'Unknown')
            category = result.get('category', 'Unknown')
            status = result.get('status_code', 0)
            
            rows.append(f"""
                <tr>
                    <td>{i}</td>
                    <td>{platform}</td>
                    <td>{category}</td>
                    <td><a href="{url}" target="_blank">{url[:50]}...</a></td>
                    <td class="{conf_class}">{confidence}%</td>
                    <td>{status}</td>
                </tr>
            """)
        
        return "\n".join(rows)
    
    def export_pdf(self, results: List[Dict], filename: str = None) -> Optional[str]:
        """Export to PDF (requires reportlab)"""
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter, landscape
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            
            if not filename:
                filename = f"alcy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            filepath = f"{self.export_dir}/{filename}"
            doc = SimpleDocTemplate(filepath, pagesize=landscape(letter))
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.green)
            story.append(Paragraph("The Alcyoneus DB - OSINT Report", title_style))
            story.append(Spacer(1, 0.25*inch))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Spacer(1, 0.25*inch))
            
            # Table data
            table_data = [['Platform', 'Category', 'URL', 'Confidence', 'Status']]
            for result in results[:50]:
                table_data.append([
                    result.get('platform', ''),
                    result.get('category', ''),
                    result.get('url', ''),
                    f"{result.get('confidence', 0)}%",
                    str(result.get('status_code', 0))
                ])
            
            # Create table
            table = Table(table_data, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.green),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            story.append(table)
            doc.build(story)
            
            return filepath
        
        except ImportError:
            print(f"{Y}[!] ReportLab not installed. PDF export requires: pip install reportlab{RESET}")
            return None
    
    def export_markdown(self, results: List[Dict], query: str = None, filename: str = None) -> str:
        """Export to Markdown format"""
        if not filename:
            filename = f"alcy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        content = []
        content.append(f"# 🔥 The Alcyoneus DB - OSINT Report\n")
        content.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if query:
            content.append(f"**Query:** `{query}`")
        
        content.append(f"\n## 📊 Statistics")
        content.append(f"- **Total Results:** {len(results)}")
        content.append(f"- **High Confidence (80%+):** {sum(1 for r in results if r.get('confidence', 0) >= 80)}")
        content.append(f"- **Medium Confidence (50-79%):** {sum(1 for r in results if 50 <= r.get('confidence', 0) < 80)}")
        content.append(f"- **Low Confidence (<50%):** {sum(1 for r in results if r.get('confidence', 0) < 50)}")
        
        content.append(f"\n## 📍 Detailed Results\n")
        content.append("| # | Platform | Category | URL | Confidence |")
        content.append("|---|----------|----------|-----|------------|")
        
        for i, result in enumerate(results[:50], 1):
            platform = result.get('platform', 'N/A')
            category = result.get('category', 'N/A')
            url = result.get('url', '#')
            confidence = result.get('confidence', 0)
            content.append(f"| {i} | {platform} | {category} | {url} | {confidence}% |")
        
        if len(results) > 50:
            content.append(f"\n*... and {len(results) - 50} more results*")
        
        content.append(f"\n---")
        content.append(f"*The Alcyoneus DB - Power beyond limits | #ZK-Phantom*")
        
        filepath = f"{self.export_dir}/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        return filepath
