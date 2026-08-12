"""Print-friendly reports."""

import os
import webbrowser
from datetime import datetime
from config import BASE_DIR
from database import get_all_items, get_stats


def generate_inventory_report() -> str:
    stats = get_stats()
    items = get_all_items()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Spot Inventory Report</title>
<style>
@media print {{ .no-print {{ display: none; }} body {{ -webkit-print-color-adjust: exact; }} }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f5f5f5; padding: 40px; color: #1a1b21; }}
.container {{ max-width: 900px; margin: 0 auto; background: white; padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
.header {{ border-bottom: 3px solid #FF7A00; padding-bottom: 20px; margin-bottom: 30px; }}
.header h1 {{ font-size: 32px; color: #1a1b21; }}
.header p {{ color: #6b7280; margin-top: 5px; }}
.stats {{ display: flex; gap: 20px; margin-bottom: 30px; }}
.stat-box {{ flex: 1; background: #f9fafb; border-radius: 8px; padding: 16px; text-align: center; border: 1px solid #e5e7eb; }}
.stat-box .number {{ font-size: 28px; font-weight: bold; color: #FF7A00; }}
.stat-box .label {{ font-size: 12px; color: #6b7280; text-transform: uppercase; margin-top: 4px; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
th {{ background: #1a1b21; color: white; padding: 12px; text-align: left; font-size: 12px; text-transform: uppercase; }}
td {{ padding: 12px; border-bottom: 1px solid #e5e7eb; font-size: 13px; }}
tr:hover {{ background: #f9fafb; }}
.status {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; }}
.status-stored {{ background: #d1fae5; color: #065f46; }}
.status-lent {{ background: #ffedd5; color: #9a3412; }}
.status-borrowed {{ background: #dbeafe; color: #1e40af; }}
.status-lost {{ background: #fee2e2; color: #991b1b; }}
.no-print {{ text-align: center; margin-top: 30px; }}
.no-print button {{ background: #FF7A00; color: white; border: none; padding: 12px 30px; border-radius: 6px; font-size: 14px; cursor: pointer; font-weight: bold; }}
.footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; color: #9ca3af; font-size: 12px; }}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>Spot Inventory Report</h1><p>Generated on {now}</p></div>
<div class="stats">
<div class="stat-box"><div class="number">{stats['total']}</div><div class="label">Total Items</div></div>
<div class="stat-box"><div class="number">{stats['stored']}</div><div class="label">Available</div></div>
<div class="stat-box"><div class="number">{stats['lent']}</div><div class="label">Lent Out</div></div>
<div class="stat-box"><div class="number">{stats['borrowed']}</div><div class="label">Borrowed</div></div>
<div class="stat-box"><div class="number">{stats['overdue']}</div><div class="label">Overdue</div></div>
</div>
<table>
<thead><tr><th>Name</th><th>Category</th><th>Location</th><th>Status</th><th>Person</th><th>Due Date</th></tr></thead>
<tbody>
"""

    status_class = {
        "stored": "status-stored",
        "lent": "status-lent",
        "borrowed": "status-borrowed",
        "lost": "status-lost",
    }

    for item in items:
        status = item.get("status", "stored")
        location = item.get("room", "")
        if item.get("container"):
            location += f" → {item['container']}"
        html += f"""
<tr>
<td><strong>{item.get('name', '')}</strong></td>
<td>{item.get('category', 'General')}</td>
<td>{location}</td>
<td><span class="status {status_class.get(status, 'status-stored')}">{status.title()}</span></td>
<td>{item.get('person', '-')}</td>
<td>{item.get('due_date', '-')}</td>
</tr>
"""

    html += """
</tbody></table>
<div class="no-print"><button onclick="window.print()">Print Report</button></div>
<div class="footer"><p>Spot Personal Inventory v2.0</p></div>
</div>
</body>
</html>
"""

    report_path = os.path.join(BASE_DIR, "inventory_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    return report_path


def open_report():
    path = generate_inventory_report()
    webbrowser.open(f"file:///{path.replace(os.sep, '/')}")