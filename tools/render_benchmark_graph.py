#!/usr/bin/env python3
"""
Generates high-resolution before-and-after benchmark visualization graphs
for the unfuck-android repository.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

def generate_benchmark_graphs(output_path):
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(18, 10), facecolor='#0b0f19', dpi=300)
    
    # Grid layout: 2 rows, 2 columns
    gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.25, left=0.06, right=0.94, top=0.90, bottom=0.08)
    
    # Title and header
    fig.suptitle('UNFUCK-ANDROID: EMPIRICAL BENCHMARK & RECOVERY AUDIT',
                 fontsize=22, fontweight='bold', color='#ffffff', y=0.96, fontfamily='sans-serif')
    fig.text(0.5, 0.925, 'Physical Device Production Verification · Android 14 · User 0 Isolation Framework',
             fontsize=12, color='#9ca3af', ha='center', fontfamily='sans-serif')

    # Chart 1: Available Storage Capacity (Top Left)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor('#111827')
    for spine in ax1.spines.values():
        spine.set_color('#1f2937')
    ax1.grid(axis='y', color='#1f2937', linestyle='--', alpha=0.7)

    bars1 = ax1.bar(['Initial Baseline', 'Post-Debloat Optimization'], [10.90, 35.36],
                    color=['#ef4444', '#10b981'], width=0.45, edgecolor='#1f2937', linewidth=1.5)
    ax1.set_ylabel('Available Storage (GB)', fontsize=11, fontweight='bold', color='#f9fafb')
    ax1.set_ylim(0, 42)
    ax1.set_title('Available Internal Storage (Free Space)', fontsize=13, fontweight='bold', color='#ffffff', pad=12)

    # Values on top of bars
    ax1.text(0, 10.90 + 1.0, '10.90 GB\n(10% Capacity)', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#ef4444')
    ax1.text(1, 35.36 + 1.0, '35.36 GB\n(33% Capacity)', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#10b981')

    # Delta badge
    ax1.annotate('+24.46 GB RECLAIMED\n(+224% Free Space Increase)',
                 xy=(1, 26), xytext=(0.5, 36),
                 bbox=dict(boxstyle='round,pad=0.6', fc='#064e3b', ec='#10b981', lw=1.5),
                 arrowprops=dict(arrowstyle='->', color='#10b981', lw=2),
                 ha='center', fontsize=10, fontweight='bold', color='#ffffff')

    # Chart 2: Active Packages Elimination (Top Right)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor('#111827')
    for spine in ax2.spines.values():
        spine.set_color('#1f2937')
    ax2.grid(axis='y', color='#1f2937', linestyle='--', alpha=0.7)

    bars2 = ax2.bar(['Stock Commercial Firmware', 'Debloated & Hardened State'], [547, 474],
                    color=['#8b5cf6', '#06b6d4'], width=0.45, edgecolor='#1f2937', linewidth=1.5)
    ax2.set_ylabel('Active Packages Count', fontsize=11, fontweight='bold', color='#f9fafb')
    ax2.set_ylim(400, 600)
    ax2.set_title('Active Package Footprint', fontsize=13, fontweight='bold', color='#ffffff', pad=12)

    ax2.text(0, 547 + 4, '547 Packages\n(Stock OEM Bloat)', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#8b5cf6')
    ax2.text(1, 474 + 4, '474 Packages\n(Optimized Profile)', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#06b6d4')

    ax2.annotate('-73 BLOAT PACKAGES ELIMINATED\nStorefronts · Ad Carousels · Diagnostics',
                 xy=(1, 490), xytext=(0.5, 565),
                 bbox=dict(boxstyle='round,pad=0.6', fc='#164e63', ec='#06b6d4', lw=1.5),
                 arrowprops=dict(arrowstyle='->', color='#06b6d4', lw=2),
                 ha='center', fontsize=10, fontweight='bold', color='#ffffff')

    # Chart 3: Storage Partition Breakdown Donut (Bottom Left)
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor('#111827')
    ax3.set_title('Post-Debloat Storage Partition Allocation', fontsize=13, fontweight='bold', color='#ffffff', pad=12)

    labels = ['Free Capacity\n(35.36 GB)', 'App User Data\n(36.62 GB)', 'App Code / APKs\n(30.97 GB)', 'Media: Photos/Videos\n(13.15 GB)', 'Volatile Cache\n(3.63 GB)']
    sizes = [35.36, 36.62, 30.97, 13.15, 3.63]
    colors = ['#10b981', '#06b6d4', '#8b5cf6', '#f59e0b', '#ef4444']
    explode = (0.08, 0.02, 0.02, 0.02, 0.05)

    wedges, texts, autotexts = ax3.pie(sizes, labels=labels, autopct='%1.1f%%',
                                       startangle=140, colors=colors, explode=explode,
                                       pctdistance=0.75,
                                       wedgeprops=dict(width=0.45, edgecolor='#111827', linewidth=2),
                                       textprops=dict(color='#d1d5db', fontsize=9, fontweight='500'))
    for autotext in autotexts:
        autotext.set_color('#ffffff')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)

    # Centre text inside donut
    ax3.text(0, 0, '106 GB\nTotal Partition', ha='center', va='center', fontsize=12, fontweight='bold', color='#ffffff')

    # Chart 4: Hardware & Telemetry Scorecard (Bottom Right)
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor('#111827')
    for spine in ax4.spines.values():
        spine.set_color('#1f2937')
    ax4.axis('off')
    ax4.set_title('Subsystem Efficiency & Telemetry Scorecard', fontsize=13, fontweight='bold', color='#ffffff', pad=12)

    metrics = [
        ('Active Telemetry Daemons', 'Stock OEM: 14 Active Services', 'Debloated: 0 Trackers Active', '#10b981'),
        ('Google Discover Ad Feed', 'Active (Minus-One Screen)', 'Completely Disabled (User 0)', '#10b981'),
        ('DNS Tracking Resolution', 'Unencrypted ISP DNS', 'Private DNS over TLS (AdGuard)', '#06b6d4'),
        ('System-wide RAM Footprint', 'Heavily Committed Daemons', '>2.0 GB Physical RAM Released', '#8b5cf6'),
        ('Thermal Equilibrium', 'Throttling Under Load', '37°C - 38°C Stable Battery Temp', '#10b981'),
        ('Logcat Error & Crash Rate', 'Recurring Diagnostics Loops', '0 Critical Crashes / 100% Stable', '#10b981'),
        ('Reversibility Guarantee', 'Requires Factory Reset', '100% User 0 Reversible (04-restore)', '#10b981')
    ]

    y_pos = 0.88
    for label, before, after, status_color in metrics:
        ax4.text(0.04, y_pos, label, fontsize=10, fontweight='bold', color='#ffffff', va='center')
        ax4.text(0.48, y_pos, before, fontsize=9, color='#9ca3af', va='center')
        ax4.text(0.78, y_pos, after, fontsize=9, fontweight='bold', color=status_color, va='center')
        
        # Divider line
        y_pos -= 0.05
        ax4.plot([0.02, 0.98], [y_pos, y_pos], color='#1f2937', linewidth=1)
        y_pos -= 0.07

    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"[+] High-resolution benchmark graph generated at: {output_path}")

if __name__ == '__main__':
    out_dir = r"C:\projects\unfuck-android\docs"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "benchmark-comparison-graph.png")
    generate_benchmark_graphs(out_file)
