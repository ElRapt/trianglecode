from PIL import Image, ImageDraw
from reedsolo import RSCodec, ReedSolomonError
import math
from calculator import message_to_bits, required_levels, bits_to_bytes, bytes_to_string
from decoder import decode_message_from_message, decode_message_from_triangle
from encoder import encode_message_in_triangle
from drawer import generate_img

cell_size = 20 

messageToCode = "A" 
rs = RSCodec(10) 

message_encoded = rs.encode(bytearray(messageToCode, 'utf-8'))

message_bits = message_to_bits(message_encoded)
levels = required_levels(message_bits)
triangle_size = levels * cell_size

img = generate_img(levels, cell_size)
encode_message_in_triangle(message_bits, img, cell_size, levels, triangle_size)
img.show()

# Lancer le décodage sur l'image encodée à partir du message
decoded_message_message = decode_message_from_message(message_encoded)
print("Message décodé à partir du message : ", decoded_message_message)

# Lancer le décodage sur l'image encodée à partir de l'image
decoded_message_img = decode_message_from_triangle(img, cell_size)
print("Message décodé à partir de l'image : ", decoded_message_img)