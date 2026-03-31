import time 
import random 
from collections import deque 
  
  
def limpiar_pantalla(): 
    print("\n" * 40) 
  
  
def imprimir_tablero(estado, n): 
    separador = "+" + ("---+" * n) 
    for fila in range(n): 
        print(separador) 
        linea = "|" 
        for col in range(n): 
            if estado[fila] == col: 
                linea += " Q |" 
            else: 
                linea += "   |" 
        print(linea) 
    print(separador) 
    print() 
  
  
def heuristica(estado): 
    """ 
    Cuenta pares de reinas en conflicto (columna o diagonal). 
    h = 0 indica solucion valida. 
    """ 
    n = len(estado) 
    conflictos = 0 
    for i in range(n): 
        for j in range(i + 1, n): 
            if estado[i] == estado[j] or \
               abs(estado[i] - estado[j]) == abs(i - j): 
                conflictos += 1 
    return conflictos 
  
  
def swap(estado, i, j): 
    """Intercambia columnas i y j; retorna nuevo estado.""" 
    nuevo = estado[:] 
    nuevo[i], nuevo[j] = nuevo[j], nuevo[i] 
    return nuevo 
  
  
def tabu_search(n, max_iter=1000, tamano_tabu=None, verbose=True): 
    """ 
    Busqueda Tabu para el problema de las N-Reinas. 
  
    Parametros 
    ---------- 
    n           : int  -- numero de reinas 
    max_iter    : int  -- maximo de iteraciones 
    tamano_tabu : int  -- capacidad de la lista tabu (default: n) 
    verbose     : bool -- si True, imprime el tablero en cada paso 
  
    Retorna 
    ------- 
    mejor_estado : list[int] 
    metricas     : dict 
    """ 
    if tamano_tabu is None: 
        tamano_tabu = n 
  
    # Estado inicial: permutacion aleatoria 
    estado = list(range(n)) 
    random.shuffle(estado) 
  
    mejor = estado[:] 
    h_mejor = heuristica(mejor) 
  
    # Cola circular de tamano fijo 
    lista_tabu = deque(maxlen=tamano_tabu) 
  
    # Metricas 
    inicio = time.time() 
    total_movimientos = 0 
    iteracion = 0 
  
    print(f"\nBUSQUEDA TABU | N={n} | max_iter={max_iter} | lista_tabu={tamano_tabu}") 
    print(f"Estado inicial (aleatorio) | h = {h_mejor}") 
    imprimir_tablero(estado, n) 
  
    for iteracion in range(1, max_iter + 1): 
  
        # Condicion de parada: solucion perfecta 
        if h_mejor == 0: 
            break 
  
        # Generar vecindario: todos los swaps (i,j) con i < j 
        candidatos = [] 
        for i in range(n): 
            for j in range(i + 1, n): 
                nuevo = swap(estado, i, j) 
                h_nuevo = heuristica(nuevo) 
                movimiento = (i, j) 
  
                es_tabu = movimiento in lista_tabu 
                # Criterio de aspiracion: aceptar si mejora el mejor global 
                mejora_global = h_nuevo < h_mejor 
  
                if not es_tabu or mejora_global: 
                    candidatos.append((h_nuevo, i, j, nuevo)) 
  
        if not candidatos: 
            break 
  
        # Seleccionar el mejor candidato (menor h) 
        candidatos.sort(key=lambda x: x[0]) 
        h_vec, i_mov, j_mov, estado = candidatos[0] 
        total_movimientos += 1 
  
        # Actualizar mejor global 
        if h_vec < h_mejor: 
            mejor = estado[:] 
            h_mejor = h_vec 
  
        # Agregar movimiento a la lista tabu 
        lista_tabu.append((i_mov, j_mov)) 
  
        if verbose: 
            limpiar_pantalla() 
            print(f"TABU | Iter {iteracion}/{max_iter} | swap({i_mov},{j_mov})" 
                  f" | h={h_vec} | h_mejor={h_mejor}") 
            imprimir_tablero(estado, n) 
            time.sleep(0.05) 
  
    fin = time.time() 
    tiempo_total = round(fin - inicio, 4) 
  
    print(f"\n{chr(61)*50}") 
    if h_mejor == 0: 
        print(f"  SOLUCION ENCONTRADA en {iteracion} iteraciones") 
    else: 
        print(f"  No se encontro solucion perfecta (h_mejor={h_mejor})") 
    print(f"{chr(61)*50}") 
    imprimir_tablero(mejor, n) 
  
    metricas = { 
        "tiempo_seg"      : tiempo_total, 
        "movimientos"     : total_movimientos, 
        "iteraciones"     : iteracion, 
        "h_final"         : h_mejor, 
        "solucion_optima" : h_mejor == 0, 
    } 
  
    print(f"  Tiempo de ejecucion : {tiempo_total} segundos") 
    print(f"  Movimientos (swaps) : {total_movimientos}") 
    print(f"  Iteraciones         : {iteracion}") 
    print(f"  Conflictos finales  : {h_mejor}") 
    print(f"  Solucion optima?    : {'SI' if h_mejor == 0 else 'NO'}") 
  
    return mejor, metricas 
  
  
def prueba_rendimiento(n, repeticiones=10): 
    """ 
    Ejecuta la busqueda tabu varias veces y reporta estadisticas. 
    """ 
    print(f"\nPRUEBA DE RENDIMIENTO | N={n} | {repeticiones} ejecuciones") 
  
    exitos, tiempos, movimientos, iteraciones = [], [], [], [] 
  
    for i in range(1, repeticiones + 1): 
        _, m = tabu_search(n, max_iter=2000, verbose=False) 
        exitos.append(m["solucion_optima"]) 
        tiempos.append(m["tiempo_seg"]) 
        movimientos.append(m["movimientos"]) 
        iteraciones.append(m["iteraciones"]) 
        estado = "OK" if m["solucion_optima"] else "FALLO" 
        print(f"  Ejecucion {i:>2}: {estado} | {m['tiempo_seg']}s" 
              f" | {m['movimientos']} swaps | h={m['h_final']}") 
  
    n_exitos = sum(exitos) 
    print(f"\n  Tasa de exito       : {n_exitos}/{repeticiones}") 
    print(f"  Tiempo promedio     : {round(sum(tiempos)/repeticiones, 4)}s") 
    print(f"  Movimientos promedio: {round(sum(movimientos)/repeticiones, 1)}") 
    print(f"  Iteraciones promedio: {round(sum(iteraciones)/repeticiones, 1)}") 
  
  
def menu(): 
    print("\nPROBLEMA N-REINAS - BUSQUEDA TABU") 
    n = int(input("\n  Ingrese el numero de reinas (default 8): ") or 8) 
  
    print("\n  Opciones:") 
    print("  1. Ejecutar Busqueda Tabu (con visualizacion)") 
    print("  2. Prueba de rendimiento (multiples ejecuciones)") 
  
    opcion = input("\n  Opcion: ").strip() 
  
    if opcion == "1": 
        max_iter = int(input("  Maximo de iteraciones (default 1000): ") or 1000) 
        tam = input(f"  Tamano lista tabu (default {n}): ").strip() 
        tam = int(tam) if tam else n 
        tabu_search(n, max_iter=max_iter, tamano_tabu=tam, verbose=True) 
    elif opcion == "2": 
        reps = int(input("  Numero de repeticiones (default 10): ") or 10) 
        prueba_rendimiento(n, repeticiones=reps) 
    else: 
        print("  Opcion invalida.") 
  
  
if __name__ == "__main__": 
    menu() 