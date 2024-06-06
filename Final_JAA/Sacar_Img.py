import cv2
import numpy as np
import os

# Paths
input_folder = 'Test/CebollaB'  # Path to the folder containing input images
output_folder = 'Train/CebollaB'  # Path to the folder to save rotated images

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List all image files in the input folder
image_files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Iterate over each image file
for image_file in image_files:
    image_path = os.path.join(input_folder, image_file)
    image = cv2.imread(image_path)

    if image is None:
        print(f"Failed to load image {image_path}")
        continue

    # Get the image dimensions
    height, width = image.shape[:2]
    center = (width // 2, height // 2)

    # Create a window to show images
    cv2.namedWindow('Rotated Image', cv2.WINDOW_NORMAL)

    # Rotate the image in increments of 1 degree from -5 to +5 degrees
    for angle in range(-5, 6):
        # Compute the rotation matrix
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        # Apply the rotation to the image
        rotated_image = cv2.warpAffine(image, M, (width, height))
        
        # Show the rotated image
        cv2.imshow('Rotated Image', rotated_image)
        cv2.waitKey(5)  # Wait for 0.5 seconds to view each image

        # Save the rotated image in the output folder
        filename = os.path.join(output_folder, f'{os.path.splitext(image_file)[0]}_rotated_{angle}.jpg')
        cv2.imwrite(filename, rotated_image)

    # Close the image window
    cv2.destroyAllWindows()
