# image_processing/qr_generator.py

import cv2
import os
import random
import numpy as np

class QRGenerator:
    def __init__(self, config):
        self.config = config
        self.background_size = config["background_size"]
        self.qr_code_size = config["qr_code_size"]
        self.qr_min_size = config["qr_min_size"]
        self.qr_max_size = config["qr_max_size"]
        self.qr_folder = config["qr_images_folder"]
        self.output_folder = config["output_folder"]
        self.output_image = config["output_image"]
        self.num_qr_codes = config["num_qr_codes"]

        os.makedirs(self.output_folder, exist_ok=True)

    def _load_qr_images(self):
        qr_files = [
            os.path.join(self.qr_folder, f)
            for f in os.listdir(self.qr_folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        if len(qr_files) < self.num_qr_codes:
            raise ValueError("Not enough QR images in the folder!")
        selected_qrs = random.sample(qr_files, self.num_qr_codes)
        return [cv2.imread(qr, cv2.IMREAD_UNCHANGED) for qr in selected_qrs]

    def generate_fixed(self):
        """Generate an image with fixed-size QR codes randomly placed on a white background."""
        background = np.ones((self.background_size[1], self.background_size[0], 3), dtype=np.uint8) * 255
        qr_images = self._load_qr_images()
        placed_positions = []

        for qr_img in qr_images:
            qr_img = cv2.resize(qr_img, self.qr_code_size)

            # Place QR without overlap
            while True:
                x = random.randint(0, self.background_size[0] - self.qr_code_size[0])
                y = random.randint(0, self.background_size[1] - self.qr_code_size[1])
                overlap = any(abs(x - px) < self.qr_code_size[0] and abs(y - py) < self.qr_code_size[1]
                              for px, py in placed_positions)
                if not overlap:
                    placed_positions.append((x, y))
                    break

            background[y:y+self.qr_code_size[1], x:x+self.qr_code_size[0]] = qr_img

        cv2.imwrite(self.output_image, background)
        print(f"✅ Fixed QR image saved at {self.output_image}")

    def generate_random(self):
        """Generate an image with randomly-sized QR codes."""
        background = np.ones((self.background_size[1], self.background_size[0], 3), dtype=np.uint8) * 255
        qr_images = self._load_qr_images()
        placed_boxes = []

        for qr_img in qr_images:
            random_size = random.randint(self.qr_min_size, self.qr_max_size)
            qr_resized = cv2.resize(qr_img, (random_size, random_size))

            for _ in range(100):
                x = random.randint(0, self.background_size[0] - random_size)
                y = random.randint(0, self.background_size[1] - random_size)
                new_box = (x, y, random_size, random_size)

                if all(
                    not (x < bx + bw and x + random_size > bx and y < by + bh and y + random_size > by)
                    for bx, by, bw, bh in placed_boxes
                ):
                    placed_boxes.append(new_box)
                    break
            else:
                print("⚠ Skipping one QR due to overlapping issues.")
                continue

            # Alpha blending if present
            if qr_resized.shape[2] == 4:
                alpha = qr_resized[:, :, 3] / 255.0
                for c in range(3):
                    background[y:y+random_size, x:x+random_size, c] = (
                        alpha * qr_resized[:, :, c] +
                        (1 - alpha) * background[y:y+random_size, x:x+random_size, c]
                    )
            else:
                background[y:y+random_size, x:x+random_size] = qr_resized

        cv2.imwrite(self.output_image, background)
        print(f"✅ Random QR image saved at {self.output_image}")
