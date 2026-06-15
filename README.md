# Juegos Básicos

Este repositorio contiene dos juegos programados con `pygame`: Conecta 4 y Tres en Raya Pro+. Ambos están pensados como ejemplos didácticos y reutilizan una misma arquitectura (entidades gráficas, entidad lógica, escena con Input→Update→Render).

**Juegos incluidos**
- **Conecta 4**: [JUEGOSBASICOS/conecta4.py](JUEGOSBASICOS/conecta4.py) — Implementación de Connect Four (7 columnas × 6 filas). Interfaz gráfica con fichas rojas y amarillas.
- **Tres en Raya Pro+**: [JUEGOSBASICOS/tresEnRayaPro.py](JUEGOSBASICOS/tresEnRayaPro.py) — Versión ampliada del clásico Tres en Raya (3×3) con indicadores animados y estadísticas (victorias/partidas).

**Requisitos**
- Python 3.8+ (se probó con Python 3.12 en este entorno)
- `pygame` (versión moderna; instalar con `pip install pygame`)

**Instalación rápida**
1. (Opcional) Crear y activar un entorno virtual:

```bash
python -m venv env
source env/bin/activate
```

2. Instalar `pygame`:

```bash
pip install pygame
```

3. Ejecutar cualquiera de los juegos:

```bash
# Ejecutar Conecta 4
python JUEGOSBASICOS/conecta4.py

# Ejecutar Tres en Raya Pro+
python JUEGOSBASICOS/tresEnRayaPro.py
```

**Controles y jugabilidad**

- Conecta 4 ([JUEGOSBASICOS/conecta4.py](JUEGOSBASICOS/conecta4.py))
  - Objetivo: conseguir 4 fichas en línea (horizontal, vertical o diagonal).
  - Controles: `←` / `→` para mover el cursor de columna, `Enter` para soltar la ficha.
  - Reiniciar partida: `R` (solo disponible después de finalizar la partida o empate).
  - Ventana: 530×560 px.

- Tres en Raya Pro+ ([JUEGOSBASICOS/tresEnRayaPro.py](JUEGOSBASICOS/tresEnRayaPro.py))
  - Objetivo: conseguir 3 fichas en línea (filas, columnas o diagonales).
  - Controles: Flechas para mover el cursor, `Space` para colocar la ficha.
    - Nota: el panel de ayuda en pantalla muestra "Flechas+Enter", pero el código usa `Space` para confirmar la jugada.
  - Reiniciar partida: `R` (después de victoria o empate).
  - Estadísticas: el juego lleva registro de `Victorias X`, `Victorias O` y `Partidas`.
  - Ventana: 600×420 px.

**Estructura del código**

- `Base`, `Tablero`, `X`/`O` / `FichaRoja` / `FichaAmarilla`: entidades gráficas que implementan `render()`.
- `TresEnRaya` / `Conecta4`: entidades lógicas con la matriz del juego, control de turnos, verificación de ganador y reinicio.
- `Cursor` / `CursorColumna`: entidades lógicas para navegar las celdas o columnas.
- `EscenaTresEnRaya` / `EscenaConecta4`: coordinan entrada, actualización y renderizado; contienen el bucle principal de cada juego.


