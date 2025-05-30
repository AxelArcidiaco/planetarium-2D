import pygame
import math
from datetime import datetime, timedelta

# Initialisation de Pygame
pygame.init()
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Planétarium Interactif")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SUN_COLOR = (255, 200, 0)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER_COLOR = (100, 100, 100)

# Centre du planétarium
center_x, center_y = width // 2, height // 2

# Vitesse de simulation (jours ajoutés par tick)
speed = 1

# Date de départ
current_date = datetime.now()

# Informations simplifiées sur les planètes
# Format : nom, rayon_orbite (en millions de km), période_orbitale (en jours), couleur, taille (pixels)
planets = [
    ("Mercure", 58, 88, (169, 169, 169), 4),
    ("Vénus", 108, 225, (255, 215, 0), 6),
    ("Terre", 150, 365, (100, 149, 237), 6),
    ("Mars", 228, 687, (188, 39, 50), 5),
    ("Jupiter", 778, 4333, (255, 165, 0), 10),
    ("Saturne", 1427, 10759, (210, 180, 140), 9),
    ("Uranus", 2871, 30685, (173, 216, 230), 7),
    ("Neptune", 4497, 60190, (72, 61, 139), 7),
]

# Échelle pour adapter les distances à l'écran
default_scale = 0.15
scale = default_scale
min_scale = 0.03
max_scale = 0.5

# Police
font = pygame.font.SysFont(None, 28)

# Bouton de réinitialisation
button_rect = pygame.Rect(10, 40, 180, 35)

# Boucle principale
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # Limite à 60 FPS
    screen.fill(BLACK)

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Zoom avec molette de la souris
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Molette vers le haut
                scale = min(scale * 1.1, max_scale)
            elif event.button == 5:  # Molette vers le bas
                scale = max(scale * 0.9, min_scale)
            elif event.button == 1:
                if button_rect.collidepoint(event.pos):
                    scale = default_scale

    # Touches pour changer la date
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        current_date += timedelta(days=speed)
    if keys[pygame.K_LEFT]:
        current_date -= timedelta(days=speed)
    if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:  # + pour zoom
        scale = min(scale * 1.05, max_scale)
    if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:  # - pour dézoom
        scale = max(scale * 0.95, min_scale)

    # Afficher la date
    font = pygame.font.SysFont(None, 28)
    date_text = font.render(current_date.strftime("%d/%m/%Y"), True, WHITE)
    screen.blit(date_text, (10, 10))

    # Bouton "Réinitialiser le zoom"
    mouse_pos = pygame.mouse.get_pos()
    button_color = (
        BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    )
    pygame.draw.rect(screen, button_color, button_rect)
    button_text = font.render("Réinitialiser le zoom", True, WHITE)
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 7))

    # Dessiner le Soleil
    pygame.draw.circle(screen, SUN_COLOR, (center_x, center_y), 12)

    # Afficher les planètes
    for name, orbit_radius, period, color, size in planets:
        # Calcul de la position orbitale (approximation circulaire)
        days_since_epoch = (current_date - datetime(2000, 1, 1)).days
        angle = 2 * math.pi * (days_since_epoch % period) / period

        # Position en coordonnées cartésiennes
        x = center_x + math.cos(angle) * orbit_radius * scale
        y = center_y + math.sin(angle) * orbit_radius * scale

        # Dessiner l'orbite
        pygame.draw.circle(
            screen, (50, 50, 50), (center_x, center_y), int(orbit_radius * scale), 1
        )

        # Dessiner la planète
        pygame.draw.circle(screen, color, (int(x), int(y)), size)

        # Étiquette de la planète
        label = font.render(name, True, WHITE)
        screen.blit(label, (int(x) + 10, int(y)))

    # Mettre à jour l'affichage
    pygame.display.flip()

pygame.quit()
