import pygame
import random

pygame.font.init()

#Variables globales
s_width = 800
s_height = 700
play_width = 300  # significa que  300 // 10 = 30 width por bloque
play_height = 600  # significa 600 // 20 = 30 altura por bloque
bloque_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


#Formato piezas

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

#Conjunto de piezas y sus colores
formas = [S, Z, I, O, J, L, T]
color_pieza = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]



class Pieza(object):  # *
    def __init__(self, x, y, forma):
        self.x = x
        self.y = y
        self.forma = forma
        self.color = color_pieza[formas.index(forma)]
        self.rotation = 0


def create_cuadricula(bloqueado_pos={}):  # *
    cuadricula = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(cuadricula)):
        for j in range(len(cuadricula[i])):
            if (j, i) in bloqueado_pos:
                c = bloqueado_pos[(j,i)]
                cuadricula[i][j] = c
    return cuadricula


def convert_forma_format(forma):
    posiciones = []
    format = forma.forma[forma.rotation % len(forma.forma)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                posiciones.append((forma.x + j, forma.y + i))

    for i, pos in enumerate(posiciones):
        posiciones[i] = (pos[0] - 2, pos[1] - 4)

    return posiciones


def espacio_valido(forma, cuadricula):
    oc_pos = [[(j, i) for j in range(10) if cuadricula[i][j] == (0,0,0)] for i in range(20)]
    oc_pos = [j for sub in oc_pos for j in sub]

    format = convert_forma_format(forma)

    for pos in format:
        if pos not in oc_pos:
            if pos[1] > -1:
                return False
    return True


def perdiste(posiciones):
    for pos in posiciones:
        x, y = pos
        if y < 1:
            return True

    return False


def get_forma():
    return Pieza(5, 0, random.choice(formas))


def draw_text_middle(superficie, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    superficie.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


def draw_cuadricula(superficie, cuadricula):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(cuadricula)):
        pygame.draw.line(superficie, (128,128,128), (sx, sy + i*bloque_size), (sx+play_width, sy+ i*bloque_size))
        for j in range(len(cuadricula[i])):
            pygame.draw.line(superficie, (128, 128, 128), (sx + j*bloque_size, sy),(sx + j*bloque_size, sy + play_height))


def limpiar_filas(cuadricula, bloqueado):

    inc = 0
    for i in range(len(cuadricula)-1, -1, -1):
        row = cuadricula[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del bloqueado[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(bloqueado), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                bloqueado[newKey] = bloqueado.pop(key)

    return inc


def draw_next_forma(forma, superficie):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Siguiente pieza', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = forma.forma[forma.rotation % len(forma.forma)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(superficie, forma.color, (sx + j*bloque_size, sy + i*bloque_size, bloque_size, bloque_size), 0)

    superficie.blit(label, (sx + 10, sy - 30))


def actualizar_puntuacion(npuntuacion):
    puntuacion = punt_max()

    with open('puntuaciones.txt', 'w') as f:
        if int(puntuacion) > npuntuacion:
            f.write(str(puntuacion))
        else:
            f.write(str(npuntuacion))


def punt_max():
    with open('puntuaciones.txt', 'r') as f:
        lines = f.readlines()
        puntuacion = lines[0].strip()

    return puntuacion


def draw_ventana(superficie, cuadricula, puntuacion=0, ultima_puntuacion = 0):
    superficie.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    superficie.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # current puntuacion
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Puntuación: ' + str(puntuacion), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    superficie.blit(label, (sx + 20, sy + 160))
    # ultima puntuacion
    label = font.render('Record: ' + ultima_puntuacion, 1, (255,255,255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    superficie.blit(label, (sx + 20, sy + 160))

    for i in range(len(cuadricula)):
        for j in range(len(cuadricula[i])):
            pygame.draw.rect(superficie, cuadricula[i][j], (top_left_x + j*bloque_size, top_left_y + i*bloque_size, bloque_size, bloque_size), 0)

    pygame.draw.rect(superficie, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_cuadricula(superficie, cuadricula)
    #pygame.display.update()


def main(win):  # *
    ultima_puntuacion = punt_max()
    bloqueado_posiciones = {}
    cuadricula = create_cuadricula(bloqueado_posiciones)

    change_Pieza = False
    run = True
    current_Pieza = get_forma()
    next_Pieza = get_forma()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    puntuacion = 0

    while run:
        cuadricula = create_cuadricula(bloqueado_posiciones)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_Pieza.y += 1
            if not(espacio_valido(current_Pieza, cuadricula)) and current_Pieza.y > 0:
                current_Pieza.y -= 1
                change_Pieza = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_Pieza.x -= 1
                    if not(espacio_valido(current_Pieza, cuadricula)):
                        current_Pieza.x += 1
                if event.key == pygame.K_RIGHT:
                    current_Pieza.x += 1
                    if not(espacio_valido(current_Pieza, cuadricula)):
                        current_Pieza.x -= 1
                if event.key == pygame.K_DOWN:
                    current_Pieza.y += 1
                    if not(espacio_valido(current_Pieza, cuadricula)):
                        current_Pieza.y -= 1
                if event.key == pygame.K_UP:
                    current_Pieza.rotation += 1
                    if not(espacio_valido(current_Pieza, cuadricula)):
                        current_Pieza.rotation -= 1

        forma_pos = convert_forma_format(current_Pieza)

        for i in range(len(forma_pos)):
            x, y = forma_pos[i]
            if y > -1:
                cuadricula[y][x] = current_Pieza.color

        if change_Pieza:
            for pos in forma_pos:
                p = (pos[0], pos[1])
                bloqueado_posiciones[p] = current_Pieza.color
            current_Pieza = next_Pieza
            next_Pieza = get_forma()
            change_Pieza = False
            puntuacion += limpiar_filas(cuadricula, bloqueado_posiciones) * 10

        draw_ventana(win, cuadricula, puntuacion, ultima_puntuacion)
        draw_next_forma(next_Pieza, win)
        pygame.display.update()

        if perdiste(bloqueado_posiciones):
            draw_text_middle(win, "¡Perdiste!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            actualizar_puntuacion(puntuacion)


def menup(win):  # *
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Presiona cualquier tecla', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
menup(win)