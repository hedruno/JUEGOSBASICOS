import pygame
import sys
import math
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Base:
    
    def __init__(self, x, y, e):
        self.x = x
        self.y = y
        self.e = e
        self.color = (255, 255, 255)
        self.alfa = 0

    def setColor(self, color):
        self.color = color

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setXY(self, x, y):
        self.x = x
        self.y = y

    def setEscala(self, e):
        self.e = e

class X(Base):
    
    def __init__(self, x, y, e):
        super().__init__(x, y, e)

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((3*e, 3*e), pygame.SRCALPHA)

        pygame.draw.rect(lienzo, (180, 0, 0), (4, 4, 3*e-8, 3*e-8), 2)

        pygame.draw.line(lienzo, self.color, (6, 6), (3*e-6, 3*e-6), 3)
        pygame.draw.line(lienzo, self.color, (3*e-6, 6), (6, 3*e-6), 3)

        pygame.draw.line(lienzo, (255, 100, 100), (10, 6), (3*e-6, 3*e-10), 1)
        pygame.draw.line(lienzo, (255, 100, 100), (3*e-10, 6), (6, 3*e-10), 1)

        Rotacion  = pygame.transform.rotate(lienzo, self.alfa)
        Traslacion = Rotacion.get_rect(topleft=(self.x, self.y))
        pantalla.blit(Rotacion, Traslacion)

class O(Base):
    
    def __init__(self, x, y, e):
        super().__init__(x, y, e)

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((3*e, 3*e), pygame.SRCALPHA)

        cx = int(3*e / 2)
        cy = int(3*e / 2)
        r  = int(3*e / 2) - 4

        pygame.draw.circle(lienzo, self.color, (cx, cy), r, 3)
        pygame.draw.circle(lienzo, (0, 180, 200), (cx, cy), max(r - 6, 2), 1)
        pygame.draw.circle(lienzo, self.color, (cx, cy), 3)

        Rotacion   = pygame.transform.rotate(lienzo, self.alfa)
        Traslacion = Rotacion.get_rect(topleft=(self.x, self.y))
        pantalla.blit(Rotacion, Traslacion)

class Tablero(Base):
    
    def __init__(self, x, y, e):
        super().__init__(x, y, e)

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((9*e, 9*e), pygame.SRCALPHA)

        pygame.draw.rect(lienzo, (100, 100, 255), (0, 0, 9*e, 9*e), 3)

        pygame.draw.line(lienzo, self.color, (3*e, 0), (3*e, 9*e), 2)
        pygame.draw.line(lienzo, self.color, (6*e, 0), (6*e, 9*e), 2)
        pygame.draw.line(lienzo, self.color, (0, 3*e), (9*e, 3*e), 2)
        pygame.draw.line(lienzo, self.color, (0, 6*e), (9*e, 6*e), 2)

        Rotacion   = pygame.transform.rotate(lienzo, self.alfa)
        Traslacion = Rotacion.get_rect(topleft=(self.x, self.y))
        pantalla.blit(Rotacion, Traslacion)

class Cursor:
    

    def __init__(self, fila, columna):
        self.fila    = fila
        self.columna = columna

    def moverArriba(self):
        if self.fila > 0:
            self.fila -= 1

    def moverAbajo(self):
        if self.fila < 2:
            self.fila += 1

    def moverIzquierda(self):
        if self.columna > 0:
            self.columna -= 1

    def moverDerecha(self):
        if self.columna < 2:
            self.columna += 1

    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna

    def getPosicion(self):
        return (self.fila, self.columna)

class CursorGrafico:
    

    def render(self, pantalla, x, y, e, color, pulso):
        lienzo = pygame.Surface((3*e, 3*e), pygame.SRCALPHA)

        grosor = 2 + pulso // 8
        pygame.draw.rect(lienzo, color, (e//2, e//2, 2*e, 2*e), grosor)

        tam = e // 3
        pygame.draw.line(lienzo, (255, 255, 0), (e//2, e//2), (e//2 + tam, e//2), 2)
        pygame.draw.line(lienzo, (255, 255, 0), (e//2, e//2), (e//2, e//2 + tam), 2)

        Rotacion   = pygame.transform.rotate(lienzo, 0)
        Traslacion = Rotacion.get_rect(topleft=(x, y))
        pantalla.blit(Rotacion, Traslacion)

class TresEnRaya:
    

    VACIO   = 0
    FICHA_X = 1
    FICHA_O = 2
    MAX_FICHAS = 6

    def __init__(self):
        self.matriz = [
            [self.VACIO, self.VACIO, self.VACIO],
            [self.VACIO, self.VACIO, self.VACIO],
            [self.VACIO, self.VACIO, self.VACIO]
        ]
        self.turno   = self.FICHA_X
        self.ganador = self.VACIO
        self.fichasColocadas = []

        self.victoriasX  = 0
        self.victoriasO  = 0
        self.partidas    = 0

    def getMatriz(self):
        return self.matriz

    def getTurno(self):
        return self.turno

    def getGanador(self):
        return self.ganador

    def jugar(self, fila, columna):
        if self.matriz[fila][columna] != self.VACIO:
            return False

        self.matriz[fila][columna] = self.turno

        self.fichasColocadas.append((fila, columna))
        if len(self.fichasColocadas) > self.MAX_FICHAS:
            filaAnt, colAnt = self.fichasColocadas.pop(0)
            self.matriz[filaAnt][colAnt] = self.VACIO

        self.verificarGanador()

        if self.ganador == self.VACIO:
            if self.turno == self.FICHA_X:
                self.turno = self.FICHA_O
            else:
                self.turno = self.FICHA_X
        else:
            self.partidas += 1
            if self.ganador == self.FICHA_X:
                self.victoriasX += 1
            else:
                self.victoriasO += 1

        return True

    def verificarGanador(self):
        m = self.matriz

        for fila in range(3):
            if m[fila][0] != self.VACIO and \
               m[fila][0] == m[fila][1] == m[fila][2]:
                self.ganador = m[fila][0]
                return

        for columna in range(3):
            if m[0][columna] != self.VACIO and \
               m[0][columna] == m[1][columna] == m[2][columna]:
                self.ganador = m[0][columna]
                return

        if m[0][0] != self.VACIO and m[0][0] == m[1][1] == m[2][2]:
            self.ganador = m[0][0]
            return

        if m[0][2] != self.VACIO and m[0][2] == m[1][1] == m[2][0]:
            self.ganador = m[0][2]
            return

    def hayEmpate(self):
        if self.ganador != self.VACIO:
            return False
        for fila in self.matriz:
            for casilla in fila:
                if casilla == self.VACIO:
                    return False
        self.partidas += 1
        return True

    def reiniciar(self):
        self.matriz = [
            [self.VACIO, self.VACIO, self.VACIO],
            [self.VACIO, self.VACIO, self.VACIO],
            [self.VACIO, self.VACIO, self.VACIO]
        ]
        self.turno   = self.FICHA_X
        self.ganador = self.VACIO
        self.fichasColocadas = []

class EscenaTresEnRaya:
    

    def __init__(self):
        self.e = 30

        self.incEscalaX = 0.5
        self.incEscalaO = 0.5
        
        try:
            ruta_vic = os.path.join(BASE_DIR, "victoria.mp3")
            self.sonido_victoria = pygame.mixer.Sound(ruta_vic)
        except Exception as e:
            print("No se pudo cargar victoria.mp3:", e)
            self.sonido_victoria = None
            
        try:
            ruta_emp = os.path.join(BASE_DIR, "empate.mp3")
            self.sonido_empate = pygame.mixer.Sound(ruta_emp)
        except Exception as e:
            print("No se pudo cargar empate.mp3:", e)
            self.sonido_empate = None
            
        self.sonido_reproducido = False

        self.tablero = Tablero(50, 50, self.e)
        self.tablero.setColor((200, 200, 255))

        self.cursor = Cursor(1, 1)
        self.cursorGrafico = CursorGrafico()
        self.cursorPulso = 0
        self.cursorIncPulso = 2

        self.juego = TresEnRaya()

        self.xTurno = X(380, 60, self.e // 2)
        self.xTurno.setColor((255, 80, 80))

        self.oTurno = O(460, 60, self.e // 2)
        self.oTurno.setColor((0, 220, 220))

        self.fuente      = pygame.font.SysFont("monospace", 18)
        self.fuenteGrande = pygame.font.SysFont("monospace", 28, bold=True)

    def input(self, evento):
        if evento.type != pygame.KEYDOWN:
            return

        if self.juego.getGanador() != TresEnRaya.VACIO or self.juego.hayEmpate():
            if evento.key == pygame.K_r:
                self.reiniciar()
            return

        if evento.key == pygame.K_UP:
            self.cursor.moverArriba()
        elif evento.key == pygame.K_DOWN:
            self.cursor.moverAbajo()
        elif evento.key == pygame.K_LEFT:
            self.cursor.moverIzquierda()
        elif evento.key == pygame.K_RIGHT:
            self.cursor.moverDerecha()
        elif evento.key == pygame.K_SPACE:
            self.juego.jugar(self.cursor.getFila(), self.cursor.getColumna())

    def update(self):
        ganador = self.juego.getGanador()
        empate = self.juego.hayEmpate()
        
        if ganador != TresEnRaya.VACIO or empate:
            if not self.sonido_reproducido:
                self.sonido_reproducido = True
                try:
                    pygame.mixer.stop()
                    pygame.mixer.music.stop()
                except: pass
                
                if ganador != TresEnRaya.VACIO:
                    if self.sonido_victoria: self.sonido_victoria.play()
                else:
                    if self.sonido_empate: self.sonido_empate.play()
            return

        if self.juego.getTurno() == TresEnRaya.FICHA_X:
            if self.xTurno.e >= 0.5*self.e or self.xTurno.e <= self.e//4:
                self.incEscalaX = -self.incEscalaX
            self.xTurno.e += self.incEscalaX
        else:
            if self.oTurno.e >= 0.5*self.e or self.oTurno.e <= self.e//4:
                self.incEscalaO = -self.incEscalaO
            self.oTurno.e += self.incEscalaO

        if self.juego.getTurno() == TresEnRaya.FICHA_X:
            self.xTurno.alfa += 2
        else:
            self.oTurno.alfa += 2

        self.cursorPulso += self.cursorIncPulso
        if self.cursorPulso >= 20 or self.cursorPulso <= 0:
            self.cursorIncPulso = -self.cursorIncPulso

    def render(self, pantalla):
        self.tablero.render(pantalla)

        x = self.tablero.x + self.cursor.getColumna() * 3 * self.e
        y = self.tablero.y + self.cursor.getFila()    * 3 * self.e

        colorCursor = (255, 80, 80) if self.juego.getTurno() == TresEnRaya.FICHA_X \
                      else (0, 220, 220)
        self.cursorGrafico.render(pantalla, x, y, self.e, colorCursor, self.cursorPulso)

        matriz = self.juego.getMatriz()
        for fila in range(3):
            for columna in range(3):
                px = self.tablero.x + columna * 3 * self.e
                py = self.tablero.y + fila    * 3 * self.e

                if matriz[fila][columna] == TresEnRaya.FICHA_X:
                    ficha = X(px, py, self.e)
                    ficha.setColor((255, 80, 80))
                    ficha.render(pantalla)

                elif matriz[fila][columna] == TresEnRaya.FICHA_O:
                    ficha = O(px, py, self.e)
                    ficha.setColor((0, 220, 220))
                    ficha.render(pantalla)

        self.xTurno.render(pantalla)
        self.oTurno.render(pantalla)

        self._renderPanel(pantalla)

        ganador = self.juego.getGanador()
        if ganador != TresEnRaya.VACIO:
            nombre = "X" if ganador == TresEnRaya.FICHA_X else "O"
            self._renderMensaje(pantalla, f"¡Gana {nombre}!  [R] reiniciar")
        elif self.juego.hayEmpate():
            self._renderMensaje(pantalla, "¡Empate!  [R] reiniciar")

    def _renderPanel(self, pantalla):
        
        turno   = self.juego.getTurno()
        nombre  = "X" if turno == TresEnRaya.FICHA_X else "O"
        textoT  = self.fuente.render(f"Turno: {nombre}", True, (220, 220, 220))
        pantalla.blit(textoT, (360, 30))

        textoX  = self.fuente.render(
            f"Victorias X: {self.juego.victoriasX}", True, (255, 100, 100))
        textoO  = self.fuente.render(
            f"Victorias O: {self.juego.victoriasO}", True, (0, 220, 220))
        textoP  = self.fuente.render(
            f"Partidas: {self.juego.partidas}",      True, (200, 200, 200))

        pantalla.blit(textoX, (360, 160))
        pantalla.blit(textoO, (360, 185))
        pantalla.blit(textoP, (360, 210))

        ayuda = self.fuente.render("Flechas+Espacio", True, (150, 150, 150))
        pantalla.blit(ayuda, (360, 350))

    def _renderMensaje(self, pantalla, texto):
        
        superficie = self.fuenteGrande.render(texto, True, (255, 255, 0))
        rect = superficie.get_rect(center=(300, 370))
        pantalla.blit(superficie, rect)

    def reiniciar(self):
        try:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
        except:
            pass
        self.sonido_reproducido = False

        self.juego.reiniciar()
        self.cursor   = Cursor(1, 1)
        self.cursorPulso = 0
        self.cursorIncPulso = 2
        self.xTurno.alfa = 0
        self.oTurno.alfa = 0
        self.xTurno.e    = self.e // 2
        self.oTurno.e    = self.e // 2

pygame.init()
try:
    pygame.mixer.init()
except:
    pass

ANCHO = 600
ALTO  = 420
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tres en Raya Pro+")

clock = pygame.time.Clock()

escena = EscenaTresEnRaya()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        escena.input(evento)

    escena.update()

    pantalla.fill((20, 20, 40))
    escena.render(pantalla)

    pygame.display.flip()
    clock.tick(60)
