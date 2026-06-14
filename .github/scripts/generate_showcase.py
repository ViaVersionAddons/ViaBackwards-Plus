import os
import json
import urllib.request
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter

CONFIG_PATH = "showcase_config.json"
INV_SLOT_PATH = "../images/inv_slot.png"
OUTPUT_PATH = "../images/vbp_showcase.png"
CUSTOM_ASSETS_DIR = "../images/showcase_assets"

MC_ASSETS_BASE = "https://raw.githubusercontent.com/Owen1212055/mc-assets/main/item-assets/"

GRID_COLS = 9
GRID_ROWS = 3
SLOT_SIZE = 162
ITEM_SIZE = 144
GAP = 54
SIDEBAR_WIDTH = 360

def download_image(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return Image.open(BytesIO(response.read())).convert("RGBA")
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        # Return a transparent dummy image
        return Image.new("RGBA", (256, 256), (0, 0, 0, 0))

def get_texture(path):
    is_block = path.startswith("block/")
    # Try local first
    local_path = os.path.join(CUSTOM_ASSETS_DIR, f"{path}.png")
    if os.path.exists(local_path):
        img = Image.open(local_path).convert("RGBA")
    else:
        # Convert "block/oak_log" to "OAK_LOG.png"
        item_name = path.split("/")[-1].upper()
        url = f"{MC_ASSETS_BASE}{item_name}.png"
        img = download_image(url)
        
    # Scale from 256x256 to 144x144
    if is_block:
        # Blocks use Lanczos for smooth 3D edges
        img = img.resize((ITEM_SIZE, ITEM_SIZE), Image.Resampling.LANCZOS)
    else:
        # Items are downscaled to 16x16 nearest neighbor, then upscaled to 144x144 nearest neighbor
        img = img.resize((16, 16), Image.Resampling.NEAREST)
        img = img.resize((ITEM_SIZE, ITEM_SIZE), Image.Resampling.NEAREST)
        
    return img

def create_background(width, height, config):
    override_path = config.get("background_override")
    if override_path and os.path.exists(override_path):
        bg = Image.open(override_path).convert("RGBA")
        # Resize to fill, center crop
        ratio = max(width / bg.width, height / bg.height)
        new_size = (int(bg.width * ratio), int(bg.height * ratio))
        bg = bg.resize(new_size, Image.Resampling.LANCZOS)
        left = (bg.width - width) / 2
        top = (bg.height - height) / 2
        bg = bg.crop((left, top, left + width, top + height))
        
        blur_radius = config.get("background_blur_radius", 5)
        if blur_radius > 0:
            bg = bg.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        return bg
    else:
        # Default gradient (solid color as a fallback if no dynamic gen is wanted)
        color_arr = config.get("background_color", [211, 140, 83, 255])
        color = tuple(color_arr)
        bg = Image.new("RGBA", (width, height), color)
        return bg

def main():
    # Resolve paths relative to script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    if not os.path.exists(CONFIG_PATH):
        print(f"Config not found at {CONFIG_PATH}")
        return

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
        
    grid_width = GRID_COLS * SLOT_SIZE
    grid_height = GRID_ROWS * SLOT_SIZE
    
    canvas_width = 1920
    canvas_height = 1080
    
    bg = create_background(canvas_width, canvas_height, config)
    
    try:
        inv_slot = Image.open(INV_SLOT_PATH).convert('RGBA')
        if config.get("transparent_inventory", False):
            data = inv_slot.getdata()
            new_data = []
            for item in data:
                if abs(item[0]-139) < 15 and abs(item[1]-139) < 15 and abs(item[2]-139) < 15:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            inv_slot.putdata(new_data)
        inv_slot = inv_slot.resize((SLOT_SIZE, SLOT_SIZE), Image.Resampling.NEAREST)
    except Exception:
        # fallback if inv_slot doesn't exist yet
        inv_slot = Image.new("RGBA", (SLOT_SIZE, SLOT_SIZE), (255, 0, 0, 100))
        
    off_grid = Image.new("RGBA", (grid_width, grid_height), (0,0,0,0))
    on_grid = Image.new("RGBA", (grid_width, grid_height), (0,0,0,0))
    
    # Draw empty slots
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            x = c * SLOT_SIZE
            y = r * SLOT_SIZE
            off_grid.paste(inv_slot, (x, y), inv_slot)
            on_grid.paste(inv_slot, (x, y), inv_slot)
            
    # Draw items
    for item in config.get("items", []):
        slot = item.get("slot", 0)
        r = slot // GRID_COLS
        c = slot % GRID_COLS
        if r >= GRID_ROWS:
            continue
            
        x = c * SLOT_SIZE + (SLOT_SIZE - ITEM_SIZE) // 2
        y = r * SLOT_SIZE + (SLOT_SIZE - ITEM_SIZE) // 2
        
        if "off_texture" in item:
            off_img = get_texture(item["off_texture"])
            off_grid.paste(off_img, (x, y), off_img)
            
        if "on_texture" in item:
            on_img = get_texture(item["on_texture"])
            on_grid.paste(on_img, (x, y), on_img)
        
    # Paste grids to bg directly
    grid_x = SIDEBAR_WIDTH
    top_y = 27
    bottom_y = top_y + grid_height + GAP
    
    bg.alpha_composite(off_grid, dest=(grid_x, top_y))
    bg.alpha_composite(on_grid, dest=(grid_x, bottom_y))
    
    # Draw sidebar
    draw = ImageDraw.Draw(bg, 'RGBA')
    try:
        # Try to get a system font or download one
        url = "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        font_bytes = BytesIO(urllib.request.urlopen(req).read())
        font = ImageFont.truetype(font_bytes, 144)
    except Exception:
        font = ImageFont.load_default()
        
    # Draw rotated text
    def draw_rotated_text(text, cx, cy, alpha=255):
        txt_img = Image.new('RGBA', (600, 300), (0, 0, 0, 0))
        txt_draw = ImageDraw.Draw(txt_img)
        try:
            bbox = txt_draw.textbbox((0, 0), text, font=font)
            txt_w = bbox[2] - bbox[0]
            txt_h = bbox[3] - bbox[1]
            x_draw = (600 - txt_w) // 2 - bbox[0]
            y_draw = (300 - txt_h) // 2 - bbox[1]
        except:
            x_draw, y_draw = 150, 80
            
        txt_draw.text((x_draw, y_draw), text, font=font, fill=(255, 255, 255, alpha))
        txt_img = txt_img.rotate(90, expand=1) # becomes 300x600
        # Use alpha_composite to perfectly blend the text into the background
        bg.alpha_composite(txt_img, dest=(int(cx - 150), int(cy - 300)))
        
    draw_rotated_text("OFF", 180, 270, alpha=150)
    draw_rotated_text("ON", 180, 810, alpha=255)
    
    # Load and draw chevron image
    try:
        chevron_path = os.path.join(script_dir, "../images/vback_chevrons_white.png")
        chevron_img = Image.open(chevron_path).convert("RGBA")
        
        # Crop to bounding box of visible pixels to guarantee perfect mathematical centering
        bbox = chevron_img.getbbox()
        if bbox:
            chevron_img = chevron_img.crop(bbox)
            
        chevron_img = chevron_img.rotate(90, expand=1)
        
        # Center the chevron between OFF and ON (cy: 540)
        bg.alpha_composite(chevron_img, dest=(int(180 - chevron_img.width//2), int(540 - chevron_img.height//2)))
    except Exception as e:
        print(f"Failed to load chevron image: {e}")
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    bg.save(OUTPUT_PATH)
    print(f"Saved to {os.path.abspath(OUTPUT_PATH)}")

if __name__ == "__main__":
    main()
