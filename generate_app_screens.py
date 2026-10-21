import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 720, 1520

APP_DIR = r"C:\nj\thumbnailkrunal\app\src\main"
RES_DRAWABLE = os.path.join(APP_DIR, "res", "drawable")
RES_NODPI = os.path.join(APP_DIR, "res", "drawable-nodpi")
FONT_NUNITO_PATH = os.path.join(APP_DIR, "res", "font", "nunitobold.ttf")
FONT_BEBAS_PATH = os.path.join(APP_DIR, "assets", "font", "BebasNeue Bold.ttf")

# Load Fonts
FONT_TITLE = ImageFont.truetype(FONT_NUNITO_PATH, 28)
FONT_HEADING = ImageFont.truetype(FONT_NUNITO_PATH, 22)
FONT_SUB = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 20)
FONT_SM = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 16)
FONT_SMB = ImageFont.truetype(FONT_NUNITO_PATH, 16)
FONT_STATUS = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 22)
FONT_BEBAS_XL = ImageFont.truetype(FONT_BEBAS_PATH, 48)
FONT_BEBAS_LG = ImageFont.truetype(FONT_BEBAS_PATH, 36)
FONT_BEBAS_MD = ImageFont.truetype(FONT_BEBAS_PATH, 26)
FONT_BEBAS_SM = ImageFont.truetype(FONT_BEBAS_PATH, 20)

# Colors
COLOR_BG = (33, 32, 41)          # #212029 (Real App Background)
COLOR_BAR = (47, 45, 58)         # #2F2D3A (Real App Action/Top Bar)
COLOR_BAR_BORDER = (58, 55, 72)  # Subtle divider
COLOR_ACCENT = (14, 172, 255)    # #0EACFF (Real App Active Cyan/Blue)
COLOR_ACCENT_ALT = (0, 209, 143) # Emerald highlight
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_MUTED = (156, 163, 175)
COLOR_CARD_BG = (42, 40, 52)

def load_app_drawable(filename, size=None):
    path = os.path.join(RES_NODPI, filename)
    if not os.path.exists(path):
        path = os.path.join(RES_DRAWABLE, filename)
    if not os.path.exists(path):
        print(f"Warning: {filename} not found")
        return None
    im = Image.open(path).convert("RGBA")
    if size:
        im = im.resize(size, Image.Resampling.LANCZOS)
    return im

def draw_status_bar(draw, dark=False):
    text_color = (255, 255, 255) if not dark else (20, 20, 20)
    # Time
    draw.text((45, 18), "22:04", fill=text_color, font=FONT_STATUS)
    # 5G & Battery
    draw.text((W - 160, 18), "5G  100%", fill=text_color, font=FONT_STATUS)
    # Battery Outline
    draw.rounded_rectangle((W - 60, 22, W - 32, 42), radius=3, outline=text_color, width=2)
    draw.rectangle((W - 56, 26, W - 38, 38), fill=text_color)
    draw.rectangle((W - 32, 28, W - 30, 36), fill=text_color)
    # Camera punch hole
    draw.ellipse((W//2 - 12, 18, W//2 + 12, 42), fill=(15, 15, 18))

def draw_bottom_dock(img, draw, active_idx=0):
    nav_h = 105
    nav_y = H - nav_h - 25 # leave 25px for system bar
    draw.rectangle((0, nav_y, W, nav_y + nav_h), fill=COLOR_BAR)
    draw.line((0, nav_y, W, nav_y), fill=COLOR_BAR_BORDER, width=2)
    
    # 4 Items: CREATE, FRAME, MY EDIT, MY SAVE
    items = [
        ("btn_create.png", "CREATE"),
        (None, "FRAME"),
        ("btn_my_edit.png", "MY EDIT"),
        ("btn_my_save.png", "MY SAVE")
    ]
    tab_w = W // len(items)
    for i, (icon_name, label) in enumerate(items):
        cx = i * tab_w + tab_w // 2
        is_active = (i == active_idx)
        text_color = COLOR_ACCENT if is_active else COLOR_TEXT_MUTED
        
        # Load icon
        icon = load_app_drawable(icon_name, (40, 40)) if icon_name else None
        if icon:
            img.paste(icon, (cx - 20, nav_y + 14), icon)
        else:
            # FRAME 4-pane grid vector icon
            if label == "FRAME":
                draw.rounded_rectangle((cx - 18, nav_y + 14, cx + 18, nav_y + 50), radius=4, outline=text_color, width=2)
                draw.line((cx, nav_y + 14, cx, nav_y + 50), fill=text_color, width=2)
                draw.line((cx - 18, nav_y + 30, cx + 18, nav_y + 30), fill=text_color, width=2)
            else:
                draw.rectangle((cx - 16, nav_y + 14, cx + 16, nav_y + 46), fill=text_color)
        
        draw.text((cx - len(label)*4 - 6, nav_y + 62), label, fill=text_color, font=FONT_SMB)
        if is_active:
            draw.rounded_rectangle((cx - 22, nav_y + 88, cx + 22, nav_y + 92), radius=2, fill=COLOR_ACCENT)
            
    # System bar pill
    draw.rectangle((0, H - 25, W, H), fill=(20, 19, 25))
    draw.rounded_rectangle((W//2 - 60, H - 15, W//2 + 60, H - 9), radius=3, fill=(100, 100, 110))

# -------------------------------------------------------------
# Rich Thumbnail Generators (16:9 ratio, 325 x 183 px)
# -------------------------------------------------------------
def create_gaming_thumb(w=325, h=183):
    thumb = Image.new("RGBA", (w, h), (15, 12, 35, 255))
    d = ImageDraw.Draw(thumb)
    # Background neon mesh
    for y in range(h):
        r = int(25 + 50 * (y / h))
        g = int(10 + 30 * (1 - y / h))
        b = int(70 + 80 * (y / h))
        d.line((0, y, w, y), fill=(r, g, b, 255))
    # Tech lines
    d.polygon([(w - 120, 0), (w, 0), (w, h), (w - 60, h)], fill=(40, 20, 90, 200))
    d.line((w - 120, 0, w - 60, h), fill=(0, 240, 255), width=3)
    # Text
    d.text((15, 20), "CYBERPUNK", fill=(255, 220, 0), font=FONT_BEBAS_LG)
    d.text((15, 65), "RAY TRACING 4K", fill=(255, 255, 255), font=FONT_BEBAS_MD)
    # Badge
    d.rounded_rectangle((15, 130, 95, 160), radius=6, fill=(255, 0, 85))
    d.text((25, 134), "60 FPS", fill=(255, 255, 255), font=FONT_BEBAS_SM)
    # Time badge
    d.rounded_rectangle((w - 70, h - 35, w - 10, h - 10), radius=4, fill=(0, 0, 0, 200))
    d.text((w - 62, h - 32), "14:28", fill=(255, 255, 255), font=FONT_SM)
    return thumb

def create_fitness_thumb(w=325, h=183):
    thumb = Image.new("RGBA", (w, h), (30, 25, 20, 255))
    d = ImageDraw.Draw(thumb)
    for y in range(h):
        r = int(80 + 120 * (1 - y / h))
        g = int(35 + 40 * (y / h))
        b = int(10 + 10 * (y / h))
        d.line((0, y, w, y), fill=(r, g, b, 255))
    # Diagonal energy stripe
    d.polygon([(0, 0), (80, 0), (140, h), (0, h)], fill=(255, 80, 0, 180))
    d.text((15, 18), "10-MIN HIIT", fill=(255, 255, 255), font=FONT_BEBAS_LG)
    d.text((15, 65), "BURN FAT FAST", fill=(255, 220, 0), font=FONT_BEBAS_MD)
    # Badge
    d.rounded_rectangle((15, 130, 120, 160), radius=6, fill=(0, 0, 0, 200))
    d.text((22, 134), "NO EQUIPMENT", fill=(0, 255, 180), font=FONT_BEBAS_SM)
    # Time badge
    d.rounded_rectangle((w - 70, h - 35, w - 10, h - 10), radius=4, fill=(0, 0, 0, 200))
    d.text((w - 62, h - 32), "10:00", fill=(255, 255, 255), font=FONT_SM)
    return thumb

def create_growth_thumb(w=325, h=183):
    thumb = Image.new("RGBA", (w, h), (15, 23, 42, 255))
    d = ImageDraw.Draw(thumb)
    for y in range(h):
        r = int(15 + 20 * (y / h))
        g = int(30 + 60 * (y / h))
        b = int(60 + 90 * (y / h))
        d.line((0, y, w, y), fill=(r, g, b, 255))
    # Upward green growth chart line
    points = [(20, 140), (80, 125), (150, 95), (220, 60), (300, 25)]
    d.line(points, fill=(16, 185, 129), width=5)
    for p in points:
        d.ellipse((p[0]-6, p[1]-6, p[0]+6, p[1]+6), fill=(52, 211, 153), outline=(255, 255, 255), width=2)
    d.text((15, 18), "0 TO 100K", fill=(255, 255, 255), font=FONT_BEBAS_LG)
    d.text((15, 65), "SUBSCRIBERS", fill=(239, 68, 68), font=FONT_BEBAS_MD)
    # Badge
    d.rounded_rectangle((15, 130, 110, 160), radius=6, fill=(16, 185, 129))
    d.text((22, 134), "+340% GROWTH", fill=(255, 255, 255), font=FONT_BEBAS_SM)
    d.rounded_rectangle((w - 70, h - 35, w - 10, h - 10), radius=4, fill=(0, 0, 0, 200))
    d.text((w - 62, h - 32), "18:45", fill=(255, 255, 255), font=FONT_SM)
    return thumb

def create_podcast_thumb(w=325, h=183):
    thumb = Image.new("RGBA", (w, h), (20, 15, 30, 255))
    d = ImageDraw.Draw(thumb)
    for y in range(h):
        r = int(40 + 70 * (1 - y / h))
        g = int(20 + 30 * (y / h))
        b = int(60 + 80 * (y / h))
        d.line((0, y, w, y), fill=(r, g, b, 255))
    # Soundwave bars
    for i, bh in enumerate([30, 55, 80, 45, 95, 110, 75, 40, 90, 60, 30]):
        bx = w - 140 + i * 11
        d.rounded_rectangle((bx, 90 - bh//2, bx + 6, 90 + bh//2), radius=3, fill=(168, 85, 247))
    d.text((15, 18), "THE FUTURE", fill=(255, 255, 255), font=FONT_BEBAS_LG)
    d.text((15, 65), "OF CREATIVE AI", fill=(192, 132, 252), font=FONT_BEBAS_MD)
    d.rounded_rectangle((15, 130, 95, 160), radius=6, fill=(147, 51, 234))
    d.text((22, 134), "EPISODE 42", fill=(255, 255, 255), font=FONT_BEBAS_SM)
    d.rounded_rectangle((w - 70, h - 35, w - 10, h - 10), radius=4, fill=(0, 0, 0, 200))
    d.text((w - 62, h - 32), "45:12", fill=(255, 255, 255), font=FONT_SM)
    return thumb

def create_cinematic_thumb(w=325, h=183):
    thumb = Image.new("RGBA", (w, h), (10, 15, 25, 255))
    d = ImageDraw.Draw(thumb)
    for y in range(h):
        r = int(10 + 30 * (y / h))
        g = int(20 + 40 * (y / h))
        b = int(40 + 70 * (y / h))
        d.line((0, y, w, y), fill=(r, g, b, 255))
    # Bokeh circles
    d.ellipse((w - 110, 20, w - 30, 100), fill=(255, 180, 0, 50))
    d.ellipse((w - 80, 60, w - 10, 130), fill=(0, 200, 255, 40))
    d.text((15, 18), "CINEMATIC", fill=(255, 255, 255), font=FONT_BEBAS_LG)
    d.text((15, 65), "COLOR GRADING", fill=(56, 189, 248), font=FONT_BEBAS_MD)
    d.rounded_rectangle((15, 130, 80, 160), radius=6, fill=(14, 165, 233))
    d.text((25, 134), "4K HDR", fill=(255, 255, 255), font=FONT_BEBAS_SM)
    d.rounded_rectangle((w - 70, h - 35, w - 10, h - 10), radius=4, fill=(0, 0, 0, 200))
    d.text((w - 62, h - 32), "22:10", fill=(255, 255, 255), font=FONT_SM)
    return thumb

def create_car_thumb(w=325, h=183):
    thumb = Image.new("RGBA", (w, h), (20, 20, 25, 255))
    d = ImageDraw.Draw(thumb)
    for y in range(h):
        r = int(30 + 40 * (1 - y / h))
        g = int(25 + 30 * (1 - y / h))
        b = int(35 + 40 * (y / h))
        d.line((0, y, w, y), fill=(r, g, b, 255))
    # Speed light trails
    d.line((0, 120, w, 60), fill=(239, 68, 68), width=4)
    d.line((0, 135, w, 80), fill=(245, 158, 11), width=3)
    d.text((15, 18), "TESLA PLAID", fill=(255, 255, 255), font=FONT_BEBAS_LG)
    d.text((15, 65), "0-60 MPH LAUNCH", fill=(239, 68, 68), font=FONT_BEBAS_MD)
    d.rounded_rectangle((15, 130, 100, 160), radius=6, fill=(220, 38, 38))
    d.text((22, 134), "1.99 SECONDS", fill=(255, 255, 255), font=FONT_BEBAS_SM)
    d.rounded_rectangle((w - 70, h - 35, w - 10, h - 10), radius=4, fill=(0, 0, 0, 200))
    d.text((w - 62, h - 32), "12:05", fill=(255, 255, 255), font=FONT_SM)
    return thumb


# =============================================================
# 1. SCREEN: Hero App Feed (Home Screen - Exact App Structure, NO ADS)
# =============================================================
def make_hero_feed():
    img = Image.new("RGBA", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Top Bar: Background #2F2D3A (height 125px)
    draw.rectangle((0, 0, W, 125), fill=COLOR_BAR)
    draw.line((0, 125, W, 125), fill=COLOR_BAR_BORDER, width=2)
    draw_status_bar(draw, dark=False)
    
    # Header Icons & Title
    # Left: info icon
    info_icon = load_app_drawable("info.png", (38, 38))
    if info_icon:
        img.paste(info_icon, (24, 65), info_icon)
        
    # Center: "Thumbnail Maker"
    draw.text((W//2 - 120, 66), "Thumbnail Maker", fill=COLOR_TEXT, font=FONT_TITLE)
    
    # Right: PRO Crown icon
    pro_icon = load_app_drawable("pro_ic.png", (46, 38))
    if pro_icon:
        img.paste(pro_icon, (W - 70, 65), pro_icon)
        
    # ---------------------------------------------------------
    # NO BANNER ADS! Social Presets Strip sits right below header!
    # ---------------------------------------------------------
    strip_y = 145
    cards = [
        ("f_cover.png", "Facebook Cover"),
        ("y_cover.png", "YouTube Cover"),
        ("ad_logo.png", "Logo Maker"),
        ("fb_in_post.png", "Instagram Post"),
        ("w_cover.png", "Twitter Header")
    ]
    card_w, card_h = 125, 140
    for idx, (cfile, clabel) in enumerate(cards):
        cx = 20 + idx * (card_w + 14)
        cimg = load_app_drawable(cfile, (card_w, card_h))
        if cimg and cx < W:
            img.paste(cimg, (cx, strip_y), cimg)
            
    # ---------------------------------------------------------
    # Category Tabs Bar (Height 55px, at y = 305)
    # ---------------------------------------------------------
    tabs_y = 305
    draw.rectangle((0, tabs_y, W, tabs_y + 55), fill=COLOR_BAR)
    draw.line((0, tabs_y + 55, W, tabs_y + 55), fill=COLOR_BAR_BORDER, width=1)
    
    cat_tabs = ["FITNESS", "GAMING", "MIX", "ART", "AUTOMOBILE"]
    tab_spacing = W // len(cat_tabs)
    for idx, tab_name in enumerate(cat_tabs):
        tx = idx * tab_spacing + tab_spacing // 2
        is_active = (idx == 1) # GAMING active
        t_color = COLOR_TEXT if is_active else COLOR_TEXT_MUTED
        draw.text((tx - len(tab_name)*5, tabs_y + 16), tab_name, fill=t_color, font=FONT_SMB)
        if is_active:
            # Cyan indicator line
            draw.rectangle((tx - 32, tabs_y + 50, tx + 32, tabs_y + 54), fill=COLOR_ACCENT)
            
    # ---------------------------------------------------------
    # 2-Column Grid of 16:9 Thumbnail Cards (at y = 380)
    # ---------------------------------------------------------
    grid_y = 380
    cw, ch = 325, 183
    grid_items = [
        create_gaming_thumb(cw, ch),
        create_fitness_thumb(cw, ch),
        create_growth_thumb(cw, ch),
        create_podcast_thumb(cw, ch),
        create_cinematic_thumb(cw, ch),
        create_car_thumb(cw, ch)
    ]
    
    for idx, gthumb in enumerate(grid_items):
        col = idx % 2
        row = idx // 2
        gx = 22 + col * (cw + 26)
        gy = grid_y + row * (ch + 115)
        
        if gy + ch > H - 130:
            break
            
        # Draw Card Container with subtle drop shadow
        draw.rounded_rectangle((gx - 4, gy - 4, gx + cw + 4, gy + ch + 90), radius=14, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=1)
        
        # Paste 16:9 thumbnail
        # Create mask with rounded top corners
        mask = Image.new("L", (cw, ch), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle((0, 0, cw, ch), radius=10, fill=255)
        img.paste(gthumb, (gx, gy), mask)
        
        # Card meta info below thumbnail
        if idx == 0:
            draw.text((gx + 10, gy + ch + 12), "Cyberpunk Pro Streamer 4K", fill=COLOR_TEXT, font=FONT_SMB)
            draw.text((gx + 10, gy + ch + 38), "1280x720 HD • 42.5K views", fill=COLOR_TEXT_MUTED, font=FONT_SM)
        elif idx == 1:
            draw.text((gx + 10, gy + ch + 12), "10-Min HIIT Body Blast", fill=COLOR_TEXT, font=FONT_SMB)
            draw.text((gx + 10, gy + ch + 38), "1280x720 HD • 89.1K views", fill=COLOR_TEXT_MUTED, font=FONT_SM)
        elif idx == 2:
            draw.text((gx + 10, gy + ch + 12), "0 to 100K YouTube Strategy", fill=COLOR_TEXT, font=FONT_SMB)
            draw.text((gx + 10, gy + ch + 38), "1280x720 HD • 115K views", fill=COLOR_TEXT_MUTED, font=FONT_SM)
        elif idx == 3:
            draw.text((gx + 10, gy + ch + 12), "Future of AI Podcast #42", fill=COLOR_TEXT, font=FONT_SMB)
            draw.text((gx + 10, gy + ch + 38), "1280x720 HD • 34.2K views", fill=COLOR_TEXT_MUTED, font=FONT_SM)
        elif idx == 4:
            draw.text((gx + 10, gy + ch + 12), "Cinematic Color Masterclass", fill=COLOR_TEXT, font=FONT_SMB)
            draw.text((gx + 10, gy + ch + 38), "1280x720 HD • 58.7K views", fill=COLOR_TEXT_MUTED, font=FONT_SM)
        elif idx == 5:
            draw.text((gx + 10, gy + ch + 12), "Tesla Model S Plaid Speed", fill=COLOR_TEXT, font=FONT_SMB)
            draw.text((gx + 10, gy + ch + 38), "1280x720 HD • 91.3K views", fill=COLOR_TEXT_MUTED, font=FONT_SM)
            
        # PRO Badge or Edit button
        draw.rounded_rectangle((gx + cw - 65, gy + ch + 52, gx + cw - 10, gy + ch + 78), radius=6, fill=COLOR_ACCENT)
        draw.text((gx + cw - 52, gy + ch + 56), "EDIT", fill=(255, 255, 255), font=FONT_SM)

    # Bottom Navigation Dock
    draw_bottom_dock(img, draw, active_idx=0)
    return img


# =============================================================
# 2. SCREEN: Templates Category Screen (Youtube Cover Browser)
# =============================================================
def make_templates_screen():
    img = Image.new("RGBA", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Top Bar: Background #2F2D3A (height 125px)
    draw.rectangle((0, 0, W, 125), fill=COLOR_BAR)
    draw.line((0, 125, W, 125), fill=COLOR_BAR_BORDER, width=2)
    draw_status_bar(draw, dark=False)
    
    # Left: Back arrow
    draw.polygon([(40, 84), (55, 72), (55, 96)], fill=COLOR_TEXT)
    draw.line((45, 84, 70, 84), fill=COLOR_TEXT, width=4)
    
    # Center: Title "Youtube Cover"
    draw.text((95, 68), "Youtube Cover", fill=COLOR_TEXT, font=FONT_TITLE)
    
    # Right: Search & PRO
    # Search icon
    draw.ellipse((W - 120, 72, W - 102, 90), outline=COLOR_TEXT, width=2)
    draw.line((W - 106, 86, W - 98, 94), fill=COLOR_TEXT, width=3)
    # PRO Crown icon
    pro_icon = load_app_drawable("pro_ic.png", (46, 38))
    if pro_icon:
        img.paste(pro_icon, (W - 70, 65), pro_icon)
        
    # Category Sub-tabs (Fitness, Business, Fashion, Food, Summer, Gaming)
    tabs_y = 135
    draw.rectangle((0, tabs_y, W, tabs_y + 60), fill=COLOR_BAR)
    draw.line((0, tabs_y + 60, W, tabs_y + 60), fill=COLOR_BAR_BORDER, width=1)
    
    sub_tabs = ["Fitness", "Business", "Fashion", "Food", "Summer"]
    tab_spacing = W // len(sub_tabs)
    for idx, tab_name in enumerate(sub_tabs):
        tx = idx * tab_spacing + tab_spacing // 2
        is_active = (idx == 0) # Fitness active
        t_color = COLOR_TEXT if is_active else COLOR_TEXT_MUTED
        draw.text((tx - len(tab_name)*5, tabs_y + 18), tab_name, fill=t_color, font=FONT_SMB)
        if is_active:
            draw.rectangle((tx - 28, tabs_y + 54, tx + 28, tabs_y + 58), fill=COLOR_ACCENT)
            
    # 2-Column Grid of Youtube Cover Templates (aspect ratio 16:9)
    grid_y = 215
    cw, ch = 325, 183
    grid_items = [
        create_fitness_thumb(cw, ch),
        create_growth_thumb(cw, ch),
        create_gaming_thumb(cw, ch),
        create_podcast_thumb(cw, ch),
        create_cinematic_thumb(cw, ch),
        create_car_thumb(cw, ch)
    ]
    
    for idx, gthumb in enumerate(grid_items):
        col = idx % 2
        row = idx // 2
        gx = 22 + col * (cw + 26)
        gy = grid_y + row * (ch + 115)
        
        if gy + ch > H - 130:
            break
            
        draw.rounded_rectangle((gx - 4, gy - 4, gx + cw + 4, gy + ch + 90), radius=14, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=1)
        
        mask = Image.new("L", (cw, ch), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle((0, 0, cw, ch), radius=10, fill=255)
        img.paste(gthumb, (gx, gy), mask)
        
        # Meta info
        labels = [
            ("Daily Fitness Routine", "High Energy • 1080p HD"),
            ("Business Growth Pitch", "Investor Ready • Pro"),
            ("Esports Tournament 2026", "Twitch / YT Banner"),
            ("Tech & AI Insights", "Podcast Series Cover"),
            ("Filmmaking Secrets", "Cinematic Preset"),
            ("Hypercar Track Day", "Automobile Feature")
        ]
        title, sub = labels[idx]
        draw.text((gx + 10, gy + ch + 12), title, fill=COLOR_TEXT, font=FONT_SMB)
        draw.text((gx + 10, gy + ch + 38), sub, fill=COLOR_TEXT_MUTED, font=FONT_SM)
        
        # Action button: "USE TEMPLATE"
        draw.rounded_rectangle((gx + cw - 120, gy + ch + 52, gx + cw - 10, gy + ch + 78), radius=6, fill=COLOR_ACCENT)
        draw.text((gx + cw - 110, gy + ch + 56), "USE TEMPLATE", fill=(255, 255, 255), font=FONT_SM)

    # Bottom Navigation Dock
    draw_bottom_dock(img, draw, active_idx=1)
    return img


# =============================================================
# 3. SCREEN: Multi-Layer Studio Editor (activity_poster.xml)
# =============================================================
def make_editor_screen():
    img = Image.new("RGBA", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Top Bar: Background #2F2D3A (height 125px)
    draw.rectangle((0, 0, W, 125), fill=COLOR_BAR)
    draw.line((0, 125, W, 125), fill=COLOR_BAR_BORDER, width=2)
    draw_status_bar(draw, dark=False)
    
    # Left: Back arrow and "Editor"
    draw.polygon([(35, 84), (50, 72), (50, 96)], fill=COLOR_TEXT)
    draw.line((40, 84, 65, 84), fill=COLOR_TEXT, width=4)
    draw.text((85, 68), "Editor", fill=COLOR_TEXT, font=FONT_TITLE)
    
    # Right: Add layer '+', Save '💾', Overflow '⋮'
    # '+' icon
    draw.line((W - 170, 84, W - 146, 84), fill=COLOR_TEXT, width=4)
    draw.line((W - 158, 72, W - 158, 96), fill=COLOR_TEXT, width=4)
    
    # Save icon (ic_save.png)
    save_icon = load_app_drawable("ic_save.png", (38, 38))
    if save_icon:
        img.paste(save_icon, (W - 125, 66), save_icon)
    else:
        draw.rectangle((W - 125, 68, W - 95, 98), outline=COLOR_TEXT, width=2)
        
    # Overflow menu '⋮'
    for my in [74, 84, 94]:
        draw.ellipse((W - 60, my - 2, W - 56, my + 2), fill=COLOR_TEXT)
        
    # Quick Tool Strip: Background #282733 (height 65px)
    tools_y = 135
    draw.rectangle((0, tools_y, W, tools_y + 65), fill=(40, 39, 50))
    draw.line((0, tools_y + 65, W, tools_y + 65), fill=COLOR_BAR_BORDER, width=1)
    
    # Undo icon
    undo_icon = load_app_drawable("ic_undo_1.png", (32, 32))
    if undo_icon:
        img.paste(undo_icon, (45, tools_y + 16), undo_icon)
        
    # Redo icon
    redo_icon = load_app_drawable("ic_redo_1.png", (32, 32))
    if redo_icon:
        img.paste(redo_icon, (115, tools_y + 16), redo_icon)
        
    # Zoom icon
    zoom_icon = load_app_drawable("ic_zoom.png", (32, 32))
    if zoom_icon:
        img.paste(zoom_icon, (185, tools_y + 16), zoom_icon)
        
    # Snap Grid icon
    draw.rectangle((260, tools_y + 18, 290, tools_y + 48), outline=COLOR_TEXT_MUTED, width=2)
    draw.line((275, tools_y + 18, 275, tools_y + 48), fill=COLOR_TEXT_MUTED, width=1)
    draw.line((260, tools_y + 33, 290, tools_y + 33), fill=COLOR_TEXT_MUTED, width=1)
    
    # Layers stack icon
    draw.polygon([(335, tools_y + 20), (355, tools_y + 12), (375, tools_y + 20), (355, tools_y + 28)], fill=COLOR_TEXT_MUTED)
    draw.polygon([(335, tools_y + 30), (355, tools_y + 22), (375, tools_y + 30), (355, tools_y + 38)], fill=COLOR_TEXT_MUTED)
    
    # Layer Count Badge
    draw.rounded_rectangle((W - 145, tools_y + 16, W - 35, tools_y + 50), radius=17, fill=COLOR_CARD_BG, outline=COLOR_ACCENT, width=1)
    draw.text((W - 130, tools_y + 22), "4 LAYERS", fill=COLOR_ACCENT, font=FONT_SMB)

    # ---------------------------------------------------------
    # MAIN CANVAS (16:9 Aspect Ratio: 660 x 372 px)
    # ---------------------------------------------------------
    canv_w, canv_h = 660, 372
    canv_x = (W - canv_w) // 2
    canv_y = 240
    
    # Canvas drop shadow
    draw.rounded_rectangle((canv_x - 4, canv_y - 4, canv_x + canv_w + 4, canv_y + canv_h + 4), radius=16, fill=(15, 14, 20))
    
    # Inside Canvas: High-Energy Gaming Thumbnail
    canvas_img = Image.new("RGBA", (canv_w, canv_h), (12, 10, 25, 255))
    cd = ImageDraw.Draw(canvas_img)
    # Neon background
    for cy in range(canv_h):
        r = int(20 + 70 * (cy / canv_h))
        g = int(10 + 20 * (1 - cy / canv_h))
        b = int(50 + 110 * (cy / canv_h))
        cd.line((0, cy, canv_w, cy), fill=(r, g, b, 255))
    # Angular laser lines
    cd.polygon([(canv_w - 240, 0), (canv_w, 0), (canv_w, canv_h), (canv_w - 120, canv_h)], fill=(60, 25, 120, 210))
    cd.line((canv_w - 240, 0, canv_w - 120, canv_h), fill=(0, 240, 255), width=4)
    cd.line((canv_w - 280, 0, canv_w - 160, canv_h), fill=(255, 0, 128), width=3)
    
    # Paste Creator Cutout on Right
    creator_path = "assets/images/creator-cutout.png"
    if os.path.exists(creator_path):
        c_cutout = Image.open(creator_path).convert("RGBA").resize((270, 338))
        canvas_img.paste(c_cutout, (canv_w - 260, canv_h - 338), c_cutout)
        
    # Bold 3D Text on Left
    cd.text((32, 45), "APEX HERO", fill=(0, 0, 0), font=FONT_BEBAS_XL) # shadow
    cd.text((30, 42), "APEX HERO", fill=(255, 220, 0), font=FONT_BEBAS_XL)
    
    cd.text((32, 102), "ROAD TO PREDATOR", fill=(0, 0, 0), font=FONT_BEBAS_LG)
    cd.text((30, 100), "ROAD TO PREDATOR", fill=(255, 255, 255), font=FONT_BEBAS_LG)
    
    # 4K & 60FPS Badges
    cd.rounded_rectangle((30, 290, 120, 335), radius=8, fill=(255, 0, 85))
    cd.text((45, 297), "4K 60FPS", fill=(255, 255, 255), font=FONT_BEBAS_SM)
    
    cd.rounded_rectangle((135, 290, 240, 335), radius=8, fill=(0, 209, 143))
    cd.text((148, 297), "SOLO QUEUE", fill=(255, 255, 255), font=FONT_BEBAS_SM)
    
    # Active selected bounding box around "APEX HERO"
    box_x1, box_y1 = 20, 30
    box_x2, box_y2 = 300, 95
    # Dashed cyan line
    for dx in range(box_x1, box_x2, 12):
        cd.line((dx, box_y1, min(dx + 6, box_x2), box_y1), fill=COLOR_ACCENT, width=2)
        cd.line((dx, box_y2, min(dx + 6, box_x2), box_y2), fill=COLOR_ACCENT, width=2)
    for dy in range(box_y1, box_y2, 12):
        cd.line((box_x1, dy, box_x1, min(dy + 6, box_y2)), fill=COLOR_ACCENT, width=2)
        cd.line((box_x2, dy, box_x2, min(dy + 6, box_y2)), fill=COLOR_ACCENT, width=2)
        
    # Corner Handles
    cd.ellipse((box_x1 - 8, box_y1 - 8, box_x1 + 8, box_y1 + 8), fill=(239, 68, 68), outline=(255, 255, 255), width=2) # Delete
    cd.ellipse((box_x2 - 8, box_y1 - 8, box_x2 + 8, box_y1 + 8), fill=COLOR_ACCENT, outline=(255, 255, 255), width=2) # Rotate
    cd.ellipse((box_x2 - 8, box_y2 - 8, box_x2 + 8, box_y2 + 8), fill=COLOR_ACCENT, outline=(255, 255, 255), width=2) # Scale
    cd.ellipse((box_x1 - 8, box_y2 - 8, box_x1 + 8, box_y2 + 8), fill=(245, 158, 11), outline=(255, 255, 255), width=2) # Lock
    
    # Paste Canvas onto Screen
    mask_c = Image.new("L", (canv_w, canv_h), 0)
    mdraw_c = ImageDraw.Draw(mask_c)
    mdraw_c.rounded_rectangle((0, 0, canv_w, canv_h), radius=14, fill=255)
    img.paste(canvas_img, (canv_x, canv_y), mask_c)
    
    # ---------------------------------------------------------
    # Floating Layer Inspector Card (below canvas)
    # ---------------------------------------------------------
    insp_y = canv_y + canv_h + 25
    draw.rounded_rectangle((canv_x, insp_y, canv_x + canv_w, insp_y + 110), radius=16, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=1)
    draw.text((canv_x + 20, insp_y + 18), "Active Text Layer: APEX HERO", fill=COLOR_TEXT, font=FONT_SMB)
    draw.text((canv_x + 20, insp_y + 44), "Font: Bebas Neue • Size: 48 • Stroke: 4px Cyan", fill=COLOR_TEXT_MUTED, font=FONT_SM)
    
    # Quick sliders: Opacity & Shadow
    draw.text((canv_x + 20, insp_y + 72), "Opacity", fill=COLOR_TEXT_MUTED, font=FONT_SM)
    draw.rounded_rectangle((canv_x + 90, insp_y + 78, canv_x + 290, insp_y + 86), radius=4, fill=(60, 58, 75))
    draw.rounded_rectangle((canv_x + 90, insp_y + 78, canv_x + 270, insp_y + 86), radius=4, fill=COLOR_ACCENT)
    draw.ellipse((canv_x + 265, insp_y + 73, canv_x + 279, insp_y + 91), fill=(255, 255, 255))
    draw.text((canv_x + 305, insp_y + 72), "100%", fill=COLOR_TEXT, font=FONT_SM)
    
    draw.text((canv_x + 370, insp_y + 72), "Shadow", fill=COLOR_TEXT_MUTED, font=FONT_SM)
    draw.rounded_rectangle((canv_x + 445, insp_y + 78, canv_x + 580, insp_y + 86), radius=4, fill=(60, 58, 75))
    draw.rounded_rectangle((canv_x + 445, insp_y + 78, canv_x + 540, insp_y + 86), radius=4, fill=COLOR_ACCENT)
    draw.ellipse((canv_x + 535, insp_y + 73, canv_x + 549, insp_y + 91), fill=(255, 255, 255))
    draw.text((canv_x + 595, insp_y + 72), "+8", fill=COLOR_TEXT, font=FONT_SM)

    # ---------------------------------------------------------
    # Bottom Editing Toolbar (5 Tools: Text, Sticker, Image, Effect, Background)
    # ---------------------------------------------------------
    nav_h = 115
    nav_y = H - nav_h - 25
    draw.rectangle((0, nav_y, W, nav_y + nav_h), fill=COLOR_BAR)
    draw.line((0, nav_y, W, nav_y), fill=COLOR_BAR_BORDER, width=2)
    
    tools = [
        ("btn_text.png", "Text"),
        ("btn_sticker.png", "Sticker"),
        ("btn_image.png", "Image"),
        ("btn_effect.png", "Effect"),
        ("btn_background.png", "Background")
    ]
    tool_w = W // len(tools)
    for idx, (tfile, tlabel) in enumerate(tools):
        cx = idx * tool_w + tool_w // 2
        is_active = (idx == 0) # Text active
        timg = load_app_drawable(tfile, (42, 42))
        if timg:
            img.paste(timg, (cx - 21, nav_y + 16), timg)
        else:
            draw.rectangle((cx - 18, nav_y + 16, cx + 18, nav_y + 52), fill=COLOR_ACCENT if is_active else COLOR_TEXT_MUTED)
        t_color = COLOR_ACCENT if is_active else COLOR_TEXT_MUTED
        draw.text((cx - len(tlabel)*4 - 4, nav_y + 68), tlabel, fill=t_color, font=FONT_SMB)
        if is_active:
            draw.rounded_rectangle((cx - 20, nav_y + 96, cx + 20, nav_y + 100), radius=2, fill=COLOR_ACCENT)
            
    # System bar pill
    draw.rectangle((0, H - 25, W, H), fill=(20, 19, 25))
    draw.rounded_rectangle((W//2 - 60, H - 15, W//2 + 60, H - 9), radius=3, fill=(100, 100, 110))
    return img


# =============================================================
# 4. SCREEN: 1-Tap Cutout & Background Eraser (activity_eraser.xml)
# =============================================================
def make_cutout_screen():
    img = Image.new("RGBA", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Top Bar: Background #2F2D3A (height 125px)
    draw.rectangle((0, 0, W, 125), fill=COLOR_BAR)
    draw.line((0, 125, W, 125), fill=COLOR_BAR_BORDER, width=2)
    draw_status_bar(draw, dark=False)
    
    # Left: Back arrow
    draw.polygon([(40, 84), (55, 72), (55, 96)], fill=COLOR_TEXT)
    draw.line((45, 84, 70, 84), fill=COLOR_TEXT, width=4)
    
    # Center: "Cut Photo"
    draw.text((95, 68), "Cut Photo", fill=COLOR_TEXT, font=FONT_TITLE)
    
    # Right: Save / Download Icon
    draw.rounded_rectangle((W - 85, 64, W - 30, 102), radius=10, fill=COLOR_ACCENT)
    # Down arrow download symbol
    draw.line((W - 58, 74, W - 58, 90), fill=(255, 255, 255), width=3)
    draw.polygon([(W - 65, 86), (W - 58, 94), (W - 51, 86)], fill=(255, 255, 255))
    
    # ---------------------------------------------------------
    # MAIN WORKSPACE CANVAS (Checkerboard Transparency)
    # ---------------------------------------------------------
    canv_y = 135
    canv_h = 880
    
    # Draw Checkerboard Pattern
    sq_size = 24
    for cy in range(canv_y, canv_y + canv_h, sq_size):
        for cx in range(0, W, sq_size):
            is_dark = ((cx // sq_size) + (cy // sq_size)) % 2 == 0
            sq_color = (42, 40, 52) if is_dark else (55, 52, 68)
            draw.rectangle((cx, cy, min(cx + sq_size, W), min(cy + sq_size, canv_y + canv_h)), fill=sq_color)
            
    # Paste Subject Cutout
    creator_path = "assets/images/creator-cutout.png"
    if os.path.exists(creator_path):
        c_cutout = Image.open(creator_path).convert("RGBA").resize((440, 550))
        img.paste(c_cutout, (W//2 - 220, canv_y + 120), c_cutout)
        
    # Offset Cursor Brush Mechanism (Exact App Offset Feature)
    # Red Touch circle (where user places finger)
    finger_x, finger_y = 440, canv_y + 580
    draw.ellipse((finger_x - 30, finger_y - 30, finger_x + 30, finger_y + 30), outline=(239, 68, 68), width=3)
    draw.ellipse((finger_x - 6, finger_y - 6, finger_x + 6, finger_y + 6), fill=(239, 68, 68))
    draw.text((finger_x + 38, finger_y - 10), "Touch Point", fill=(255, 255, 255), font=FONT_SMB)
    
    # Offset dashed line going up 150px
    brush_x, brush_y = finger_x, finger_y - 150
    for dy in range(brush_y + 15, finger_y - 15, 10):
        draw.line((finger_x, dy, finger_x, dy + 5), fill=COLOR_ACCENT, width=2)
        
    # Eraser Brush Circle + Crosshair (Offset position)
    draw.ellipse((brush_x - 35, brush_y - 35, brush_x + 35, brush_y + 35), outline=COLOR_ACCENT, width=3)
    draw.line((brush_x - 45, brush_y, brush_x + 45, brush_y), fill=COLOR_ACCENT, width=2)
    draw.line((brush_x, brush_y - 45, brush_x, brush_y + 45), fill=COLOR_ACCENT, width=2)
    draw.text((brush_x + 42, brush_y - 10), "Offset Eraser (150px)", fill=COLOR_ACCENT, font=FONT_SMB)

    # ---------------------------------------------------------
    # Adjustment Sliders Panel (Offset & Threshold Seekbars)
    # ---------------------------------------------------------
    panel_y = canv_y + canv_h + 15
    draw.rounded_rectangle((20, panel_y, W - 20, panel_y + 160), radius=16, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=1)
    
    # Offset seekbar
    draw.text((45, panel_y + 22), "OFFSET", fill=COLOR_TEXT, font=FONT_SMB)
    draw.rounded_rectangle((150, panel_y + 30, W - 120, panel_y + 38), radius=4, fill=(60, 58, 75))
    draw.rounded_rectangle((150, panel_y + 30, 150 + int((W - 270) * 0.5), panel_y + 38), radius=4, fill=COLOR_ACCENT)
    thumb_x = 150 + int((W - 270) * 0.5)
    draw.ellipse((thumb_x - 12, panel_y + 22, thumb_x + 12, panel_y + 46), fill=(255, 255, 255), outline=COLOR_ACCENT, width=3)
    draw.text((W - 90, panel_y + 22), "150", fill=COLOR_ACCENT, font=FONT_SMB)
    
    # Threshold seekbar
    draw.text((45, panel_y + 92), "THRESHOLD", fill=COLOR_TEXT, font=FONT_SMB)
    draw.rounded_rectangle((150, panel_y + 100, W - 120, panel_y + 108), radius=4, fill=(60, 58, 75))
    draw.rounded_rectangle((150, panel_y + 100, 150 + int((W - 270) * 0.65), panel_y + 108), radius=4, fill=COLOR_ACCENT)
    thumb_x2 = 150 + int((W - 270) * 0.65)
    draw.ellipse((thumb_x2 - 12, panel_y + 92, thumb_x2 + 12, panel_y + 116), fill=(255, 255, 255), outline=COLOR_ACCENT, width=3)
    draw.text((W - 90, panel_y + 92), "52", fill=COLOR_ACCENT, font=FONT_SMB)

    # ---------------------------------------------------------
    # Bottom Cutout Toolbar (5 Modes: Auto, Lasso, Erase, Restore, Zoom)
    # ---------------------------------------------------------
    nav_h = 115
    nav_y = H - nav_h - 25
    draw.rectangle((0, nav_y, W, nav_y + nav_h), fill=COLOR_BAR)
    draw.line((0, nav_y, W, nav_y), fill=COLOR_BAR_BORDER, width=2)
    
    tools = [
        ("ic_slated_auto.png", "Auto"),
        ("ic_slated_extract.png", "Lasso"),
        ("ic_slated_manual.png", "Erase"),
        ("ic_slated_restore.png", "Restore"),
        ("ic_slated_zoom.png", "Zoom")
    ]
    tool_w = W // len(tools)
    for idx, (tfile, tlabel) in enumerate(tools):
        cx = idx * tool_w + tool_w // 2
        is_active = (idx == 0) # Auto active
        timg = load_app_drawable(tfile, (42, 42))
        if timg:
            img.paste(timg, (cx - 21, nav_y + 16), timg)
        else:
            draw.rectangle((cx - 18, nav_y + 16, cx + 18, nav_y + 52), fill=COLOR_ACCENT if is_active else COLOR_TEXT_MUTED)
        t_color = COLOR_ACCENT if is_active else COLOR_TEXT_MUTED
        draw.text((cx - len(tlabel)*4 - 4, nav_y + 68), tlabel, fill=t_color, font=FONT_SMB)
        if is_active:
            draw.rounded_rectangle((cx - 20, nav_y + 96, cx + 20, nav_y + 100), radius=2, fill=COLOR_ACCENT)
            
    # System bar pill
    draw.rectangle((0, H - 25, W, H), fill=(20, 19, 25))
    draw.rounded_rectangle((W//2 - 60, H - 15, W//2 + 60, H - 9), radius=3, fill=(100, 100, 110))
    return img


# =============================================================
# 5. SCREEN: 1-Tap Save & Export Ready for YouTube Studio
# =============================================================
def make_export_screen():
    img = Image.new("RGBA", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Top Bar: Background #2F2D3A (height 125px)
    draw.rectangle((0, 0, W, 125), fill=COLOR_BAR)
    draw.line((0, 125, W, 125), fill=COLOR_BAR_BORDER, width=2)
    draw_status_bar(draw, dark=False)
    
    # Left: Back arrow
    draw.polygon([(40, 84), (55, 72), (55, 96)], fill=COLOR_TEXT)
    draw.line((45, 84, 70, 84), fill=COLOR_TEXT, width=4)
    
    # Center: "Thumbnail Saved"
    draw.text((95, 68), "Thumbnail Saved", fill=COLOR_TEXT, font=FONT_TITLE)
    
    # Right: Share icon
    draw.ellipse((W - 68, 70, W - 48, 90), outline=COLOR_TEXT, width=2)
    draw.polygon([(W - 58, 68), (W - 58, 80), (W - 52, 74)], fill=COLOR_TEXT)
    
    # Success Pill Banner
    draw.rounded_rectangle((40, 145, W - 40, 205), radius=16, fill=(16, 185, 129, 40), outline=(16, 185, 129), width=2)
    draw.text((W//2 - 170, 162), "✓ Saved in Full 1280x720 HD Quality", fill=(52, 211, 153), font=FONT_SMB)
    
    # Hero Preview Card (16:9 Thumbnail, 640 x 360 px)
    card_w, card_h = 640, 360
    card_x = (W - card_w) // 2
    card_y = 225
    
    gaming_thumb = create_gaming_thumb(card_w, card_h)
    draw.rounded_rectangle((card_x - 4, card_y - 4, card_x + card_w + 4, card_y + card_h + 4), radius=18, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=2)
    
    mask = Image.new("L", (card_w, card_h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, card_w, card_h), radius=16, fill=255)
    img.paste(gaming_thumb, (card_x, card_y), mask)
    
    # Resolution Specs Card
    specs_y = card_y + card_h + 30
    draw.rounded_rectangle((40, specs_y, W - 40, specs_y + 110), radius=16, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=1)
    draw.text((65, specs_y + 20), "File Details", fill=COLOR_TEXT, font=FONT_SMB)
    draw.text((65, specs_y + 52), "Resolution: 1280 × 720 px (16:9 Ratio)", fill=COLOR_TEXT_MUTED, font=FONT_SM)
    draw.text((65, specs_y + 76), "Format: PNG • 300 DPI • Ready for YouTube Studio", fill=(52, 211, 153), font=FONT_SM)
    
    # Quick Action Buttons
    btn_y = specs_y + 135
    # Primary YouTube Studio button (Red)
    draw.rounded_rectangle((40, btn_y, W - 40, btn_y + 65), radius=16, fill=(239, 68, 68))
    # Play icon
    draw.polygon([(75, btn_y + 20), (75, btn_y + 44), (95, btn_y + 32)], fill=(255, 255, 255))
    draw.text((115, btn_y + 18), "Open in YouTube Studio", fill=(255, 255, 255), font=FONT_HEADING)
    
    # Share to Instagram
    draw.rounded_rectangle((40, btn_y + 85, W - 40, btn_y + 150), radius=16, fill=(225, 48, 108))
    draw.text((W//2 - 90, btn_y + 103), "Share to Instagram", fill=(255, 255, 255), font=FONT_HEADING)
    
    # Save to Photos
    draw.rounded_rectangle((40, btn_y + 170, W - 40, btn_y + 235), radius=16, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=2)
    draw.text((W//2 - 95, btn_y + 188), "Save to Device Photos", fill=COLOR_TEXT, font=FONT_HEADING)
    
    # Bottom Navigation Dock
    draw_bottom_dock(img, draw, active_idx=3)
    return img


if __name__ == "__main__":
    os.makedirs("assets/images", exist_ok=True)
    print("Generating authentic ad-free screens with real app structure...")
    
    feed = make_hero_feed()
    feed.save("assets/images/app-screen-feed.webp", "WEBP", quality=95)
    print("[OK] Saved assets/images/app-screen-feed.webp (720x1520)")
    
    templates = make_templates_screen()
    templates.save("assets/images/app-screen-templates.webp", "WEBP", quality=95)
    print("[OK] Saved assets/images/app-screen-templates.webp (720x1520)")
    
    editor = make_editor_screen()
    editor.save("assets/images/app-screen-editor.webp", "WEBP", quality=95)
    print("[OK] Saved assets/images/app-screen-editor.webp (720x1520)")
    
    cutout = make_cutout_screen()
    cutout.save("assets/images/app-screen-cutout.webp", "WEBP", quality=95)
    print("[OK] Saved assets/images/app-screen-cutout.webp (720x1520)")
    
    export_screen = make_export_screen()
    export_screen.save("assets/images/app-screen-export.webp", "WEBP", quality=95)
    print("[OK] Saved assets/images/app-screen-export.webp (720x1520)")
    
    print("\nAll 5 mobile app screens generated successfully with real app fidelity and zero ads!")
