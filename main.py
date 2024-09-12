import cv2 # type: ignore 

# Path to the input image
image_path = '/Vision-Bot/NHRL-Sept-2022.jpg'

# Read the image in color
color_image = cv2.imread(image_path)

# Convert the color image to grayscale
gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

# Save the grayscale image
output_path = 'path/to/save/black_and_white_image.jpg'
cv2.imwrite(output_path, gray_image)

# Display the original and grayscale images
cv2.imshow('Original Image', color_image)
cv2.imshow('Black and White Image', gray_image)

# Wait for a key press and close the image windows
cv2.waitKey(0)
cv2.destroyAllWindows()
