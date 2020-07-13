import pygame
import random
from mimodulo import *
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

# index 0 - 6 represent shape
arch = open("colores.txt", "r")
dicc = {}
lista_codes = []
lista_nombres = []


def obtenerDicc_colores(arch):
    for linea in arch:
        color, codigo = linea.split(" ")
        codigo = codigo.strip('\n')
        codigo = codigo.split(",")
        dicc[color] = codigo
    # print(dicc)
    for codes in list(dicc.values()):
        codes = [int(x) for x in codes]
        lista_codes.append(tuple(codes))
    # print(lista_codes)
    for nombres in list(dicc.keys()):
        lista_nombres.append(nombres)
    # print(lista_nombres)
    return lista_codes


def obtenerPieza(column, fila, figura, arch):
    x = column
    y = fila
    lista_color = obtenerDicc_colores(arch)
    color = lista_color[bloques.index(figura)]
    rotation = 0
    return [x, y, figura, color, rotation]


def verifica_pierde(posiciones):
    for pos in posiciones:
        x, y = pos
        if y < 1:
            return True
    return False


def obtener_bloque():
    global bloques

    return obtenerPieza(5, 0, random.choice(bloques), arch)


def dibuja_texto_medio(superficie, text, size, color):
    font = pygame.font.SysFont('Raleway', size, bold=True)
    label = font.render(text, 1, color)

    superficie.blit(label, (superior_izquierda_x + bloque_ancho/2 - (label.get_width() / 2),
                            superior_izquierda_y + bloque_altura/2 - label.get_height()/2))


def dibujar_rejilla(superficie, rejilla):
    sx = superior_izquierda_x
    sy = superior_izquierda_y
    for i in range(len(rejilla)):
        pygame.draw.line(superficie, (128, 128, 128), (sx, sy + i*30),
                         (sx + bloque_ancho, sy + i * 30))  # horizontal lines
        for j in range(len(rejilla[i])):
            pygame.draw.line(superficie, (128, 128, 128), (sx + j * 30, sy),
                             (sx + j * 30, sy + bloque_altura))  # vertical lines


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


def update_score(nscore):
    score = max_score()
    arch = open("max_score.txt", "w")
    if int(score) > nscore:
        arch.write(str(score))
    else:
        arch.write(str(nscore))
    arch.close()


def max_score():
    with open('max_score.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def dibujar_ventana(superficie, rejilla, score=0, last_score=0):
    superficie.fill((74, 112, 139))
    pygame.font.init()
    # Tetris Title
    font = pygame.font.SysFont('Raleway', 60)
    label = font.render('TETRIX', 1, (255, 255, 255))

    superficie.blit(label, (superior_izquierda_x + bloque_ancho /
                            2 - (label.get_width() / 2), 30))
    # current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    sx = superior_izquierda_x + bloque_ancho + 50
    sy = superior_izquierda_y + bloque_altura/2 - 100

    superficie.blit(label, (sx + 20, sy + 160))
    # last score
    label = font.render('High Score: ' + last_score, 1, (255, 255, 255))

    sx = superior_izquierda_x - 200
    sy = superior_izquierda_y + 200

    superficie.blit(label, (sx + 20, sy + 160))
    for i in range(len(rejilla)):
        for j in range(len(rejilla[i])):
            pygame.draw.rect(
                superficie, rejilla[i][j], (superior_izquierda_x + j * 30, superior_izquierda_y + i * 30, 30, 30), 0)

    # draw rejilla and border
    dibujar_rejilla(superficie, rejilla)
    pygame.draw.rect(superficie, (108, 123, 139), (superior_izquierda_x,
                                                   superior_izquierda_y, bloque_ancho, bloque_altura), 5)

    # pygame.display.update()
lista_score = []


def store_score(score):
    lista_score.append(score)
    with open('total_scores.txt', 'w') as f:
        for elem in range(len(lista_score)):
            f.write(str(lista_score[elem])+'\n')


def main(pantalla):
    last_score = max_score()
    cerrar_posiciones = {}  # (x,y):(255,0,0)
    rejilla = crear_rejilla(cerrar_posiciones)

    cambiar_pieza = False
    run = True
    pieza_actual = obtener_bloque()
    pieza_siguiente = obtener_bloque()
    clock = pygame.time.Clock()
    fall_time = 0
    rapidez = 0.27
    level_time = 0
    score = 0
    while run:
        rejilla = crear_rejilla(cerrar_posiciones)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()
        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pieza_actual[0] -= 1
                    if not espacio_valido(pieza_actual, rejilla):
                        pieza_actual[0] += 1
                if event.key == pygame.K_RIGHT:
                    pieza_actual[0] += 1
                    if not espacio_valido(pieza_actual, rejilla):
                        pieza_actual[0] -= 1
                if event.key == pygame.K_DOWN:
                    pieza_actual[1] += 1
                    if not espacio_valido(pieza_actual, rejilla):
                        pieza_actual[1] -= 1
                if event.key == pygame.K_UP:
                    pieza_actual[4] += 1
                    if not espacio_valido(pieza_actual, rejilla):
                        pieza_actual[4] -= 1
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
            score += despejar_filas(rejilla, cerrar_posiciones)*10

        dibujar_ventana(pantalla, rejilla, score, last_score)
        siguiente_figura(pieza_siguiente, pantalla)
        pygame.display.update()

        # Check if user lost
        if verifica_pierde(cerrar_posiciones):
            dibuja_texto_medio(pantalla, "Game Over", 40,
                               (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)
            store_score(score)


def main_menu(pantalla):
    run = True
    while run:
        pantalla.fill((74, 112, 139))
        player(playerX, playerY)
        dibuja_texto_medio(pantalla, 'Lets play TetriX', 60, (255, 255, 255))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main(pantalla)
    pygame.quit()


pantalla = pygame.display.set_mode((s_ancho, s_altura))
playerImg = pygame.image.load('future.png')
pygame.display.set_caption('TetriX')
playerX = 370  # shows on the middle of screen
playerY = 480  # shows on the middle of screen


def player(x, y):
    pantalla.blit(playerImg, (x, y))


main_menu(pantalla)  # start game
