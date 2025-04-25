# image_processing/config.py

CONFIG = {
    "background_size": (600, 600),              # Width x Height
    "qr_code_size": (150, 150),                 # Fixed size for QR code (used in fixed generator)
    "qr_min_size": 100,                         # Minimum size for random QR codes
    "qr_max_size": 200,                         # Maximum size for random QR codes
    "qr_images_folder": "assets/qr_dataset",           # Folder containing original QR images
    "output_folder": "qr_code_images",          # Output folder for generated images
    "output_image": "qr_code_images/generated_qr_image.png",  # Final output path
    "num_qr_codes": 8,                          # Number of QR codes to generate
    "cropped_output_folder": "cropped_qr_codes",# Folder to save cropped QR codes
    "default_image_name": "generated_qr_image.png",
    "sliding_window_size": 200,
    "sliding_stride": 50,
    "margin": 10                                 # Margin for cropping detected QR codes
}
