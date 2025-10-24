import pygame
import random

# --- Impostazioni ---
LARGHEZZA, ALTEZZA = 10, 20  # celle
DIM_CELLA = 30
LARGHEZZA_SCHERMO = LARGHEZZA * DIM_CELLA
ALTEZZA_SCHERMO = ALTEZZA * DIM_CELLA
FPS = 10

COLORI = [
    (0, 0, 0),      # Nero (vuoto)
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (255, 0, 0),    # Z
    (128, 0, 128),  # T
]

# --- Forme ---
FORME = [
    [[1, 1, 1, 1]],  # I
    [[2, 0, 0],
     [2, 2, 2]],     # J
    [[0, 0, 3],
     [3, 3, 3]],     # L
    [[4, 4],
     [4, 4]],        # O
    [[0, 5, 5],
     [5, 5, 0]],     # S
    [[6, 6, 0],
     [0, 6, 6]],     # Z
    [[0, 7, 0],
     [7, 7, 7]],     # T
]

# --- Funzioni ---
def nuova_forma():
    return [row[:] for row in random.choice(FORME)], random.randint(1, 7)

def ruota(mat):
    return [list(row) for row in zip(*mat[::-1])]

def posizione_valida(griglia, forma, offset):
    off_x, off_y = offset
    for y, riga in enumerate(forma):
        for x, val in enumerate(riga):
            if val:
                nx, ny = off_x + x, off_y + y
                if nx < 0 or nx >= LARGHEZZA or ny >= ALTEZZA:
                    return False
                if ny >= 0 and griglia[ny][nx]:
                    return False
    return True

def unisci(griglia, forma, offset, colore):
    off_x, off_y = offset
    for y, riga in enumerate(forma):
        for x, val in enumerate(riga):
            if val and 0 <= off_y + y < ALTEZZA:
                griglia[off_y + y][off_x + x] = colore

def rimuovi_linee(griglia):
    nuove = [r for r in griglia if any(c == 0 for c in r)]
    while len(nuove) < ALTEZZA:
        nuove.insert(0, [0] * LARGHEZZA)
    return nuove

# --- Inizializzazione ---
pygame.init()
finestra = pygame.display.set_mode((LARGHEZZA_SCHERMO, ALTEZZA_SCHERMO))
clock = pygame.time.Clock()

griglia = [[0]*LARGHEZZA for _ in range(ALTEZZA)]
forma, colore = nuova_forma()
pos = [LARGHEZZA//2 - len(forma[0])//2, 0]

# --- Ciclo di gioco ---
running = True
tick = 0
spazio_premuto = False  # Flag per la barra spaziatrice

while running:
    clock.tick(FPS)
    tick += 1

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                if posizione_valida(griglia, forma, (pos[0]-1, pos[1])):
                    pos[0] -= 1
            elif evento.key == pygame.K_RIGHT:
                if posizione_valida(griglia, forma, (pos[0]+1, pos[1])):
                    pos[0] += 1
            elif evento.key == pygame.K_UP:
                nuova = ruota(forma)
                if posizione_valida(griglia, nuova, pos):
                    forma = nuova
            elif evento.key == pygame.K_DOWN:
                pos[1] += 1
            elif evento.key == pygame.K_SPACE:
                spazio_premuto = True  # Imposta il flag quando la barra spaziatrice è premuta

    # Movimento automatico verso il basso
    if tick % 10 == 0 and not spazio_premuto:  # Movimento normale
        pos[1] += 1
        if not posizione_valida(griglia, forma, pos):
            pos[1] -= 1
            unisci(griglia, forma, pos, colore)
            griglia = rimuovi_linee(griglia)
            forma, colore = nuova_forma()
            pos = [LARGHEZZA//2 - len(forma[0])//2, 0]
            if not posizione_valida(griglia, forma, pos):
                running = False

    # Se la barra spaziatrice è premuta, far cadere il tetromino velocemente
    if spazio_premuto:
        while posizione_valida(griglia, forma, (pos[0], pos[1] + 1)):
            pos[1] += 1
        spazio_premuto = False  # Reset del flag dopo l'azione

    # Disegno
    finestra.fill((0, 0, 0))
    for y, riga in enumerate(griglia):
        for x, val in enumerate(riga):
            if val:
                pygame.draw.rect(finestra, COLORI[val],
                                 (x*DIM_CELLA, y*DIM_CELLA, DIM_CELLA-1, DIM_CELLA-1))

    for y, riga in enumerate(forma):
        for x, val in enumerate(riga):
            if val:
                pygame.draw.rect(finestra, COLORI[colore],
                                 ((pos[0]+x)*DIM_CELLA, (pos[1]+y)*DIM_CELLA, DIM_CELLA-1, DIM_CELLA-1))

    pygame.display.flip()

pygame.quit()
