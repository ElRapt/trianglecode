import math

def message_to_bits(message):
    return ''.join(format(c, '08b') for c in message)

def bits_to_message(bits):
    return bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

def bits_to_bytes(bit_list):
    byte_array = bytearray()
    for i in range(0, len(bit_list), 8):
        byte = sum([bit_list[i + j] << (7 - j) for j in range(8)])
        byte_array.append(byte)
    return byte_array

def bytes_to_string(byte_array):
    return byte_array.decode('utf-8')

def required_levels_for_encoding(message_bits):
    return int(math.ceil((-1 + math.sqrt(1 + 8 * len(message_bits))) / 2))