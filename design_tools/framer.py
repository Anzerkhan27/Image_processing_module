from PIL import Image, ImageDraw, ImageFont

def circular_crop(image, size=(200, 200)):
    image = image.resize(size, resample=Image.LANCZOS)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    circular_img = Image.new('RGBA', size, (0, 0, 0, 0))
    circular_img.paste(image, (0, 0), mask=mask)
    return circular_img

def place_logo(base_img, logo_path, position=(0, 0), logo_size=(120, 120), rotation=0):
    logo = Image.open(logo_path).convert("RGBA")
    if rotation != 0:
        logo = logo.rotate(rotation, expand=True, resample=Image.NEAREST)
    logo = logo.resize(logo_size, resample=Image.LANCZOS)
    base_img.paste(logo, position, logo)


def square_crop(image, size=(200, 200)):
    # Get original dimensions
    w, h = image.size
    # Crop a square that spans the full width (for portrait images)
    if h > w:
        top = (h - w) // 2
        box = (0, top, w, top + w)
    else:
        # In case of a landscape image, crop horizontally to get a centered square
        left = (w - h) // 2
        box = (left, 0, left + h, h)
    cropped = image.crop(box)
    cropped = cropped.resize(size, resample=Image.LANCZOS)
    return cropped

   
def create_frame(
    output_path,
    main_image_path,
    rocket_logo_path,
    team_logo_path,
    person_name="Name Placeholder",
    person_role="Role Placeholder",
    person_extra="Third Text Field",
    bg_color=(0, 0, 0),
    frame_size=(400, 500),
    circle_size=(220, 220),
    circle_position=None,
    # Rocket logo params
    rocket_logo_position=(10, 10),
    rocket_logo_size=(120, 120),
    # Team logo params
    team_logo_size=(200, 50),  # Already doubled in size
    # Font
    font_path="arial.ttf"
):
    base_img = Image.new("RGB", frame_size, bg_color)

    # Position the circular image
    if circle_position is None:
        circle_x = (frame_size[0] - circle_size[0]) // 2
        circle_y = (frame_size[1] - circle_size[1]) // 2 - 50
        circle_position = (circle_x, circle_y)

    # Open & circular-crop the main image
    main_image = Image.open(main_image_path).convert("RGB")
  #  circular_person = circular_crop(main_image, circle_size)
  #  base_img.paste(circular_person, circle_position, circular_person)
    squared_person = square_crop(main_image, circle_size)
    base_img.paste(squared_person, circle_position)

    # Place rocket logo (top-left)
    # Place rocket logo (top-left) with a slight tilt to the right
    place_logo(base_img, rocket_logo_path, rocket_logo_position, rocket_logo_size, rotation=-15)


    # Place team logo (centered at the bottom)
    # Calculate center-x for the team logo
    team_logo_x = (frame_size[0] - team_logo_size[0]) // 2
    # Position it near the bottom, leaving some padding
    team_logo_y = frame_size[1] - team_logo_size[1] - 20
    place_logo(base_img, team_logo_path, (team_logo_x, team_logo_y), team_logo_size)
    

    # Prepare for drawing text
    draw = ImageDraw.Draw(base_img)
    try:
        font_name = ImageFont.truetype(font_path, 20)  # Larger name
        font_role = ImageFont.truetype(font_path, 15)  # Role & extra
    except IOError:
        # Fallback if TTF not found
        font_name = ImageFont.load_default()
        font_role = ImageFont.load_default()

    # --- Name ---
    bbox_name = font_name.getbbox(person_name)
    text_width_name = bbox_name[2] - bbox_name[0]
    text_height_name = bbox_name[3] - bbox_name[1]
    name_x = (frame_size[0] - text_width_name) // 2
    name_y = circle_position[1] + circle_size[1] + 20
    draw.text((name_x, name_y), person_name, font=font_name, fill=(255, 255, 255))

    # --- Role ---
    bbox_role = font_role.getbbox(person_role)
    text_width_role = bbox_role[2] - bbox_role[0]
    text_height_role = bbox_role[3] - bbox_role[1]
    role_x = (frame_size[0] - text_width_role) // 2
    role_y = name_y + text_height_name + 10
    draw.text((role_x, role_y), person_role, font=font_role, fill=(200, 200, 200))

    # --- Extra Field ---
    bbox_extra = font_role.getbbox(person_extra)
    text_width_extra = bbox_extra[2] - bbox_extra[0]
    text_height_extra = bbox_extra[3] - bbox_extra[1]
    extra_x = (frame_size[0] - text_width_extra) // 2
    extra_y = role_y + text_height_role + 10
    draw.text((extra_x, extra_y), person_extra, font=font_role, fill=(200, 200, 200))

    base_img.save(output_path, format="PNG")
    print(f"Frame created and saved to {output_path}")

# Example usage:
if __name__ == "__main__":
    create_frame(
        output_path="assets/team_images/kanum.png",
        main_image_path="team_images/person3.jpg",       # Replace with actual path
        rocket_logo_path="team_images/rocket_logo.png", # Replace with actual path
        team_logo_path="team_images/team_ray_logo.jpg", # Replace with actual path
        person_name="Kanum Ullah",
        person_role="Mechanical Engineer",
        person_extra="Project name: RV01 Haytham",         # Third text field
        font_path="arial.ttf"
        # Optionally customize positions, sizes, or font_path here
    )
