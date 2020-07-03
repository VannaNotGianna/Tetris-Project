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

#FORMAS DE ANDREA
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
    # Tetris Title
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
    run = True
    pieza_ahora = obtener_figura()
    pieza_siguiente = obtener_figura()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        rapidez = 0.27

        rejilla = crear_rejilla(cerrado_posiciones)
        rapidez += clock.get_rawtime()
        clock.tick()

        # PIECE FALLING CODE
        if fall_time/1000 >= rapidez:
            fall_time = 0
            pieza_ahora.y += 1
            if not (espacio_valido(pieza_ahora, rejilla)) and pieza_ahora.y > 0:
                pieza_ahora.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
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
                    # rotate shape
                    pieza_ahora.rotation = pieza_ahora.rotation + 1 % len(pieza_ahora.shape)
                    if not espacio_valido(pieza_ahora, rejilla):
                        pieza_ahora.rotation = pieza_ahora.rotation - 1 % len(pieza_ahora.shape)

                if event.key == pygame.K_DOWN:
                    # move shape down
                    pieza_ahora.y += 1
                    if not espacio_valido(pieza_ahora, rejilla):
                        pieza_ahora.y -= 1

#HATA ACA
        shape_pos = convert_shape_format(pieza_ahora)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                rejilla[y][x] = pieza_ahora.color

        # IF PIECE HIT GROUND
        if cambiar_pieza:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            clear_rows(grid, locked_positions)

        draw_window(win)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

    draw_text_middle("You Lost", 40, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(\'Press any key to begin.\', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption(\'Tetris\')

main_menu()  # start game



 
