from flask import Flask, render_template, request
from PIL import Image
import PIL
import numpy as np

app = Flask(__name__)

def find_most_common_colors(image_path):
    # Open the image file
    image = Image.open(image_path)
def find_most_common_colors(image_path, num_colors=5):
    image = Image.open(image_path)
    image = image.convert('RGB')  # Convert image to RGB mode

    # Resize the image to a smaller size for faster processing
    image.thumbnail((200, 200))

    # Convert image to a NumPy array
    image_array = np.array(image)

    # Flatten the array to a 2D shape
    flattened_array = image_array.reshape(-1, 3)

    # Count the occurrence of each color
    unique_colors, counts = np.unique(flattened_array, axis=0, return_counts=True)

    # Sort the colors based on their counts in descending order
    sorted_colors = sorted(zip(unique_colors, counts), key=lambda x: x[1], reverse=True)

    # Extract the most common colors
    most_common_colors = sorted_colors[:num_colors]
    print(most_common_colors)
    return most_common_colors

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('index.html', error='No image file provided.')

        file = request.files['image']

        if not file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return render_template('index.html', error='Only image files (JPG, PNG, GIF) are allowed.')

        image_path = 'static/uploaded_image.jpg'
        try:
            file.save(image_path)
        except IOError:
            return render_template('index.html', error='Error saving the uploaded image.')

        try:
            most_common_colors = find_most_common_colors(image_path)
        except PIL.UnidentifiedImageError:
            return render_template('index.html', error='Invalid image file.')

        return render_template('index.html', image_path=image_path, colors=most_common_colors)

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
