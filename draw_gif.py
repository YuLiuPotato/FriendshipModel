import imageio
import os

# Directory containing the PNG images
image_folder = 'graph/friend_ship_net'

# Output file path for the GIF animation
output_path = 'output_dis_net.gif'

# Create a list to store the image file names
images = []

# Loop through the PNG images in the directory
for filename in sorted(os.listdir(image_folder)):
    if filename.endswith('.png'):
        file_path = os.path.join(image_folder, filename)
        images.append(imageio.imread(file_path))

# Save the list of images as a GIF animation
imageio.mimsave(output_path, images, duration=0.1)
