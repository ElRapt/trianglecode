from PIL import Image, ImageDraw
from reedsolo import RSCodec, ReedSolomonError
import math

# Crée une image vide avec des cellules de forme triangulaire
def generate_img(levels, cell_size):
    # Calculer la taille de l'image en fonction du nombre de niveaux et de la taille des cellules
    triangle_size = levels * cell_size
    # Créer une nouvelle image avec un arrirèe plan en niveaux de gris 
    img = Image.new('RGB', (triangle_size, triangle_size), color=(200,200,200))
    draw = ImageDraw.Draw(img)

    # Dessiner les cellules du TriangleCode
    for level in range(levels):
        for i in range(level + 1):
            # Calculer les coordonées x et y de chaque cellule
            cell_x = triangle_size // 2 - (level + 1) * cell_size // 2 + i * cell_size
            cell_y = level * cell_size
            # Définir les points pour dessiner un triangle
            points = [(cell_x, cell_y), (cell_x + cell_size // 2, cell_y + cell_size), (cell_x - cell_size // 2, cell_y + cell_size)]
            # Dessiner le triangle dans l'image
            draw.polygon(points, fill=1)
    
    return img

# Convertir un message en une chaîne de bits
def message_to_bits(message):
    return ''.join(format(c, '08b') for c in message)

# Convertir une chaîne de bits en un message
def bits_to_message(bits):
    return bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

# Convertir une liste de bits en un tableau d'octets
def bits_to_bytes(bit_list):
    byte_array = bytearray()
    for i in range(0, len(bit_list), 8):
        byte = sum([bit_list[i + j] << (7 - j) for j in range(8)])
        byte_array.append(byte)
    return byte_array

# Convertir un tableau d'octects en une chaîne de caractères
def bytes_to_string(byte_array):
    return byte_array.decode('utf-8')

# Calculer le nombre de niveaux nécessaires pour stocker tous les bits du message
def required_levels(message_bits):
    return int(math.ceil((-1 + math.sqrt(1 + 8 * len(message_bits))) / 2))


# Encodage du message dans l'image vide du TriangleCode
def encode_message_in_triangle(message, img, cell_size):
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



# Décodage du message de l'image du TriangleCode
def decode_message_from_triangle(img, cell_size):
    # Récupère les dimensions de l'image
    img_width, img_height = img.size
    triangle_size = min(img_width, img_height)
    # Calcule le nombre de niveaux dans le TriangleCode en se basant sur la taille de l'image
    levels = img.size[0] // cell_size

    bit_list = []
    # Parcourir chaque niveau du TriangleCode
    for level in range(levels):
        # Pour chaque niveau, parcourir chaque cellule
        for i in range(level + 1):
            # Calculer la position de la cellule
            cell_x = triangle_size // 2 - (level + 1) * cell_size // 2 + i * cell_size
            cell_y = level * cell_size
            # Définir le point central du triangle pour échantillonner l'intensité des pixels
            point = (cell_x + cell_size // 2, cell_y + cell_size // 2)

            # S'assurer que le point est dans les limites de l'image pour éviter les index errors
            if 0 <= point[0] < img_width and 0 <= point[1] < img_height:
                # Récupérer la valeur du pixel pour ce point
                pixel_value = img.getpixel(point)[0]
                # Si la valeur est supérieure à 128 (seuil), alors le bit est 1, sinon il est à 0
                bit = 1 if pixel_value > 128 else 0
                bit_list.append(bit)
    
    while len(bit_list) % 8 != 0:
        bit_list.append(0)

    byte_array = bits_to_bytes(bit_list)

    # Décode le message avec Reed-Solomon
    rs = RSCodec(10)
    try:
        # Décode le message avec Reed-Solomon
        message_decoded = rs.decode(byte_array)
        # Convertir le tableau de bytes en une chaîne de caractères
        message = bytes_to_string(message_decoded)
    except ReedSolomonError as e:
        print("ReedSolomonError :", str(e))
        return None

    return message


# Décodage du message à partir du message encodé avec Reed-Solomon
def decode_message_from_message(encoded_bytes):
    # Création d'une instance Reed-Solomon avec 10 octets de redondance
    rs = RSCodec(10)
    print("Longueur du message encodé :", len(encoded_bytes))
    print("Message encodé :", encoded_bytes)

    try:
        # Essaye de décoder les octets encodés avec Reed-Solomon
        decoded_bytes = rs.decode(encoded_bytes)[0]
        # Affiche la longueur du message décodé 
        print("Longueur du message décodé :", len(decoded_bytes))
        # Affiche le contenu du message décodé
        print("Contenu du message décodé :", decoded_bytes)
    except ReedSolomonError as e:
        # En cas d'erreur lors du décodage, imprime l'erreur
        print("ReedSolomonError :", str(e))
        return None

    # Convertit le tableau d'octets en une chaîne de caractères et la renvoie
    return bytes_to_string(decoded_bytes)





cell_size = 20 # Modifier ici pour changer la taille des cellules

message = "A" # Modifier ici pour coder un autre message
rs = RSCodec(10)  # Utiliser 10 octets de redondance

# Encoder avec ReedSolomon
message_encoded = rs.encode(bytearray(message, 'utf-8'))

message_bits = message_to_bits(message_encoded)
levels = required_levels(message_bits)
triangle_size = levels * cell_size

img = generate_img(levels, cell_size)
encode_message_in_triangle(message_bits, img, cell_size)
img.show()

# Lancer le décodage sur l'image encodée à partir du message
decoded_message_message = decode_message_from_message(message_encoded)
print("Message décodé à partir du message : ", decoded_message_message)

# Lancer le décodage sur l'image encodée à partir de l'image
decoded_message_img = decode_message_from_triangle(img, cell_size)
print("Message décodé à partir de l'image : ", decoded_message_img)