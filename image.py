import random
import os,json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Define constants for layout
IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 1000
TITLE_Y = 30
QUESTION_Y = 150
OPTIONS_START_Y = 400
ANSWER_Y = 850
CIRCLE_RADIUS = 30
MAX_TEXT_WIDTH = 990
GRID_CELL_WIDTH = 350

# Load fonts (adjust paths to match your environment)
bangla_question_font = ImageFont.truetype("kalpurush.ttf", 60)
eng_question_font = ImageFont.truetype("Montserrat-ExtraBold.ttf", 60)
option_font = ImageFont.truetype("Montserrat-ExtraBold.ttf", 40)
label_font = ImageFont.truetype("Helvetica-Bold.ttf", 50)
copyright_font = ImageFont.truetype("Tinos-Italic.ttf", 40)

# Lists of gradient colors
gradient_white = [
    ('#3B1E54', '#9B7EBD'),
    ('#091057', "#091057"),
    ("#789DBC", "#789DBC"),
    ("#222831", "#222831"),
    ("#112D4E", "#112D4E"), 
    ("#522546", "#522546"),
    
]

option_colors = ['#1ABC9C', '#2ECC71', '#3498DB', '#9B59B6', '#34495E']

def get_random_gradient():
    return random.choice(gradient_white), "white"

def apply_gradient(draw, img_width, img_height, color1, color2):
    for i in range(img_height):
        r = int(int(color1[1:3], 16) + (int(color2[1:3], 16) - int(color1[1:3], 16)) * i / img_height)
        g = int(int(color1[3:5], 16) + (int(color2[3:5], 16) - int(color1[3:5], 16)) * i / img_height)
        b = int(int(color1[5:7], 16) + (int(color2[5:7], 16) - int(color1[5:7], 16)) * i / img_height)
        draw.line([(0, i), (img_width, i)], fill=(r, g, b), width=1)

def draw_centered_text(draw, text, font, width, y, color, max_width=MAX_TEXT_WIDTH):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and draw.textlength(line + words[0], font=font) <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line.strip())
    for line in lines:
        text_width = draw.textlength(line, font=font)
        x = (width - text_width) / 2
        draw.text((x, y), line, font=font, fill=color)
        y += font.size + 5

def draw_vertical_options(draw, options, start_y, img_width, circle_color, text_color):
    y_offset = start_y
    for key, value in options.items():
        circle_x = img_width // 2 - 250
        circle_y = y_offset + 20
        draw.ellipse(
            (circle_x - CIRCLE_RADIUS, circle_y - CIRCLE_RADIUS, 
             circle_x + CIRCLE_RADIUS, circle_y + CIRCLE_RADIUS),
            fill=circle_color
        )
        label_width = draw.textlength(key, font=label_font)
        label_x = circle_x - label_width / 2
        label_y = circle_y - label_font.size / 2
        draw.text((label_x, label_y), key, font=label_font, fill=text_color)
        draw.text((circle_x + 50, y_offset), value, font=option_font, fill=text_color)
        y_offset += 70

def draw_grid_options(draw, options, start_y, img_width, circle_color, text_color):
    num_columns = 2
    cell_height = 80
    padding = 10
    for idx, (key, value) in enumerate(options.items()):
        row = idx // num_columns
        col = idx % num_columns
        cell_x = (img_width - (num_columns * GRID_CELL_WIDTH + (num_columns - 1) * padding)) / 2 + col * (GRID_CELL_WIDTH + padding)
        cell_y = start_y + row * (cell_height + padding)
        circle_x = cell_x + 40
        circle_y = cell_y + cell_height // 2
        draw.ellipse(
            (circle_x - CIRCLE_RADIUS, circle_y - CIRCLE_RADIUS, 
             circle_x + CIRCLE_RADIUS, circle_y + CIRCLE_RADIUS),
            fill=circle_color
        )
        label_width = draw.textlength(key, font=label_font)
        label_x = circle_x - label_width / 2
        label_y = circle_y - label_font.size / 2
        draw.text((label_x, label_y), key, font=label_font, fill=text_color)
        draw.text((circle_x + 50, cell_y + cell_height // 4), value, font=option_font, fill=text_color)

def can_use_grid_layout(draw, options):
    for value in options.values():
        if draw.textlength(value, font=option_font) > GRID_CELL_WIDTH - 50:
            return False
    return True

def generate_mcq_image(question, options, output_filename="mcqImage/mcq_image.png"):
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color=(255, 255, 255))
    img = img.filter(ImageFilter.SHARPEN)
    draw = ImageDraw.Draw(img)
    
    gradient_colors, text_color = get_random_gradient()
    apply_gradient(draw, img.width, img.height, *gradient_colors)
    
    if any(ord(char) > 127 for char in question):
        question_font = bangla_question_font
    else:
        question_font = eng_question_font
    
    circle_color = random.choice(option_colors)
    
    draw_centered_text(draw, "MCQ Challenge", label_font, img.width, TITLE_Y, text_color)
    draw_centered_text(draw, question, question_font, img.width, QUESTION_Y, text_color)
    
    if random.choice([True, False]) and can_use_grid_layout(draw, options):
        draw_grid_options(draw, options, start_y=OPTIONS_START_Y, img_width=img.width, circle_color=circle_color, text_color=text_color)
    else:
        draw_vertical_options(draw, options, start_y=OPTIONS_START_Y, img_width=img.width, circle_color=circle_color, text_color=text_color)
    
    draw_centered_text(draw, f"© Admission English Helpline", copyright_font, img.width, ANSWER_Y, text_color)
    img.save(output_filename)
    print(f"Image saved as {output_filename}")

# Function to process JSON data and generate images
def process_json_file(json_filename):
    with open(json_filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for entry in data:
            question_no = entry.get('id')
            question = entry.get('question')
            options = {chr(65 + i): opt.split(": ")[1] for i, opt in enumerate(entry.get('options', []))}
            output_filename = f"mcqImage/mcq_image_{question_no}.png"
            generate_mcq_image(question, options, output_filename)

# Example JSON data file
json_filename = 'questions.json'
process_json_file(json_filename)