from reedsolo import RSCodec, ReedSolomonError
from PIL import Image, ImageDraw
from calculator import bytes_to_string, bits_to_bytes, bits_to_message


def decode_message_from_triangle(img, img_width, img_height, levels, triangle_size, cell_size, bit_list):
    for level in range(levels):

        for i in range(level + 1):
            cell_x = triangle_size // 2 - (level + 1) * cell_size // 2 + i * cell_size
            cell_y = level * cell_size
            point = (cell_x + cell_size // 2, cell_y + cell_size // 2)

            if 0 <= point[0] < img_width and 0 <= point[1] < img_height:
                pixel_value = img.getpixel(point)[0]
                bit = 1 if pixel_value > 128 else 0
                bit_list.append(bit)
    
    while len(bit_list) % 8 != 0:
        bit_list.append(0)

    return bits_to_bytes(bit_list)


def decode_message_from_message(encoded_bytes):
    rs = RSCodec(10)
    try:
        decoded_bytes = rs.decode(encoded_bytes)[0]
    except ReedSolomonError as e:
        print("ReedSolomonError :", str(e))
        return None
    return bytes_to_string(decoded_bytes)

def decode_message_from_triangle(img, cell_size):
    img_width, img_height = img.size
    triangle_size = min(img_width, img_height)
    levels = img.size[0] // cell_size
    bit_list = []

    byte_array = decode_message_from_triangle(img, img_width, img_height, levels, triangle_size, cell_size, bit_list)

    rs = RSCodec(10)
    try:
        message_decoded = rs.decode(byte_array)
        message = bytes_to_string(message_decoded)
    except ReedSolomonError as e:
        print("ReedSolomonError :", str(e))
        return None

    return message