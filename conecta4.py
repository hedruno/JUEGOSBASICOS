import pygame
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Base:
    
    def __init__(self, x, y, e):
        self.x = x
        self.y = y
        self.e = e
        self.color = (255, 255, 255)
        self.alfa  = 0

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

class FichaO(Base):
    

    def __init__(self, x, y, e, color_principal, color_detalle):
        super().__init__(x, y, e)
        self.color_principal = color_principal
        self.color_detalle   = color_detalle

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((e, e), pygame.SRCALPHA)

        cx = e // 2
        cy = e // 2
        r  = e // 2 - 4

        pygame.draw.circle(lienzo, self.color_principal, (cx, cy), r, 3)
        pygame.draw.circle(lienzo, self.color_detalle,   (cx, cy), max(r - 4, 1), 1)
        pygame.draw.circle(lienzo, self.color_principal, (cx, cy), 3)

        Rotacion   = pygame.transform.rotate(lienzo, self.alfa)
        Traslacion = Rotacion.get_rect(topleft=(self.x, self.y))
        pantalla.blit(Rotacion, Traslacion)

class TableroConecta(Base):
    
    COLUMNAS = 7
    FILAS    = 6

    def __init__(self, x, y, e):
        super().__init__(x, y, e)

    def render(self, pantalla):
        e   = self.e
        col = self.COLUMNAS
        fil = self.FILAS

        lienzo = pygame.Surface((col*e, fil*e), pygame.SRCALPHA)

        pygame.draw.rect(lienzo, (50, 50, 200), (0, 0, col*e, fil*e), 4)

        for c in range(1, col):
            pygame.draw.line(lienzo, self.color, (c*e, 0), (c*e, fil*e), 1)

        for f in range(1, fil):
            pygame.draw.line(lienzo, self.color, (0, f*e), (col*e, f*e), 1)

        Rotacion   = pygame.transform.rotate(lienzo, self.alfa)
        Traslacion = Rotacion.get_rect(topleft=(self.x, self.y))
        pantalla.blit(Rotacion, Traslacion)

class CursorColumna:
    

    def __init__(self, columna=0):
        self.columna  = columna

    def moverIzquierda(self):
        if self.columna > 0:
            self.columna -= 1

    def moverDerecha(self):
        if self.columna < TableroConecta.COLUMNAS - 1:
            self.columna += 1

    def getColumna(self):
        return self.columna

class CursorColumnaGrafico:
    

    def render(self, pantalla, x, y, e, color, pulso):
        lienzo = pygame.Surface((e, e), pygame.SRCALPHA)

        margen = 4 + pulso // 6
        puntos = [
            (e // 2,          e - margen),
            (margen,          margen),
            (e - margen,      margen)
        ]
        pygame.draw.polygon(lienzo, color, puntos)

        Rotacion   = pygame.transform.rotate(lienzo, 0)
        Traslacion = Rotacion.get_rect(topleft=(x, y))
        pantalla.blit(Rotacion, Traslacion)

class Conecta4:

    VACIO    = 0
    JUGADOR1 = 1
    JUGADOR2 = 2

    FILAS    = 6
    COLUMNAS = 7

    def __init__(self):
        self.matriz = [
            [self.VACIO] * self.COLUMNAS
            for _ in range(self.FILAS)
        ]
        self.turno   = self.JUGADOR1
        self.ganador = self.VACIO
        self.victoriasRojo     = 0
        self.victoriasAmarillo = 0
        self.empates           = 0
        self.partidas          = 0

    def getMatriz(self):
        return self.matriz

    def getTurno(self):
        return self.turno

    def getGanador(self):
        return self.ganador

    def jugar(self, columna):
        
        fila = self._filaLibre(columna)
        if fila is None:
            return False

        self.matriz[fila][columna] = self.turno
        self.verificarGanador()

        if self.ganador != self.VACIO:
            self.partidas += 1
            if self.ganador == self.JUGADOR1:
                self.victoriasRojo += 1
            else:    
                self.victoriasAmarillo += 1
        elif self.hayEmpate():
            self.partidas += 1
            self.empates += 1
        else:
            if self.turno == self.JUGADOR1:
                self.turno = self.JUGADOR2
            else:
                self.turno = self.JUGADOR1

        return True

    def _filaLibre(self, columna):
        
        for fila in range(self.FILAS - 1, -1, -1):
            if self.matriz[fila][columna] == self.VACIO:
                return fila
        return None

    def columnaLlena(self, columna):
        return self._filaLibre(columna) is None

    def verificarGanador(self):
        
        m   = self.matriz
        fil = self.FILAS
        col = self.COLUMNAS

        for f in range(fil):
            for c in range(col - 3):
                val = m[f][c]
                if val != self.VACIO and \
                   val == m[f][c+1] == m[f][c+2] == m[f][c+3]:
                    self.ganador = val
                    return

        for f in range(fil - 3):
            for c in range(col):
                val = m[f][c]
                if val != self.VACIO and \
                   val == m[f+1][c] == m[f+2][c] == m[f+3][c]:
                    self.ganador = val
                    return

        for f in range(fil - 3):
            for c in range(col - 3):
                val = m[f][c]
                if val != self.VACIO and \
                   val == m[f+1][c+1] == m[f+2][c+2] == m[f+3][c+3]:
                    self.ganador = val
                    return

        for f in range(3, fil):
            for c in range(col - 3):
                val = m[f][c]
                if val != self.VACIO and \
                   val == m[f-1][c+1] == m[f-2][c+2] == m[f-3][c+3]:
                    self.ganador = val
                    return

    def hayEmpate(self):
        
        if self.ganador != self.VACIO:
            return False
        for c in range(self.COLUMNAS):
            if not self.columnaLlena(c):
                return False
        return True

    def reiniciar(self):
        self.matriz = [
            [self.VACIO] * self.COLUMNAS
            for _ in range(self.FILAS)
        ]
        self.turno   = self.JUGADOR1
        self.ganador = self.VACIO

class EscenaConecta4:

    def __init__(self):
        self.e = 70

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

        self.tablero = TableroConecta(30, 60, self.e)
        self.tablero.setColor((100, 100, 200))

        self.cursor = CursorColumna(0)
        self.cursorGrafico = CursorColumnaGrafico()
        self.cursorPulso = 0
        self.cursorIncPulso = 3

        self.juego = Conecta4()

        self.fuente       = pygame.font.SysFont("monospace", 16)
        self.fuenteGrande = pygame.font.SysFont("monospace", 26, bold=True)

    def input(self, evento):
        if evento.type != pygame.KEYDOWN:
            return

        if self.juego.getGanador() != Conecta4.VACIO or self.juego.hayEmpate():
            if evento.key == pygame.K_r:
                self.reiniciar()
            return

        if evento.key == pygame.K_LEFT:
            self.cursor.moverIzquierda()
        elif evento.key == pygame.K_RIGHT:
            self.cursor.moverDerecha()
        elif evento.key == pygame.K_SPACE:
            self.juego.jugar(self.cursor.getColumna())

    def update(self):
        ganador = self.juego.getGanador()
        empate = self.juego.hayEmpate()
        
        if ganador != Conecta4.VACIO or empate:
            if not self.sonido_reproducido:
                self.sonido_reproducido = True
                try:
                    pygame.mixer.stop()
                    pygame.mixer.music.stop()
                except: pass
                
                if ganador != Conecta4.VACIO:
                    if self.sonido_victoria: self.sonido_victoria.play()
                else:
                    if self.sonido_empate: self.sonido_empate.play()
            return

        self.cursorPulso += self.cursorIncPulso
        if self.cursorPulso >= 18 or self.cursorPulso <= 0:
            self.cursorIncPulso = -self.cursorIncPulso

    def render(self, pantalla):
        self.tablero.render(pantalla)

        xCursor = self.tablero.x + self.cursor.getColumna() * self.e
        yCursor = self.tablero.y - self.e

        colorCursor = (255, 80, 80) if self.juego.getTurno() == Conecta4.JUGADOR1 \
                      else (255, 220, 0)
        self.cursorGrafico.render(pantalla, xCursor, yCursor, self.e, colorCursor, self.cursorPulso)

        matriz = self.juego.getMatriz()
        for fila in range(Conecta4.FILAS):
            for columna in range(Conecta4.COLUMNAS):
                px = self.tablero.x + columna * self.e
                py = self.tablero.y + fila    * self.e

                if matriz[fila][columna] == Conecta4.JUGADOR1:
                    ficha = FichaO(px, py, self.e,
                   color_principal=(220, 50, 50),
                   color_detalle=(200, 0, 0))
                    ficha.render(pantalla)

                elif matriz[fila][columna] == Conecta4.JUGADOR2:
                    ficha = FichaO(px, py, self.e,
                   color_principal=(230, 210, 0),
                   color_detalle=(180, 160, 0))
                    ficha.render(pantalla)

        self._renderPanel(pantalla)

        ganador = self.juego.getGanador()
        if ganador != Conecta4.VACIO:
            nombre = "Rojo" if ganador == Conecta4.JUGADOR1 else "Amarillo"
            self._renderMensaje(pantalla, f"¡Gana {nombre}!  [R] reiniciar")
        elif self.juego.hayEmpate():
            self._renderMensaje(pantalla, "¡Empate!  [R] reiniciar")

    def _renderPanel(self, pantalla):
        turno  = self.juego.getTurno()
        nombre = "Rojo" if turno == Conecta4.JUGADOR1 else "Amarillo"
        color  = (255, 100, 100) if turno == Conecta4.JUGADOR1 else (255, 220, 0)

        textoT = self.fuente.render(f"Turno: {nombre}", True, color)
        pantalla.blit(textoT, (550, 10))

        textoR = self.fuente.render(f"Victorias Rojo: {self.juego.victoriasRojo}", True, (200, 50, 50))
        pantalla.blit(textoR, (550, 40))

        textoA = self.fuente.render(f"Victorias Amarillo: {self.juego.victoriasAmarillo}", True, (230, 210, 0))
        pantalla.blit(textoA, (550, 70))

        textoE = self.fuente.render(f"Empates: {self.juego.empates}", True, (150, 150, 150))
        pantalla.blit(textoE, (550, 100))

        textoP = self.fuente.render(f"Partidas: {self.juego.partidas}", True, (150, 150, 150))
        pantalla.blit(textoP, (550, 130))

        ayuda = self.fuente.render("← → para mover  Espacio para soltar", True, (150, 150, 150))
        pantalla.blit(ayuda, (10, 530))

    def _renderMensaje(self, pantalla, texto):
        superficie = self.fuenteGrande.render(texto, True, (255, 255, 0))
        rect = superficie.get_rect(center=(265, 510))
        pantalla.blit(superficie, rect)

    def reiniciar(self):
        try:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
        except:
            pass
        self.sonido_reproducido = False

        self.juego.reiniciar()
        self.cursor = CursorColumna(0)
        self.cursorPulso = 0
        self.cursorIncPulso = 3

pygame.init()
try:
    pygame.mixer.init()
except:
    pass

ANCHO = 800
ALTO  = 560
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Conecta 4")

clock = pygame.time.Clock()

escena = EscenaConecta4()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        escena.input(evento)

    escena.update()

    pantalla.fill((10, 10, 30))
    escena.render(pantalla)

    pygame.display.flip()
    clock.tick(60)