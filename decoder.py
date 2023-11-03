from reedsolo import RSCodec, ReedSolomonError
from PIL import Image, ImageDraw
from calculator import bytes_to_string, bits_to_bytes, bits_to_message


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