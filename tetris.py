
import pygame
import random

"""
10 x 20 rejilla cuadrada
Formas: S, Z, I, O, J, L, T
representado en orden por 0 - 6
"""

pygame.font.init()

# VARIABLE  GLOBALES
s_ancho = 800
s_altura = 700
bloque_ancho = 300  # quiere decir 300 // 10 = 30 ancho por bloque
bloque_altura = 600  # quiere decir 600 // 20 = 20 altura por bloque
tamano_bloque = 30

superior_izquierda_x = (s_ancho - bloque_ancho) // 2
superior_izquierda_y = s_altura - bloque_altura

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

formas = [S, Z, I, O, J, L, T]
formas_colores = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 representa forma

#clase

def crear_rejilla(cerrar_posiciones={}):
    rejilla = [[(0,0,0) for x in range(10)] for x in range (20)]

    for i in range(len(rejilla)):
        for j in range (len(rejilla[i])):
            if (i,j) in cerrar_posiciones:
                c = cerrar_posiciones[(j,i)]
                rejilla[i][j] = c
    return rejilla

def convertir_figura_formato(figura):
    posiciones = []
    formato = figura.figura[figura.rotacion % len(figura.figura)]

    for i, linea in enumerate(formato):
        fila = list(linea)
        for j, column in enumerate(fila):
            if column == '0':
                posiciones.append((figura.x + j, figura.y + i))

    for i, pos in enumerate(posiciones):
        posiciones[i] = (pos[0] - 2, pos[1] - 4)

    return posiciones

def espacio_valido(figura, rejilla):
    posisiones_acceptadas = [[(j, i) for j in range(10) if rejilla[i][j] == (0,0,0)] for i in range(20)]
    posisiones_acceptadas = [j for sub in posisiones_acceptadas for j in sub]
    formateado = convertir_figura_formato(figura)

    for pos in formateado:
        if pos not in posisiones_acceptadas:
            if pos[1] > -1:
                return False

    return True

def verifica_pierde (posiciones):
    for pos in posiciones:
        x, y = pos
        if y < 1:
            return True
    return False

def obtener_figura():
    global figuras, figuras_colores

    return pieza(5, 0, random.choice(figuras))

def dibujar_texto_almedio(texto, tamano, color, superficie):
    font = pygame.font.SysFont("century gothic", tamano, bold = True)
    label = font.render(texto, 1, color)

    superficie.blit(label, (superior_izquierda_x + bloque_ancho/2 - (label.obtener_ancho() / 2), superior_izquierda_y + bloque_altura/2 - label.obtener_altura()/2))
def dibujar_rejilla(superficie, fila, column):
    x = superior_izquierda_x
    y = superior_izquierda_y
    for i in range(fila):
        pygame.draw.line(superficie, (128, 128, 128), (x, y + i*30), (x + bloque_ancho, y + i*30)) #lineas horizontales
        for j in range(column):
            pygame.draw.line(superficie, (128, 128, 128), (x + j*30, y), (x + j *30, y + bloque_altura)) # lineas verticales

def despejar_filas(rejilla, cerrado):
    # se necesita ver si la fila esta despejada
    c = 0
    for i in range(len(rejilla)-1,-1,-1):
        fila = rejilla[i]
        if (0, 0, 0) not in fila:
            c += 1
            # añadir posiciones para remover del cerrado
            ind = i
            for j in range(len(fila)):
                try:
                    del cerrado[(j, i)]
                except:
                    continue
    if c > 0:
        for key in sorted(list(cerrado), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + c)
                cerrado[newKey] = cerrado.pop(key)



def dibujar_siguiente_figura(figura, superficie):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Siguiente Figura', 1, (255,255,255))

    sx = superior_izquierda_x + bloque_ancho + 50
    sy = superior_izquierda_y + bloque_altura/2 - 100
    formato = figura.shape[figura.rotation % len(figura.shape)]

    for i, line in enumerate(formato):
        fila = list(line)
        for j, column in enumerate(fila):
            if column == '0':
                pygame.draw.rect(superficie, figura.color, (sx + j*30, sy + i*30, 30, 30), 0)

    superficie.blit(label, (sx + 10, sy- 30))


def draw_venatana(superficie):
    superficie.fill((0,0,0))
    # Tetris Titulo
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255,255,255))

    superficie.blit(label, (superior_izquierda_x + bloque_ancho / 2 - (label.get_width() / 2), 30))

    for i in range(len(rejilla)):
        for j in range(len(rejilla[i])):
            pygame.draw.rect(superficie, rejilla[i][j], (superior_izquierda_x + j* 30, superior_izquierda_y + i * 30, 30, 30), 0)

    # draw grid and border
    dibujar_rejilla(superficie, 20, 10)
    pygame.draw.rect(superficie, (255, 0, 0), (superior_izquierda_x, superior_izquierda_y, bloque_ancho, bloque_altura), 5)
    # pygame.display.update()


def main():
    global rejilla

    cerrado_posiciones = {}  # (x,y):(255,0,0)
    rejilla = crear_rejilla(cerrado_posiciones)

    cambiar_pieza = False
    correr = True
    pieza_ahora = obtener_figura()
    pieza_siguiente = obtener_figura()
    clock = pygame.time.Clock()
    fall_time = 0

    while correr:
        rapidez = 0.27

        rejilla = crear_rejilla(cerrado_posiciones)
        rapidez += clock.get_rawtime()
        clock.tick()

        # PIEZA CAE
        if fall_time/1000 >= rapidez:
            fall_time = 0
            pieza_ahora.y += 1
            if not (espacio_valido(pieza_ahora, rejilla)) and pieza_ahora.y > 0:
                pieza_ahora.y -= 1
                cambiar_pieza= True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                correr = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pieza_ahora.x -= 1
                    if not espacio_valido(pieza_ahora, rejilla):
                        pieza_ahora.x += 1

                elif event.key == pygame.K_RIGHT:
                    pieza_ahora.x += 1
                    if not espacio_valido(pieza_ahora, rejilla):
                        pieza_ahora.x -= 1
                elif event.key == pygame.K_UP:
                    # rotar pieza
                    pieza_ahora.rotation = pieza_ahora.rotation + 1 % len(pieza_ahora.shape)
                    if not espacio_valido(pieza_ahora, rejilla):
                        pieza_ahora.rotation = pieza_ahora.rotation - 1 % len(pieza_ahora.shape)

                if event.key == pygame.K_DOWN:
                    # mover la pieza abajo
                    pieza_ahora.y += 1
                    if not espacio_valido(pieza_ahora, rejilla):
                        pieza_ahora.y -= 1

        posicion_figura = convertir_figura_formato(pieza_ahora)

        # añadir una pieza a la rejilla p
        for i in range(len(posicion_figura)):
            x, y = posicion_figura[i]
            if y > -1:
                rejilla[y][x] = pieza_ahora.color

        # SI LA PIEZA TOCA EL SUELO
        if cambiar_pieza:
            for pos in posicion_figura:
                p = (pos[0], pos[1])
                cerrado_posiciones[p] = pieza_ahora.color
            pieza_ahora = pieza_siguiente
            pieza_siguiente = obtener_figura()
            cambiar_pieza= False

            # CHEQUEAR PARA VER FILAS DISPONIBLES
            despejar_filas(rejilla, cerrado_posiciones)

        draw_venatana(ganar) 
        dibujar_siguiente_figura(pieza_siguiente, ganar)
        pygame.display.update()

        # Chequear si perdiste
        if check_lost(cerrado_posiciones): 
            correr= False

    dibujar_texto_almedio("Perdiste", 40, (255,255,255), ganar)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    correr = True
    while correr:
        ganar.fill((0,0,0))
        dibujar_texto_almedio()\'Presiona cualquier pieza para comenzar.\', 60, (255, 255, 255), ganar)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                correr = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


ganar = pygame.display.set_mode((s_ancho, s_altura)) 
pygame.display.set_caption(\'Tetris\')

main_menu()  # start game



 
