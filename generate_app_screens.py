import os
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 1520

# Load Fonts
FONT_TITLE = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 34)
FONT_HEADING = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 30)
FONT_SUB = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 24)
FONT_SM = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 20)
FONT_SMB = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 20)
FONT_STATUS = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 22)
FONT_BEBAS_LG = ImageFont.truetype('assets/fonts/BebasNeue Bold.ttf', 50)
FONT_BEBAS_MD = ImageFont.truetype('assets/fonts/BebasNeue Bold.ttf', 36)
FONT_BEBAS_SM = ImageFont.truetype('assets/fonts/BebasNeue Bold.ttf', 28)

def draw_status_bar(draw, dark=False):
    text_color = (15, 23, 42) if dark else (255, 255, 255)
    draw.text((45, 22), "22:04", fill=text_color, font=FONT_STATUS)
    draw.text((W - 150, 22), "5G  100%", fill=text_color, font=FONT_STATUS)
    # Battery icon outline & fill
    draw.rounded_rectangle((W - 55, 25, W - 30, 45), radius=3, outline=text_color, width=2)
    draw.rectangle((W - 51, 29, W - 35, 41), fill=text_color)
    draw.rectangle((W - 30, 31, W - 28, 39), fill=text_color)
    # Camera punch hole
    draw.ellipse((W//2 - 12, 20, W//2 + 12, 44), fill=(10, 10, 10))

def draw_vector_icon(draw, name, cx, cy, color, size=24):
    s = size // 2
    if name == 'home':
        # Roof
        draw.polygon([(cx, cy - s), (cx - s, cy), (cx + s, cy)], fill=color)
        # Body
        draw.rectangle((cx - s + 3, cy, cx + s - 3, cy + s), fill=color)
        # Door cutout
        draw.rectangle((cx - 3, cy + s - 6, cx + 3, cy + s), fill=(255, 255, 255))
    elif name == 'templates':
        # 4 grid squares
        h = s - 2
        draw.rounded_rectangle((cx - s, cy - s, cx - 2, cy - 2), radius=2, fill=color)
        draw.rounded_rectangle((cx + 2, cy - s, cx + s, cy - 2), radius=2, fill=color)
        draw.rounded_rectangle((cx - s, cy + 2, cx - 2, cy + s), radius=2, fill=color)
        draw.rounded_rectangle((cx + 2, cy + 2, cx + s, cy + s), radius=2, fill=color)
    elif name == 'cutout':
        # Scissors/Cutout shape
        draw.line((cx - s + 2, cy - s + 2, cx + s - 2, cy + s - 2), fill=color, width=3)
        draw.line((cx - s + 2, cy + s - 2, cx + s - 2, cy - s + 2), fill=color, width=3)
        draw.ellipse((cx - s, cy + s - 8, cx - s + 8, cy + s), outline=color, width=2)
        draw.ellipse((cx + s - 8, cy + s - 8, cx + s, cy + s), outline=color, width=2)
    elif name == 'projects':
        # Folder
        draw.rounded_rectangle((cx - s, cy - s + 3, cx + s, cy + s), radius=3, fill=color)
        draw.rectangle((cx - s, cy - s, cx - s + 8, cy - s + 4), fill=color)
    elif name == 'settings':
        # Sliders/settings icon
        draw.line((cx - s, cy - 6, cx + s, cy - 6), fill=color, width=2)
        draw.ellipse((cx - 3, cy - 9, cx + 3, cy - 3), fill=color)
        draw.line((cx - s, cy + 6, cx + s, cy + 6), fill=color, width=2)
        draw.ellipse((cx + 1, cy + 3, cx + 7, cy + 9), fill=color)

def draw_bottom_nav(draw, active_idx=0):
    nav_y = H - 110
    draw.rectangle((0, nav_y, W, H), fill=(255, 255, 255))
    draw.line((0, nav_y, W, nav_y), fill=(226, 232, 240), width=2)
    
    tabs = [('home', "Home"), ('templates', "Templates"), ('cutout', "Cutout"), ('projects', "Projects"), ('settings', "Settings")]
    tab_w = W // len(tabs)
    for i, (icon_name, label) in enumerate(tabs):
        tx = i * tab_w + tab_w // 2
        is_active = (i == active_idx)
        color = (6, 167, 74) if is_active else (100, 116, 139)
        draw_vector_icon(draw, icon_name, tx, nav_y + 32, color, size=24)
        draw.text((tx - 26, nav_y + 54), label, fill=color, font=FONT_SM)
        if is_active:
            draw.rounded_rectangle((tx - 24, nav_y + 82, tx + 24, nav_y + 86), radius=2, fill=(6, 167, 74))

# -------------------------------------------------------------
# 1. SCREEN: Hero App Feed (Home Feed with Trending & Templates)
# -------------------------------------------------------------
def make_hero_feed():
    img = Image.new("RGBA", (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(img)
    
    # Top Emerald Curved Header
    draw.rectangle((0, 0, W, 225), fill=(6, 167, 74))
    draw_status_bar(draw, dark=False)
    
    # App brand row
    app_icon = Image.open('assets/images/app-icon.png').convert("RGBA").resize((56, 56))
    img.paste(app_icon, (40, 75), app_icon)
    draw.text((110, 74), "Ultimate Thumbnail", fill=(255, 255, 255), font=FONT_HEADING)
    draw.text((110, 112), "500+ Creator Templates • 1280x720 HD", fill=(209, 250, 229), font=FONT_SM)
    
    # Search bar
    draw.rounded_rectangle((40, 150, W - 40, 210), radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    # Magnifier
    draw.ellipse((62, 172, 74, 184), outline=(148, 163, 184), width=2)
    draw.line((72, 182, 80, 190), fill=(148, 163, 184), width=2)
    draw.text((90, 168), "Search 500+ templates & creator layouts...", fill=(148, 163, 184), font=FONT_SUB)
    
    # Category Pills row
    pills = [("Trending", True), ("Gaming", False), ("Tech", False), ("Vlogs", False), ("3D Fonts", False)]
    px = 40
    for name, is_sel in pills:
        pw = int(len(name) * 16) + 36
        bg = (6, 167, 74) if is_sel else (255, 255, 255)
        tc = (255, 255, 255) if is_sel else (71, 85, 105)
        draw.rounded_rectangle((px, 240, px + pw, 285), radius=20, fill=bg, outline=(203, 213, 225), width=1)
        draw.text((px + 18, 250), name, fill=tc, font=FONT_SMB)
        px += pw + 14

    # Featured Hero Template Card (16:9)
    fy = 310
    draw.text((40, fy), "Featured Layout of the Day", fill=(15, 23, 42), font=FONT_HEADING)
    draw.text((W - 145, fy + 6), "See All (500+) >", fill=(6, 167, 74), font=FONT_SMB)
    
    hero_card_y = fy + 48
    draw.rounded_rectangle((40, hero_card_y, W - 40, hero_card_y + 440), radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    feat_img = Image.open('assets/templates/gaming-hardcore.webp').convert("RGBA").resize((640, 360))
    mask = Image.new('L', (640, 360), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 640, 360), radius=18, fill=255)
    img.paste(feat_img, (40, hero_card_y), mask)
    
    # Floating Badge on thumbnail
    draw.rounded_rectangle((55, hero_card_y + 16, 230, hero_card_y + 54), radius=10, fill=(239, 68, 68))
    draw.text((70, hero_card_y + 23), "TOP GAMING TREND", fill=(255, 255, 255), font=FONT_SMB)
    
    # Card Details below image
    dy = hero_card_y + 375
    draw.text((60, dy), "100 DAYS HARDCORE SURVIVAL", fill=(15, 23, 42), font=FONT_BEBAS_MD)
    draw.text((60, dy + 38), "1280 x 720 HD • Bebas Neue • 24.8% CTR", fill=(100, 116, 139), font=FONT_SM)
    # Quick Edit button
    draw.rounded_rectangle((W - 180, dy + 5, W - 60, dy + 55), radius=12, fill=(6, 167, 74))
    draw.text((W - 162, dy + 18), "Use Layout", fill=(255, 255, 255), font=FONT_SMB)
    
    # Category Split Section
    sy = hero_card_y + 465
    draw.text((40, sy), "Trending Categories", fill=(15, 23, 42), font=FONT_HEADING)
    
    cw, ch = 305, 172
    # Card 1: Tech Review
    t1 = Image.open('assets/templates/tech-review.webp').convert("RGBA").resize((cw, ch))
    t1_mask = Image.new('L', (cw, ch), 0)
    ImageDraw.Draw(t1_mask).rounded_rectangle((0, 0, cw, ch), radius=16, fill=255)
    img.paste(t1, (40, sy + 45), t1_mask)
    draw.text((45, sy + 225), "New M4 Pro Review", fill=(15, 23, 42), font=FONT_SMB)
    draw.text((45, sy + 252), "Tech • 19.5% CTR", fill=(6, 167, 74), font=FONT_SM)
    
    # Card 2: Arctic Survival
    t2 = Image.open('assets/templates/arctic-survival.webp').convert("RGBA").resize((cw, ch))
    t2_mask = Image.new('L', (cw, ch), 0)
    ImageDraw.Draw(t2_mask).rounded_rectangle((0, 0, cw, ch), radius=16, fill=255)
    img.paste(t2, (W - 40 - cw, sy + 45), t2_mask)
    draw.text((W - 35 - cw, sy + 225), "24H Arctic Survival", fill=(15, 23, 42), font=FONT_SMB)
    draw.text((W - 35 - cw, sy + 252), "Action • Glow FX", fill=(6, 167, 74), font=FONT_SM)
    
    # Floating "+" Action Button (FAB)
    fab_x, fab_y = W - 100, H - 190
    draw.ellipse((fab_x, fab_y, fab_x + 70, fab_y + 70), fill=(6, 167, 74))
    draw.text((fab_x + 22, fab_y + 12), "+", fill=(255, 255, 255), font=FONT_HEADING)
    
    draw_bottom_nav(draw, active_idx=0)
    img.convert("RGB").save('assets/images/app-screen-feed.webp', 'WEBP', quality=95)
    print("Generated app-screen-feed.webp")

# -------------------------------------------------------------
# 2. SCREEN: Templates Browser (For Section 2: Explore)
# -------------------------------------------------------------
def make_templates_screen():
    img = Image.new("RGBA", (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle((0, 0, W, 140), fill=(255, 255, 255))
    draw.line((0, 140, W, 140), fill=(226, 232, 240), width=1)
    draw_status_bar(draw, dark=True)
    
    draw.text((40, 75), "Templates Library", fill=(15, 23, 42), font=FONT_TITLE)
    draw.rounded_rectangle((W - 140, 75, W - 40, 120), radius=10, fill=(209, 250, 229))
    draw.text((W - 128, 86), "500+ Pro", fill=(6, 167, 74), font=FONT_SMB)
    
    tabs = ["All (520)", "Gaming (140)", "Tech (85)", "Vlogs (110)", "Tutorials (95)"]
    tx = 40
    for i, t in enumerate(tabs):
        is_sel = (i == 1)
        bg = (6, 167, 74) if is_sel else (255, 255, 255)
        tc = (255, 255, 255) if is_sel else (71, 85, 105)
        tw = int(len(t) * 14) + 26
        draw.rounded_rectangle((tx, 160, tx + tw, 205), radius=16, fill=bg, outline=(203, 213, 225), width=1)
        draw.text((tx + 14, 170), t, fill=tc, font=FONT_SMB)
        tx += tw + 14
        
    cards_data = [
        ('assets/templates/gaming-hardcore.webp', "100 DAYS HARDCORE SURVIVAL", "Gaming • Bebas Neue • 1280x720", "24.8% CTR"),
        ('assets/templates/tech-review.webp', "NEW M4 PRO: BRUTAL TRUTH", "Tech Hardware • High-Contrast Red", "19.5% CTR"),
        ('assets/templates/arctic-survival.webp', "SURVIVED 24H IN ARCTIC FREEZE", "Challenge / Vlog • Ice Glow FX", "21.3% CTR"),
        ('assets/templates/vlog-travel.webp', "I FOUND A SECRET HIDDEN CITY", "Travel Vlog • Sunset Scrim", "18.9% CTR"),
        ('assets/templates/passive-income.webp', "HOW I MADE $10,000/MONTH", "Finance • Money Green Glow", "27.4% CTR"),
    ]
    
    cy = 225
    for img_path, title, sub, badge in cards_data:
        draw.rounded_rectangle((40, cy, W - 40, cy + 225), radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        
        thumb = Image.open(img_path).convert("RGBA").resize((320, 180))
        tmask = Image.new('L', (320, 180), 0)
        ImageDraw.Draw(tmask).rounded_rectangle((0, 0, 320, 180), radius=14, fill=255)
        img.paste(thumb, (55, cy + 22), tmask)
        
        ix = 395
        draw.rounded_rectangle((ix, cy + 25, ix + 120, cy + 55), radius=8, fill=(209, 250, 229))
        draw.text((ix + 12, cy + 30), badge, fill=(6, 167, 74), font=FONT_SM)
        
        draw.text((ix, cy + 68), title[:22], fill=(15, 23, 42), font=FONT_BEBAS_SM)
        draw.text((ix, cy + 105), sub[:30], fill=(100, 116, 139), font=FONT_SM)
        
        draw.rounded_rectangle((ix, cy + 145, ix + 130, cy + 190), radius=10, fill=(6, 167, 74))
        draw.text((ix + 20, cy + 155), "Use Preset", fill=(255, 255, 255), font=FONT_SMB)
        
        cy += 245
        if cy > H - 150:
            break
            
    draw_bottom_nav(draw, active_idx=1)
    img.convert("RGB").save('assets/images/app-screen-templates.webp', 'WEBP', quality=95)
    print("Generated app-screen-templates.webp")

# -------------------------------------------------------------
# 3. SCREEN: Multi-Layer Editor Studio (For Section 3: Customize)
# -------------------------------------------------------------
def make_editor_screen():
    img = Image.new("RGBA", (W, H), (15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    draw_status_bar(draw, dark=False)
    
    # Top Action Bar
    draw.rectangle((0, 60, W, 130), fill=(30, 41, 59))
    draw.text((40, 78), "< Back", fill=(255, 255, 255), font=FONT_SUB)
    draw.text((W//2 - 90, 78), "1280 x 720 Studio", fill=(209, 250, 229), font=FONT_SMB)
    draw.rounded_rectangle((W - 150, 72, W - 40, 118), radius=10, fill=(6, 167, 74))
    draw.text((W - 135, 82), "Export HD", fill=(255, 255, 255), font=FONT_SMB)
    
    # Center 16:9 Canvas (640x360)
    canvas_y = 155
    canvas_img = Image.open('assets/templates/gaming-hardcore.webp').convert("RGBA").resize((640, 360))
    cmask = Image.new('L', (640, 360), 0)
    ImageDraw.Draw(cmask).rounded_rectangle((0, 0, 640, 360), radius=16, fill=255)
    img.paste(canvas_img, (40, canvas_y), cmask)
    
    # Bounding Box around text layer with resize handles
    bx1, by1, bx2, by2 = 65, canvas_y + 160, 480, canvas_y + 260
    draw.rectangle((bx1, by1, bx2, by2), outline=(56, 189, 248), width=3)
    for cx, cy in [(bx1, by1), (bx2, by1), (bx1, by2), (bx2, by2)]:
        draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=(255, 255, 255), outline=(56, 189, 248), width=2)
    draw.line((bx1 + (bx2 - bx1)//2, by1, bx1 + (bx2 - bx1)//2, by1 - 25), fill=(56, 189, 248), width=2)
    draw.ellipse((bx1 + (bx2 - bx1)//2 - 8, by1 - 33, bx1 + (bx2 - bx1)//2 + 8, by1 - 17), fill=(6, 167, 74))
    
    # Canvas Meta Bar
    draw.text((45, canvas_y + 375), "Canvas: 1280 x 720 (16:9) • Zoom: 100%", fill=(148, 163, 184), font=FONT_SM)
    draw.text((W - 180, canvas_y + 375), "Undo  |  Redo", fill=(56, 189, 248), font=FONT_SMB)
    
    # Layer Stack Panel
    ly = canvas_y + 420
    draw.text((40, ly), "Active Layers (4)", fill=(255, 255, 255), font=FONT_HEADING)
    draw.text((W - 140, ly + 6), "+ Add Layer", fill=(6, 167, 74), font=FONT_SMB)
    
    layers = [
        ("Layer 4: Headline Text", "'SECRET GLITCH!' (Bebas Neue)", True, "TEXT"),
        ("Layer 3: Cutout Character", "Gamer with Headset (AI Cutout)", False, "CUT"),
        ("Layer 2: Graphic Overlay", "Speed Lines & Sparkles (FX)", False, "FX"),
        ("Layer 1: Background Canvas", "Dark Arena Gradient", False, "BG")
    ]
    
    row_y = ly + 45
    for name, desc, is_active, tag in layers:
        bg = (51, 65, 85) if is_active else (30, 41, 59)
        border = (6, 167, 74) if is_active else (51, 65, 85)
        draw.rounded_rectangle((40, row_y, W - 40, row_y + 75), radius=14, fill=bg, outline=border, width=2)
        
        # Tag badge
        draw.rounded_rectangle((55, row_y + 20, 105, row_y + 55), radius=6, fill=(6, 167, 74) if is_active else (71, 85, 105))
        draw.text((63, row_y + 26), tag, fill=(255, 255, 255), font=FONT_SM)
        
        draw.text((120, row_y + 14), name, fill=(255, 255, 255) if is_active else (203, 213, 225), font=FONT_SMB)
        draw.text((120, row_y + 42), desc, fill=(148, 163, 184), font=FONT_SM)
        
        draw.text((W - 120, row_y + 24), "Visible • Locked", fill=(148, 163, 184), font=FONT_SM)
        row_y += 90
        
    # Bottom Tooldock
    dock_y = H - 180
    draw.rectangle((0, dock_y, W, H), fill=(30, 41, 59))
    draw.line((0, dock_y, W, dock_y), fill=(51, 65, 85), width=2)
    
    tools = ["Text", "50+ Fonts", "3D Glow", "Colors", "Stickers", "Cutout"]
    tw = W // len(tools)
    for i, label in enumerate(tools):
        tx = i * tw + tw // 2
        is_sel = (i == 1)
        draw.rounded_rectangle((tx - 36, dock_y + 25, tx + 36, dock_y + 65), radius=10, fill=(6, 167, 74) if is_sel else (51, 65, 85))
        draw.text((tx - 24, dock_y + 35), str(i + 1), fill=(255, 255, 255), font=FONT_SMB)
        draw.text((tx - 26, dock_y + 80), label, fill=(6, 167, 74) if is_sel else (148, 163, 184), font=FONT_SM)
        
    img.convert("RGB").save('assets/images/app-screen-editor.webp', 'WEBP', quality=95)
    print("Generated app-screen-editor.webp")

# -------------------------------------------------------------
# 4. SCREEN: Background Cutout Eraser (For Section 4: Cutout)
# -------------------------------------------------------------
def make_cutout_screen():
    img = Image.new("RGBA", (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle((0, 0, W, 140), fill=(255, 255, 255))
    draw.line((0, 140, W, 140), fill=(226, 232, 240), width=1)
    draw_status_bar(draw, dark=True)
    
    draw.text((40, 78), "< Cancel", fill=(100, 116, 139), font=FONT_SUB)
    draw.text((W//2 - 95, 78), "1-Tap AI Cutout", fill=(15, 23, 42), font=FONT_TITLE)
    draw.rounded_rectangle((W - 130, 72, W - 40, 118), radius=10, fill=(6, 167, 74))
    draw.text((W - 110, 82), "Done", fill=(255, 255, 255), font=FONT_SMB)
    
    # Canvas with Checkerboard
    cy = 160
    cw, ch = W - 80, 680
    draw.rounded_rectangle((40, cy, 40 + cw, cy + ch), radius=24, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    
    sq = 20
    for y in range(cy + 4, cy + ch - 4, sq):
        for x in range(44, 44 + cw - 8, sq):
            if ((x // sq) + (y // sq)) % 2 == 0:
                draw.rectangle((x, y, min(x + sq, 40 + cw - 4), min(y + sq, cy + ch - 4)), fill=(241, 245, 249))
                
    if os.path.exists('assets/images/creator-cutout.png'):
        subject = Image.open('assets/images/creator-cutout.png').convert("RGBA")
        sw = int(cw * 0.75)
        sh = int(sw * (subject.height / subject.width))
        subject = subject.resize((sw, sh))
        img.paste(subject, (W//2 - sw//2, cy + ch - sh - 20), subject)
        
    # Offset Cursor Crosshair Brush Effect
    brush_x, brush_y = W//2 + 40, cy + 240
    draw.ellipse((brush_x - 30, brush_y - 30, brush_x + 30, brush_y + 30), outline=(239, 68, 68), width=3)
    draw.ellipse((brush_x - 4, brush_y - 4, brush_x + 4, brush_y + 4), fill=(239, 68, 68))
    draw.line((brush_x, brush_y + 30, brush_x, brush_y + 120), fill=(239, 68, 68), width=2)
    draw.ellipse((brush_x - 18, brush_y + 110, brush_x + 18, brush_y + 146), fill=(6, 167, 74, 180), outline=(255, 255, 255), width=2)
    draw.text((brush_x + 25, brush_y + 118), "Fingertip Offset (120px)", fill=(15, 23, 42), font=FONT_SMB)
    
    draw.rounded_rectangle((W//2 - 110, cy + 25, W//2 + 110, cy + 65), radius=20, fill=(6, 167, 74))
    draw.text((W//2 - 95, cy + 32), "0.2s Auto Isolated", fill=(255, 255, 255), font=FONT_SMB)
    
    # Control Panel Container
    py = cy + ch + 30
    draw.rounded_rectangle((40, py, W - 40, H - 40), radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    draw.text((65, py + 25), "Auto Color Threshold: 70%", fill=(15, 23, 42), font=FONT_SMB)
    draw.text((W - 140, py + 25), "Smooth: 8px", fill=(100, 116, 139), font=FONT_SM)
    
    draw.rounded_rectangle((65, py + 65, W - 65, py + 77), radius=6, fill=(226, 232, 240))
    draw.rounded_rectangle((65, py + 65, int(65 + (W - 130) * 0.7), py + 77), radius=6, fill=(6, 167, 74))
    tx = int(65 + (W - 130) * 0.7)
    draw.ellipse((tx - 16, py + 55, tx + 16, py + 87), fill=(255, 255, 255), outline=(6, 167, 74), width=4)
    
    modes = [("Auto", True), ("Lasso", False), ("Brush", False), ("Restore", False), ("Zoom", False)]
    mx = 65
    mw = (W - 130 - (len(modes)-1)*10) // len(modes)
    for name, is_sel in modes:
        bg = (6, 167, 74) if is_sel else (241, 245, 249)
        tc = (255, 255, 255) if is_sel else (71, 85, 105)
        draw.rounded_rectangle((mx, py + 115, mx + mw, py + 165), radius=12, fill=bg)
        draw.text((mx + 14, py + 128), name, fill=tc, font=FONT_SMB)
        mx += mw + 10
        
    draw.rounded_rectangle((65, py + 195, W - 65, py + 255), radius=14, fill=(6, 167, 74))
    draw.text((W//2 - 110, py + 210), "Save Isolated Sticker", fill=(255, 255, 255), font=FONT_HEADING)
    
    img.convert("RGB").save('assets/images/app-screen-cutout.webp', 'WEBP', quality=95)
    print("Generated app-screen-cutout.webp")

# -------------------------------------------------------------
# 5. SCREEN: HD Export Screen (For Section 5: Export & Share)
# -------------------------------------------------------------
def make_export_screen():
    img = Image.new("RGBA", (W, H), (248, 250, 252, 255))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle((0, 0, W, 140), fill=(255, 255, 255))
    draw.line((0, 140, W, 140), fill=(226, 232, 240), width=1)
    draw_status_bar(draw, dark=True)
    
    draw.text((40, 78), "< Edit", fill=(100, 116, 139), font=FONT_SUB)
    draw.text((W//2 - 90, 78), "Export Thumbnail", fill=(15, 23, 42), font=FONT_TITLE)
    
    canvas_y = 170
    thumb = Image.open('assets/templates/arctic-survival.webp').convert("RGBA").resize((640, 360))
    tmask = Image.new('L', (640, 360), 0)
    ImageDraw.Draw(tmask).rounded_rectangle((0, 0, 640, 360), radius=20, fill=255)
    img.paste(thumb, (40, canvas_y), tmask)
    
    draw.rounded_rectangle((55, canvas_y + 15, 220, canvas_y + 55), radius=10, fill=(6, 167, 74))
    draw.text((70, canvas_y + 22), "1280 x 720 FULL HD", fill=(255, 255, 255), font=FONT_SMB)
    draw.text((50, canvas_y + 380), "File: 24h_arctic_survival.png • 1.4 MB • Lossless PNG", fill=(100, 116, 139), font=FONT_SM)
    
    sy = canvas_y + 430
    draw.rounded_rectangle((40, sy, W - 40, sy + 380), radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((65, sy + 25), "Export Settings", fill=(15, 23, 42), font=FONT_HEADING)
    
    draw.text((65, sy + 75), "Format:", fill=(71, 85, 105), font=FONT_SUB)
    draw.rounded_rectangle((170, sy + 68, 330, sy + 115), radius=12, fill=(6, 167, 74))
    draw.text((195, sy + 78), "PNG (Lossless)", fill=(255, 255, 255), font=FONT_SMB)
    draw.rounded_rectangle((350, sy + 68, 480, sy + 115), radius=12, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((385, sy + 78), "JPG (Fast)", fill=(71, 85, 105), font=FONT_SMB)
    
    draw.text((65, sy + 145), "Resolution:", fill=(71, 85, 105), font=FONT_SUB)
    draw.rounded_rectangle((200, sy + 138, 420, sy + 185), radius=12, fill=(6, 167, 74))
    draw.text((220, sy + 148), "1280 x 720 (Standard)", fill=(255, 255, 255), font=FONT_SMB)
    draw.rounded_rectangle((440, sy + 138, 620, sy + 185), radius=12, fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    draw.text((475, sy + 148), "1920 x 1080 (4K)", fill=(71, 85, 105), font=FONT_SMB)
    
    draw.text((65, sy + 215), "Watermark:  None (100% Ad-Free)", fill=(6, 167, 74), font=FONT_SMB)
    draw.text((65, sy + 250), "Aspect Ratio:  16:9 YouTube Certified", fill=(100, 116, 139), font=FONT_SM)
    
    by = sy + 300
    draw.rounded_rectangle((65, by, W - 65, by + 65), radius=14, fill=(6, 167, 74))
    draw.text((W//2 - 130, by + 18), "Save Directly to Gallery", fill=(255, 255, 255), font=FONT_HEADING)
    
    sy2 = sy + 410
    draw.rounded_rectangle((40, sy2, W//2 - 15, sy2 + 65), radius=14, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((70, sy2 + 18), "YouTube Studio", fill=(15, 23, 42), font=FONT_SMB)
    
    draw.rounded_rectangle((W//2 + 15, sy2, W - 40, sy2 + 65), radius=14, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw.text((W//2 + 50, sy2 + 18), "Share Cover", fill=(15, 23, 42), font=FONT_SMB)
    
    draw_bottom_nav(draw, active_idx=3)
    img.convert("RGB").save('assets/images/app-screen-export.webp', 'WEBP', quality=95)
    print("Generated app-screen-export.webp")

if __name__ == '__main__':
    make_hero_feed()
    make_templates_screen()
    make_editor_screen()
    make_cutout_screen()
    make_export_screen()
