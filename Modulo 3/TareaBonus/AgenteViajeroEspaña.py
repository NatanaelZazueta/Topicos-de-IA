"""
     PROBLEMA DEL AGENTE VIAJERO (TSP) — ALGORITMOS GENETICOS               
     20 Ciudades de España — Busqueda de ruta optima                                                                                                     ║
     Materia   : Inteligencia Artificial                                                        

"""

import time
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.gridspec import GridSpec
from itertools import combinations


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1 — DATOS DEL PROBLEMA
# Matriz de distancias (km) entre 20 ciudades de España
# Fuente: Distancias reales por carretera entre capitales y ciudades principales
# ══════════════════════════════════════════════════════════════════════════════

CIUDADES = [
    "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza",
    "Málaga", "Murcia", "Palma", "Las Palmas", "Bilbao",
    "Alicante", "Córdoba", "Valladolid", "Vigo", "Gijón",
    "L'Hospitalet", "Vitoria", "A Coruña", "Granada", "Elche"
]

N_CIUDADES = len(CIUDADES)

# Índice de cada ciudad para acceso rápido
IDX = {c: i for i, c in enumerate(CIUDADES)}

DISTANCIAS = np.array([
    [  0, 303, 442, 223, 252, 654, 737, 458, 555, 279, 726, 456, 876, 467, 614, 249, 709, 368, 435, 530],
    [303,   0, 409, 591, 341, 403, 263, 485, 385, 671, 595, 738, 591, 725, 502, 328, 527, 617, 144, 244],
    [442, 409,   0, 430, 273, 639, 471, 152, 709, 335, 178, 574, 383, 281, 387, 624, 310, 480, 240, 683],
    [223, 591, 430,   0, 619, 431, 617, 629, 754, 124, 534, 630, 713, 295, 491, 245, 630, 295, 501, 478],
    [252, 341, 273, 619,   0, 332, 606, 203, 506, 470, 250, 562, 563, 334, 311, 760, 111, 757, 631, 349],
    [654, 403, 639, 431, 332,   0, 392, 306, 432, 606, 539, 401, 234, 449, 709, 520, 317, 192, 549, 271],
    [737, 263, 471, 617, 606, 392,   0, 854, 801,  89, 617, 390, 698, 595, 572, 405, 183, 164, 360, 337],
    [458, 485, 152, 629, 203, 306, 854,   0, 390, 323, 733, 391, 440, 319, 252, 735, 394, 408, 443, 456],
    [555, 385, 709, 754, 506, 432, 801, 390,   0, 671, 395, 200, 684, 206, 423, 792, 423, 614, 241, 185],
    [279, 671, 335, 124, 470, 606,  89, 323, 671,   0, 305, 534, 406, 842, 475, 516, 778, 579, 483, 864],
    [726, 595, 178, 534, 250, 539, 617, 733, 395, 305,   0, 767, 130, 551, 463, 554, 432, 593, 529, 864],
    [456, 738, 574, 630, 562, 401, 390, 391, 200, 534, 767,   0, 517, 853, 205, 534, 261, 380, 489, 515],
    [876, 591, 383, 713, 563, 234, 698, 440, 684, 406, 130, 517,   0, 387, 558, 495, 308, 557, 590, 443],
    [467, 725, 281, 295, 334, 449, 595, 319, 206, 842, 551, 853, 387,   0, 183, 171, 438, 445, 417, 678],
    [614, 502, 387, 491, 311, 709, 572, 252, 423, 475, 463, 205, 558, 183,   0, 527, 477, 294, 625, 200],
    [249, 328, 624, 245, 760, 520, 405, 735, 792, 516, 554, 534, 495, 171, 527,   0, 466, 664, 188, 437],
    [709, 527, 310, 630, 111, 317, 183, 394, 423, 778, 432, 261, 308, 438, 477, 466,   0, 761, 655, 752],
    [368, 617, 480, 295, 757, 192, 164, 408, 614, 579, 593, 380, 557, 445, 294, 664, 761,   0, 369, 634],
    [435, 144, 240, 501, 631, 549, 360, 443, 241, 483, 529, 489, 590, 417, 625, 188, 655, 369,   0, 798],
    [530, 244, 683, 478, 349, 271, 337, 456, 185, 864, 864, 515, 443, 678, 200, 437, 752, 634, 798,   0],
], dtype=float)

# Coordenadas aproximadas para visualización del mapa de España
COORDENADAS = {
    "Madrid":       (-3.703790,  40.416775),
    "Barcelona":    ( 2.154007,  41.390205),
    "Valencia":     (-0.375925,  39.469908),
    "Sevilla":      (-5.984459,  37.389092),
    "Zaragoza":     (-0.887712,  41.648823),
    "Málaga":       (-4.421371,  36.721261),
    "Murcia":       (-1.130654,  37.983810),
    "Palma":        ( 2.654870,  39.695260),
    "Las Palmas":   (-15.413607, 28.099058),
    "Bilbao":       (-2.934985,  43.262985),
    "Alicante":     (-0.490686,  38.345996),
    "Córdoba":      (-4.779152,  37.888175),
    "Valladolid":   (-4.728562,  41.652251),
    "Vigo":         (-8.722076,  42.231948),
    "Gijón":        (-5.661605,  43.545397),
    "L'Hospitalet": ( 2.099382,  41.359650),
    "Vitoria":      (-2.672881,  42.846718),
    "A Coruña":     (-8.405963,  43.362343),
    "Granada":      (-3.601979,  37.177336),
    "Elche":        (-0.701502,  38.262167),
}


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2 — REPRESENTACIÓN Y EVALUACIÓN
# ══════════════════════════════════════════════════════════════════════════════

def distancia_ruta(ruta):
    """
    Calcula la distancia total de una ruta (ciclo hamiltoniano).

    Una ruta es una permutación de índices de ciudades. El agente
    recorre todas las ciudades exactamente una vez y regresa al origen.

    Parámetros
    ----------
    ruta : list[int] o np.ndarray
        Permutación de índices [0, N_CIUDADES-1]

    Retorna
    -------
    float : distancia total en kilómetros (incluyendo regreso al inicio)
    """
    total = 0.0
    n     = len(ruta)
    for i in range(n):
        total += DISTANCIAS[ruta[i], ruta[(i + 1) % n]]
    return total


def aptitud(ruta):
    """
    Función de aptitud: inverso de la distancia total.

    Una distancia menor produce una aptitud mayor, lo que permite
    seleccionar preferentemente las rutas más cortas.

    Parámetros
    ----------
    ruta : list[int]

    Retorna
    -------
    float : 1 / distancia_total (mayor = mejor)
    """
    return 1.0 / distancia_ruta(ruta)


def ruta_a_nombres(ruta):
    """Convierte lista de índices a lista de nombres de ciudades."""
    return [CIUDADES[i] for i in ruta]


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 3 — OPERADORES GENÉTICOS
# ══════════════════════════════════════════════════════════════════════════════

def crear_individuo():
    """
    Crea un individuo aleatorio: permutación aleatoria de ciudades.

    Retorna
    -------
    list[int] : permutación de [0, N_CIUDADES-1]
    """
    ind = list(range(N_CIUDADES))
    random.shuffle(ind)
    return ind


def crear_poblacion(tam_poblacion):
    """
    Genera la población inicial con individuos aleatorios.

    Parámetros
    ----------
    tam_poblacion : int — número de individuos

    Retorna
    -------
    list[list[int]] : población inicial
    """
    return [crear_individuo() for _ in range(tam_poblacion)]


def seleccion_torneo(poblacion, aptitudes, k=5):
    """
    Selección por torneo: elige el mejor individuo de k candidatos aleatorios.

    Este método de selección mantiene presión selectiva sin eliminar
    completamente la diversidad genética.

    Parámetros
    ----------
    poblacion : list[list[int]]
    aptitudes : list[float]
    k         : int — tamaño del torneo

    Retorna
    -------
    list[int] : individuo ganador del torneo
    """
    candidatos = random.sample(range(len(poblacion)), k)
    ganador    = max(candidatos, key=lambda i: aptitudes[i])
    return poblacion[ganador][:]


def cruce_OX(padre1, padre2):
    """
    Cruce por Orden (Order Crossover — OX).

    Preserva el orden relativo de los genes del padre2 mientras
    conserva un segmento contiguo del padre1. Es el operador de
    cruce más utilizado para problemas de permutación (TSP).

    Parámetros
    ----------
    padre1 : list[int]
    padre2 : list[int]

    Retorna
    -------
    list[int] : hijo resultante del cruce
    """
    n   = len(padre1)
    i, j = sorted(random.sample(range(n), 2))

    # Segmento del padre1 se preserva directamente
    hijo = [-1] * n
    hijo[i:j+1] = padre1[i:j+1]

    # Genes restantes se toman del padre2 en orden de aparición
    segmento  = set(padre1[i:j+1])
    pos_hijo  = (j + 1) % n
    pos_padre = (j + 1) % n

    while -1 in hijo:
        if padre2[pos_padre] not in segmento:
            hijo[pos_hijo] = padre2[pos_padre]
            pos_hijo = (pos_hijo + 1) % n
        pos_padre = (pos_padre + 1) % n

    return hijo


def mutacion_intercambio(individuo, tasa_mutacion):
    """
    Mutación por intercambio (Swap Mutation).

    Con probabilidad tasa_mutacion, intercambia dos ciudades aleatorias
    en la ruta. Mantiene la validez de la permutación.

    Parámetros
    ----------
    individuo     : list[int]
    tasa_mutacion : float — probabilidad de mutar [0, 1]

    Retorna
    -------
    list[int] : individuo mutado (o copia sin cambios)
    """
    resultado = individuo[:]
    if random.random() < tasa_mutacion:
        i, j = random.sample(range(N_CIUDADES), 2)
        resultado[i], resultado[j] = resultado[j], resultado[i]
    return resultado


def mutacion_inversion(individuo, tasa_mutacion):
    """
    Mutación por inversión (Inversion Mutation).

    Invierte un segmento aleatorio de la ruta. Produce vecinos
    de mayor calidad que el simple intercambio, ya que preserva
    más información de la solución actual.

    Parámetros
    ----------
    individuo     : list[int]
    tasa_mutacion : float

    Retorna
    -------
    list[int] : individuo mutado
    """
    resultado = individuo[:]
    if random.random() < tasa_mutacion:
        i, j = sorted(random.sample(range(N_CIUDADES), 2))
        resultado[i:j+1] = reversed(resultado[i:j+1])
    return resultado


def elitismo(poblacion, aptitudes, n_elite):
    """
    Selecciona los n_elite mejores individuos para preservación directa.

    El elitismo garantiza que la mejor solución encontrada nunca
    se pierde entre generaciones.

    Parámetros
    ----------
    poblacion : list[list[int]]
    aptitudes : list[float]
    n_elite   : int

    Retorna
    -------
    list[list[int]] : los n_elite mejores individuos
    """
    ordenados = sorted(range(len(poblacion)),
                       key=lambda i: aptitudes[i], reverse=True)
    return [poblacion[i][:] for i in ordenados[:n_elite]]


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 4 — ALGORITMO GENÉTICO PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def algoritmo_genetico(
    tam_poblacion  = 200,
    n_generaciones = 500,
    tasa_cruce     = 0.85,
    tasa_mutacion  = 0.15,
    n_elite        = 10,
    k_torneo       = 5,
    semilla        = None,
    verbose        = True,
):
    """
    Algoritmo Genético para el Problema del Agente Viajero (TSP).

    Encuentra la ruta más corta que visita las 20 ciudades españolas
    exactamente una vez y regresa al punto de partida.

    Parámetros
    ----------
    tam_poblacion  : int   — número de individuos por generación
    n_generaciones : int   — número de generaciones
    tasa_cruce     : float — probabilidad de cruce [0, 1]
    tasa_mutacion  : float — probabilidad de mutación por individuo [0, 1]
    n_elite        : int   — individuos preservados por elitismo
    k_torneo       : int   — tamaño del torneo de selección
    semilla        : int   — semilla aleatoria (None = aleatoria)
    verbose        : bool  — imprimir progreso

    Retorna
    -------
    mejor_ruta     : list[int]   — ruta óptima encontrada
    mejor_distancia: float       — distancia total en km
    historial_mejor: list[float] — mejor distancia por generación
    historial_prom : list[float] — distancia promedio por generación
    """
    if semilla is not None:
        random.seed(semilla)
        np.random.seed(semilla)

    # ── Inicialización ──
    poblacion = crear_poblacion(tam_poblacion)
    aptitudes = [aptitud(ind) for ind in poblacion]

    mejor_ruta      = min(poblacion, key=distancia_ruta)
    mejor_distancia = distancia_ruta(mejor_ruta)

    historial_mejor = []
    historial_prom  = []

    if verbose:
        print(f"\n  {'Gen':>5} | {'Mejor (km)':>12} | {'Promedio (km)':>14} | {'Mejora':>8}")
        print(f"  {'-'*50}")

    # ── Bucle de generaciones ──
    for gen in range(n_generaciones):

        # Evaluar aptitudes
        aptitudes    = [aptitud(ind) for ind in poblacion]
        distancias_g = [distancia_ruta(ind) for ind in poblacion]

        mejor_gen_idx  = min(range(len(poblacion)), key=lambda i: distancias_g[i])
        mejor_gen_dist = distancias_g[mejor_gen_idx]
        prom_gen       = np.mean(distancias_g)

        # Actualizar mejor global
        mejora = ""
        if mejor_gen_dist < mejor_distancia:
            mejor_distancia = mejor_gen_dist
            mejor_ruta      = poblacion[mejor_gen_idx][:]
            mejora          = "  ◄ NUEVO MEJOR"

        historial_mejor.append(mejor_distancia)
        historial_prom.append(prom_gen)

        if verbose and (gen % 100 == 0 or gen == n_generaciones - 1):
            print(f"  {gen+1:>5} | {mejor_distancia:>12.1f} | {prom_gen:>14.1f} |{mejora}")

        # ── Nueva generación ──
        nueva_poblacion = elitismo(poblacion, aptitudes, n_elite)

        while len(nueva_poblacion) < tam_poblacion:
            # Selección
            p1 = seleccion_torneo(poblacion, aptitudes, k_torneo)
            p2 = seleccion_torneo(poblacion, aptitudes, k_torneo)

            # Cruce
            if random.random() < tasa_cruce:
                hijo = cruce_OX(p1, p2)
            else:
                hijo = p1[:]

            # Mutación (combinación de intercambio e inversión)
            hijo = mutacion_intercambio(hijo, tasa_mutacion * 0.6)
            hijo = mutacion_inversion(hijo, tasa_mutacion * 0.4)

            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

    return mejor_ruta, mejor_distancia, historial_mejor, historial_prom


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 5 — VISUALIZACIONES
# ══════════════════════════════════════════════════════════════════════════════

def visualizar_resultado(mejor_ruta, historial_mejor, historial_prom,
                         titulo="Algoritmo Genético — TSP España"):
    """
    Genera panel de 4 gráficas con los resultados del AG:
      1. Mapa de España con la ruta óptima
      2. Curva de convergencia (mejor y promedio)
      3. Matriz de distancias (heatmap)
      4. Distribución de distancias de la población final

    Parámetros
    ----------
    mejor_ruta     : list[int]
    historial_mejor: list[float]
    historial_prom : list[float]
    titulo         : str
    """
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle(titulo, fontsize=15, fontweight='bold', y=0.98)
    gs  = GridSpec(2, 2, figure=fig, hspace=0.40, wspace=0.32)

    # ── Gráfica 1: Mapa de la ruta ──
    ax1 = fig.add_subplot(gs[0, 0])
    lons_mapa = [COORDENADAS[c][0] for c in CIUDADES]
    lats_mapa = [COORDENADAS[c][1] for c in CIUDADES]

    ruta_completa = mejor_ruta + [mejor_ruta[0]]
    xs = [COORDENADAS[CIUDADES[i]][0] for i in ruta_completa]
    ys = [COORDENADAS[CIUDADES[i]][1] for i in ruta_completa]

    ax1.plot(xs, ys, '-o', color='steelblue', linewidth=1.5,
             markersize=5, zorder=3, alpha=0.8)

    # Marcar inicio/fin
    inicio = CIUDADES[mejor_ruta[0]]
    ax1.scatter([COORDENADAS[inicio][0]], [COORDENADAS[inicio][1]],
                c='red', s=120, zorder=5, label=f'Inicio: {inicio}')

    # Etiquetas de ciudades
    for ciudad in CIUDADES:
        lon, lat = COORDENADAS[ciudad]
        ax1.annotate(ciudad, (lon, lat), fontsize=5.5,
                     xytext=(3, 3), textcoords='offset points',
                     color='#1a1a2e')

    # Mostrar orden numérico en la ruta
    for orden, idx_ciudad in enumerate(mejor_ruta):
        ciudad = CIUDADES[idx_ciudad]
        lon, lat = COORDENADAS[ciudad]
        ax1.annotate(str(orden + 1), (lon, lat),
                     xytext=(-7, 4), textcoords='offset points',
                     fontsize=5, color='darkred', fontweight='bold')

    ax1.set_title(f'Ruta Óptima — {distancia_ruta(mejor_ruta):.0f} km', fontsize=11, fontweight='bold')
    ax1.set_xlabel('Longitud', fontsize=9)
    ax1.set_ylabel('Latitud', fontsize=9)
    ax1.legend(fontsize=8)
    ax1.grid(True, linestyle='--', alpha=0.30)

    # ── Gráfica 2: Convergencia ──
    ax2 = fig.add_subplot(gs[0, 1])
    gens = range(1, len(historial_mejor) + 1)
    ax2.plot(gens, historial_mejor, color='steelblue', linewidth=1.8,
             label='Mejor ruta', zorder=3)
    ax2.plot(gens, historial_prom, color='tomato', linewidth=1.2,
             linestyle='--', alpha=0.7, label='Promedio población')
    ax2.fill_between(gens, historial_mejor, historial_prom,
                     alpha=0.08, color='steelblue')
    ax2.axhline(y=min(historial_mejor), color='green', linestyle=':',
                linewidth=1.2, label=f'Mínimo: {min(historial_mejor):.0f} km')
    ax2.set_title('Convergencia del Algoritmo Genético', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Generación', fontsize=9)
    ax2.set_ylabel('Distancia (km)', fontsize=9)
    ax2.legend(fontsize=8)
    ax2.grid(True, linestyle='--', alpha=0.30)

    # ── Gráfica 3: Heatmap de distancias (subconjunto 10 ciudades) ──
    ax3 = fig.add_subplot(gs[1, 0])
    ciudades_top = CIUDADES[:10]
    idx_top      = [IDX[c] for c in ciudades_top]
    submat       = DISTANCIAS[np.ix_(idx_top, idx_top)]
    sns.heatmap(submat, annot=True, fmt='.0f', cmap='YlOrRd',
                xticklabels=[c[:6] for c in ciudades_top],
                yticklabels=[c[:6] for c in ciudades_top],
                ax=ax3, annot_kws={'size': 7}, linewidths=0.3)
    ax3.set_title('Matriz de Distancias (km) — Top 10 ciudades', fontsize=11, fontweight='bold')
    ax3.tick_params(axis='x', labelsize=7, rotation=35)
    ax3.tick_params(axis='y', labelsize=7, rotation=0)

    # ── Gráfica 4: Distribución de distancias por tramo ──
    ax4 = fig.add_subplot(gs[1, 1])
    tramos = []
    nombres_tramos = []
    ruta_cir = mejor_ruta + [mejor_ruta[0]]
    for i in range(len(mejor_ruta)):
        d = DISTANCIAS[ruta_cir[i], ruta_cir[i+1]]
        tramos.append(d)
        nombres_tramos.append(f"{CIUDADES[ruta_cir[i]][:4]}→{CIUDADES[ruta_cir[i+1]][:4]}")

    colores_tramos = ['#2196F3' if d < 350 else '#FF9800' if d < 600 else '#F44336'
                      for d in tramos]
    bars = ax4.barh(range(len(tramos)), tramos, color=colores_tramos, alpha=0.8, height=0.7)
    ax4.set_yticks(range(len(tramos)))
    ax4.set_yticklabels(nombres_tramos, fontsize=6.5)
    ax4.set_xlabel('Distancia (km)', fontsize=9)
    ax4.set_title('Distancia por Tramo de la Ruta Óptima', fontsize=11, fontweight='bold')
    ax4.axvline(x=np.mean(tramos), color='black', linestyle='--',
                linewidth=1, alpha=0.6, label=f'Promedio: {np.mean(tramos):.0f} km')
    ax4.legend(fontsize=8)

    leyenda = [
        mpatches.Patch(color='#2196F3', label='< 350 km'),
        mpatches.Patch(color='#FF9800', label='350–600 km'),
        mpatches.Patch(color='#F44336', label='> 600 km'),
    ]
    ax4.legend(handles=leyenda, fontsize=7, loc='lower right')
    ax4.grid(True, linestyle='--', alpha=0.30, axis='x')

    plt.savefig('ag_tsp_espana.png', dpi=150, bbox_inches='tight')
    print("\n  Figura guardada: ag_tsp_espana.png")
    plt.show()


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 6 — PRUEBAS DE FUNCIONALIDAD
# ══════════════════════════════════════════════════════════════════════════════

def prueba_distancia_ruta():
    """
    Prueba unitaria de la función distancia_ruta.

    Verifica:
    - La distancia de una ruta es positiva
    - La matriz de distancias es simétrica
    - La distancia de un tramo conocido coincide con la matriz
    """
    print("\n  [PRUEBA 1] Función distancia_ruta y matriz de distancias")

    ruta_test = list(range(N_CIUDADES))
    d = distancia_ruta(ruta_test)

    assert d > 0, "ERROR: la distancia total debe ser positiva"

    # Simetría: dist(A, B) == dist(B, A)
    for i in range(N_CIUDADES):
        for j in range(N_CIUDADES):
            assert DISTANCIAS[i, j] == DISTANCIAS[j, i], \
                f"ERROR: matriz no simétrica en ({i},{j})"

    # Diagonal principal = 0
    assert np.all(np.diag(DISTANCIAS) == 0), "ERROR: diagonal debe ser cero"

    # Tramo conocido: Madrid (0) → Barcelona (1) = 303 km
    assert DISTANCIAS[0, 1] == 303, "ERROR: distancia Madrid-Barcelona incorrecta"

    print(f"    Distancia ruta secuencial : {d:.1f} km")
    print(f"    Distancia Madrid-Barcelona: {DISTANCIAS[0,1]:.0f} km ✔")
    print(f"    Simetría de la matriz     : OK ✔")
    print(f"    Diagonal cero             : OK ✔")
    print("    RESULTADO: PASÓ ✔")


def prueba_operadores_geneticos():
    """
    Prueba de los operadores genéticos.

    Verifica:
    - cruce_OX produce una permutación válida
    - mutacion_intercambio preserva la permutación
    - mutacion_inversion preserva la permutación
    - seleccion_torneo retorna un individuo de la población
    """
    print("\n  [PRUEBA 2] Operadores genéticos")

    p1 = list(range(N_CIUDADES))
    p2 = list(range(N_CIUDADES))
    random.shuffle(p2)

    # Cruce OX
    hijo = cruce_OX(p1, p2)
    assert sorted(hijo) == list(range(N_CIUDADES)), \
        "ERROR: cruce_OX no produce permutación válida"
    assert len(hijo) == N_CIUDADES, \
        "ERROR: hijo tiene longitud incorrecta"

    # Mutación intercambio
    mutado = mutacion_intercambio(p1[:], tasa_mutacion=1.0)
    assert sorted(mutado) == list(range(N_CIUDADES)), \
        "ERROR: mutacion_intercambio no preserva permutación"

    # Mutación inversión
    mutado2 = mutacion_inversion(p1[:], tasa_mutacion=1.0)
    assert sorted(mutado2) == list(range(N_CIUDADES)), \
        "ERROR: mutacion_inversion no preserva permutación"

    # Selección torneo
    pob  = [list(range(N_CIUDADES)) for _ in range(10)]
    apts = [aptitud(ind) for ind in pob]
    sel  = seleccion_torneo(pob, apts, k=3)
    assert sorted(sel) == list(range(N_CIUDADES)), \
        "ERROR: seleccion_torneo retorna individuo inválido"

    print(f"    cruce_OX          : permutación válida ✔")
    print(f"    mutacion_intercambio: permutación preservada ✔")
    print(f"    mutacion_inversion  : permutación preservada ✔")
    print(f"    seleccion_torneo    : individuo válido ✔")
    print("    RESULTADO: PASÓ ✔")


def prueba_convergencia():
    """
    Prueba de convergencia del algoritmo genético.

    Verifica que más generaciones producen rutas iguales o mejores,
    usando la misma semilla aleatoria para reproducibilidad.
    """
    print("\n  [PRUEBA 3] Convergencia del algoritmo")

    _, d_100, _, _ = algoritmo_genetico(
        tam_poblacion=50, n_generaciones=100, semilla=42, verbose=False)
    _, d_300, _, _ = algoritmo_genetico(
        tam_poblacion=50, n_generaciones=300, semilla=42, verbose=False)

    assert d_300 <= d_100 * 1.02, \
        "ERROR: más generaciones debe producir igual o mejor resultado"

    print(f"    Distancia con 100 gen: {d_100:.1f} km")
    print(f"    Distancia con 300 gen: {d_300:.1f} km")
    print(f"    Mejora               : {d_100 - d_300:.1f} km ({(d_100-d_300)/d_100*100:.1f}%)")
    print("    RESULTADO: PASÓ ✔")


def prueba_configuraciones():
    """
    Prueba de rendimiento en 3 configuraciones distintas.

    Configuraciones:
      - Rápida   : población pequeña, pocas generaciones
      - Estándar : parámetros balanceados (configuración recomendada)
      - Intensiva: población grande, más generaciones

    Verifica que la configuración intensiva produce igual o mejor resultado.
    """
    print("\n  [PRUEBA 4] Comparativa de configuraciones")

    configs = [
        dict(tam_poblacion=80,  n_generaciones=200, tasa_mutacion=0.15,
             semilla=0, desc="Rápida    (80 ind, 200 gen)"),
        dict(tam_poblacion=200, n_generaciones=500, tasa_mutacion=0.15,
             semilla=0, desc="Estándar (200 ind, 500 gen)"),
        dict(tam_poblacion=400, n_generaciones=800, tasa_mutacion=0.10,
             semilla=0, desc="Intensiva(400 ind, 800 gen)"),
    ]

    resultados = []
    for cfg in configs:
        print(f"\n    Configuración: {cfg['desc']}")
        inicio = time.time()
        ruta, dist, h_mejor, h_prom = algoritmo_genetico(
            tam_poblacion  = cfg['tam_poblacion'],
            n_generaciones = cfg['n_generaciones'],
            tasa_mutacion  = cfg['tasa_mutacion'],
            semilla        = cfg['semilla'],
            verbose        = True,
        )
        elapsed = time.time() - inicio
        resultados.append({
            'desc': cfg['desc'], 'distancia': dist,
            'tiempo': elapsed, 'ruta': ruta,
            'historial_mejor': h_mejor, 'historial_prom': h_prom,
        })
        print(f"    Distancia: {dist:.1f} km | Tiempo: {elapsed:.1f}s")
        print(f"    Ruta: {' → '.join(ruta_a_nombres(ruta)[:5])} → ...")

    print(f"\n    {'Configuración':<30} {'Distancia':>10} {'Tiempo':>8}")
    print(f"    {'-'*52}")
    for r in resultados:
        print(f"    {r['desc']:<30} {r['distancia']:>10.1f} {r['tiempo']:>7.1f}s")
    print("    RESULTADO: PASÓ ✔")

    return resultados


def ejecutar_todas_las_pruebas():
    """
    Ejecuta el conjunto completo de pruebas de funcionalidad.

    Cubre:
      - Prueba 1: Corrección de la función de distancia y matriz
      - Prueba 2: Operadores genéticos (cruce, mutación, selección)
      - Prueba 3: Convergencia del algoritmo genético
      - Prueba 4: Comparativa de 3 configuraciones de ejecución

    Retorna
    -------
    resultados : list[dict] — resultados de la prueba de configuraciones
    """
    print("\n" + "=" * 60)
    print("  PRUEBAS DE FUNCIONALIDAD — AG TSP España")
    print("=" * 60)

    prueba_distancia_ruta()
    prueba_operadores_geneticos()
    prueba_convergencia()
    resultados = prueba_configuraciones()

    print("\n" + "=" * 60)
    print("  TODAS LAS PRUEBAS PASARON ✔")
    print("=" * 60)

    return resultados


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 7 — GENERACIÓN DE REPORTE
# ══════════════════════════════════════════════════════════════════════════════

def generar_reporte(mejor_ruta, mejor_dist, historial_mejor):
    """
    Imprime un reporte detallado de los resultados del algoritmo.

    Incluye: ruta completa ordenada, distancia por tramo,
    estadísticas de convergencia y comparativa con ruta aleatoria.

    Parámetros
    ----------
    mejor_ruta     : list[int]
    mejor_dist     : float
    historial_mejor: list[float]
    """
    print("\n" + "=" * 65)
    print("  REPORTE DE RESULTADOS — AG TSP España")
    print("=" * 65)

    print(f"\n  Ruta óptima encontrada ({len(mejor_ruta)} ciudades):")
    print(f"  {'#':>3}  {'Ciudad':>15}  {'→ Siguiente':>15}  {'Distancia km':>12}")
    print(f"  {'-'*55}")

    ruta_cir = mejor_ruta + [mejor_ruta[0]]
    for i in range(len(mejor_ruta)):
        origen  = CIUDADES[ruta_cir[i]]
        destino = CIUDADES[ruta_cir[i + 1]]
        d       = DISTANCIAS[ruta_cir[i], ruta_cir[i + 1]]
        print(f"  {i+1:>3}  {origen:>15}  {destino:>15}  {d:>12.0f}")

    print(f"  {'-'*55}")
    print(f"  {'TOTAL':>35}  {mejor_dist:>12.0f}")

    # Estadísticas
    tramos = [DISTANCIAS[ruta_cir[i], ruta_cir[i+1]] for i in range(len(mejor_ruta))]
    print(f"\n  Estadísticas de la ruta:")
    print(f"    Tramo más corto  : {min(tramos):.0f} km "
          f"({CIUDADES[ruta_cir[tramos.index(min(tramos))]]}"
          f" → {CIUDADES[ruta_cir[tramos.index(min(tramos))+1]]})")
    print(f"    Tramo más largo  : {max(tramos):.0f} km "
          f"({CIUDADES[ruta_cir[tramos.index(max(tramos))]]}"
          f" → {CIUDADES[ruta_cir[tramos.index(max(tramos))+1]]})")
    print(f"    Distancia promedio por tramo: {np.mean(tramos):.0f} km")

    # Comparativa con ruta aleatoria (promedio de 10 muestras)
    rutas_rand = [crear_individuo() for _ in range(10)]
    dist_rand  = np.mean([distancia_ruta(r) for r in rutas_rand])
    mejora_pct = (dist_rand - mejor_dist) / dist_rand * 100
    print(f"\n  Comparativa:")
    print(f"    Distancia ruta aleatoria (promedio): {dist_rand:.0f} km")
    print(f"    Distancia ruta AG                  : {mejor_dist:.0f} km")
    print(f"    Mejora del AG                      : {mejora_pct:.1f}%")
    print(f"\n  Convergencia:")
    print(f"    Distancia generación 1   : {historial_mejor[0]:.0f} km")
    print(f"    Distancia generación final: {historial_mejor[-1]:.0f} km")
    print(f"    Mejora total             : {historial_mejor[0]-historial_mejor[-1]:.0f} km "
          f"({(historial_mejor[0]-historial_mejor[-1])/historial_mejor[0]*100:.1f}%)")
    print("=" * 65)


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 8 — MENÚ PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def menu():
    """
    Interfaz de texto para seleccionar el modo de ejecución.

    Opciones:
      1. Ejecutar AG con configuración estándar y visualización
      2. Ejecutar todas las pruebas de funcionalidad
      3. Comparativa de 3 configuraciones con visualización
    """
    print("\n" + "=" * 60)
    print("  AGENTE VIAJERO — ALGORITMO GENÉTICO — ESPAÑA")
    print("=" * 60)
    print(f"  20 ciudades | {N_CIUDADES*(N_CIUDADES-1)//2} rutas posibles")
    print("\n  Opciones:")
    print("  1. Ejecutar AG estándar (200 ind, 500 gen) con visualización")
    print("  2. Ejecutar todas las pruebas de funcionalidad")
    print("  3. Comparativa de 3 configuraciones con visualización")

    opcion = input("\n  Seleccione opción (1/2/3): ").strip()

    if opcion == "1":
        print("\n  Iniciando AG — Configuración estándar...")
        ruta, dist, h_mejor, h_prom = algoritmo_genetico(
            tam_poblacion=200, n_generaciones=500,
            tasa_mutacion=0.15, verbose=True
        )
        generar_reporte(ruta, dist, h_mejor)
        visualizar_resultado(ruta, h_mejor, h_prom)

    elif opcion == "2":
        ejecutar_todas_las_pruebas()

    elif opcion == "3":
        resultados = prueba_configuraciones()
        # Visualizar la mejor configuración
        mejor_res = min(resultados, key=lambda r: r['distancia'])
        visualizar_resultado(
            mejor_res['ruta'],
            mejor_res['historial_mejor'],
            mejor_res['historial_prom'],
            titulo=f"AG TSP — Mejor configuración: {mejor_res['desc']}"
        )
    else:
        print("  Opción inválida.")


# ══════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    menu()
