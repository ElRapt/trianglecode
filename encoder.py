import math
from reedsolo import RSCodec, ReedSolomonError
from PIL import Image, ImageDraw


def encode_message_in_triangle(message, img, cell_size, levels, triangle_size):
    # Encode le message avec Reed-Solomon
    rs = RSCodec(10)  # Utilise 10 octets de redondance
    message_encoded = rs.encode(bytearray(message, 'utf-8'))

    draw = ImageDraw.Draw(img)
    bit_index = 0

    # Parcourir chaque niveau du TriangleCode
    for level in range(levels):
        # Pour chaque niveau, parcourir chaque cellule
        for i in range(level + 1):
            # Vérifier que nous n'avons pas atteint la fin du message
            if bit_index < len(message_encoded) * 8:
                # Calculer l'index de l'octet et la position du bit dans l'octet
                byte_index = bit_index // 8
                bit_position = bit_index % 8
                # Récupérer le bit à partir de l'octet
                bit = (message_encoded[byte_index] >> (7 - bit_position)) & 1

                # Calculer la position de la cellule
                cell_x = triangle_size // 2 - (level + 1) * cell_size // 2 + i * cell_size
                cell_y = level * cell_size
                # Définir les points pour dessiner un triangle
                points = [(cell_x, cell_y), (cell_x + cell_size // 2, cell_y + cell_size), (cell_x - cell_size // 2, cell_y + cell_size)]

                # Si le bit est 1, remplir la cellule avec du blanc ; sinon, la remplir avec du noir.
                if bit:
                    draw.polygon(points, fill=(255, 255, 255))
                else:
                    draw.polygon(points, fill=(0, 0, 0))

                bit_index += 1
