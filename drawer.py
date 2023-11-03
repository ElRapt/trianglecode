from PIL import Image, ImageDraw
from encoder import encode_message_in_triangle

def calculate_and_draw_cells(draw, triangle_size, cell_size, levels):
    for level in range(levels):
        for i in range(level + 1):
            cell_x = triangle_size // 2 - (level + 1) * cell_size // 2 + i * cell_size
            cell_y = level * cell_size
            points = [(cell_x, cell_y), (cell_x + cell_size // 2, cell_y + cell_size), (cell_x - cell_size // 2, cell_y + cell_size)]
            draw.polygon(points, fill=1)

def generate_img(levels, cell_size):
    triangle_size = levels * cell_size
    img = Image.new('RGB', (triangle_size, triangle_size), color=(200,200,200))
    draw = ImageDraw.Draw(img)
    
    calculate_and_draw_cells(draw, triangle_size, cell_size, levels)

    return img

def show_triangle(levels, cell_size, message_bits, triangle_size):
    img = generate_img(levels, cell_size)
    encode_message_in_triangle(message_bits, img, cell_size, levels, triangle_size)
    img.show()
    return img