import pygame
import random
from perlin_noise import PerlinNoise
import constantes as ct

class Mundo:
    def __init__(self):
        self.seed = random.randint(0, 1000)
        self.mapa = self._generar_terreno()

    def _generar_terreno(self):
        """Genera un terreno básico con Perlin Noise optimizado"""
        mapa = [[0 for _ in range(ct.COLUMNAS)] for _ in range(ct.FILAS)]
        noise = PerlinNoise(octaves=3, seed=self.seed)
        altura_media = ct.FILAS // 2
        
        for col in range(ct.COLUMNAS):
            # Altura con variación suave
            altura = altura_media + int(noise(col/15) * 10)
            
            for fila in range(ct.FILAS):
                if fila > altura:
                    if fila == altura + 1:
                        mapa[fila][col] = 3  # Pasto en superficie
                    elif fila <= altura + 4:
                        mapa[fila][col] = 1  # Capa de tierra
                    else:
                        mapa[fila][col] = 2  # Piedra bajo tierra
        return mapa

    def dibujar(self, pantalla):
        """Renderizado optimizado con pre-cálculo de rectángulos"""
        for fila in range(ct.FILAS):
            for col in range(ct.COLUMNAS):
                bloque = self.mapa[fila][col]
                if bloque != 0:  # No dibujar aire
                    rect = pygame.Rect(
                        col * ct.TILE_SIZE,
                        fila * ct.TILE_SIZE,
                        ct.TILE_SIZE,
                        ct.TILE_SIZE
                    )
                    pygame.draw.rect(pantalla, ct.COLORES[bloque], rect)

    def colisiona(self, x, y):
        """Detección de colisiones optimizada"""
        col = int(x // ct.TILE_SIZE)
        fila = int(y // ct.TILE_SIZE)
         # Verificar límites del mundo primero
        if not (0 <= col < ct.COLUMNAS and 0 <= fila < ct.FILAS):
            return False  # o True si quieres que los bordes sean sólidos
        return self.mapa[fila][col] in ct.BLOQUES_SOLIDOS