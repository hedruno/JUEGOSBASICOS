import pygame
import sys
import math

# ─────────────────────────────────────────────
#  ENTIDADES GRAFICAS  (solo saben dibujarse)
# ─────────────────────────────────────────────

class Base:
    """Clase base con traslación, rotación y escalado."""
    def __init__(self, x, y, e):
        self.x = x
        self.y = y
        self.e = e
        self.color = (255, 255, 255)
        self.alfa = 0          # ángulo de rotación

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
    """Ficha X: dos líneas diagonales con borde decorativo."""
    def __init__(self, x, y, e):
        super().__init__(x, y, e)

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((3*e, 3*e), pygame.SRCALPHA)

        # Borde exterior
        pygame.draw.rect(lienzo, (180, 0, 0), (4, 4, 3*e-8, 3*e-8), 2)

        # Líneas principales más gruesas
        pygame.draw.line(lienzo, self.color, (6, 6), (3*e-6, 3*e-6), 3)
        pygame.draw.line(lienzo, self.color, (3*e-6, 6), (6, 3*e-6), 3)

        # Líneas secundarias (color más suave)
        pygame.draw.line(lienzo, (255, 100, 100), (10, 6), (3*e-6, 3*e-10), 1)
        pygame.draw.line(lienzo, (255, 100, 100), (3*e-10, 6), (6, 3*e-10), 1)

        # Traslación + Rotación + Escalado (igual que el original)
        Rotacion  = pygame.transform.rotate(lienzo, self.alfa)
        Traslacion = Rotacion.get_rect(topleft=(self.x, self.y))
        pantalla.blit(Rotacion, Traslacion)


class O(Base):
    """Ficha O: doble circunferencia con punto central."""
    def __init__(self, x, y, e):
        super().__init__(x, y, e)

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((3*e, 3*e), pygame.SRCALPHA)

        cx = int(3*e / 2)
        cy = int(3*e / 2)
        r  = int(3*e / 2) - 4

        # Circunferencia exterior
        pygame.draw.circle(lienzo, self.color, (cx, cy), r, 3)
        # Circunferencia interior (detalle decorativo)
        pygame.draw.circle(lienzo, (0, 180, 200), (cx, cy), max(r - 6, 2), 1)
        # Punto central
        pygame.draw.circle(lienzo, self.color, (cx, cy), 3)

        Rotacion   = pygame.transform.rotate(lienzo, self.alfa)
        Traslacion = Rotacion.get_rect(topleft=(self.x, self.y))
        pantalla.blit(Rotacion, Traslacion)


class Tablero(Base):
    """Tablero con líneas de color y marco exterior."""
    def __init__(self, x, y, e):
        super().__init__(x, y, e)

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((9*e, 9*e), pygame.SRCALPHA)

        # Marco exterior
        pygame.draw.rect(lienzo, (100, 100, 255), (0, 0, 9*e, 9*e), 3)

        # Líneas interiores más gruesas con color diferente
        pygame.draw.line(lienzo, self.color, (3*e, 0), (3*e, 9*e), 2)
        pygame.draw.line(lienzo, self.color, (6*e, 0), (6*e, 9*e), 2)
        pygame.draw.line(lienzo, self.color, (0, 3*e), (9*e, 3*e), 2)
        pygame.draw.line(lienzo, self.color, (0, 6*e), (9*e, 6*e), 2)

        Rotacion   = pygame.transform.rotate(lienzo, self.alfa)
        Traslacion = Rotacion.get_rect(topleft=(self.x, self.y))
        pantalla.blit(Rotacion, Traslacion)


class Cursor:
    """Entidad lógica: posición en fila/columna.
       Solo mantiene la posición y las reglas de movimiento (sin animación)."""

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
    """Parte gráfica del cursor: dibuja según pulso y posición recibidos desde la escena."""

    def render(self, pantalla, x, y, e, color, pulso):
        lienzo = pygame.Surface((3*e, 3*e), pygame.SRCALPHA)

        # Borde pulsante (varía el grosor con el pulso)
        grosor = 2 + pulso // 8
        pygame.draw.rect(lienzo, color, (e//2, e//2, 2*e, 2*e), grosor)

        # Esquinas decorativas
        tam = e // 3
        pygame.draw.line(lienzo, (255, 255, 0), (e//2, e//2), (e//2 + tam, e//2), 2)
        pygame.draw.line(lienzo, (255, 255, 0), (e//2, e//2), (e//2, e//2 + tam), 2)

        Rotacion   = pygame.transform.rotate(lienzo, 0)
        Traslacion = Rotacion.get_rect(topleft=(x, y))
        pantalla.blit(Rotacion, Traslacion)


# ─────────────────────────────────────────────
#  ENTIDAD LÓGICA  (reglas del juego)
# ─────────────────────────────────────────────

class TresEnRaya:
    """Administra el estado del juego: matriz, turnos, ganador y empate."""

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

        # Estadísticas (Trabajo 01 - nueva funcionalidad)
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
            # Eliminar la ficha más antigua del tablero
            filaAnt, colAnt = self.fichasColocadas.pop(0)
            self.matriz[filaAnt][colAnt] = self.VACIO


        self.verificarGanador()

        if self.ganador == self.VACIO:
            if self.turno == self.FICHA_X:
                self.turno = self.FICHA_O
            else:
                self.turno = self.FICHA_X
        else:
            # Sumar victoria
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
        # Contar empate como partida
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


# ─────────────────────────────────────────────
#  ESCENA  (coordinadora de todo)
# ─────────────────────────────────────────────

class EscenaTresEnRaya:
    """Coordina cursor, juego, tablero y fichas.
       Organiza Input → Update → Render."""

    def __init__(self):
        self.e = 30

        self.incEscalaX = 0.5
        self.incEscalaO = 0.5

        # Entidades gráficas
        self.tablero = Tablero(50, 50, self.e)
        self.tablero.setColor((200, 200, 255))

        # Entidad lógica: cursor
        self.cursor = Cursor(1, 1)
        # Cursor gráfico y animación de pulso (antes estaba en la entidad)
        self.cursorGrafico = CursorGrafico()
        self.cursorPulso = 0
        self.cursorIncPulso = 2

        # Entidad lógica: juego
        self.juego = TresEnRaya()

        # Indicadores de turno (animados)
        self.xTurno = X(380, 60, self.e // 2)
        self.xTurno.setColor((255, 80, 80))

        self.oTurno = O(460, 60, self.e // 2)
        self.oTurno.setColor((0, 220, 220))

        # Fuente para texto
        self.fuente      = pygame.font.SysFont("monospace", 18)
        self.fuenteGrande = pygame.font.SysFont("monospace", 28, bold=True)

    # ── INPUT ──────────────────────────────────
    def input(self, evento):
        if evento.type != pygame.KEYDOWN:
            return

        # Si hay ganador o empate solo se acepta R para reiniciar
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

    # ── UPDATE ─────────────────────────────────
    def update(self):
        if self.juego.getGanador() != TresEnRaya.VACIO:
            return
        if self.juego.hayEmpate():
            return

        # Animación de escala en el indicador de turno activo
        if self.juego.getTurno() == TresEnRaya.FICHA_X:
            if self.xTurno.e >= 0.5*self.e or self.xTurno.e <= self.e//4:
                self.incEscalaX = -self.incEscalaX
            self.xTurno.e += self.incEscalaX
        else:
            if self.oTurno.e >= 0.5*self.e or self.oTurno.e <= self.e//4:
                self.incEscalaO = -self.incEscalaO
            self.oTurno.e += self.incEscalaO

        # Rotación continua del indicador de turno
        if self.juego.getTurno() == TresEnRaya.FICHA_X:
            self.xTurno.alfa += 2
        else:
            self.oTurno.alfa += 2

        # Cursor pulsante (la escena maneja la animación y pasa el pulso
        # a la parte gráfica `CursorGrafico` en el render)
        self.cursorPulso += self.cursorIncPulso
        if self.cursorPulso >= 20 or self.cursorPulso <= 0:
            self.cursorIncPulso = -self.cursorIncPulso

    # ── RENDER ─────────────────────────────────
    def render(self, pantalla):
        # Tablero
        self.tablero.render(pantalla)

        # Cursor (conversión mundo lógico → mundo gráfico)
        x = self.tablero.x + self.cursor.getColumna() * 3 * self.e
        y = self.tablero.y + self.cursor.getFila()    * 3 * self.e

        colorCursor = (255, 80, 80) if self.juego.getTurno() == TresEnRaya.FICHA_X \
                      else (0, 220, 220)
        self.cursorGrafico.render(pantalla, x, y, self.e, colorCursor, self.cursorPulso)

        # Fichas en el tablero
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

        # Indicadores de turno
        self.xTurno.render(pantalla)
        self.oTurno.render(pantalla)

        # Panel derecho: turno e instrucciones
        self._renderPanel(pantalla)

        # Mensaje fin de juego
        ganador = self.juego.getGanador()
        if ganador != TresEnRaya.VACIO:
            nombre = "X" if ganador == TresEnRaya.FICHA_X else "O"
            self._renderMensaje(pantalla, f"¡Gana {nombre}!  [R] reiniciar")
        elif self.juego.hayEmpate():
            self._renderMensaje(pantalla, "¡Empate!  [R] reiniciar")

    def _renderPanel(self, pantalla):
        """Dibuja el panel lateral con turno y estadísticas."""
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
        """Mensaje centrado al pie de la ventana."""
        superficie = self.fuenteGrande.render(texto, True, (255, 255, 0))
        rect = superficie.get_rect(center=(300, 370))
        pantalla.blit(superficie, rect)

    # ── REINICIAR ──────────────────────────────
    def reiniciar(self):
        self.juego.reiniciar()
        self.cursor   = Cursor(1, 1)
        self.cursorPulso = 0
        self.cursorIncPulso = 2
        self.xTurno.alfa = 0
        self.oTurno.alfa = 0
        self.xTurno.e    = self.e // 2
        self.oTurno.e    = self.e // 2


# ─────────────────────────────────────────────
#  GAME LOOP
# ─────────────────────────────────────────────

pygame.init()

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

    pantalla.fill((20, 20, 40))      # fondo azul oscuro
    escena.render(pantalla)

    pygame.display.flip()
    clock.tick(60)
