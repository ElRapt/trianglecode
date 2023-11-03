from PIL import Image, ImageDraw


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
