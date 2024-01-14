import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
font = ImageFont.truetype("arialbd.ttf", size=22)

def text_to_image(text):
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    # Draw a white background
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    # set text
    (font_width, font_height) = font.getsize(text)
    text_pos_x = oled.width // 2 - font_width // 2 
    text_pos_y = oled.height // 2 - font_height // 2  
    draw.text(
        (text_pos_x, text_pos_y),
        text,
        font=font,
        fill=255,
    )
    return image 

def draw_image(image): 
    oled.image(image) 
    oled.show() 

def draw_text(text): 
    print(f"[oled] draw text = {text}")
    draw_image(text_to_image(text))
