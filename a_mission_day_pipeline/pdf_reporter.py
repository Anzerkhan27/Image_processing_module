# pdf_reporter.py

import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PIL import Image


def draw_summary(c, summary):
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, 800, f"Olympus QR Site Report – Site: {summary['site']}")

    c.setFont("Helvetica", 12)
    c.drawString(40, 780, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(40, 760, f"Total QR Codes Detected: {summary['total_detected']}")
    c.drawString(40, 740, f"Submitted QR Index: {summary['submitted_qr_index']}")

    submitted = summary['regions'][summary['submitted_qr_index'] - 1]

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, 710, "Submitted QR Details:")

    c.setFont("Helvetica", 12)
    c.drawString(60, 690, f"Decoded: {'Yes' if submitted['decoded'] else 'No'}")
    c.drawString(60, 675, f"Data: {submitted['data'] if submitted['decoded'] else 'UNREADABLE'}")
    c.drawString(60, 660, f"Decoder: {submitted['decoder'] or 'N/A'}")
    c.drawString(60, 645, f"BBox: {submitted['bbox']}")
    c.drawString(60, 630, f"Area: {submitted['area']} pixels²")


def draw_image(c, img_path, y_offset=580):
    if not os.path.exists(img_path):
        c.drawString(40, y_offset, "[ERROR] Annotated image not found.")
        return

    try:
        img = Image.open(img_path)
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.ANTIALIAS  # for older Pillow versions

        img.thumbnail((500, 500), resample)

        img_io = ImageReader(img)

        x = 40
        y = y_offset - img.height
        c.drawImage(img_io, x, y)
    except Exception as e:
        c.drawString(40, y_offset, f"[ERROR] Failed to load image: {str(e)}")


def generate_report(site_folder):
    print(f"[INFO] Generating report for: {site_folder}")
    
    summary_path = os.path.join(site_folder, "summary.json")
    annotated_path = os.path.join(site_folder, "annotated.jpg")
    output_pdf = os.path.join(site_folder, f"{os.path.basename(site_folder)}_report.pdf")

    print(f"[INFO] Looking for summary: {summary_path}")
    print(f"[INFO] Looking for image: {annotated_path}")

    if not os.path.exists(summary_path):
        print(f"[ERROR] summary.json not found.")
        return

    with open(summary_path, 'r') as f:
        summary = json.load(f)

    print(f"[INFO] Loaded summary.json. Drawing report...")

    c = canvas.Canvas(output_pdf, pagesize=A4)
    draw_summary(c, summary)
    draw_image(c, annotated_path)
    c.save()

    print(f"[✅] PDF report saved: {output_pdf}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python pdf_reporter.py <path_to_site_folder>")
    else:
        site_folder = sys.argv[1]
        generate_report(site_folder)
