import pygame
import random
from perlin_noise import PerlinNoise
import constantes as ct

class Mundo:
    def __init__(self):
        self.seed = random.randint(0, 1000)
        self.mapa = self._generar_terreno()

    def _generar_terreno(self):
        mapa = [[0 for _ in range(ct.COLUMNAS)] for _ in range(ct.FILAS)]
        noise = PerlinNoise(octaves=3, seed=self.seed)
        altura_media = ct.FILAS // 2
        
        for col in range(ct.COLUMNAS):
            altura = altura_media + int(noise(col/15) * 10)
            
            for fila in range(ct.FILAS):
                if fila > altura:
                    if fila == altura + 1:
                        mapa[fila][col] = 3
                    elif fila <= altura + 4:
                        mapa[fila][col] = 1
                    else:
                        mapa[fila][col] = 2
        return mapa

    def dibujar(self, pantalla):
        for fila in range(ct.FILAS):
            for col in range(ct.COLUMNAS):
                if (bloque := self.mapa[fila][col]) != 0:
                    pygame.draw.rect(
                        pantalla, 
                        ct.COLORES[bloque], 
                        (col * ct.TILE_SIZE, fila * ct.TILE_SIZE, ct.TILE_SIZE, ct.TILE_SIZE)
                    )

    def colisiona(self, x, y):
        col, fila = int(x // ct.TILE_SIZE), int(y // ct.TILE_SIZE)
        return (0 <= col < ct.COLUMNAS and 0 <= fila < ct.FILAS and 
                self.mapa[fila][col] in ct.BLOQUES_SOLIDOS)