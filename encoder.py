import math
from reedsolo import RSCodec, ReedSolomonError
from PIL import Image, ImageDraw


def encode_and_draw_cells(encoded_message, draw, triangle_size, cell_size, levels):
    bit_index = 0
    for level in range(levels):
        for i in range(level + 1):
            if bit_index < len(encoded_message) * 8:
                byte_index = bit_index // 8
                bit_position = bit_index % 8
                bit = (encoded_message[byte_index] >> (7 - bit_position)) & 1

                cell_x = triangle_size // 2 - (level + 1) * cell_size // 2 + i * cell_size
                cell_y = level * cell_size
                points = [(cell_x, cell_y), (cell_x + cell_size // 2, cell_y + cell_size), (cell_x - cell_size // 2, cell_y + cell_size)]

                if bit:
                    draw.polygon(points, fill=(255, 255, 255))
                else:
                    draw.polygon(points, fill=(0, 0, 0))

                bit_index += 1

def encode_message_in_triangle(message, img, cell_size, levels, triangle_size):
    rs = RSCodec(10)
    encoded_message = rs.encode(bytearray(message, 'utf-8'))

    draw = ImageDraw.Draw(img)
    encode_and_draw_cells(encoded_message, draw, triangle_size, cell_size, levels)

