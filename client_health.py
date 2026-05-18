#!/usr/bin/env python3
"""
Cross-Platform Client Health Checker
Author: Jason Ray (M-Endymion)
"""

import platform
import json
import argparse
import sys
from datetime import datetime
from pathlib import Path

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

CONFIG = {}

def load_config():
    global CONFIG
    config_path = Path("config.json")
    if config_path.exists():
        with open(config_path) as f:
            CONFIG = json.load(f)
    else:
        CONFIG = {
            "disk_threshold_gb": 20,
            "memory_warning_percent": 85,
            "cpu_warning_percent": 80,
            "output_dir": "reports",
            "include_mecm_check": True
        }

def get_system_info():
    return {
        "hostname": platform.node(),
        "os": platform.system(),
        "os_version": platform.version(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "timestamp": datetime.now().isoformat()
    }

def check_disk_space():
    threshold = CONFIG.get("disk_threshold_gb", 20)
    try:
        import shutil
        total, used, free = shutil.disk_usage(Path.home().root)
        free_gb = free / (1024**3)
        return {
            "free_gb": round(free_gb, 1),
            "used_percent": round(used / total * 100, 1),
            "status": "Good" if free_gb > threshold else "Warning"
        }
    except:
        return {"status": "Unknown"}

def check_memory():
    if not PSUTIL_AVAILABLE:
        return {"status": "psutil not installed"}
    mem = psutil.virtual_memory()
    warning = CONFIG.get("memory_warning_percent", 85)
    return {
        "total_gb": round(mem.total / (1024**3), 1),
        "available_gb": round(mem.available / (1024**3), 1),
        "percent_used": mem.percent,
        "status": "Good" if mem.percent < warning else "Warning"
    }

def check_cpu():
    if not PSUTIL_AVAILABLE:
        return {"status": "psutil not installed"}
    warning = CONFIG.get("cpu_warning_percent", 80)
    usage = psutil.cpu_percent(interval=1)
    return {
        "percent_used": usage,
        "status": "Good" if usage < warning else "Warning"
    }

def check_mecm_client():
    if not CONFIG.get("include_mecm_check", True) or platform.system() != "Windows":
        return {"status": "Skipped"}
    
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\CCM") as key:
            version = winreg.QueryValueEx(key, "ProductVersion")[0]
            return {"installed": True, "version": version, "status": "Good"}
    except:
        return {"installed": False, "status": "Not Found"}

def generate_html_report(data, output_path):
    # (Same nice HTML as before - keeping it unchanged for brevity)
    html = f"""<!DOCTYPE html>
<html>
<head><title>Client Health - {data['system']['hostname']}</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 40px; background: #f8f9fa; }}
    h1 {{ color: #0078D4; }}
    table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
    th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
    th {{ background: #0078D4; color: white; }}
    .status-good {{ background: #d4edda; color: green; }}
    .status-warning {{ background: #fff3cd; color: orange; }}
</style>
</head>
<body>
    <h1>Client Health Report</h1>
    <p><strong>Generated:</strong> {data['system']['timestamp']}</p>
    
    <h2>System Information</h2>
    <table>
        <tr><th>Property</th><th>Value</th></tr>
        <tr><td>Hostname</td><td>{data['system']['hostname']}</td></tr>
        <tr><td>OS</td><td>{data['system']['os']} {data['system']['os_release']}</td></tr>
    </table>
    
    <h2>Disk • Memory • CPU</h2>
    <table>
        <tr><th>Component</th><th>Value</th><th>Status</th></tr>
        <tr><td>Disk Free</td><td>{data['disk'].get('free_gb', 'N/A')} GB</td><td class="status-{data['disk'].get('status','').lower()}">{data['disk'].get('status')}</td></tr>
        <tr><td>Memory Used</td><td>{data['memory'].get('percent_used', 'N/A')}%</td><td class="status-{data['memory'].get('status','').lower()}">{data['memory'].get('status')}</td></tr>
        <tr><td>CPU Used</td><td>{data['cpu'].get('percent_used', 'N/A')}%</td><td class="status-{data['cpu'].get('status','').lower()}">{data['cpu'].get('status')}</td></tr>
    </table>
    
    <h2>MECM/SCCM Client</h2>
    <table>
        <tr><th>Status</th><th>Details</th></tr>
        <tr><td>{'✅ Installed' if data['mecm'].get('installed') else '❌ Not Found'}</td><td>{data['mecm'].get('version', data['mecm'].get('status'))}</td></tr>
    </table>
</body>
</html>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

def main():
    load_config()
    parser = argparse.ArgumentParser(description="Cross-Platform Client Health Checker")
    parser.add_argument("--output", "-o", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output or CONFIG.get("output_dir", "reports"))
    output_dir.mkdir(exist_ok=True)

    report = {
        "system": get_system_info(),
        "disk": check_disk_space(),
        "memory": check_memory(),
        "cpu": check_cpu(),
        "mecm": check_mecm_client(),
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    base_name = f"health_{report['system']['hostname']}_{timestamp}"

    json_path = output_dir / f"{base_name}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    html_path = output_dir / f"{base_name}.html"
    generate_html_report(report, html_path)

    print(f"✅ Report generated successfully!")
    print(f"   JSON → {json_path}")
    print(f"   HTML → {html_path}")

if __name__ == "__main__":
    main()
