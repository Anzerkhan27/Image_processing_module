# main_runner.py

import os
import argparse
from scanner import process_site_image
from utils.image_io import init_output_folder

def main():
    parser = argparse.ArgumentParser(description="Olympus Rover QR Scanner")
    parser.add_argument("image", help="Path to input site image")
    parser.add_argument("--site", required=True, help="Site name (e.g., C1, B2, etc.)")
    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"[ERROR] Image not found: {args.image}")
        return

    # Create output folder per site
    site_dir = init_output_folder(args.site)

    # Process the image
    summary = process_site_image(args.image, site_dir, site_name=args.site)

    # Print summary in console
    print("\n[✅] Summary:")
    for key, val in summary.items():
        print(f"{key:>20}: {val}")

    # PDF and report generation would come here (later)

if __name__ == "__main__":
    main()
