from PIL import Image, ImageDraw
from reedsolo import RSCodec, ReedSolomonError
import math
from calculator import message_to_bits, required_levels_for_encoding
from decoder import decode_message_from_message, decode_message_from_triangle
from encoder import encode_message_in_triangle
from drawer import generate_img, show_triangle

cell_size = 20 

messageToCode = "My name is Lucas" 
rs = RSCodec(10) # 10 bytes of redundancy

message_encoded = rs.encode(bytearray(messageToCode, 'utf-8'))

message_bits = message_to_bits(message_encoded)
levels = required_levels_for_encoding(message_bits)
triangle_size = levels * cell_size

img = show_triangle(levels, cell_size, message_bits, triangle_size)

decoded_message_message = decode_message_from_message(message_encoded)
print("Decoded message using message : ", decoded_message_message)

decoded_message_img = decode_message_from_triangle(img, cell_size)
print("Decoded message using image : ", decoded_message_img)