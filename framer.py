from PIL import Image, ImageDraw, ImageFont

def circular_crop(image, size=(200, 200)):
    """
    Crops the given image into a circular shape.
    """
    image = image.resize(size, resample=Image.LANCZOS)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    circular_img = Image.new('RGBA', size, (0, 0, 0, 0))
    circular_img.paste(image, (0, 0), mask=mask)
    return circular_img

def place_logo(base_img, logo_path, position=(25, 25), logo_size=(120, 120)):
    """
    Opens a logo, resizes it, and pastes it onto base_img.
    """
    logo = Image.open(logo_path).convert("RGBA")
    logo = logo.resize(logo_size, resample=Image.LANCZOS)
    base_img.paste(logo, position, logo)

def create_frame(
    output_path,
    main_image_path,
    rocket_logo_path,
    team_logo_path,
    person_name="Name Placeholder",
    person_role="Role Placeholder",
    bg_color=(0, 0, 0),
    frame_size=(400, 500),
    circle_size=(200, 200),
    circle_position=None,
    rocket_logo_position=(25, 25),
    rocket_logo_size=(120, 120),
    team_logo_position=(150, 450),
    team_logo_size=(100, 25),
    font_path=None
):
    """
    Creates the final frame with a circular cutout for the person's image,
    logos, and center-aligned text placeholders for name and role.
    """
    base_img = Image.new("RGB", frame_size, bg_color)

    # Default circle position (centered, slightly above the vertical center)
    if circle_position is None:
        circle_x = (frame_size[0] - circle_size[0]) // 2
        circle_y = (frame_size[1] - circle_size[1]) // 2 - 50
        circle_position = (circle_x, circle_y)

    # Open and circular-crop the main person's image
    main_image = Image.open(main_image_path).convert("RGB")
    circular_person = circular_crop(main_image, circle_size)
    base_img.paste(circular_person, circle_position, circular_person)

    # Place the rocket logo
    place_logo(base_img, rocket_logo_path, rocket_logo_position, rocket_logo_size)

    # Place the team logo
    place_logo(base_img, team_logo_path, team_logo_position, team_logo_size)

    # Prepare for drawing text
    draw = ImageDraw.Draw(base_img)

    # Setup fonts; if no custom font is provided, use default.
    if font_path:
        font_name = ImageFont.truetype(font_path, 20)  # For the name
        font_role = ImageFont.truetype(font_path, 15)  # For the role
    else:
        font_name = ImageFont.load_default()
        font_role = ImageFont.load_default()

    # Calculate bounding box for the name text
    bbox_name = font_name.getbbox(person_name)
    text_width_name = bbox_name[2] - bbox_name[0]
    text_height_name = bbox_name[3] - bbox_name[1]
    name_x = (frame_size[0] - text_width_name) // 2
    name_y = circle_position[1] + circle_size[1] + 20
    draw.text((name_x, name_y), person_name, font=font_name, fill=(255, 255, 255))

    # Calculate bounding box for the role text
    bbox_role = font_role.getbbox(person_role)
    text_width_role = bbox_role[2] - bbox_role[0]
    text_height_role = bbox_role[3] - bbox_role[1]
    role_x = (frame_size[0] - text_width_role) // 2
    role_y = name_y + text_height_name + 10
    draw.text((role_x, role_y), person_role, font=font_role, fill=(200, 200, 200))

    base_img.save(output_path, format="PNG")
    print(f"Frame created and saved to {output_path}")


# Example usage:
if __name__ == "__main__":
    create_frame(
        output_path="team_images/example_output.png",
        main_image_path="team_images/person.jpg",       # Replace with actual path
        rocket_logo_path="team_images/rocket_logo.png", # Replace with actual path
        team_logo_path="team_images/team_ray_logo.jpg", # Replace with actual path
        person_name="Anzer Khan",
        person_role="Software Engineer",
        # Optionally customize positions, sizes, or font_path here
    )
