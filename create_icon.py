"""Script pour generer l'icone de l'application"""
from PIL import Image, ImageDraw

def create_icon():
    # Tailles pour l'icone ICO
    sizes = [16, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        # Creer une image avec fond transparent
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Couleurs du theme
        accent_color = (233, 69, 96)  # #e94560
        bg_color = (26, 26, 46)       # #1a1a2e

        # Dessiner un cercle de fond
        padding = size // 8
        draw.ellipse(
            [padding, padding, size - padding, size - padding],
            fill=bg_color,
            outline=accent_color,
            width=max(1, size // 16)
        )

        # Dessiner un curseur stylise (fleche)
        center_x = size // 2
        center_y = size // 2
        cursor_size = size // 3

        # Points du curseur (forme de fleche)
        cursor_points = [
            (center_x - cursor_size // 2, center_y - cursor_size // 2),  # Pointe haute gauche
            (center_x - cursor_size // 2, center_y + cursor_size // 3),  # Bas gauche
            (center_x - cursor_size // 6, center_y + cursor_size // 6),  # Angle
            (center_x, center_y + cursor_size // 2),                      # Pointe basse
            (center_x + cursor_size // 6, center_y + cursor_size // 6),  # Angle droit
            (center_x + cursor_size // 3, center_y - cursor_size // 2),  # Haut droit
        ]

        draw.polygon(cursor_points, fill=accent_color)

        # Dessiner des cercles concentriques pour l'effet "clic"
        ring_color = (233, 69, 96, 150)
        for i in range(2):
            ring_size = size // 4 + i * (size // 8)
            ring_width = max(1, size // 32)
            draw.ellipse(
                [center_x - ring_size, center_y - ring_size,
                 center_x + ring_size, center_y + ring_size],
                outline=accent_color,
                width=ring_width
            )

        images.append(img)

    # Sauvegarder en ICO
    images[0].save(
        'assets/icon.ico',
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )
    print("Icone creee: assets/icon.ico")

if __name__ == "__main__":
    import os
    os.makedirs("assets", exist_ok=True)
    create_icon()
