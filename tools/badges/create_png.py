from PIL import Image, ImageDraw, ImageFont
import freetype as ft
import uharfbuzz as hb
import math
import subprocess

# Regular font
# kerning_overrides = {
#    ("A", "T"): -6.11,
#    ("D", "A"): -2.45,
#    ("O", "V"): -2.42,
#    ("P", "A"): -5.31,
#    ("T", "O"): -2.14,
#}

# Bold font
kerning_overrides = {
    ("O", "V"): -2.88,
    ("A", "S"): -1.09,
    ("D", "A"): -3.02,
    ("T", "O"): -2.28,
    ("A", "T"): -6.39,
    ("P", "A"): -5.97,
}

def shape_text(text, font_path, size_pt):
    face = ft.Face(font_path)
    face.set_char_size(size_pt * 64)
    with open(font_path, "rb") as f:
        fontdata = f.read()
    hb_face = hb.Face(fontdata)
    hb_font = hb.Font(hb_face)
    hb_font.scale = (face.size.ascender, face.size.ascender)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf)
    return buf.glyph_infos, buf.glyph_positions

def draw_badge(project_text, badge_text, badge_color,
               font_project_path="Inter-Bold.ttf",
               font_title_path="Inter-Bold.ttf",
               output_path="badge_output.png"):
    colors = {"1": "red", "2": "blue", "3": "purple"}
    badge_color = colors.get(badge_color, "red")
    template_path = f"badge_{badge_color}.png"

    image = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(image)

    font_project = ImageFont.truetype(font_project_path, 88)
    project_lines = project_text.upper().split()
    line_height = font_project.getbbox("Hg")[3]
    total_height = len(project_lines) * line_height
    y_start = 312 - total_height // 2
    for i, line in enumerate(project_lines):
        line_width = font_project.getlength(line)
        draw.text(((1024 - line_width) / 2, y_start + i * line_height), line, font=font_project, fill="white")

    font_size = 72
    base_y = 600
    amplitude = 20
    center_x = 512
    badge_width = 1024
    base_kerning_pt = 72

    title_text = badge_text.upper()
    infos, positions = shape_text(title_text, font_title_path, font_size)
    total_width = sum(p.x_advance for p in positions) / 64.0
    layout_x = center_x - total_width / 2.0
    prev_char = ""

    face = ft.Face(font_title_path)
    face.set_char_size(font_size * 64)

    for i, (info, pos) in enumerate(zip(infos, positions)):
        glyph_id = info.codepoint
        x_advance = pos.x_advance / 64.0
        x_offset = pos.x_offset / 64.0
        y_offset = pos.y_offset / 64.0

        raw_adjust = kerning_overrides.get((prev_char, chr(info.codepoint)), 0.0)
        kerning_adjust = raw_adjust * (font_size / base_kerning_pt)
        effective_x = layout_x + x_offset + kerning_adjust

        face.load_glyph(glyph_id, ft.FT_LOAD_RENDER | ft.FT_LOAD_TARGET_NORMAL)
        bitmap = face.glyph.bitmap
        width = bitmap.width
        height = bitmap.rows

        prev_char = chr(info.codepoint)

        rel_x = (effective_x + width / 2.0) - center_x
        curve_y_offset = -amplitude * math.cos((rel_x / (badge_width / 2.0)) * math.pi / 2.0)
        curve_y = base_y + curve_y_offset
        dy = amplitude * math.pi / badge_width * math.sin((rel_x / (badge_width / 2.0)) * math.pi / 2.0)
        angle = math.degrees(math.atan2(dy, 1.0))

        char_img = Image.frombuffer("L", (width, height), bytes(bitmap.buffer), "raw", "L", 0, 1)
        rgba = Image.merge("RGBA", (
            Image.new("L", char_img.size, 0), 
            Image.new("L", char_img.size, 0),
            Image.new("L", char_img.size, 0),
            char_img
        ))

        box_w, box_h = width * 2, height * 2
        padded = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
        padded.paste(rgba, ((box_w - width) // 2, (box_h - height) // 2))
        rotated = padded.rotate(-angle, resample=Image.BICUBIC, center=(box_w // 2, box_h // 2))

        px = int(round(effective_x - (box_w - width) / 2))
        py = int(round(curve_y - box_h / 2 + y_offset))
        image.alpha_composite(rotated, dest=(px, py))

        layout_x += x_advance

    image = image.resize((256, 256), resample=Image.LANCZOS)
    image.save(output_path)
    subprocess.run(["open", output_path])

if __name__ == "__main__":
    project = input("Enter project name: ")
    title = input("Enter badge title: ")
    print("Choose badge color:")
    print("1. Red\n2. Blue\n3. Purple")
    color_choice = input("Enter number (1-3): ").strip()
    draw_badge(project, title, color_choice)
