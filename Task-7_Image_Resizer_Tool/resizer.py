import os
from PIL import Image

# Set folder paths
input_folder = 'input_images'
output_folder = 'resized_images'
new_size = (300, 300)  # Resize to 300x300 pixels

# Create output folder if not present
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Resize and save images
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            img = Image.open(input_path)
            img_resized = img.resize(new_size)
            img_resized.save(output_path)
            print(f"✅ Resized and saved: {filename}")
        except Exception as e:
            print(f"❌ Error with {filename}: {e}")
