import pygame


def load_image(path, size=(32, 32)):
    img = pygame.image.load(path)
    return pygame.transform.scale(img, size)
