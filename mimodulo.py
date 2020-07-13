s_ancho = 800
s_altura = 700
bloque_ancho = 300  # meaning 300 // 10 = 30 width per block
bloque_altura = 600  # meaning 600 // 20 = 30 height per blo ck
tamano_bloque = 30

superior_izquierda_x = (s_ancho - bloque_ancho) // 2
superior_izquierda_y = s_altura - bloque_altura


def crear_rejilla(cerrar_posiciones={}):
    rejilla = [[(74, 112, 139) for x in range(10)] for x in range(20)]

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
        10) if rejilla[i][j] == (74, 112, 139)] for i in range(20)]
    posiciones_aceptadas = [j for sub in posiciones_aceptadas for j in sub]
    formateado = convierte_formato_figura(figura)

    for pos in formateado:
        if pos not in posiciones_aceptadas:
            if pos[1] > -1:
                return False

    return True


def despejar_filas(rejilla, locked):
    inc = 0
    for i in range(len(rejilla)-1, -1, -1):
        fila = rejilla[i]
        if (74, 112, 139) not in fila:
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
    return inc
