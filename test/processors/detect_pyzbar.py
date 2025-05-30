from pyzbar.pyzbar import decode

def decode_qr(img):
    decoded = decode(img)
    results = []
    for obj in decoded:
        results.append({
            "data": obj.data.decode("utf-8"),
            "points": [(pt.x, pt.y) for pt in obj.polygon]
        })
    return results
