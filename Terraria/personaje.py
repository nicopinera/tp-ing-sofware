import pygame
import constantes as ct
from inventario import Inventario

class Personaje:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vel_x = self.vel_y = 0
        self.ancho, self.alto = ct.TILE_SIZE // 2, ct.TILE_SIZE
        self.en_el_suelo = False
        self.direccion = 1
        self.inventario = Inventario()

    def mover(self, teclas, mundo):
        # Movimiento horizontal
        self.vel_x = (teclas[pygame.K_d] - teclas[pygame.K_a]) * ct.VELOCIDAD_PERSONAJE
        if self.vel_x != 0:
            self.direccion = 1 if self.vel_x > 0 else -1
        
        # Aplicar movimiento horizontal
        nueva_x = self.x + self.vel_x
        if not any(mundo.colisiona(nueva_x + offset, self.y) for offset in (0, self.ancho - 1)):
            self.x = nueva_x

        # Gravedad y salto
        self.vel_y += ct.GRAVEDAD
        if (teclas[pygame.K_w] or teclas[pygame.K_SPACE]) and self.en_el_suelo:
            self.vel_y = -ct.FUERZA_SALTO
            self.en_el_suelo = False

        # Movimiento vertical
        nueva_y = self.y + self.vel_y
        if not any(mundo.colisiona(self.x + offset, nueva_y + self.alto) for offset in (0, self.ancho - 1)):
            self.y = nueva_y
            self.en_el_suelo = False
        else:
            self.y = (int((nueva_y + self.alto) // ct.TILE_SIZE) * ct.TILE_SIZE - self.alto)
            self.vel_y, self.en_el_suelo = 0, True

    def minar_bloque(self, mundo, x, y):
        col, fila = int(x // ct.TILE_SIZE), int(y // ct.TILE_SIZE)
        if not (0 <= col < ct.COLUMNAS and 0 <= fila < ct.FILAS):
            return False
            
        tipo_bloque = mundo.mapa[fila][col]
        herramienta = self.inventario.obtener_herramienta_actual()
        
        if tipo_bloque in ct.BLOQUES_SOLIDOS:
            if herramienta == "mano" or tipo_bloque in ct.HERRAMIENTAS[herramienta]["bloques_efectivos"]:
                mundo.mapa[fila][col] = 0
                self.inventario.agregar_bloque(tipo_bloque)
                self.inventario.usar_herramienta()
                return True
        return False

    def colocar_bloque(self, mundo, x, y):
        item = self.inventario.obtener_item_actual()
        if item["tipo"] != "bloque" or not self.inventario.tiene_bloques(item["id"]):
            return False
            
        col, fila = int(x // ct.TILE_SIZE), int(y // ct.TILE_SIZE)
        if (0 <= col < ct.COLUMNAS and 0 <= fila < ct.FILAS and
            mundo.mapa[fila][col] == 0 and
            (fila == ct.FILAS - 1 or mundo.mapa[fila + 1][col] != 0)):
            
            if self.inventario.usar_bloque(item["id"]):
                mundo.mapa[fila][col] = item["id"]
                return True
        return False

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, (255, 0, 0), (self.x, self.y, self.ancho, self.alto))