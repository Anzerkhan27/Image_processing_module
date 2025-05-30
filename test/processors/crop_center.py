from test.utils.image_io import save_image

def crop_center(img, scale=0.5):
    h, w = img.shape[:2]
    new_w, new_h = int(w * scale), int(h * scale)
    start_x, start_y = (w - new_w) // 2, (h - new_h) // 2
    cropped = img[start_y:start_y + new_h, start_x:start_x + new_w]
    save_image(cropped, "01_crop_raw.jpg")
    return cropped, start_x, start_y
