import pygame
from inventario import Inventario
import constantes as ct

class Personaje:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.ancho = ct.TILE_SIZE // 2
        self.alto = ct.TILE_SIZE
        self.en_el_suelo = False
        self.direccion = 1
        self.inventario = Inventario()

    def minar_bloque(self, mundo, x, y):
        """Intenta minar un bloque en las coordenadas (x, y)"""
        col = int(x // ct.TILE_SIZE)
        fila = int(y // ct.TILE_SIZE)
        
        if 0 <= col < ct.COLUMNAS and 0 <= fila < ct.FILAS:
            tipo_bloque = mundo.mapa[fila][col]
            
            # Verificar si la herramienta es efectiva
            herramienta = self.inventario.obtener_herramienta_actual()
            bloques_efectivos = ct.HERRAMIENTAS[herramienta].get("bloques_efectivos", [])
            
            if tipo_bloque in ct.BLOQUES_SOLIDOS and (herramienta == "mano" or tipo_bloque in bloques_efectivos):
                mundo.mapa[fila][col] = 0  # Convertir en aire
                self.inventario.agregar_bloque(tipo_bloque)
                self.inventario.usar_herramienta()
                return True
        return False

    def mover(self, teclas, mundo):
    # Movimiento horizontal
        self.vel_x = 0
        if teclas[pygame.K_a]:
            self.vel_x = -ct.VELOCIDAD_PERSONAJE
            self.direccion = -1
        if teclas[pygame.K_d]:
            self.vel_x = ct.VELOCIDAD_PERSONAJE
            self.direccion = 1

    # Aplicar movimiento horizontal
        nueva_x = self.x + self.vel_x
    
    # Verificar colisiones en X (ambos lados del personaje)
        if not (mundo.colisiona(nueva_x, self.y) or 
            mundo.colisiona(nueva_x, self.y + self.alto - 1)):
            self.x = nueva_x

    # Aplicar gravedad
        self.vel_y += ct.GRAVEDAD
    
    # Salto
        if (teclas[pygame.K_w] or teclas[pygame.K_SPACE]) and self.en_el_suelo:
            self.vel_y = -ct.FUERZA_SALTO
            self.en_el_suelo = False
        
    # Movimiento vertical
        nueva_y = self.y + self.vel_y
    
    # Verificar colisión vertical (solo pies)
        if not mundo.colisiona(self.x, nueva_y + self.alto) and \
            not mundo.colisiona(self.x + self.ancho - 1, nueva_y + self.alto):
                self.y = nueva_y
                self.en_el_suelo = False
        else:
            # Ajustar posición para "snap" al grid
            self.y = (int((nueva_y + self.alto) // ct.TILE_SIZE) * ct.TILE_SIZE - self.alto)
            self.vel_y = 0
            self.en_el_suelo = True

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, (255, 0, 0), (self.x, self.y, self.ancho, self.alto))

    def colocar_bloque(self, mundo, x, y):
        """Intenta colocar el bloque seleccionado"""
        item = self.inventario.obtener_item_actual()
    
        # Solo podemos colocar si tenemos un bloque seleccionado
        if item["tipo"] != "bloque":
            return False
        
        tipo_bloque = item["id"]
        if not self.inventario.tiene_bloques(tipo_bloque):
            return False
        
        col = int(x // ct.TILE_SIZE)
        fila = int(y // ct.TILE_SIZE)
    
        condiciones = (
            0 <= col < ct.COLUMNAS,
            0 <= fila < ct.FILAS,
            mundo.mapa[fila][col] == 0,  # Solo colocar en aire
            fila == ct.FILAS - 1 or mundo.mapa[fila + 1][col] != 0  # Con soporte debajo
        )
    
        if all(condiciones) and self.inventario.usar_bloque(tipo_bloque):
            mundo.mapa[fila][col] = tipo_bloque
            return True
        return False