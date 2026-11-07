#!/usr/bin/env python3
"""
CleanYourPhone - Professional Brand Lineup Banner Generator
Renders an ultra-clean, minimal, high-resolution graphic for Supported Brands.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH = 1600
HEIGHT = 920

# Create base canvas with dark slate gradient
img = Image.new("RGBA", (WIDTH, HEIGHT), (12, 15, 20, 255))
draw = ImageDraw.Draw(img)

# Subtle background gradient
for y in range(HEIGHT):
    factor = y / float(HEIGHT)
    r = int(10 + factor * 6)
    g = int(13 + factor * 7)
    b = int(18 + factor * 10)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

# Font loaders
FONT_DIR = "C:/Windows/Fonts"
font_title = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 38)
font_subtitle = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 18)
font_badge = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 12)
font_brand = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 26)
font_os = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 14)
font_status = ImageFont.truetype(os.path.join(FONT_DIR, "segoeuib.ttf"), 11)
font_clock = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 20)
font_date = ImageFont.truetype(os.path.join(FONT_DIR, "segoeui.ttf"), 9)

# Draw Header
header_tag = "MULTI-OEM ARCHITECTURE"
bbox_tag = draw.textbbox((0, 0), header_tag, font=font_badge)
tag_w = bbox_tag[2] - bbox_tag[0]
tag_x = (WIDTH - tag_w) // 2
tag_y = 42

# Pill outline for header tag
draw.rounded_rectangle([tag_x - 14, tag_y - 4, tag_x + tag_w + 14, tag_y + 20], radius=12, fill=(255, 255, 255, 12), outline=(255, 255, 255, 45), width=1)
draw.text((tag_x, tag_y), header_tag, font=font_badge, fill=(120, 180, 255, 255))

title_text = "Supported Brands & Operating Systems"
bbox_title = draw.textbbox((0, 0), title_text, font=font_title)
title_w = bbox_title[2] - bbox_title[0]
draw.text(((WIDTH - title_w) // 2, 75), title_text, font=font_title, fill=(255, 255, 255, 255))

sub_text = "Verified zero-root debloating and native Liquid Glass interface across all 5 BBK & OPLUS ecosystems"
bbox_sub = draw.textbbox((0, 0), sub_text, font=font_subtitle)
sub_w = bbox_sub[2] - bbox_sub[0]
draw.text(((WIDTH - sub_w) // 2, 128), sub_text, font=font_subtitle, fill=(155, 168, 185, 255))

# Brands metadata
BRANDS = [
    {
        "name": "OPPO",
        "os": "ColorOS 11 – 15",
        "accent": (0, 180, 110),
        "bg_top": (8, 35, 25),
        "bg_bot": (5, 18, 14)
    },
    {
        "name": "vivo",
        "os": "Funtouch OS / OriginOS",
        "accent": (65, 115, 255),
        "bg_top": (14, 28, 55),
        "bg_bot": (8, 15, 30)
    },
    {
        "name": "OnePlus",
        "os": "OxygenOS 11 – 15",
        "accent": (240, 50, 70),
        "bg_top": (45, 15, 22),
        "bg_bot": (22, 8, 12)
    },
    {
        "name": "realme",
        "os": "Realme UI 2.0 – 6.0",
        "accent": (255, 185, 25),
        "bg_top": (40, 32, 12),
        "bg_bot": (20, 16, 6)
    },
    {
        "name": "iQOO",
        "os": "Monster / OriginOS",
        "accent": (255, 115, 20),
        "bg_top": (45, 24, 10),
        "bg_bot": (24, 12, 5)
    }
]

# Layout dimensions
PHONE_W = 236
PHONE_H = 470
CORNER = 30
START_Y = 185
TOTAL_PHONES_W = len(BRANDS) * PHONE_W
SPACING = (WIDTH - 120 - TOTAL_PHONES_W) // (len(BRANDS) - 1)
START_X = 60

for i, b in enumerate(BRANDS):
    px = START_X + i * (PHONE_W + SPACING)
    py = START_Y

    # Draw soft subtle accent glow under phone
    glow_color = (*b["accent"], 28)
    draw.rounded_rectangle([px - 4, py - 4, px + PHONE_W + 4, py + PHONE_H + 4], radius=CORNER + 4, fill=glow_color)

    # Phone chassis outer border (aluminum/titanium)
    draw.rounded_rectangle([px, py, px + PHONE_W, py + PHONE_H], radius=CORNER, fill=(28, 32, 40, 255), outline=(75, 85, 100, 255), width=2)

    # Phone screen bezel (inner dark margin)
    BEZEL = 7
    sx = px + BEZEL
    sy = py + BEZEL
    sw = PHONE_W - (BEZEL * 2)
    sh = PHONE_H - (BEZEL * 2)
    sc = CORNER - 6

    # Draw screen gradient
    screen_img = Image.new("RGBA", (sw, sh), (*b["bg_bot"], 255))
    sdraw = ImageDraw.Draw(screen_img)
    for yline in range(sh):
        factor = yline / float(sh)
        sr = int(b["bg_top"][0] * (1 - factor) + b["bg_bot"][0] * factor)
        sg = int(b["bg_top"][1] * (1 - factor) + b["bg_bot"][1] * factor)
        sb = int(b["bg_top"][2] * (1 - factor) + b["bg_bot"][2] * factor)
        sdraw.line([(0, yline), (sw, yline)], fill=(sr, sg, sb, 255))

    # Mask screen to rounded rect
    mask = Image.new("L", (sw, sh), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, sw, sh], radius=sc, fill=255)
    img.paste(screen_img, (sx, sy), mask)

    # Re-draw screen border
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=sc, outline=(255, 255, 255, 30), width=1)

    # Centered punch-hole selfie camera
    cam_x = px + (PHONE_W // 2)
    cam_y = sy + 13
    draw.ellipse([cam_x - 4, cam_y - 4, cam_x + 4, cam_y + 4], fill=(8, 10, 14, 255), outline=(40, 45, 55, 255), width=1)

    # Screen UI: Liquid Glass Header Glance Widget
    gw_w = sw - 28
    gw_h = 60
    gw_x = sx + 14
    gw_y = sy + 38
    draw.rounded_rectangle([gw_x, gw_y, gw_x + gw_w, gw_y + gw_h], radius=16, fill=(255, 255, 255, 26), outline=(255, 255, 255, 65), width=1)
    draw.text((gw_x + 16, gw_y + 10), "10:48", font=font_clock, fill=(255, 255, 255, 255))
    draw.text((gw_x + 16, gw_y + 36), "Thursday, Nov 5", font=font_date, fill=(200, 215, 230, 220))

    # Clean small status pill in widget
    draw.rounded_rectangle([gw_x + gw_w - 56, gw_y + 20, gw_x + gw_w - 12, gw_y + 40], radius=10, fill=(*b["accent"], 60), outline=(*b["accent"], 180), width=1)
    draw.text((gw_x + gw_w - 49, gw_y + 24), "SAFE", font=font_status, fill=(255, 255, 255, 255))

    # Frosted Search Capsule Pill
    sb_w = sw - 28
    sb_h = 32
    sb_x = sx + 14
    sb_y = gw_y + gw_h + 16
    draw.rounded_rectangle([sb_x, sb_y, sb_x + sb_w, sb_y + sb_h], radius=16, fill=(255, 255, 255, 18), outline=(255, 255, 255, 45), width=1)
    draw.text((sb_x + 16, sb_y + 9), "Search apps...", font=font_date, fill=(160, 175, 195, 180))

    # Clean 4x3 App Grid Dots/Squircles (Material You Clean Style)
    grid_y_start = sb_y + sb_h + 24
    for row in range(3):
        for col in range(4):
            app_size = 28
            gap_x = (sw - 28 - (4 * app_size)) // 3
            ax = sx + 14 + col * (app_size + gap_x)
            ay = grid_y_start + row * (app_size + 24)
            # App icon squircle with subtle theme tint
            tint = (*b["accent"], 70) if (row + col) % 3 == 0 else (255, 255, 255, 35)
            draw.rounded_rectangle([ax, ay, ax + app_size, ay + app_size], radius=8, fill=tint, outline=(255, 255, 255, 50), width=1)
            # Small label line beneath
            draw.line([(ax + 4, ay + app_size + 6), (ax + app_size - 4, ay + app_size + 6)], fill=(255, 255, 255, 90), width=2)

    # Floating Liquid Glass Dock Pill at Bottom
    dock_w = sw - 24
    dock_h = 52
    dock_x = sx + 12
    dock_y = sy + sh - dock_h - 14
    # Frosted dock fill & specular top edge
    draw.rounded_rectangle([dock_x, dock_y, dock_x + dock_w, dock_y + dock_h], radius=22, fill=(255, 255, 255, 40), outline=(255, 255, 255, 95), width=1)
    # 4 dock icons
    d_icon_size = 28
    d_gap = (dock_w - (4 * d_icon_size)) // 5
    for di in range(4):
        dix = dock_x + d_gap + di * (d_icon_size + d_gap)
        diy = dock_y + (dock_h - d_icon_size) // 2
        d_tint = (*b["accent"], 110) if di == 0 else (255, 255, 255, 55)
        draw.rounded_rectangle([dix, diy, dix + d_icon_size, diy + d_icon_size], radius=9, fill=d_tint, outline=(255, 255, 255, 80), width=1)

    # --- BELOW PHONE LABELS & BRANDING ---
    label_y = py + PHONE_H + 22

    # Brand Name (Bold, large, pristine)
    bbox_b = draw.textbbox((0, 0), b["name"], font=font_brand)
    bw = bbox_b[2] - bbox_b[0]
    bx = px + (PHONE_W - bw) // 2
    draw.text((bx, label_y), b["name"], font=font_brand, fill=(255, 255, 255, 255))

    # OS Badge Pill
    bbox_os = draw.textbbox((0, 0), b["os"], font=font_os)
    osw = bbox_os[2] - bbox_os[0]
    osx = px + (PHONE_W - osw) // 2
    osy = label_y + 36

    # Glass badge outline
    draw.rounded_rectangle([osx - 10, osy - 3, osx + osw + 10, osy + 21], radius=11, fill=(255, 255, 255, 14), outline=(*b["accent"], 120), width=1)
    draw.text((osx, osy), b["os"], font=font_os, fill=(210, 220, 235, 255))

    # Safe status indicator with colored dot
    stat_text = "Verified Safe"
    bbox_st = draw.textbbox((0, 0), stat_text, font=font_status)
    stw = bbox_st[2] - bbox_st[0]
    stx = px + (PHONE_W - stw) // 2 + 6
    sty = osy + 34

    # Green glowing dot
    dot_x = stx - 10
    dot_y = sty + 6
    draw.ellipse([dot_x - 3, dot_y - 3, dot_x + 3, dot_y + 3], fill=(*b["accent"], 255))
    draw.text((stx, sty), stat_text, font=font_status, fill=(160, 175, 195, 220))

# Save output
output_path = "C:/Users/zeltr/.gemini/antigravity/scratch/cleanyourphone/docs/brands-lineup.jpg"
img.convert("RGB").save(output_path, "JPEG", quality=96)
print(f"Generated clean brands lineup banner: {output_path}")
