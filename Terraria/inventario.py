import pygame
import constantes as ct

class Inventario:
    def __init__(self):
        self.bloques = {
            1: {"nombre": "Tierra", "cantidad": 5, "color": ct.COLORES[1]},
            2: {"nombre": "Piedra", "cantidad": 5, "color": ct.COLORES[2]}, 
            3: {"nombre": "Pasto", "cantidad": 5, "color": ct.COLORES[3]}
        }
        
        self.herramientas = {
            "mano": {"durabilidad": float('inf')},
            "pico": {"durabilidad": 100},
            "pala": {"durabilidad": 100}
        }
        
        self.categoria_actual = "Bloques"
        self.item_seleccionado = 1
        self.visible = False
        self.posicion = (ct.ANCHO - 220, 50)
        self.ancho = 200
        self.alto_item = 40
        self.margen = 5
        self.alto_categoria = 30

    def agregar_bloque(self, tipo_bloque, cantidad=1):
        if tipo_bloque in self.bloques:
            self.bloques[tipo_bloque]["cantidad"] += cantidad

    def usar_bloque(self, tipo_bloque, cantidad=1):
        if tipo_bloque in self.bloques and self.bloques[tipo_bloque]["cantidad"] >= cantidad:
            self.bloques[tipo_bloque]["cantidad"] -= cantidad
            return True
        return False

    def obtener_item_actual(self):
        if self.categoria_actual == "Bloques":
            if self.item_seleccionado in self.bloques:
                return {
                    "tipo": "bloque",
                    "id": self.item_seleccionado,
                    "nombre": self.bloques[self.item_seleccionado]["nombre"],
                    "datos": self.bloques[self.item_seleccionado]
                }
        else:
            if isinstance(self.item_seleccionado, str) and self.item_seleccionado in self.herramientas:
                return {
                    "tipo": "herramienta",
                    "nombre": self.item_seleccionado,
                    "datos": self.herramientas[self.item_seleccionado]
                }
        
        # Fallback seguro
        return {
            "tipo": "herramienta",
            "nombre": "mano",
            "datos": {"durabilidad": float('inf')}
        }

    def obtener_herramienta_actual(self):
        item = self.obtener_item_actual()
        return item["nombre"] if item["tipo"] == "herramienta" else "mano"

    def tiene_bloques(self, tipo_bloque, cantidad=1):
        return tipo_bloque in self.bloques and self.bloques[tipo_bloque]["cantidad"] >= cantidad

    def _obtener_items_activos(self):
        """Devuelve los items de la categoría actual en formato uniforme"""
        items = []
        if self.categoria_actual == "Bloques":
            for bloque_id, datos in self.bloques.items():
                item = {
                    "tipo": "bloque",
                    "id": bloque_id,
                    "nombre": datos["nombre"],
                    "color": datos["color"],
                    "cantidad": datos["cantidad"]
                }
                items.append(item)
        else:
            for herramienta_nombre, datos in self.herramientas.items():
                item = {
                    "tipo": "herramienta",
                    "nombre": herramienta_nombre,
                    "durabilidad": datos["durabilidad"]
                }
                items.append(item)
        return items

    def usar_herramienta(self):
        item = self.obtener_item_actual()
        if item["tipo"] == "herramienta" and item["datos"]["durabilidad"] != float('inf'):
            self.herramientas[item["nombre"]]["durabilidad"] -= 1
            if self.herramientas[item["nombre"]]["durabilidad"] <= 0:
                self.herramientas[item["nombre"]]["durabilidad"] = 0
                self.item_seleccionado = 1
                self.categoria_actual = "Bloques"

    def dibujar(self, pantalla, font):
        if not self.visible:
            return
            
        # Calcular altura total
        items_activos = self._obtener_items_activos()
        altura_total = len(items_activos) * (self.alto_item + self.margen) + self.alto_categoria + 20
        
        # Fondo del inventario
        fondo = pygame.Surface((self.ancho, altura_total))
        fondo.set_alpha(220)
        fondo.fill((60, 60, 70))
        pantalla.blit(fondo, self.posicion)
        
        # Dibujar selector de categorías
        self._dibujar_categorias(pantalla, font)
        
        # Dibujar items
        y_pos = self.posicion[1] + self.alto_categoria + 10
        for item in items_activos:
            self._dibujar_item(pantalla, font, item, y_pos)
            y_pos += self.alto_item + self.margen

    def _dibujar_categorias(self, pantalla, font):
        x_pos = self.posicion[0]
        ancho_cat = self.ancho // len(ct.CATEGORIAS)
        
        for i, categoria in enumerate(ct.CATEGORIAS):
            color = (100, 100, 200) if categoria == self.categoria_actual else (70, 70, 80)
            pygame.draw.rect(pantalla, color, 
                           (x_pos + i * ancho_cat, self.posicion[1], ancho_cat, self.alto_categoria))
            
            texto = font.render(categoria, True, (255, 255, 255))
            texto_rect = texto.get_rect(center=(x_pos + i * ancho_cat + ancho_cat//2, 
                                              self.posicion[1] + self.alto_categoria//2))
            pantalla.blit(texto, texto_rect)

    def _dibujar_item(self, pantalla, font, item, y_pos):
        """Dibuja un item individual del inventario"""
        # Resaltar item seleccionado
        seleccionado = False
        if self.categoria_actual == "Bloques":
            seleccionado = (self.item_seleccionado == item["id"])
        else:
            seleccionado = (self.item_seleccionado == item["nombre"])
        
        if seleccionado:
            pygame.draw.rect(pantalla, (100, 100, 200), 
                           (self.posicion[0], y_pos, self.ancho, self.alto_item))
        
        # Dibujar icono
        if self.categoria_actual == "Bloques":
            pygame.draw.rect(pantalla, item["color"], 
                           (self.posicion[0] + 5, y_pos + 5, 30, 30))
            texto = font.render(f"{item['nombre']}: {item['cantidad']}", True, (255, 255, 255))
        else:
            color = ct.HERRAMIENTAS[item["nombre"]]["color"]
            pygame.draw.rect(pantalla, color, 
                           (self.posicion[0] + 5, y_pos + 5, 30, 30))
            durabilidad = item["durabilidad"]
            texto = font.render(f"{item['nombre']}: {durabilidad if durabilidad != float('inf') else '∞'}", 
                              True, (255, 255, 255))
        
        pantalla.blit(texto, (self.posicion[0] + 40, y_pos + 10))

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
            self.visible = not self.visible
            return
            
        if not self.visible or evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
            return
            
        mouse_x, mouse_y = evento.pos
        
        # Verificar clic en categorías
        x_pos = self.posicion[0]
        ancho_cat = self.ancho // len(ct.CATEGORIAS)
        
        for i, categoria in enumerate(ct.CATEGORIAS):
            rect = pygame.Rect(
                x_pos + i * ancho_cat,
                self.posicion[1],
                ancho_cat,
                self.alto_categoria
            )
            if rect.collidepoint(mouse_x, mouse_y):
                self.categoria_actual = categoria
                self.item_seleccionado = 1 if categoria == "Bloques" else "pico"
                return
        
        # Verificar clic en items
        items_activos = self._obtener_items_activos()
        y_pos = self.posicion[1] + self.alto_categoria + 10
        
        for item in items_activos:
            rect = pygame.Rect(
                self.posicion[0],
                y_pos,
                self.ancho,
                self.alto_item
            )
            if rect.collidepoint(mouse_x, mouse_y):
                if self.categoria_actual == "Bloques":
                    self.item_seleccionado = item["id"]
                else:
                    self.item_seleccionado = item["nombre"]
                return
            y_pos += self.alto_item + self.margen