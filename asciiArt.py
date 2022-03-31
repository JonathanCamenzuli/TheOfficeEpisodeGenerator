# Dependencies
from PIL import Image
import pyfiglet

# Get overall ASCII art
def getASCII():
    getIntroLogo()
    getTitle()

# Convert "images/logo.png" into ASCII art
def getIntroLogo():
    # Pass the image as command line argument
    image_path = "images/logo.png"
    img = Image.open(image_path)

    # Resize the image
    width, height = img.size
    aspect_ratio = height / width
    new_width = 110 # orig: 120
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))

    # Convert image to greyscale format
    img = img.convert('L')

    pixels = img.getdata()

    # Replace each pixel with a character from array
    chars = ["@", "O", "#", "$", "%", "&", "*", "!", "~", "·", " "]
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    # Split string of chars into multiple strings of length equal to new width and create a list
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
    print(ascii_image)

# Print "Episode Generator" string
def getTitle():
    bottom_text = pyfiglet.figlet_format("Episode Generator", font = "bubble" )
    print(bottom_text)