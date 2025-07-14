def compute_area(bbox):
    x1, y1, x2, y2 = bbox
    return (x2 - x1) * (y2 - y1)

def sort_by_smallest(detections):
    return sorted(detections, key=lambda d: compute_area(d["bbox"]))

def crop_with_margin(img, bbox, margin_ratio=0.3):
    h, w = img.shape[:2]
    x1, y1, x2, y2 = bbox
    bw, bh = x2 - x1, y2 - y1
    mx, my = int(bw * margin_ratio), int(bh * margin_ratio)
    x1, y1 = max(x1 - mx, 0), max(y1 - my, 0)
    x2, y2 = min(x2 + mx, w), min(y2 + my, h)
    return img[y1:y2, x1:x2]
