import pygame
import constantes as ct
from mundo import Mundo
from personaje import Personaje

# Inicialización
pygame.init()
pantalla = pygame.display.set_mode((ct.ANCHO, ct.ALTO))
pygame.display.set_caption("Terraria Clone")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Crear instancias
mundo = Mundo()
jugador = Personaje(ct.ANCHO // 2, 100)

def dibujar_item_actual():
    """Dibuja el item actualmente seleccionado"""
    item = jugador.inventario.obtener_item_actual()
    
    # Dibujar fondo del indicador
    pygame.draw.rect(pantalla, (50, 50, 50), (5, 35, 80, 40))
    
    # Dibujar icono y texto según el tipo de item
    if item["tipo"] == "bloque":
        pygame.draw.rect(pantalla, item["datos"]["color"], (10, 40, 30, 30))
        texto = font.render(f"x{item['datos']['cantidad']}", True, (255, 255, 255))
    else:
        color = ct.HERRAMIENTAS[item["nombre"]]["color"]
        pygame.draw.rect(pantalla, color, (10, 40, 30, 30))
        durabilidad = item["datos"]["durabilidad"]
        texto = font.render(f"{durabilidad if durabilidad != float('inf') else '∞'}", True, (255, 255, 255))
    
    pantalla.blit(texto, (45, 45))

# Bucle principal
ejecutando = True
while ejecutando:
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        # Pasar eventos al inventario
        jugador.inventario.manejar_evento(evento)
        
        # Eventos de mouse (solo si el inventario no está visible)
        if not jugador.inventario.visible:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if evento.button == 1:  # Clic izquierdo - minar
                    jugador.minar_bloque(mundo, mouse_x, mouse_y)
                elif evento.button == 3:  # Clic derecho - colocar
                    jugador.colocar_bloque(mundo, mouse_x, mouse_y)
    
    # Actualización
    teclas = pygame.key.get_pressed()
    jugador.mover(teclas, mundo)
    
    # Renderizado
    pantalla.fill(ct.COLORES[0])  # Fondo cielo
    mundo.dibujar(pantalla)
    jugador.dibujar(pantalla)
    
    # UI
    fps = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    pantalla.blit(fps, (10, 10))
    
    # Dibujar item actual
    dibujar_item_actual()
    
    # Dibujar inventario (si está visible)
    jugador.inventario.dibujar(pantalla, font)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()