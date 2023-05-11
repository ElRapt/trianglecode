from PIL import Image, ImageDraw
import textwrap
import numpy as np
from reedsolo import RSCodec, ReedSolomonError
import math

def create_triangle_code_image(levels, cell_size):
    triangle_size = levels * cell_size
    img = Image.new('RGB', (triangle_size, triangle_size), color=(200,200,200))
    draw = ImageDraw.Draw(img)

    # Dessiner les cellules du TriangleCode
    for level in range(levels):
        for i in range(level + 1):
            cell_x = triangle_size // 2 - (level + 1) * cell_size // 2 + i * cell_size
            cell_y = level * cell_size
            points = [(cell_x, cell_y), (cell_x + cell_size // 2, cell_y + cell_size), (cell_x - cell_size // 2, cell_y + cell_size)]
            draw.polygon(points, fill=1)
    
    return img

def message_to_bits(message):
    return ''.join(format(c, '08b') for c in message)

def bits_to_message(bits):
    return bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

def bits_to_bytes(bits):
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte_array.append(int(bits[i:i+8], 2))
    return byte_array


def bytes_to_string(byte_array):
    return byte_array.decode('utf-8')

def required_levels(message_bits):
    return int(math.ceil((-1 + math.sqrt(1 + 8 * len(message_bits))) / 2))

def encode_message_in_triangle(message, img, cell_size):
    # Encode the message with Reed-Solomon
    rs = RSCodec(20)  # Use 20 bytes of redundancy
    message_encoded = rs.encode(bytearray(message, 'utf-8'))

    draw = ImageDraw.Draw(img)
    bit_index = 0

    for level in range(levels):
        for i in range(level + 1):
            if bit_index < len(message_encoded) * 8:
                byte_index = bit_index // 8
                bit_position = bit_index % 8
                bit = (message_encoded[byte_index] >> (7 - bit_position)) & 1

                cell_x = triangle_size // 2 - (level + 1) * cell_size // 2 + i * cell_size
                cell_y = level * cell_size
                points = [(cell_x, cell_y), (cell_x + cell_size // 2, cell_y + cell_size), (cell_x - cell_size // 2, cell_y + cell_size)]

                # If bit is 1, fill the cell with white; otherwise, fill it with black.
                if bit:
                    draw.polygon(points, fill=(255, 255, 255))
                else:
                    draw.polygon(points, fill=(0, 0, 0))

                bit_index += 1
    print("Encoded message length:", len(message_encoded))
    print("Encoded message content:", message_encoded)



def decode_message_from_triangle(img, cell_size):
    img_width, img_height = img.size
    triangle_size = img_width
    levels = required_levels((message_encoded))

    bit_list = []
    for level in range(levels):
        for i in range(level + 1):
            cell_x = triangle_size // 2 - (level + 1) * cell_size // 2 + i * cell_size
            cell_y = level * cell_size
            points = [(cell_x, cell_y), (cell_x + cell_size // 2, cell_y + cell_size), (cell_x - cell_size // 2, cell_y + cell_size)]

            pixel_values = [img.getpixel(point)[0] for point in points]
            avg_pixel_value = sum(pixel_values) / len(pixel_values)
            bit = 1 if avg_pixel_value > 128 else 0

            bit_list.append(bit)

    message_bits = ''.join(str(bit) for bit in bit_list)
    message_bytes = bits_to_bytes(message_bits)
    
    # Print the message bytes for debugging purposes
    print("Message bytes length:", len(message_bytes))
    print("Message bytes content:", message_bytes)

    # Decode the message with Reed-Solomon
    rs = RSCodec(40)
    try:
        message_decoded = rs.decode(message_bytes)[0]
        print("Decoded message length:", message_decoded)
        print("Decoded message content:", message_decoded)
    except ReedSolomonError as e:
        print("ReedSolomonError:", str(e))
        return None

    return message_bits

def test_encoding_decoding(encoded_bytes):
    rs = RSCodec(40)

    try:
        decoded_bytes = rs.decode(encoded_bytes)[0]
        print("Decoded message length:", len(decoded_bytes))
        print("Decoded message content:", decoded_bytes)
    except ReedSolomonError as e:
        print("ReedSolomonError:", str(e))
        return None

    return bytes_to_string(decoded_bytes)




    


cell_size = 20

message = "Lucas"
rs = RSCodec(40)  # Utiliser 40 octets de redondance

# Encode the message with Reed-Solomon
message_encoded = rs.encode(bytearray(message, 'utf-8'))

message_bits = message_to_bits(message_encoded)
levels = required_levels(message_bits)
triangle_size = levels * cell_size

img = create_triangle_code_image(levels, cell_size)
encode_message_in_triangle(message_bits, img, cell_size)
img.show()

# Tester le décodage sur l'image du TriangleCode générée précédemment
decoded_message = test_encoding_decoding(message_encoded)
print("Decoded message:", decoded_message)