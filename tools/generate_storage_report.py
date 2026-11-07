#!/usr/bin/env python3
"""
Storage Analyzer & Reclaim Advisor for Android Devices
Queries `adb shell dumpsys diskstats` and generates a standalone, interactive
HTML dashboard visualizing storage composition, Code vs Data vs Cache,
and actionable storage recovery recommendations.
"""

import subprocess
import re
import json
import os
import sys
import webbrowser

def format_bytes(b):
    if b < 1024:
        return f"{b} B"
    elif b < 1024 * 1024:
        return f"{b / 1024:.1f} KB"
    elif b < 1024 * 1024 * 1024:
        return f"{b / (1024 * 1024):.1f} MB"
    else:
        return f"{b / (1024 * 1024 * 1024):.2f} GB"

def run_adb_command(cmd):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout
    except Exception as e:
        return None

def collect_storage_data():
    print("[*] Querying ADB device storage statistics...")
    disk_output = run_adb_command(['adb', 'shell', 'dumpsys', 'diskstats'])
    if not disk_output:
        print("[-] Unable to query ADB. Generating generic reference benchmark dataset...")
        return generate_sample_data()

    # Parse overall partition stats
    free_match = re.search(r'Data-Free:\s*(\d+)K\s*/\s*(\d+)K\s*total\s*=\s*(\d+)%', disk_output)
    app_size_match = re.search(r'App Size:\s*(\d+)', disk_output)
    app_data_size_match = re.search(r'App Data Size:\s*(\d+)', disk_output)
    app_cache_size_match = re.search(r'App Cache Size:\s*(\d+)', disk_output)
    photos_size_match = re.search(r'Photos Size:\s*(\d+)', disk_output)
    videos_size_match = re.search(r'Videos Size:\s*(\d+)', disk_output)
    audio_size_match = re.search(r'Audio Size:\s*(\d+)', disk_output)
    system_size_match = re.search(r'System Size:\s*(\d+)', disk_output)
    other_size_match = re.search(r'Other Size:\s*(\d+)', disk_output)

    total_data_bytes = int(free_match.group(2)) * 1024 if free_match else 128 * (1024**3)
    free_data_bytes = int(free_match.group(1)) * 1024 if free_match else 35 * (1024**3)
    used_data_bytes = max(0, total_data_bytes - free_data_bytes)

    app_size_bytes = int(app_size_match.group(1)) if app_size_match else 0
    app_data_size_bytes = int(app_data_size_match.group(1)) if app_data_size_match else 0
    app_cache_size_bytes = int(app_cache_size_match.group(1)) if app_cache_size_match else 0
    photos_bytes = int(photos_size_match.group(1)) if photos_size_match else 0
    videos_bytes = int(videos_size_match.group(1)) if videos_size_match else 0
    audio_bytes = int(audio_size_match.group(1)) if audio_size_match else 0
    system_bytes = int(system_size_match.group(1)) if system_size_match else 0
    other_bytes = int(other_size_match.group(1)) if other_size_match else 0

    # Parse per-package stats
    pkg_match = re.search(r'Package Names:\s*(\[.*?\])', disk_output, re.DOTALL)
    app_sizes_match = re.search(r'App Sizes:\s*(\[.*?\])', disk_output, re.DOTALL)
    app_data_sizes_match = re.search(r'App Data Sizes:\s*(\[.*?\])', disk_output, re.DOTALL)
    cache_sizes_match = re.search(r'Cache Sizes:\s*(\[.*?\])', disk_output, re.DOTALL)

    apps = []
    if pkg_match and app_sizes_match and app_data_sizes_match and cache_sizes_match:
        try:
            pkgs = json.loads(pkg_match.group(1))
            asizes = json.loads(app_sizes_match.group(1))
            dsizes = json.loads(app_data_sizes_match.group(1))
            csizes = json.loads(cache_sizes_match.group(1))

            min_len = min(len(pkgs), len(asizes), len(dsizes), len(csizes))
            for i in range(min_len):
                total = asizes[i] + dsizes[i] + csizes[i]
                if total > 5 * 1024 * 1024:  # Filter out trivial < 5MB packages
                    apps.append({
                        'package': pkgs[i],
                        'code_bytes': asizes[i],
                        'data_bytes': dsizes[i],
                        'cache_bytes': csizes[i],
                        'total_bytes': total
                    })
            apps.sort(key=lambda x: x['total_bytes'], reverse=True)
        except Exception as e:
            print(f"[-] Warning parsing package array: {e}")

    return {
        'total_partition': total_data_bytes,
        'free_partition': free_data_bytes,
        'used_partition': used_data_bytes,
        'app_code': app_size_bytes,
        'app_data': app_data_size_bytes,
        'app_cache': app_cache_size_bytes,
        'photos': photos_bytes,
        'videos': videos_bytes,
        'audio': audio_bytes,
        'system': system_bytes,
        'other': other_bytes,
        'apps': apps[:100]  # Top 100 packages
    }

def generate_sample_data():
    total = 111155168 * 1024
    free = 36989196 * 1024
    used = total - free
    return {
        'total_partition': total,
        'free_partition': free,
        'used_partition': used,
        'app_code': 30971484160,
        'app_data': 36618164675,
        'app_cache': 3630960128,
        'photos': 9945141248,
        'videos': 3208507392,
        'audio': 17895424,
        'system': 12800000000,
        'other': 13071589376,
        'apps': [
            {'package': 'com.whatsapp', 'code_bytes': 95899648, 'data_bytes': 4101144576, 'cache_bytes': 125181952, 'total_bytes': 4322226176},
            {'package': 'com.spotify.music', 'code_bytes': 86073888, 'data_bytes': 1357357652, 'cache_bytes': 938635264, 'total_bytes': 2382066804},
            {'package': 'com.google.android.youtube', 'code_bytes': 179040256, 'data_bytes': 1081794560, 'cache_bytes': 572166144, 'total_bytes': 1833000960},
            {'package': 'com.google.android.googlequicksearchbox', 'code_bytes': 169590784, 'data_bytes': 581066752, 'cache_bytes': 222031872, 'total_bytes': 972689408},
            {'package': 'org.telegram.messenger', 'code_bytes': 91787264, 'data_bytes': 646717440, 'cache_bytes': 205246464, 'total_bytes': 943751168},
            {'package': 'com.google.android.gms', 'code_bytes': 179634176, 'data_bytes': 563032064, 'cache_bytes': 107085824, 'total_bytes': 849752064},
            {'package': 'com.android.chrome', 'code_bytes': 142540800, 'data_bytes': 345128960, 'cache_bytes': 84344832, 'total_bytes': 572014592},
            {'package': 'com.heytap.market', 'code_bytes': 68476928, 'data_bytes': 318730240, 'cache_bytes': 74440704, 'total_bytes': 461647872},
            {'package': 'com.oplus.themestore', 'code_bytes': 50974720, 'data_bytes': 249761792, 'cache_bytes': 52727808, 'total_bytes': 353464320},
            {'package': 'com.heytap.pictorial', 'code_bytes': 31477760, 'data_bytes': 209825792, 'cache_bytes': 34246656, 'total_bytes': 275550208}
        ]
    }

def render_html_dashboard(data, output_path):
    total_gb = data['total_partition'] / (1024**3)
    free_gb = data['free_partition'] / (1024**3)
    used_gb = data['used_partition'] / (1024**3)
    free_pct = (data['free_partition'] / data['total_partition']) * 100 if data['total_partition'] else 0
    used_pct = 100 - free_pct

    app_code_gb = data['app_code'] / (1024**3)
    app_data_gb = data['app_data'] / (1024**3)
    app_cache_gb = data['app_cache'] / (1024**3)
    media_gb = (data['photos'] + data['videos'] + data['audio']) / (1024**3)
    system_gb = data['system'] / (1024**3)

    apps_rows = ""
    for app in data['apps']:
        pkg = app['package']
        code_str = format_bytes(app['code_bytes'])
        data_str = format_bytes(app['data_bytes'])
        cache_str = format_bytes(app['cache_bytes'])
        total_str = format_bytes(app['total_bytes'])

        # Recommend recovery path
        action = "Review Usage"
        badge_class = "badge-neutral"
        if app['cache_bytes'] > 200 * 1024 * 1024:
            action = "Purge Cache (Zero Risk)"
            badge_class = "badge-cache"
        elif "heytap" in pkg or "oplus" in pkg or "nearme" in pkg or "facebook" in pkg:
            action = "Debloat User 0"
            badge_class = "badge-bloat"
        elif "whatsapp" in pkg or "telegram" in pkg:
            action = "In-App Media Manager"
            badge_class = "badge-warning"
        elif "spotify" in pkg or "youtube" in pkg:
            action = "Clear Download Cache"
            badge_class = "badge-cache"

        apps_rows += f"""
        <tr>
            <td class="font-mono text-xs">{pkg}</td>
            <td>{code_str}</td>
            <td>{data_str}</td>
            <td class="font-bold text-amber">{cache_str}</td>
            <td class="font-bold">{total_str}</td>
            <td><span class="badge {badge_class}">{action}</span></td>
        </tr>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Android Storage Architecture & Recovery Advisor</title>
    <style>
        :root {{
            --bg: #0b0f19;
            --card-bg: #111827;
            --border: #1f2937;
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #ef4444;
            --accent-purple: #8b5cf6;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            padding: 32px 20px;
            line-height: 1.5;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{ margin-bottom: 28px; border-bottom: 1px solid var(--border); padding-bottom: 20px; }}
        h1 {{ font-size: 1.75rem; font-weight: 700; color: #fff; letter-spacing: -0.02em; }}
        .subtitle {{ font-size: 0.95rem; color: var(--text-muted); margin-top: 4px; }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .kpi-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px 20px;
        }}
        .kpi-title {{ font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); font-weight: 600; letter-spacing: 0.05em; }}
        .kpi-value {{ font-size: 1.8rem; font-weight: 800; color: #fff; margin-top: 6px; }}
        .kpi-sub {{ font-size: 0.8rem; color: var(--text-muted); margin-top: 4px; }}

        .storage-bar-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
        }}
        .storage-bar-header {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px; }}
        .storage-bar-title {{ font-size: 1.1rem; font-weight: 700; }}
        .storage-bar-stats {{ font-size: 0.9rem; color: var(--text-muted); }}
        .storage-bar-stats strong {{ color: #fff; }}
        .progress-track {{
            height: 20px;
            background: #1f2937;
            border-radius: 9999px;
            display: flex;
            overflow: hidden;
            margin-bottom: 14px;
        }}
        .pt-seg {{ height: 100%; transition: width 0.3s; }}
        .seg-used {{ background: var(--accent-rose); }}
        .seg-free {{ background: var(--accent-emerald); }}
        .seg-system {{ background: var(--accent-purple); }}
        .seg-media {{ background: var(--accent-amber); }}
        .legend-row {{ display: flex; flex-wrap: wrap; gap: 16px; font-size: 0.82rem; }}
        .legend-item {{ display: flex; align-items: center; gap: 8px; }}
        .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; }}

        .explanation-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 16px;
            margin-bottom: 28px;
        }}
        .explain-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
        }}
        .explain-card h3 {{ font-size: 1rem; font-weight: 700; margin-bottom: 8px; }}
        .explain-card p {{ font-size: 0.85rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 10px; }}
        .explain-card code {{ background: #1f2937; padding: 2px 6px; border-radius: 4px; font-size: 0.78rem; font-family: monospace; color: var(--accent-cyan); }}

        .recovery-matrix {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 28px;
        }}
        .recovery-matrix h2 {{ font-size: 1.25rem; font-weight: 700; margin-bottom: 16px; }}
        .tier-row {{ display: grid; grid-template-columns: 140px 1fr auto; gap: 16px; padding: 14px 0; border-bottom: 1px solid var(--border); align-items: center; }}
        .tier-row:last-child {{ border-bottom: none; }}
        .tier-badge {{ font-size: 0.75rem; font-weight: 700; text-transform: uppercase; padding: 4px 10px; border-radius: 6px; text-align: center; }}
        .tier-badge.t1 {{ background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald); border: 1px solid var(--accent-emerald); }}
        .tier-badge.t2 {{ background: rgba(6, 182, 212, 0.15); color: var(--accent-cyan); border: 1px solid var(--accent-cyan); }}
        .tier-badge.t3 {{ background: rgba(245, 158, 11, 0.15); color: var(--accent-amber); border: 1px solid var(--accent-amber); }}
        .tier-badge.t4 {{ background: rgba(139, 92, 246, 0.15); color: var(--accent-purple); border: 1px solid var(--accent-purple); }}
        .tier-desc strong {{ color: #fff; font-size: 0.92rem; }}
        .tier-desc p {{ font-size: 0.82rem; color: var(--text-muted); margin-top: 2px; }}
        .tier-action {{ font-family: monospace; font-size: 0.8rem; background: #1f2937; padding: 6px 12px; border-radius: 6px; color: var(--accent-cyan); white-space: nowrap; }}

        .table-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            overflow-x: auto;
        }}
        .table-card h2 {{ font-size: 1.25rem; font-weight: 700; margin-bottom: 16px; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; }}
        th {{ padding: 12px 14px; background: #1f2937; color: var(--text-muted); font-weight: 600; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.05em; }}
        td {{ padding: 12px 14px; border-bottom: 1px solid var(--border); }}
        tr:hover td {{ background: rgba(255, 255, 255, 0.02); }}
        .font-mono {{ font-family: monospace; }}
        .font-bold {{ font-weight: 700; }}
        .text-xs {{ font-size: 0.78rem; }}
        .text-amber {{ color: var(--accent-amber); }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; text-transform: uppercase; }}
        .badge-cache {{ background: rgba(245, 158, 11, 0.2); color: var(--accent-amber); }}
        .badge-bloat {{ background: rgba(239, 68, 68, 0.2); color: var(--accent-rose); }}
        .badge-warning {{ background: rgba(139, 92, 246, 0.2); color: var(--accent-purple); }}
        .badge-neutral {{ background: #1f2937; color: var(--text-muted); }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Android Storage Architecture & Recovery Advisor</h1>
            <p class="subtitle">Empirical breakdown of Data Partition, Application Code, Databases, and Volatile Caches</p>
        </header>

        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Data Partition Total</div>
                <div class="kpi-value">{total_gb:.1f} GB</div>
                <div class="kpi-sub">{used_gb:.1f} GB used ({used_pct:.0f}%)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Available Storage</div>
                <div class="kpi-value" style="color: var(--accent-emerald);">{free_gb:.1f} GB</div>
                <div class="kpi-sub">{free_pct:.0f}% free capacity</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">App Code (APKs)</div>
                <div class="kpi-value">{app_code_gb:.1f} GB</div>
                <div class="kpi-sub">Read-only binaries</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">App User Data</div>
                <div class="kpi-value" style="color: var(--accent-cyan);">{app_data_gb:.1f} GB</div>
                <div class="kpi-sub">Databases and media</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Reclaimable Cache</div>
                <div class="kpi-value" style="color: var(--accent-amber);">{app_cache_gb:.1f} GB</div>
                <div class="kpi-sub">Volatile stale files</div>
            </div>
        </div>

        <div class="storage-bar-card">
            <div class="storage-bar-header">
                <div class="storage-bar-title">Partition Capacity Utilization</div>
                <div class="storage-bar-stats"><strong>{free_gb:.2f} GB Free</strong> of {total_gb:.2f} GB</div>
            </div>
            <div class="progress-track">
                <div class="pt-seg seg-used" style="width: {used_pct:.1f}%;"></div>
                <div class="pt-seg seg-free" style="width: {free_pct:.1f}%;"></div>
            </div>
            <div class="legend-row">
                <div class="legend-item"><div class="legend-dot seg-used"></div> Allocated Space ({used_gb:.1f} GB)</div>
                <div class="legend-item"><div class="legend-dot seg-free"></div> Free Space ({free_gb:.1f} GB)</div>
                <div class="legend-item"><div class="legend-dot seg-system"></div> System & Core ({system_gb:.1f} GB)</div>
                <div class="legend-item"><div class="legend-dot seg-media"></div> User Media ({media_gb:.1f} GB)</div>
            </div>
        </div>

        <div class="explanation-grid">
            <div class="explain-card">
                <h3 style="color: var(--accent-cyan);">1. What is App Code (APK)?</h3>
                <p>The compiled Android application package binary stored on the system or data partition. This represents the raw executable instructions.</p>
                <p><strong>How to reclaim:</strong> Cannot be cleared while the app is kept. Can only be recovered by safely uninstalling or disabling unused applications via <code>pm disable-user --user 0</code>.</p>
            </div>
            <div class="explain-card">
                <h3 style="color: var(--accent-purple);">2. What is App Data?</h3>
                <p>Private user state: SQLite databases, active session tokens, account logins, downloaded offline media, and custom user configurations.</p>
                <p><strong>Caution:</strong> Executing <code>pm clear</code> wipes login credentials and databases. For messaging apps (WhatsApp/Telegram), always use the in-app storage manager.</p>
            </div>
            <div class="explain-card">
                <h3 style="color: var(--accent-amber);">3. What is App Cache?</h3>
                <p>Volatile temporary files, downloaded image previews, HTTP response caches, and temporary transcoding buffers.</p>
                <p><strong>Zero Risk:</strong> Can be safely purged at any time without logging out or losing personal conversations. System automatically trims it when disk is low.</p>
            </div>
        </div>

        <div class="recovery-matrix">
            <h2>The 4-Tier Storage Recovery Action Plan</h2>
            
            <div class="tier-row">
                <div class="tier-badge t1">Tier 1: Zero Risk</div>
                <div class="tier-desc">
                    <strong>Global Stale Cache Trim</strong>
                    <p>Instruct the Android Package Manager to immediately purge all stale application caches across the entire device.</p>
                </div>
                <div class="tier-action">adb shell pm trim-caches 1000G</div>
            </div>

            <div class="tier-row">
                <div class="tier-badge t2">Tier 2: Safe Purge</div>
                <div class="tier-desc">
                    <strong>Heavy Streaming Media Caches</strong>
                    <p>Clear temporary audio/video caches (Spotify, YouTube, Instagram) without deleting user playlists or accounts.</p>
                </div>
                <div class="tier-action">rm -rf /sdcard/Android/data/com.spotify.music/files/.../Storage</div>
            </div>

            <div class="tier-row">
                <div class="tier-badge t3">Tier 3: In-App Purge</div>
                <div class="tier-desc">
                    <strong>Messaging App Forwarded Media Cleanup</strong>
                    <p>Safely delete gigabytes of forwarded videos without endangering chat text or database keys.</p>
                </div>
                <div class="tier-action">WhatsApp Settings -> Storage and data -> Manage storage</div>
            </div>

            <div class="tier-row">
                <div class="tier-badge t4">Tier 4: Bloatware</div>
                <div class="tier-desc">
                    <strong>OEM Storefront & Diagnostic Service Debloat</strong>
                    <p>De-allocate system RAM, disk space, and battery by freezing OEM storefronts and diagnostic loggers.</p>
                </div>
                <div class="tier-action">.\\scripts\\02-debloat.ps1 -Brand auto</div>
            </div>
        </div>

        <div class="table-card">
            <h2>High-Impact Applications Storage Roster</h2>
            <table>
                <thead>
                    <tr>
                        <th>Package Identifier</th>
                        <th>App Code (APK)</th>
                        <th>User Data</th>
                        <th>App Cache</th>
                        <th>Total Footprint</th>
                        <th>Recommended Action</th>
                    </tr>
                </thead>
                <tbody>
                    {apps_rows}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[+] Storage dashboard generated successfully at: {output_path}")

def main():
    output_html = "storage-analyzer.html"
    if len(sys.argv) > 1 and sys.argv[1].endswith('.html'):
        output_html = sys.argv[1]
    
    data = collect_storage_data()
    render_html_dashboard(data, output_html)

    # Attempt to open in local browser
    try:
        webbrowser.open(os.path.abspath(output_html))
    except Exception:
        pass

if __name__ == '__main__':
    main()
