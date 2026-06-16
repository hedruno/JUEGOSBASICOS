import pygame
import sys
import math
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TAMANO = 4

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
        longitud = TAMANO * 3 * e
        lienzo = pygame.Surface((longitud, longitud), pygame.SRCALPHA)

        pygame.draw.rect(lienzo, (100, 100, 255), (0, 0, longitud, longitud), 3)

        for i in range(1, TAMANO):
            pos = i * 3 * e
            pygame.draw.line(lienzo, self.color, (pos, 0), (pos, longitud), 2)
            pygame.draw.line(lienzo, self.color, (0, pos), (longitud, pos), 2)

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
        if self.fila < TAMANO - 1:
            self.fila += 1

    def moverIzquierda(self):
        if self.columna > 0:
            self.columna -= 1

    def moverDerecha(self):
        if self.columna < TAMANO - 1:
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

    def __init__(self):
        self.matriz = [[self.VACIO for _ in range(TAMANO)] for _ in range(TAMANO)]
        self.turno   = self.FICHA_X
        self.ganador = self.VACIO
        
        self.puntosX = 0
        self.puntosO = 0
        self.lineasGanadoras = []
        
        self.juegoTerminado = False

        self.victoriasX  = 0
        self.victoriasO  = 0
        self.empates     = 0
        self.partidas    = 0

    def getMatriz(self):
        return self.matriz

    def getTurno(self):
        return self.turno

    def getGanador(self):
        return self.ganador

    def jugar(self, fila, columna):
        if self.matriz[fila][columna] != self.VACIO or self.juegoTerminado:
            return False
    
        self.matriz[fila][columna] = self.turno
        self.contarPuntos()

        if TAMANO == 3 and (self.puntosX > 0 or self.puntosO > 0):
            self.juegoTerminado = True
            self.partidas += 1
            if self.puntosX > 0:
                self.ganador = self.FICHA_X
                self.victoriasX += 1
            else:
                self.ganador = self.FICHA_O
                self.victoriasO += 1
        elif self.tableroLleno():
            self.juegoTerminado = True
            self.partidas += 1
            if self.puntosX > self.puntosO:
                self.ganador = self.FICHA_X
                self.victoriasX += 1
            elif self.puntosO > self.puntosX:
                self.ganador = self.FICHA_O
                self.victoriasO += 1
            else:
                self.ganador = self.VACIO
                self.empates += 1
        else:
            if self.turno == self.FICHA_X:
                self.turno = self.FICHA_O
            else:
                self.turno = self.FICHA_X

        return True

    def contarPuntos(self):
        m = self.matriz
        self.puntosX = 0
        self.puntosO = 0
        self.lineasGanadoras = []

        for fila in range(TAMANO):
            for columna in range(TAMANO - 2):
                if m[fila][columna] != self.VACIO and m[fila][columna] == m[fila][columna+1] == m[fila][columna+2]:
                    self.lineasGanadoras.append(((fila, columna), (fila, columna+2), m[fila][columna]))
                    if m[fila][columna] == self.FICHA_X: self.puntosX += 1
                    else: self.puntosO += 1

        for columna in range(TAMANO):
            for fila in range(TAMANO - 2):
                if m[fila][columna] != self.VACIO and m[fila][columna] == m[fila+1][columna] == m[fila+2][columna]:
                    self.lineasGanadoras.append(((fila, columna), (fila+2, columna), m[fila][columna]))
                    if m[fila][columna] == self.FICHA_X: self.puntosX += 1
                    else: self.puntosO += 1

        for fila in range(TAMANO - 2):
            for columna in range(TAMANO - 2):
                if m[fila][columna] != self.VACIO and m[fila][columna] == m[fila+1][columna+1] == m[fila+2][columna+2]:
                    self.lineasGanadoras.append(((fila, columna), (fila+2, columna+2), m[fila][columna]))
                    if m[fila][columna] == self.FICHA_X: self.puntosX += 1
                    else: self.puntosO += 1

        for fila in range(TAMANO - 2):
            for columna in range(2, TAMANO):
                if m[fila][columna] != self.VACIO and m[fila][columna] == m[fila+1][columna-1] == m[fila+2][columna-2]:
                    self.lineasGanadoras.append(((fila, columna), (fila+2, columna-2), m[fila][columna]))
                    if m[fila][columna] == self.FICHA_X: self.puntosX += 1
                    else: self.puntosO += 1

    def tableroLleno(self):
        for fila in self.matriz:
            for casilla in fila:
                if casilla == self.VACIO:
                    return False
        return True

    def hayEmpate(self):
        return self.juegoTerminado and self.ganador == self.VACIO

    def reiniciar(self):
        self.matriz = [[self.VACIO for _ in range(TAMANO)] for _ in range(TAMANO)]
        self.turno   = self.FICHA_X
        self.ganador = self.VACIO
        self.puntosX = 0
        self.puntosO = 0
        self.lineasGanadoras = []
        self.juegoTerminado = False

class EscenaTresEnRaya:
    

    def __init__(self):
        self.e = int(90 / TAMANO)
        if self.e > 30: self.e = 30

        self.incEscalaX = 0.5
        self.incEscalaO = 0.5
        
        try:
            ruta_vic = os.path.join(BASE_DIR, "victoria.mp3")
            self.sonido_victoria = pygame.mixer.Sound(ruta_vic)
            print("Sonido victoria cargado con éxito.")
        except Exception as e:
            print("No se pudo cargar victoria.mp3:", e)
            self.sonido_victoria = None
            
        try:
            ruta_emp = os.path.join(BASE_DIR, "empate.mp3")
            self.sonido_empate = pygame.mixer.Sound(ruta_emp)
            print("Sonido empate cargado con éxito.")
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

        if self.juego.juegoTerminado:
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
        if self.juego.juegoTerminado:
            if not self.sonido_reproducido:
                self.sonido_reproducido = True
                try:
                    pygame.mixer.stop()
                    pygame.mixer.music.stop()
                except: pass
                
                ganador = self.juego.getGanador()
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
        for fila in range(TAMANO):
            for columna in range(TAMANO):
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

        for (f1, c1), (f2, c2), jugador in self.juego.lineasGanadoras:
            x1 = self.tablero.x + c1 * 3 * self.e + int(1.5 * self.e)
            y1 = self.tablero.y + f1 * 3 * self.e + int(1.5 * self.e)
            x2 = self.tablero.x + c2 * 3 * self.e + int(1.5 * self.e)
            y2 = self.tablero.y + f2 * 3 * self.e + int(1.5 * self.e)
            color = (255, 255, 100) if jugador == TresEnRaya.FICHA_X else (150, 255, 150)
            pygame.draw.line(pantalla, color, (x1, y1), (x2, y2), 6)

        self.xTurno.render(pantalla)
        self.oTurno.render(pantalla)

        self._renderPanel(pantalla)

        if self.juego.juegoTerminado:
            ganador = self.juego.getGanador()
            if ganador != TresEnRaya.VACIO:
                nombre = "X" if ganador == TresEnRaya.FICHA_X else "O"
                self._renderMensaje(pantalla, f"¡Gana {nombre}! [R] reiniciar")
            else:
                self._renderMensaje(pantalla, "¡Empate! [R] reiniciar")

    def _renderPanel(self, pantalla):
        
        turno   = self.juego.getTurno()
        nombre  = "X" if turno == TresEnRaya.FICHA_X else "O"
        textoT  = self.fuente.render(f"Turno: {nombre}", True, (220, 220, 220))
        pantalla.blit(textoT, (360, 30))
        
        textoPtsX  = self.fuente.render(
            f"Puntos X: {self.juego.puntosX}", True, (255, 100, 100))
        textoPtsO  = self.fuente.render(
            f"Puntos O: {self.juego.puntosO}", True, (0, 220, 220))
        
        pantalla.blit(textoPtsX, (360, 100))
        pantalla.blit(textoPtsO, (360, 125))

        textoX  = self.fuente.render(
            f"Victorias X: {self.juego.victoriasX}", True, (255, 100, 100))
        textoO  = self.fuente.render(
            f"Victorias O: {self.juego.victoriasO}", True, (0, 220, 220))
        textoE  = self.fuente.render(
            f"Empates: {self.juego.empates}",      True, (200, 200, 200))
        textoP  = self.fuente.render(
            f"Partidas: {self.juego.partidas}",      True, (200, 200, 200))

        pantalla.blit(textoX, (360, 170))
        pantalla.blit(textoO, (360, 195))
        pantalla.blit(textoE, (360, 220))
        pantalla.blit(textoP, (360, 245))

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
