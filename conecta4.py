import pygame
import sys

# ─────────────────────────────────────────────
#  ENTIDADES GRAFICAS  (solo saben dibujarse)
#  Reutilizadas/adaptadas de Tres en Raya Pro+
# ─────────────────────────────────────────────

class Base:
    """Clase base con traslación, rotación y escalado.
       REUTILIZADA sin cambios de Tres en Raya."""
    def __init__(self, x, y, e):
        self.x = x
        self.y = y
        self.e = e
        self.color = (255, 255, 255)
        self.alfa  = 0          # ángulo de rotación

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


class FichaRoja(Base):
    """Ficha circular del jugador 1 (rojo).
       NUEVA para Conecta 4, hereda Base."""
    def __init__(self, x, y, e):
        super().__init__(x, y, e)

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((e, e), pygame.SRCALPHA)

        cx = e // 2
        cy = e // 2
        r  = e // 2 - 3

        pygame.draw.circle(lienzo, self.color,       (cx, cy), r)
        pygame.draw.circle(lienzo, (200, 0, 0),      (cx, cy), r, 2)
        # Brillo decorativo
        pygame.draw.circle(lienzo, (255, 150, 150),  (cx - r//3, cy - r//3), r//4)

        # Traslación + Rotación + Escalado (mismo patrón que el original)
        Rotacion   = pygame.transform.rotate(lienzo, self.alfa)
        Traslacion = Rotacion.get_rect(topleft=(self.x, self.y))
        pantalla.blit(Rotacion, Traslacion)


class FichaAmarilla(Base):
    """Ficha circular del jugador 2 (amarillo).
       NUEVA para Conecta 4, hereda Base."""
    def __init__(self, x, y, e):
        super().__init__(x, y, e)

    def render(self, pantalla):
        e = self.e
        lienzo = pygame.Surface((e, e), pygame.SRCALPHA)

        cx = e // 2
        cy = e // 2
        r  = e // 2 - 3

        pygame.draw.circle(lienzo, self.color,      (cx, cy), r)
        pygame.draw.circle(lienzo, (200, 180, 0),   (cx, cy), r, 2)
        # Brillo decorativo
        pygame.draw.circle(lienzo, (255, 255, 150), (cx - r//3, cy - r//3), r//4)

        Rotacion   = pygame.transform.rotate(lienzo, self.alfa)
        Traslacion = Rotacion.get_rect(topleft=(self.x, self.y))
        pantalla.blit(Rotacion, Traslacion)


class TableroConecta(Base):
    """Tablero de 7 columnas × 6 filas para Conecta 4.
       ADAPTADO del Tablero de Tres en Raya."""
    COLUMNAS = 7
    FILAS    = 6

    def __init__(self, x, y, e):
        super().__init__(x, y, e)

    def render(self, pantalla):
        e   = self.e
        col = self.COLUMNAS
        fil = self.FILAS

        lienzo = pygame.Surface((col*e, fil*e), pygame.SRCALPHA)

        # Marco exterior
        pygame.draw.rect(lienzo, (50, 50, 200), (0, 0, col*e, fil*e), 4)

        # Líneas verticales
        for c in range(1, col):
            pygame.draw.line(lienzo, self.color, (c*e, 0), (c*e, fil*e), 1)

        # Líneas horizontales
        for f in range(1, fil):
            pygame.draw.line(lienzo, self.color, (0, f*e), (col*e, f*e), 1)

        # Traslación + Rotación + Escalado (mismo patrón)
        Rotacion   = pygame.transform.rotate(lienzo, self.alfa)
        Traslacion = Rotacion.get_rect(topleft=(self.x, self.y))
        pantalla.blit(Rotacion, Traslacion)


class CursorColumna:
    """Entidad lógica: selecciona columnas (no celdas individuales).
       ADAPTADA del Cursor de Tres en Raya.
       Mundo lógico: columna  →  Mundo gráfico: x"""

    def __init__(self, columna=0):
        self.columna  = columna
        self.pulso    = 0
        self.incPulso = 3

    def moverIzquierda(self):
        if self.columna > 0:
            self.columna -= 1

    def moverDerecha(self):
        if self.columna < TableroConecta.COLUMNAS - 1:
            self.columna += 1

    def getColumna(self):
        return self.columna

    def update(self):
        """Animación pulsante."""
        self.pulso += self.incPulso
        if self.pulso >= 18 or self.pulso <= 0:
            self.incPulso = -self.incPulso

    def render(self, pantalla, x, y, e, color):
        """Dibuja un triángulo apuntando hacia abajo sobre la columna activa."""
        lienzo = pygame.Surface((e, e), pygame.SRCALPHA)

        # Triángulo indicador pulsante
        margen = 4 + self.pulso // 6
        puntos = [
            (e // 2,          e - margen),   # punta abajo
            (margen,          margen),        # esquina izquierda
            (e - margen,      margen)         # esquina derecha
        ]
        pygame.draw.polygon(lienzo, color, puntos)

        Rotacion   = pygame.transform.rotate(lienzo, 0)
        Traslacion = Rotacion.get_rect(topleft=(x, y))
        pantalla.blit(Rotacion, Traslacion)


# ─────────────────────────────────────────────
#  ENTIDAD LÓGICA  (reglas del juego)
# ─────────────────────────────────────────────

class Conecta4:
    """Administra la lógica de Conecta 4.
       NUEVA entidad lógica, misma idea que TresEnRaya:
       matriz, turnos, ganador, empate."""

    VACIO    = 0
    JUGADOR1 = 1   # rojo
    JUGADOR2 = 2   # amarillo

    FILAS    = 6
    COLUMNAS = 7

    def __init__(self):
        # Matriz bidimensional: fila 0 = arriba, fila 5 = abajo
        self.matriz = [
            [self.VACIO] * self.COLUMNAS
            for _ in range(self.FILAS)
        ]
        self.turno   = self.JUGADOR1
        self.ganador = self.VACIO

    def getMatriz(self):
        return self.matriz

    def getTurno(self):
        return self.turno

    def getGanador(self):
        return self.ganador

    def jugar(self, columna):
        """Inserta ficha en la columna: cae a la posición libre más baja."""
        fila = self._filaLibre(columna)
        if fila is None:
            return False          # columna llena

        self.matriz[fila][columna] = self.turno
        self.verificarGanador()

        if self.ganador == self.VACIO:
            # Cambio de turno
            if self.turno == self.JUGADOR1:
                self.turno = self.JUGADOR2
            else:
                self.turno = self.JUGADOR1

        return True

    def _filaLibre(self, columna):
        """Devuelve la fila más baja libre de la columna, o None si está llena."""
        for fila in range(self.FILAS - 1, -1, -1):
            if self.matriz[fila][columna] == self.VACIO:
                return fila
        return None

    def columnaLlena(self, columna):
        return self._filaLibre(columna) is None

    def verificarGanador(self):
        """Comprueba horizontal, vertical y diagonales para 4 en línea."""
        m   = self.matriz
        fil = self.FILAS
        col = self.COLUMNAS

        # Horizontal
        for f in range(fil):
            for c in range(col - 3):
                val = m[f][c]
                if val != self.VACIO and \
                   val == m[f][c+1] == m[f][c+2] == m[f][c+3]:
                    self.ganador = val
                    return

        # Vertical
        for f in range(fil - 3):
            for c in range(col):
                val = m[f][c]
                if val != self.VACIO and \
                   val == m[f+1][c] == m[f+2][c] == m[f+3][c]:
                    self.ganador = val
                    return

        # Diagonal descendente (↘)
        for f in range(fil - 3):
            for c in range(col - 3):
                val = m[f][c]
                if val != self.VACIO and \
                   val == m[f+1][c+1] == m[f+2][c+2] == m[f+3][c+3]:
                    self.ganador = val
                    return

        # Diagonal ascendente (↗)
        for f in range(3, fil):
            for c in range(col - 3):
                val = m[f][c]
                if val != self.VACIO and \
                   val == m[f-1][c+1] == m[f-2][c+2] == m[f-3][c+3]:
                    self.ganador = val
                    return

    def hayEmpate(self):
        """Tablero lleno sin ganador."""
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


# ─────────────────────────────────────────────
#  ESCENA  (coordinadora de todo)
# ─────────────────────────────────────────────

class EscenaConecta4:
    """Coordina cursor, juego, tablero y fichas.
       ADAPTADA de EscenaTresEnRaya.
       Mantiene el mismo esquema: Input → Update → Render."""

    def __init__(self):
        self.e = 70   # tamaño de cada celda

        # Entidades gráficas
        self.tablero = TableroConecta(30, 60, self.e)
        self.tablero.setColor((100, 100, 200))

        # Entidad lógica: cursor (solo columnas)
        self.cursor = CursorColumna(0)

        # Entidad lógica: juego
        self.juego = Conecta4()

        # Fuentes
        self.fuente       = pygame.font.SysFont("monospace", 16)
        self.fuenteGrande = pygame.font.SysFont("monospace", 26, bold=True)

    # ── INPUT ──────────────────────────────────
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
        elif evento.key == pygame.K_RETURN:
            self.juego.jugar(self.cursor.getColumna())

    # ── UPDATE ─────────────────────────────────
    def update(self):
        if self.juego.getGanador() != Conecta4.VACIO:
            return
        if self.juego.hayEmpate():
            return

        self.cursor.update()

    # ── RENDER ─────────────────────────────────
    def render(self, pantalla):
        # Tablero
        self.tablero.render(pantalla)

        # Cursor encima del tablero
        # Conversión mundo lógico → mundo gráfico:  columna → x
        xCursor = self.tablero.x + self.cursor.getColumna() * self.e
        yCursor = self.tablero.y - self.e           # una fila arriba del tablero

        colorCursor = (255, 80, 80) if self.juego.getTurno() == Conecta4.JUGADOR1 \
                      else (255, 220, 0)
        self.cursor.render(pantalla, xCursor, yCursor, self.e, colorCursor)

        # Fichas en el tablero
        matriz = self.juego.getMatriz()
        for fila in range(Conecta4.FILAS):
            for columna in range(Conecta4.COLUMNAS):
                # Mundo lógico (fila,columna) → mundo gráfico (px,py)
                px = self.tablero.x + columna * self.e
                py = self.tablero.y + fila    * self.e

                if matriz[fila][columna] == Conecta4.JUGADOR1:
                    ficha = FichaRoja(px, py, self.e)
                    ficha.setColor((220, 50, 50))
                    ficha.render(pantalla)

                elif matriz[fila][columna] == Conecta4.JUGADOR2:
                    ficha = FichaAmarilla(px, py, self.e)
                    ficha.setColor((230, 210, 0))
                    ficha.render(pantalla)

        # Panel de información
        self._renderPanel(pantalla)

        # Mensaje fin de juego
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
        pantalla.blit(textoT, (10, 10))

        ayuda = self.fuente.render("← → para mover  Enter para soltar", True, (150, 150, 150))
        pantalla.blit(ayuda, (10, 530))

    def _renderMensaje(self, pantalla, texto):
        superficie = self.fuenteGrande.render(texto, True, (255, 255, 0))
        rect = superficie.get_rect(center=(265, 510))
        pantalla.blit(superficie, rect)

    # ── REINICIAR ──────────────────────────────
    def reiniciar(self):
        self.juego.reiniciar()
        self.cursor = CursorColumna(0)


# ─────────────────────────────────────────────
#  GAME LOOP  (reutilizado de Tres en Raya)
# ─────────────────────────────────────────────

pygame.init()

ANCHO = 530
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

    pantalla.fill((10, 10, 30))     # fondo oscuro
    escena.render(pantalla)

    pygame.display.flip()
    clock.tick(60)
