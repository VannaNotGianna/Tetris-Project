
import pygame
import random
"""
10 x 20 square rejilla
bloques: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# VARIABLES GLOBALES
s_ancho = 800
s_altura = 700
bloque_ancho = 300  # meaning 300 // 10 = 30 width per block
bloque_altura = 600  # meaning 600 // 20 = 30 height per blo ck
tamano_bloque = 30

superior_izquierda_x = (s_ancho - bloque_ancho) // 2
superior_izquierda_y = s_altura - bloque_altura


# FORMATO DE FIGURAS

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

bloques = [S, Z, I, O, J, L, T]
lista_color = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
               (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


def obtenerPieza(column, fila, figura):
    x = column
    y = fila
    color = lista_color[bloques.index(figura)]
    rotation = 0
    return [x, y, figura, color, rotation]


def crear_rejilla(cerrar_posiciones={}):
    rejilla = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(rejilla)):
        for j in range(len(rejilla[i])):
            if (j, i) in cerrar_posiciones:
                c = cerrar_posiciones[(j, i)]
                rejilla[i][j] = c
    return rejilla


def convierte_formato_figura(figura):
    posiciones = []
    format = figura[2][figura[4] % len(figura[2])]

    for i, linea in enumerate(format):
        fila = list(linea)
        for j, column in enumerate(fila):
            if column == '0':
                posiciones.append((figura[0] + j, figura[1] + i))

    for i, pos in enumerate(posiciones):
        posiciones[i] = (pos[0] - 2, pos[1] - 4)

    return posiciones


def espacio_valido(figura, rejilla):
    posiciones_aceptadas = [[(j, i) for j in range(
        10) if rejilla[i][j] == (0, 0, 0)] for i in range(20)]
    posiciones_aceptadas = [j for sub in posiciones_aceptadas for j in sub]
    formateado = convierte_formato_figura(figura)

    for pos in formateado:
        if pos not in posiciones_aceptadas:
            if pos[1] > -1:
                return False

    return True


def verifica_pierde(posiciones):
    for pos in posiciones:
        x, y = pos
        if y < 1:
            return True
    return False


def obtener_bloque():
    global bloques, lista_color

    return obtenerPieza(5, 0, random.choice(bloques))


def dibuja_texto_medio(text, size, color, superficie):
    font = pygame.font.SysFont('Raleway', size, bold=True)
    label = font.render(text, 1, color)

    superficie.blit(label, (superior_izquierda_x + bloque_ancho/2 - (label.get_width() / 2),
                            superior_izquierda_y + bloque_altura/2 - label.get_height()/2))


def dibujar_rejilla(superficie, fila, col):
    sx = superior_izquierda_x
    sy = superior_izquierda_y
    for i in range(fila):
        pygame.draw.line(superficie, (128, 128, 128), (sx, sy + i*30),
                         (sx + bloque_ancho, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(superficie, (128, 128, 128), (sx + j * 30, sy),
                             (sx + j * 30, sy + bloque_altura))  # vertical lines


def despejar_filas(rejilla, locked):

    inc = 0
    for i in range(len(rejilla)-1, -1, -1):
        fila = rejilla[i]
        if (0, 0, 0) not in fila:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(fila)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)


def siguiente_figura(figura, superficie):
    font = pygame.font.SysFont('Raleway', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = superior_izquierda_x + bloque_ancho + 50
    sy = superior_izquierda_y + bloque_altura/2 - 100
    format = figura[2][figura[4] % len(figura[2])]

    for i, linea in enumerate(format):
        fila = list(linea)
        for j, column in enumerate(fila):
            if column == '0':
                pygame.draw.rect(superficie, figura[3],
                                 (sx + j*30, sy + i*30, 30, 30), 0)

    superficie.blit(label, (sx + 10, sy - 30))


def dibujar_ventana(superficie):
    superficie.fill((0, 0, 0))
    # Tetris Title
    font = pygame.font.SysFont('Raleway', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))

    superficie.blit(label, (superior_izquierda_x + bloque_ancho /
                            2 - (label.get_width() / 2), 30))

    for i in range(len(rejilla)):
        for j in range(len(rejilla[i])):
            pygame.draw.rect(
                superficie, rejilla[i][j], (superior_izquierda_x + j * 30, superior_izquierda_y + i * 30, 30, 30), 0)

    # draw rejilla and border
    dibujar_rejilla(superficie, 20, 10)
    pygame.draw.rect(superficie, (255, 0, 0), (superior_izquierda_x,
                                               superior_izquierda_y, bloque_ancho, bloque_altura), 5)
    # pygame.display.update()


def main():
    global rejilla

    cerrar_posiciones = {}  # (x,y):(255,0,0)
    rejilla = crear_rejilla(cerrar_posiciones)

    cambiar_pieza = False
    run = True
    pieza_actual = obtener_bloque()
    pieza_siguiente = obtener_bloque()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        rapidez = 0.27

        rejilla = crear_rejilla(cerrar_posiciones)
        fall_time += clock.get_rawtime()
        clock.tick()

        # PIECE FALLING CODE
        if fall_time/1000 >= rapidez:
            fall_time = 0
            pieza_actual[1] += 1
            if not (espacio_valido(pieza_actual, rejilla)) and pieza_actual[1] > 0:
                pieza_actual[1] -= 1
                cambiar_pieza = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pieza_actual[0] -= 1
                    if not espacio_valido(pieza_actual, rejilla):
                        pieza_actual[0] += 1

                elif event.key == pygame.K_RIGHT:
                    pieza_actual[0] += 1
                    if not espacio_valido(pieza_actual, rejilla):
                        pieza_actual[0] -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    pieza_actual[4] = pieza_actual[4] + \
                        1 % len(pieza_actual[2])
                    if not espacio_valido(pieza_actual, rejilla):
                        pieza_actual[4] = pieza_actual[4] - \
                            1 % len(pieza_actual[2])

                if event.key == pygame.K_DOWN:
                    # move shape down
                    pieza_actual[1] += 1
                    if not espacio_valido(pieza_actual, rejilla):
                        pieza_actual[1] -= 1

                if event.key == pygame.K_SPACE:
                    while espacio_valido(pieza_actual, rejilla):
                        pieza_actual[1] += 1
                    pieza_actual[1] -= 1
                    print(convierte_formato_figura(pieza_actual))  # todo fix

        shape_pos = convierte_formato_figura(pieza_actual)

        # add piece to the rejilla for drapantallag
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                rejilla[y][x] = pieza_actual[3]

        # IF PIECE HIT GROUND
        if cambiar_pieza:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                cerrar_posiciones[p] = pieza_actual[3]
            pieza_actual = pieza_siguiente
            pieza_siguiente = obtener_bloque()
            cambiar_pieza = False

            # call four times to check for multiple clear filas
            despejar_filas(rejilla, cerrar_posiciones)

        dibujar_ventana(pantalla)
        siguiente_figura(pieza_siguiente, pantalla)
        pygame.display.update()

        # Check if user lost
        if verifica_pierde(cerrar_posiciones):
            run = False

    dibuja_texto_medio("You Lost", 40, (255, 255, 255), pantalla)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        pantalla.fill((0, 0, 0))
        player(playerX, playerY)
        dibuja_texto_medio('Lets play TetriX', 60, (255, 255, 255), pantalla)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


pantalla = pygame.display.set_mode((s_ancho, s_altura))
playerImg = pygame.image.load('./git-test/ignored files/future.png')
playerX = 370  # shows on the middle of screen
playerY = 480  # shows on the middle of screen


def player(x, y):
    pantalla.blit(playerImg, (x, y))


pygame.display.set_caption('Tetris')
main_menu()  # start game
