import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 720, 1520

APP_DIR = r"C:\nj\thumbnailkrunal\app\src\main"
RES_DRAWABLE = os.path.join(APP_DIR, "res", "drawable")
RES_NODPI = os.path.join(APP_DIR, "res", "drawable-nodpi")
FONT_NUNITO_PATH = os.path.join(APP_DIR, "res", "font", "nunitobold.ttf")
FONT_BEBAS_PATH = os.path.join(APP_DIR, "assets", "font", "BebasNeue Bold.ttf")
REAL_THUMB_DIR = "scratch/real_16_9_templates"

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

# Colors matching real app
COLOR_BG = (33, 32, 41)          # #212029 (Real App Background)
COLOR_BAR = (47, 45, 58)         # #2F2D3A (Real App Action/Top Bar)
COLOR_BAR_BORDER = (58, 55, 72)  # Subtle divider
COLOR_ACCENT = (14, 172, 255)    # #0EACFF (Real App Active Cyan/Blue)
COLOR_TEXT = (255, 255, 255)
COLOR_TEXT_MUTED = (160, 160, 168)
COLOR_CARD_BG = (42, 40, 52)

# Real 16:9 thumbnail templates extracted directly from app cache (fills all rows completely)
REAL_THUMBS_FEED = [
    "real_thumb_15_960x540.jpg",
    "real_thumb_8_960x540.jpg",
    "real_thumb_36_960x540.jpg",
    "real_thumb_37_960x540.jpg",
    "real_thumb_3_706x397.jpg",
    "real_thumb_10_706x397.jpg",
    "real_thumb_14_706x397.jpg",
    "real_thumb_16_706x397.jpg",
    "real_thumb_28_706x397.jpg",
    "real_thumb_30_706x397.jpg",
    "real_thumb_12_500x281.jpg",
    "real_thumb_31_500x281.jpg"
]

REAL_THUMBS_TEMPLATES = [
    "real_thumb_18_500x281.jpg",
    "real_thumb_34_706x397.jpg",
    "real_thumb_21_706x397.jpg",
    "real_thumb_19_500x281.jpg",
    "real_thumb_23_706x397.jpg",
    "real_thumb_27_500x281.jpg",
    "real_thumb_4_500x281.jpg",
    "real_thumb_11_500x281.jpg",
    "real_thumb_9_500x281.jpg",
    "real_thumb_35_500x281.jpg",
    "real_thumb_17_500x281.jpg",
    "real_thumb_20_500x281.jpg",
    "real_thumb_22_500x281.jpg",
    "real_thumb_24_500x281.jpg"
]

RES_DIR = os.path.join(APP_DIR, "res")

def load_app_drawable(filename, size=None):
    # Check direct folders first for performance
    for folder in ["drawable-nodpi", "drawable", "drawable-xxhdpi", "drawable-xhdpi", "drawable-hdpi"]:
        p = os.path.join(RES_DIR, folder, filename)
        if os.path.exists(p):
            im = Image.open(p).convert("RGBA")
            if size:
                im = im.resize(size, Image.Resampling.LANCZOS)
            return im
    # Fallback recursive search in res directory
    for root, dirs, files in os.walk(RES_DIR):
        if filename in files:
            im = Image.open(os.path.join(root, filename)).convert("RGBA")
            if size:
                im = im.resize(size, Image.Resampling.LANCZOS)
            return im
    return None

def load_real_thumb(filename, w=330, h=186):
    p = os.path.join(REAL_THUMB_DIR, filename)
    if os.path.exists(p):
        return Image.open(p).convert("RGB").resize((w, h), Image.Resampling.LANCZOS)
    return Image.new("RGB", (w, h), (50, 48, 60))

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
    # Samsung Galaxy S24 Infinity-O Camera Punch Hole (ultra-sleek centered circle)
    draw.ellipse((W//2 - 9, 20, W//2 + 9, 38), fill=(10, 10, 14), outline=(32, 32, 40), width=1)
    draw.ellipse((W//2 - 3, 24, W//2 + 2, 29), fill=(40, 55, 80))

def draw_real_app_menu_icon(draw, name, cx, cy, color, size=26):
    """Exact vector reproduction of the app's ic_create, ic_collage, ic_edit, ic_save_icon"""
    s = size // 2
    if name == "CREATE":
        # ic_create.xml: Rounded square frame with centered +
        draw.rounded_rectangle((cx - s, cy - s, cx + s, cy + s), radius=4, outline=color, width=2)
        draw.line((cx - s + 5, cy, cx + s - 5, cy), fill=color, width=2)
        draw.line((cx, cy - s + 5, cx, cy + s - 5), fill=color, width=2)
    elif name == "FRAME":
        # ic_collage.xml: 4-pane photo frame
        draw.rounded_rectangle((cx - s, cy - s, cx + s, cy + s), radius=4, outline=color, width=2)
        draw.line((cx, cy - s, cx, cy + s), fill=color, width=2)
        draw.line((cx - s, cy, cx + s, cy), fill=color, width=2)
    elif name == "MY EDIT":
        # ic_edit.xml: Pencil editing on a baseline
        draw.line((cx - s, cy + s, cx + s, cy + s), fill=color, width=2)
        draw.line((cx - s + 3, cy + s - 3, cx + s - 3, cy - s + 3), fill=color, width=3)
        draw.polygon([(cx - s + 1, cy + s - 1), (cx - s + 5, cy + s - 1), (cx - s + 1, cy + s - 5)], fill=color)
    elif name == "MY SAVE":
        # ic_save_icon.xml: Photo frame with mountain peak and sun
        draw.rounded_rectangle((cx - s, cy - s, cx + s, cy + s), radius=4, outline=color, width=2)
        draw.ellipse((cx - s + 4, cy - s + 4, cx - s + 9, cy - s + 9), fill=color)
        draw.polygon([(cx - s + 3, cy + s - 3), (cx - 1, cy), (cx + 5, cy + s - 3)], fill=color)
        draw.polygon([(cx + 1, cy + s - 3), (cx + 6, cy + 2), (cx + s - 3, cy + s - 3)], fill=color)

def draw_bottom_dock(img, draw, active_idx=0):
    nav_h = 105
    nav_y = H - nav_h - 25 # leave 25px for system bar
    draw.rectangle((0, nav_y, W, nav_y + nav_h), fill=COLOR_BAR)
    draw.line((0, nav_y, W, nav_y), fill=COLOR_BAR_BORDER, width=1)
    
    # 4 Authentic Items matching main_activity.xml boMenu: CREATE, FRAME, MY EDIT, MY SAVE
    items = ["CREATE", "FRAME", "MY EDIT", "MY SAVE"]
    tab_w = W // len(items)
    
    for i, label in enumerate(items):
        cx = i * tab_w + tab_w // 2
        is_active = (i == active_idx)
        item_color = COLOR_ACCENT if is_active else COLOR_TEXT
        
        # Draw exact clean vector line-art icon matching app
        draw_real_app_menu_icon(draw, label, cx, nav_y + 30, item_color, size=28)
        
        # Label in Nunito Bold matching app
        text_color = COLOR_ACCENT if is_active else COLOR_TEXT
        draw.text((cx - len(label)*4 - 6, nav_y + 60), label, fill=text_color, font=FONT_SMB)
        
        if is_active:
            # Subtle cyan active indicator underline
            draw.rounded_rectangle((cx - 24, nav_y + 88, cx + 24, nav_y + 92), radius=2, fill=COLOR_ACCENT)
            
    # System bar pill (Samsung Galaxy S24 slim gesture bar)
    draw.rectangle((0, H - 25, W, H), fill=(20, 19, 25))
    draw.rounded_rectangle((W//2 - 55, H - 15, W//2 + 55, H - 10), radius=3, fill=(140, 140, 150))


# =============================================================
# 1. SCREEN: Hero App Feed (Home Screen - 100% Real Templates, Real Menu)
# =============================================================
def make_hero_feed():
    img = Image.new("RGBA", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Top Bar: Background #2F2D3A (height 125px)
    draw.rectangle((0, 0, W, 125), fill=COLOR_BAR)
    draw.line((0, 125, W, 125), fill=COLOR_BAR_BORDER, width=1)
    draw_status_bar(draw, dark=False)
    
    # Left: info icon
    info_icon = load_app_drawable("info.png", (38, 38))
    if info_icon:
        img.paste(info_icon, (24, 65), info_icon)
        
    # Center: "Thumbnail Maker" in Nunito Bold
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
    # Category Tabs Bar (Height 50px, at y = 295)
    # ---------------------------------------------------------
    tabs_y = 295
    draw.rectangle((0, tabs_y, W, tabs_y + 50), fill=COLOR_BAR)
    draw.line((0, tabs_y + 50, W, tabs_y + 50), fill=COLOR_BAR_BORDER, width=1)
    
    cat_tabs = ["FITNESS", "GAMING", "MIX", "ART", "AUTOMOBILE"]
    tab_spacing = W // len(cat_tabs)
    for idx, tab_name in enumerate(cat_tabs):
        tx = idx * tab_spacing + tab_spacing // 2
        is_active = (idx == 1) # GAMING active
        t_color = COLOR_TEXT if is_active else COLOR_TEXT_MUTED
        draw.text((tx - len(tab_name)*5, tabs_y + 14), tab_name, fill=t_color, font=FONT_SMB)
        if is_active:
            # Cyan indicator line
            draw.rectangle((tx - 32, tabs_y + 46, tx + 32, tabs_y + 50), fill=COLOR_ACCENT)
            
    # ---------------------------------------------------------
    # 2-Column Grid of 16:9 REAL Thumbnails (Fills 100% of height down to bottom dock)
    # ---------------------------------------------------------
    grid_y = 355
    cw, ch = 330, 186 # exact 16:9 ratio
    col_x = [20, 370] # 20px margin, 20px gap, 20px right margin (total 720)
    gap_y = 12
    
    mask = Image.new("L", (cw, ch), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, cw, ch), radius=12, fill=255)
    
    for idx, tfilename in enumerate(REAL_THUMBS_FEED):
        col = idx % 2
        row = idx // 2
        gx = col_x[col]
        gy = grid_y + row * (ch + gap_y)
        
        if gy >= 1420:
            break
            
        real_img = load_real_thumb(tfilename, cw, ch)
        
        # Clean CardView border outline matching app
        draw.rounded_rectangle((gx - 1, gy - 1, gx + cw + 1, gy + ch + 1), radius=13, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=1)
        # Paste real thumbnail image full-bleed inside card
        img.paste(real_img, (gx, gy), mask)

    # Bottom Navigation Dock (Drawn over grid so cards flow seamlessly under dock)
    draw_bottom_dock(img, draw, active_idx=0)
    return img


# =============================================================
# 2. SCREEN: Templates Category Screen (Youtube Cover Browser - Real Templates)
# =============================================================
def make_templates_screen():
    img = Image.new("RGBA", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Top Bar: Background #2F2D3A (height 125px)
    draw.rectangle((0, 0, W, 125), fill=COLOR_BAR)
    draw.line((0, 125, W, 125), fill=COLOR_BAR_BORDER, width=1)
    draw_status_bar(draw, dark=False)
    
    # Left: Back arrow
    draw.polygon([(40, 84), (55, 72), (55, 96)], fill=COLOR_TEXT)
    draw.line((45, 84, 70, 84), fill=COLOR_TEXT, width=4)
    
    # Center: Title "Youtube Cover" in Nunito Bold
    draw.text((95, 68), "Youtube Cover", fill=COLOR_TEXT, font=FONT_TITLE)
    
    # Right: Search & PRO
    draw.ellipse((W - 120, 72, W - 102, 90), outline=COLOR_TEXT, width=2)
    draw.line((W - 106, 86, W - 98, 94), fill=COLOR_TEXT, width=3)
    
    pro_icon = load_app_drawable("pro_ic.png", (46, 38))
    if pro_icon:
        img.paste(pro_icon, (W - 70, 65), pro_icon)
        
    # Category Sub-tabs (Fitness, Business, Fashion, Food, Summer)
    tabs_y = 135
    draw.rectangle((0, tabs_y, W, tabs_y + 55), fill=COLOR_BAR)
    draw.line((0, tabs_y + 55, W, tabs_y + 55), fill=COLOR_BAR_BORDER, width=1)
    
    sub_tabs = ["Fitness", "Business", "Fashion", "Food", "Summer"]
    tab_spacing = W // len(sub_tabs)
    for idx, tab_name in enumerate(sub_tabs):
        tx = idx * tab_spacing + tab_spacing // 2
        is_active = (idx == 0) # Fitness active
        t_color = COLOR_TEXT if is_active else COLOR_TEXT_MUTED
        draw.text((tx - len(tab_name)*5, tabs_y + 16), tab_name, fill=t_color, font=FONT_SMB)
        if is_active:
            draw.rectangle((tx - 28, tabs_y + 50, tx + 28, tabs_y + 54), fill=COLOR_ACCENT)
            
    # 2-Column Grid of 16:9 REAL Youtube Cover Templates (Fills 100% of height down to bottom dock)
    grid_y = 198
    cw, ch = 330, 186
    col_x = [20, 370]
    gap_y = 12
    
    mask = Image.new("L", (cw, ch), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, cw, ch), radius=12, fill=255)
    
    for idx, tfilename in enumerate(REAL_THUMBS_TEMPLATES):
        col = idx % 2
        row = idx // 2
        gx = col_x[col]
        gy = grid_y + row * (ch + gap_y)
        
        if gy >= 1420:
            break
            
        real_img = load_real_thumb(tfilename, cw, ch)
        
        draw.rounded_rectangle((gx - 1, gy - 1, gx + cw + 1, gy + ch + 1), radius=13, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=1)
        img.paste(real_img, (gx, gy), mask)

    # Bottom Navigation Dock (FRAME active)
    draw_bottom_dock(img, draw, active_idx=1)
    return img


# =============================================================
# 3. SCREEN: Multi-Layer Studio Editor (activity_poster.xml)
# 100% Authentic to App: Canvas in Center of Screen, Real Header & Footer,
# Layers Button at top-left, Real 4-Corner Sticker Handles, Ad-Free
# =============================================================
def make_editor_screen():
    img = Image.new("RGBA", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # ---------------------------------------------------------
    # 1. TOP BAR (activity_poster.xml: header, height 125px)
    # ---------------------------------------------------------
    draw.rectangle((0, 0, W, 125), fill=COLOR_BAR)
    draw.line((0, 125, W, 125), fill=COLOR_BAR_BORDER, width=1)
    draw_status_bar(draw, dark=False)
    
    # Left: Back arrow (btn_new_back.png)
    back_icon = load_app_drawable("btn_new_back.png", (36, 36))
    if back_icon:
        img.paste(back_icon, (24, 66), back_icon)
    else:
        draw.polygon([(28, 84), (45, 72), (45, 96)], fill=COLOR_TEXT)
        draw.line((35, 84, 55, 84), fill=COLOR_TEXT, width=4)
        
    # Title: THUMBNAIL (txtheader in activity_poster.xml, all caps)
    draw.text((75, 68), "THUMBNAIL", fill=COLOR_TEXT, font=FONT_TITLE)
    
    # Right action buttons (activity_poster.xml: btn_undo, btn_redo, btn_erase, btn_done)
    # 1) Undo
    undo_icon = load_app_drawable("undo.png", (30, 30)) or load_app_drawable("ic_undo_1.png", (30, 30))
    if undo_icon:
        img.paste(undo_icon, (W - 200, 68), undo_icon)
        
    # 2) Redo
    redo_icon = load_app_drawable("redo.png", (30, 30)) or load_app_drawable("ic_redo_1.png", (30, 30))
    if redo_icon:
        img.paste(redo_icon, (W - 150, 68), redo_icon)
        
    # 3) Erase (btn_erase / ic_selected_eraser.png)
    erase_icon = load_app_drawable("ic_selected_eraser.png", (30, 30))
    if erase_icon:
        img.paste(erase_icon, (W - 100, 68), erase_icon)
        
    # 4) Download / Save (btn_done / btn_download vector)
    tray_x, tray_y = W - 50, 83
    draw.line((tray_x - 12, tray_y + 4, tray_x - 12, tray_y + 12), fill=COLOR_TEXT, width=3)
    draw.line((tray_x - 12, tray_y + 12, tray_x + 12, tray_y + 12), fill=COLOR_TEXT, width=3)
    draw.line((tray_x + 12, tray_y + 12, tray_x + 12, tray_y + 4), fill=COLOR_TEXT, width=3)
    draw.line((tray_x, tray_y - 12, tray_x, tray_y + 5), fill=COLOR_TEXT, width=3)
    draw.line((tray_x - 6, tray_y - 1, tray_x, tray_y + 6), fill=COLOR_TEXT, width=3)
    draw.line((tray_x + 6, tray_y - 1, tray_x, tray_y + 6), fill=COLOR_TEXT, width=3)

    # ---------------------------------------------------------
    # 2. WORKSPACE AREA (activity_poster.xml: lay_remove, y = 125 to 1390)
    # ---------------------------------------------------------
    # Floating Layers button at top-left (btn_layControls / layers.png)
    lay_btn_x, lay_btn_y = 24, 150
    draw.rounded_rectangle((lay_btn_x, lay_btn_y, lay_btn_x + 56, lay_btn_y + 56), radius=16, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=1)
    layers_icon = load_app_drawable("layers.png", (38, 30))
    if layers_icon:
        img.paste(layers_icon, (lay_btn_x + 9, lay_btn_y + 13), layers_icon)

    # ---------------------------------------------------------
    # 3. MAIN CANVAS: STRICTLY CENTERED IN SCREEN (layout_centerInParent="true")
    # Workspace height: 1390 - 125 = 1265px
    # Center Y of workspace = 125 + 1265 // 2 = 757px
    # Canvas size: 670 x 377 (exact 16:9 ratio)
    # canv_y = 757 - 377 // 2 = 568px -> ends at 945px
    # (Top gap = 443px, Bottom gap = 445px -> perfectly centered!)
    # ---------------------------------------------------------
    canv_w, canv_h = 670, 377
    canv_x = (W - canv_w) // 2
    canv_y = 568
    
    # Elevation shadow & card outline
    draw.rounded_rectangle((canv_x - 4, canv_y - 4, canv_x + canv_w + 4, canv_y + canv_h + 4), radius=16, fill=(15, 14, 20))
    draw.rounded_rectangle((canv_x - 1, canv_y - 1, canv_x + canv_w + 1, canv_y + canv_h + 1), radius=14, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=1)
    
    # Real thumbnail image (Muscle Tonin Fitness template)
    real_canvas_source = load_real_thumb("real_thumb_15_960x540.jpg", canv_w, canv_h).convert("RGBA")
    mask_c = Image.new("L", (canv_w, canv_h), 0)
    mdraw_c = ImageDraw.Draw(mask_c)
    mdraw_c.rounded_rectangle((0, 0, canv_w, canv_h), radius=12, fill=255)
    img.paste(real_canvas_source, (canv_x, canv_y), mask_c)
    
    # ---------------------------------------------------------
    # 4. ACTIVE ELEMENT BOUNDING BOX & REAL APP HANDLES (AutofitTextRel / StickerView)
    # ---------------------------------------------------------
    box_x1 = canv_x + 22
    box_y1 = canv_y + 35
    box_x2 = canv_x + 380
    box_y2 = canv_y + 115
    
    # Clean dashed cyan boundary
    for dx in range(box_x1, box_x2, 12):
        draw.line((dx, box_y1, min(dx + 6, box_x2), box_y1), fill=COLOR_ACCENT, width=2)
        draw.line((dx, box_y2, min(dx + 6, box_x2), box_y2), fill=COLOR_ACCENT, width=2)
    for dy in range(box_y1, box_y2, 12):
        draw.line((box_x1, dy, box_x1, min(dy + 6, box_y2)), fill=COLOR_ACCENT, width=2)
        draw.line((box_x2, dy, box_x2, min(dy + 6, box_y2)), fill=COLOR_ACCENT, width=2)
        
    # Real app handle icons (36x36 px)
    h_size = (36, 36)
    del_icon = load_app_drawable("sticker_delete1.png", h_size)
    rot_icon = load_app_drawable("sticker_rotate.png", h_size)
    scale_icon = load_app_drawable("sticker_scale.png", h_size)
    flip_icon = load_app_drawable("sticker_flip.png", h_size)
    
    # Top-Left: Delete (sticker_delete1.png)
    if del_icon:
        img.paste(del_icon, (box_x1 - 18, box_y1 - 18), del_icon)
    # Top-Right: Rotate (sticker_rotate.png)
    if rot_icon:
        img.paste(rot_icon, (box_x2 - 18, box_y1 - 18), rot_icon)
    # Bottom-Right: Scale (sticker_scale.png)
    if scale_icon:
        img.paste(scale_icon, (box_x2 - 18, box_y2 - 18), scale_icon)
    # Bottom-Left: Flip (sticker_flip.png)
    if flip_icon:
        img.paste(flip_icon, (box_x1 - 18, box_y2 - 18), flip_icon)

    # ---------------------------------------------------------
    # 5. BOTTOM EDITING TOOLBAR (activity_poster.xml: footer, height 105px)
    # 5 Real tools: Text, Sticker, Image, Effect, Background
    # ---------------------------------------------------------
    nav_h = 105
    nav_y = H - nav_h - 25
    draw.rectangle((0, nav_y, W, nav_y + nav_h), fill=COLOR_BAR)
    draw.line((0, nav_y, W, nav_y), fill=COLOR_BAR_BORDER, width=1)
    
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
        is_active = (idx == 0) # Text tool active
        timg = load_app_drawable(tfile, (42, 42))
        if timg:
            img.paste(timg, (cx - 21, nav_y + 16), timg)
        else:
            draw.rectangle((cx - 18, nav_y + 16, cx + 18, nav_y + 52), fill=COLOR_ACCENT if is_active else COLOR_TEXT_MUTED)
        t_color = COLOR_ACCENT if is_active else COLOR_TEXT
        draw.text((cx - len(tlabel)*4 - 4, nav_y + 68), tlabel, fill=t_color, font=FONT_SMB)
        if is_active:
            draw.rounded_rectangle((cx - 20, nav_y + 96, cx + 20, nav_y + 100), radius=2, fill=COLOR_ACCENT)
            
    # System bar pill (Samsung Galaxy S24 slim gesture bar)
    draw.rectangle((0, H - 25, W, H), fill=(20, 19, 25))
    draw.rounded_rectangle((W//2 - 55, H - 15, W//2 + 55, H - 10), radius=3, fill=(140, 140, 150))
    return img


# =============================================================
# 4. SCREEN: 1-Tap Cutout & Background Eraser (activity_eraser.xml)
# Real Human YouTube Creator Cutout, Neon Edge Glow, Real Seekbars & Tools
# =============================================================
def make_cutout_screen():
    img = Image.new("RGBA", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Top Bar: Background #2F2D3A (height 125px)
    draw.rectangle((0, 0, W, 125), fill=COLOR_BAR)
    draw.line((0, 125, W, 125), fill=COLOR_BAR_BORDER, width=1)
    draw_status_bar(draw, dark=False)
    
    # Left: Back arrow (btn_new_back.png)
    back_icon = load_app_drawable("btn_new_back.png", (36, 36))
    if back_icon:
        img.paste(back_icon, (24, 66), back_icon)
    else:
        draw.polygon([(28, 84), (45, 72), (45, 96)], fill=COLOR_TEXT)
        draw.line((35, 84, 55, 84), fill=COLOR_TEXT, width=4)
        
    # Title: Cut Photo (bold)
    draw.text((75, 68), "Cut Photo", fill=COLOR_TEXT, font=FONT_TITLE)
    
    # Right: Save / Download Icon (btn_download.xml vector)
    tray_x, tray_y = W - 50, 83
    draw.line((tray_x - 12, tray_y + 4, tray_x - 12, tray_y + 12), fill=COLOR_TEXT, width=3)
    draw.line((tray_x - 12, tray_y + 12, tray_x + 12, tray_y + 12), fill=COLOR_TEXT, width=3)
    draw.line((tray_x + 12, tray_y + 12, tray_x + 12, tray_y + 4), fill=COLOR_TEXT, width=3)
    draw.line((tray_x, tray_y - 12, tray_x, tray_y + 5), fill=COLOR_TEXT, width=3)
    draw.line((tray_x - 6, tray_y - 1, tray_x, tray_y + 6), fill=COLOR_TEXT, width=3)
    draw.line((tray_x + 6, tray_y - 1, tray_x, tray_y + 6), fill=COLOR_TEXT, width=3)
    
    # 2. Bottom Cutout Toolbar (5 Modes: Auto, Lasso, Erase, Restore, Zoom)
    nav_h = 120
    nav_y = H - nav_h - 25  # 1375
    draw.rectangle((0, nav_y, W, nav_y + nav_h), fill=COLOR_BAR)
    draw.line((0, nav_y, W, nav_y), fill=COLOR_BAR_BORDER, width=1)
    
    # Collapse chevron handle (rel_down in activity_eraser.xml)
    down_icon = load_app_drawable("ic_down.png", (22, 12))
    if down_icon:
        img.paste(down_icon, (W // 2 - 11, nav_y + 6), down_icon)
    else:
        draw.line((W // 2 - 12, nav_y + 8, W // 2, nav_y + 14), fill=(160, 160, 170), width=2)
        draw.line((W // 2, nav_y + 14, W // 2 + 12, nav_y + 8), fill=(160, 160, 170), width=2)
        
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
            img.paste(timg, (cx - 21, nav_y + 24), timg)
        else:
            draw.rectangle((cx - 18, nav_y + 24, cx + 18, nav_y + 60), fill=COLOR_ACCENT if is_active else COLOR_TEXT_MUTED)
        t_color = COLOR_ACCENT if is_active else COLOR_TEXT_MUTED
        draw.text((cx - len(tlabel)*4 - 4, nav_y + 74), tlabel, fill=t_color, font=FONT_SMB)
        if is_active:
            draw.rounded_rectangle((cx - 20, nav_y + 104, cx + 20, nav_y + 108), radius=2, fill=COLOR_ACCENT)

    # 3. Adjustment Sliders Panel (Docked DIRECTLY ON TOP of Bottom Menu, ZERO VOID!)
    # Matching activity_eraser.xml rel_seek_container layout_above="@id/footer"
    panel_h = 150
    panel_gap = 10
    panel_y = nav_y - panel_h - panel_gap   # 1375 - 150 - 10 = 1215
    panel_bottom = nav_y - panel_gap        # 1365
    
    draw.rounded_rectangle((18, panel_y, W - 18, panel_bottom), radius=16, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=1)
    
    # Offset Seekbar
    draw.text((45, panel_y + 22), "OFFSET", fill=COLOR_TEXT, font=FONT_SMB)
    draw.rounded_rectangle((155, panel_y + 30, W - 120, panel_y + 38), radius=4, fill=(60, 58, 75))
    draw.rounded_rectangle((155, panel_y + 30, 155 + int((W - 275) * 0.5), panel_y + 38), radius=4, fill=COLOR_ACCENT)
    thumb_x = 155 + int((W - 275) * 0.5)
    draw.ellipse((thumb_x - 12, panel_y + 22, thumb_x + 12, panel_y + 46), fill=(255, 255, 255), outline=COLOR_ACCENT, width=3)
    draw.text((W - 90, panel_y + 22), "150", fill=COLOR_ACCENT, font=FONT_SMB)
    
    # Threshold Seekbar
    draw.text((45, panel_y + 90), "THRESHOLD", fill=COLOR_TEXT, font=FONT_SMB)
    draw.rounded_rectangle((155, panel_y + 98, W - 120, panel_y + 106), radius=4, fill=(60, 58, 75))
    draw.rounded_rectangle((155, panel_y + 98, 155 + int((W - 275) * 0.65), panel_y + 106), radius=4, fill=COLOR_ACCENT)
    thumb_x2 = 155 + int((W - 275) * 0.65)
    draw.ellipse((thumb_x2 - 12, panel_y + 90, thumb_x2 + 12, panel_y + 114), fill=(255, 255, 255), outline=COLOR_ACCENT, width=3)
    draw.text((W - 90, panel_y + 90), "52", fill=COLOR_ACCENT, font=FONT_SMB)

    # 4. Main Canvas: Checkerboard Transparency (Extending all the way down to sliders panel!)
    canv_y = 125
    canv_h = panel_y - 12 - canv_y          # 1215 - 12 - 125 = 1078px
    sq_size = 24
    for cy in range(canv_y, canv_y + canv_h, sq_size):
        for cx in range(0, W, sq_size):
            is_dark = ((cx // sq_size) + (cy // sq_size)) % 2 == 0
            sq_color = (42, 40, 52) if is_dark else (55, 52, 68)
            draw.rectangle((cx, cy, min(cx + sq_size, W), min(cy + sq_size, canv_y + canv_h)), fill=sq_color)
            
    # Paste REAL HUMAN CREATOR Cutout
    cutout_path = "assets/images/real-creator-cutout.png"
    if not os.path.exists(cutout_path):
        cutout_path = "assets/images/creator-cutout.png"
        
    if os.path.exists(cutout_path):
        c_cutout = Image.open(cutout_path).convert("RGBA")
        cw, ch = 480, 750
        c_cutout = c_cutout.resize((cw, ch), Image.Resampling.LANCZOS)
        
        # Draw dynamic neon cyan boundary glow around creator
        glow_mask = Image.new("RGBA", (cw + 16, ch + 16), (0, 0, 0, 0))
        alpha_mask = c_cutout.split()[-1]
        for ox, oy in [(-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,2),(-2,2),(2,-2)]:
            glow_mask.paste(Image.new("RGBA", (cw, ch), (14, 172, 255, 75)), (ox + 8, oy + 8), alpha_mask)
        img.paste(glow_mask, (W//2 - cw//2 - 8, canv_y + 132), glow_mask)
        img.paste(c_cutout, (W//2 - cw//2, canv_y + 140), c_cutout)
        
    # Offset Cursor Brush Mechanism (Exact App Offset Feature)
    finger_x, finger_y = 440, canv_y + 680
    draw.ellipse((finger_x - 30, finger_y - 30, finger_x + 30, finger_y + 30), outline=(239, 68, 68), width=3)
    draw.ellipse((finger_x - 6, finger_y - 6, finger_x + 6, finger_y + 6), fill=(239, 68, 68))
    draw.text((finger_x + 38, finger_y - 10), "Touch Point", fill=(255, 255, 255), font=FONT_SMB)
    
    brush_x, brush_y = finger_x, finger_y - 150
    for dy in range(brush_y + 15, finger_y - 15, 10):
        draw.line((finger_x, dy, finger_x, dy + 5), fill=COLOR_ACCENT, width=2)
        
    draw.ellipse((brush_x - 35, brush_y - 35, brush_x + 35, brush_y + 35), outline=COLOR_ACCENT, width=3)
    draw.line((brush_x - 45, brush_y, brush_x + 45, brush_y), fill=COLOR_ACCENT, width=2)
    draw.line((brush_x, brush_y - 45, brush_x, brush_y + 45), fill=COLOR_ACCENT, width=2)
    draw.text((brush_x + 42, brush_y - 10), "Offset Eraser (150px)", fill=COLOR_ACCENT, font=FONT_SMB)

    # 5. System bar pill (Samsung Galaxy S24 slim gesture bar)
    draw.rectangle((0, H - 25, W, H), fill=(20, 19, 25))
    draw.rounded_rectangle((W//2 - 55, H - 15, W//2 + 55, H - 10), radius=3, fill=(140, 140, 150))
    return img


# =============================================================
# 5. SCREEN: 1-Tap Save & Export Ready for YouTube Studio (activity_share_image.xml)
# 100% Authentic: Clean Vector Checkmark (No Broken Glyphs), Real Share Actions, No Misplaced Menu
# =============================================================
def make_export_screen():
    img = Image.new("RGBA", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Top Bar: Background #2F2D3A (height 125px, activity_share_image.xml: top_layout)
    draw.rectangle((0, 0, W, 125), fill=COLOR_BAR)
    draw.line((0, 125, W, 125), fill=COLOR_BAR_BORDER, width=1)
    draw_status_bar(draw, dark=False)
    
    # Left: Back arrow (btn_new_back.png)
    back_icon = load_app_drawable("btn_new_back.png", (36, 36))
    if back_icon:
        img.paste(back_icon, (24, 66), back_icon)
    else:
        draw.polygon([(28, 84), (45, 72), (45, 96)], fill=COLOR_TEXT)
        draw.line((35, 84, 55, 84), fill=COLOR_TEXT, width=4)
        
    # Title: SHARE IMAGE (txt_toolbar in activity_share_image.xml)
    draw.text((75, 68), "SHARE IMAGE", fill=COLOR_TEXT, font=FONT_TITLE)
    
    # Right: Share icon & Home icon (btnShareMore & img_home in activity_share_image.xml)
    share_icon = load_app_drawable("ic_share_share.png", (32, 32)) or load_app_drawable("ic_share.png", (32, 32))
    if share_icon:
        img.paste(share_icon, (W - 110, 68), share_icon)
    home_icon = load_app_drawable("ic_home.png", (32, 32))
    if home_icon:
        img.paste(home_icon, (W - 55, 68), home_icon)
    
    # Success Pill Banner with SHARP VECTOR CHECKMARK (Zero Broken Unicode Glyphs!)
    pill_y = 150
    draw.rounded_rectangle((30, pill_y, W - 30, pill_y + 60), radius=16, fill=(16, 185, 129, 35), outline=(16, 185, 129), width=2)
    # Vector Checkmark Circle
    draw.ellipse((55, pill_y + 14, 87, pill_y + 46), fill=(16, 185, 129))
    draw.line((63, pill_y + 30, 70, pill_y + 38), fill=(255, 255, 255), width=3)
    draw.line((70, pill_y + 38, 79, pill_y + 22), fill=(255, 255, 255), width=3)
    draw.text((98, pill_y + 20), "Saved to Gallery in Full 1280x720 HD Quality", fill=(52, 211, 153), font=FONT_SMB)
    
    # Hero Preview Card (16:9 Thumbnail, 660 x 371 px)
    card_w, card_h = 660, 371
    card_x = (W - card_w) // 2
    card_y = 235
    
    real_thumb = load_real_thumb("real_thumb_15_960x540.jpg", card_w, card_h)
    draw.rounded_rectangle((card_x - 4, card_y - 4, card_x + card_w + 4, card_y + card_h + 4), radius=18, fill=(15, 14, 20), outline=COLOR_BAR_BORDER, width=2)
    
    mask = Image.new("L", (card_w, card_h), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, card_w, card_h), radius=16, fill=255)
    img.paste(real_thumb, (card_x, card_y), mask)
    
    # File Specs Card (activity_share_image.xml: txt_path, txt_size)
    specs_y = card_y + card_h + 30
    draw.rounded_rectangle((30, specs_y, W - 30, specs_y + 120), radius=16, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=1)
    draw.text((55, specs_y + 18), "File Details", fill=COLOR_TEXT, font=FONT_SMB)
    draw.text((55, specs_y + 50), "Location: DCIM / ThumbnailMaker / thumb_export_hd.png", fill=COLOR_TEXT_MUTED, font=FONT_SM)
    draw.text((55, specs_y + 80), "Resolution: 1280 × 720 px (16:9 HD) • PNG 300 DPI", fill=(52, 211, 153), font=FONT_SMB)
    
    # Action Buttons (Cleanly laid out, NO misplaced bottom dock!)
    btn_y = specs_y + 150
    # 1) Primary Share Your Image button (activity_share_image.xml: btn_share)
    draw.rounded_rectangle((30, btn_y, W - 30, btn_y + 68), radius=18, fill=COLOR_ACCENT)
    draw.polygon([(65, btn_y + 24), (65, btn_y + 46), (82, btn_y + 35)], fill=(255, 255, 255))
    draw.text((95, btn_y + 20), "Share your image", fill=(255, 255, 255), font=FONT_TITLE)
    
    # 2) YouTube Studio Export (Red)
    draw.rounded_rectangle((30, btn_y + 88, W - 30, btn_y + 152), radius=18, fill=(239, 68, 68))
    # Play icon
    draw.polygon([(65, btn_y + 107), (65, btn_y + 131), (84, btn_y + 119)], fill=(255, 255, 255))
    draw.text((95, btn_y + 104), "Open in YouTube Studio", fill=(255, 255, 255), font=FONT_HEADING)
    
    # 3) Share to Instagram (Magenta)
    draw.rounded_rectangle((30, btn_y + 172, W - 30, btn_y + 236), radius=18, fill=(225, 48, 108))
    draw.text((W//2 - 95, btn_y + 188), "Share to Instagram", fill=(255, 255, 255), font=FONT_HEADING)
    
    # 4) Save to Photos Gallery
    draw.rounded_rectangle((30, btn_y + 256, W - 30, btn_y + 320), radius=18, fill=COLOR_CARD_BG, outline=COLOR_BAR_BORDER, width=2)
    draw.text((W//2 - 105, btn_y + 272), "Saved to Device Photos", fill=COLOR_TEXT, font=FONT_HEADING)
    
    # System bar pill (Samsung Galaxy S24 slim gesture bar)
    draw.rectangle((0, H - 25, W, H), fill=(20, 19, 25))
    draw.rounded_rectangle((W//2 - 55, H - 15, W//2 + 55, H - 10), radius=3, fill=(140, 140, 150))
    return img


if __name__ == "__main__":
    os.makedirs("assets/images", exist_ok=True)
    print("Generating authentic ad-free screens with REAL APP THUMBNAILS & EXACT APP MENU...")
    
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
    
    print("\nAll 5 mobile app screens generated successfully with exact app menu and real thumbnails!")
