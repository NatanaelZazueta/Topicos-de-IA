# PROYECTO FINAL
# OPTIMIZACION DE COLOCACION DE SENSORES DE HUMEDAD UTILIZANDO PSO

# Importacion de librerias necesarias
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pyswarms as ps


# CLASE PRINCIPAL DEL CAMPO AGRICOLA

class CampoAgricola:

    """
    Esta clase representa un campo agricola donde se analizaran
    diferentes variables para la colocacion de sensores.
    """

    CULTIVOS = {
        0: {"nombre": "Sin cultivo", "req_humedad": 0.3, "color": "#d9c8a0"},
        1: {"nombre": "Maiz", "req_humedad": 0.7, "color": "#e8b84b"},
        2: {"nombre": "Tomate rojo", "req_humedad": 0.85, "color": "#c0392b"},
        3: {"nombre": "Chile verde", "req_humedad": 0.6, "color": "#27ae60"}
    }

    def __init__(self, tamanio=100, semilla=20):

        print("Inicializando campo agricola...")

        np.random.seed(semilla)

        self.tamanio = tamanio

        #TOPOGRAFIA


        arreglo_x = np.linspace(0, 4*np.pi, tamanio)
        arreglo_y = np.linspace(0, 4*np.pi, tamanio)

        xx, yy = np.meshgrid(arreglo_x, arreglo_y)

        parte_1 = np.sin(xx * 0.5) * 3
        parte_2 = np.cos(yy * 0.4) * 2
        parte_3 = np.sin((xx + yy) * 0.3) * 1.5

        ondas = parte_1 + parte_2 + parte_3

        ruido = np.random.normal(0, 1.5, (tamanio, tamanio))

        self.topografia = np.clip(25 + ondas + ruido, 10, 50)


        #HUMEDAD


        elevacion_normalizada = (self.topografia - 10) / 40

        humedad_base = np.random.uniform(0.2, 0.9, (tamanio, tamanio))

        ruido_humedad = np.random.normal(0, 0.05, (tamanio, tamanio))

        self.humedad = np.clip(
            humedad_base - 0.25 * elevacion_normalizada + ruido_humedad,
            0.05,
            1.0
        )

        # CALIDAD DEL SUELO

        self.suelo = np.random.uniform(0.5, 1.0, (tamanio, tamanio))

        # DISTRIBUCION DE CULTIVO

        self.cultivos = np.zeros((tamanio, tamanio), dtype=int)

        self.generar_cultivos()

        print("Campo generado correctamente.")


    def generar_cultivos(self):

        """
        Metodo encargado de asignar regiones del terreno
        a distintos cultivos.
        """

        t = self.tamanio

        # maiz
        self.cultivos[:t//2, :t//2] = 1
        self.cultivos[t//4:3*t//4, t//4:3*t//4] = 1

        # tomate
        self.cultivos[3*t//4:, :] = 2

        # chile
        self.cultivos[:, 3*t//4:] = 3

        # zonas vacias
        self.cultivos[:t//8, :] = 0
        self.cultivos[:, :t//8] = 0


    def obtener_valores(self, x, y):

        """
        Retorna valores del terreno para una coordenada dada.
        """

        posicion_x = int(np.clip(x, 0, self.tamanio - 1))
        posicion_y = int(np.clip(y, 0, self.tamanio - 1))

        humedad = self.humedad[posicion_x][posicion_y]
        suelo = self.suelo[posicion_x][posicion_y]
        elevacion = self.topografia[posicion_x][posicion_y]
        cultivo = self.cultivos[posicion_x][posicion_y]

        return humedad, suelo, elevacion, cultivo


    def obtener_requerimiento_hidrico(self, tipo):

        """
        Metodo para devolver el requerimiento hidrico
        segun el tipo de cultivo.
        """

        return self.CULTIVOS[tipo]["req_humedad"]

#FITNESS
def evaluar_configuracion(posiciones, campo, numero_sensores):

    """
    Funcion objetivo para evaluar cada particula.
    """

    lista_fitness = []

    for particula in posiciones:

        matriz_coordenadas = particula.reshape(numero_sensores, 2)

        # PENALIZACION POR DISTANCIA
        lista_distancias = []

        for i in range(numero_sensores):

            for j in range(i + 1, numero_sensores):

                distancia = np.linalg.norm(
                    matriz_coordenadas[i] - matriz_coordenadas[j]
                )

                lista_distancias.append(distancia)

        arreglo_distancias = np.array(lista_distancias)

        penalizacion = np.sum(np.exp(-arreglo_distancias / 10))

        suma_humedad = 0
        suma_suelo = 0
        suma_cultivo = 0
        suma_topografia = 0

        lista_humedades = []

        for punto in matriz_coordenadas:

            x = punto[0]
            y = punto[1]

            humedad, suelo, elevacion, cultivo = campo.obtener_valores(x, y)

            req = campo.obtener_requerimiento_hidrico(cultivo)

            lista_humedades.append(humedad)

            suma_humedad = suma_humedad + humedad
            suma_suelo = suma_suelo + suelo

            adecuacion = 1 - abs(humedad - req)

            suma_cultivo = suma_cultivo + adecuacion

            elevacion_norm = (elevacion - 10) / 40

            valor_topografico = 1 - elevacion_norm

            suma_topografia = suma_topografia + valor_topografico

        varianza_humedad = np.var(lista_humedades)

        # formula final
        resultado = (
            suma_humedad
            + (varianza_humedad * 3)
            + (suma_suelo * 0.8)
            + (suma_cultivo * 1.5)
            + suma_topografia
            - (0.4 * penalizacion)
        )

        fitness_final = -resultado

        lista_fitness.append(fitness_final)

    return np.array(lista_fitness)


# Ejecuciones

def ejecutar_pruebas(campo, numero_sensores, corridas=5, iteraciones=150):

    print("\nIniciando pruebas multiples...\n")

    lista_semillas = [42, 7, 123, 99, 2024]

    resultados = []

    dimensiones = numero_sensores * 2

    limite_inferior = np.zeros(dimensiones)
    limite_superior = np.ones(dimensiones) * campo.tamanio

    opciones = {
        "c1": 2.0,
        "c2": 2.0,
        "w": 0.7
    }

    for i in range(corridas):

        np.random.seed(lista_semillas[i])

        optimizador = ps.single.GlobalBestPSO(
            n_particles=50,
            dimensions=dimensiones,
            options=opciones,
            bounds=(limite_inferior, limite_superior)
        )

        def funcion_auxiliar(pos):
            return evaluar_configuracion(
                pos,
                campo,
                numero_sensores
            )

        mejor_costo, mejor_posicion = optimizador.optimize(
            funcion_auxiliar,
            iters=iteraciones,
            verbose=False
        )

        historial = optimizador.cost_history

        resultados.append(
            (mejor_costo, mejor_posicion, historial)
        )

        print("Corrida", i+1, "terminada.")

    return resultados


# GRAFICAS

def mostrar_graficas(campo, coordenadas, resultados):

    print("Generando graficas del sistema...")

    # GRAFICA 1

    figura1, arreglo_graficas = plt.subplots(1, 4, figsize=(22, 5))

    # GRAFICA DE CULTIVOS

    imagen_1 = arreglo_graficas[0].imshow(
        campo.cultivos,
        cmap="tab10",
        origin="lower",
        vmin=0,
        vmax=9,
        alpha=0.85
    )

    arreglo_graficas[0].scatter(
        coordenadas[:, 0],
        coordenadas[:, 1],
        color="white",
        edgecolors="black",
        marker="^",
        s=100
    )

    arreglo_graficas[0].set_title("Distribucion de Cultivos")

    lista_leyenda = []

    for valor in campo.CULTIVOS.values():

        elemento = mpatches.Patch(
            color=valor["color"],
            label=valor["nombre"]
        )

        lista_leyenda.append(elemento)

    arreglo_graficas[0].legend(
        handles=lista_leyenda,
        fontsize=7,
        loc="lower right"
    )

    # GRAFICA DE HUMEDAD

    imagen_2 = arreglo_graficas[1].imshow(
        campo.humedad,
        cmap="Blues",
        origin="lower"
    )

    arreglo_graficas[1].scatter(
        coordenadas[:, 0],
        coordenadas[:, 1],
        color="red",
        marker="x",
        s=80
    )

    arreglo_graficas[1].set_title("Distribucion de Humedad")

    plt.colorbar(
        imagen_2,
        ax=arreglo_graficas[1],
        fraction=0.046,
        pad=0.04
    )

    # GRAFICA DE SUELO

    imagen_3 = arreglo_graficas[2].imshow(
        campo.suelo,
        cmap="YlOrBr",
        origin="lower"
    )

    arreglo_graficas[2].scatter(
        coordenadas[:, 0],
        coordenadas[:, 1],
        color="blue",
        marker="x",
        s=80
    )

    arreglo_graficas[2].set_title("Calidad del Suelo")

    plt.colorbar(
        imagen_3,
        ax=arreglo_graficas[2],
        fraction=0.046,
        pad=0.04
    )

    # GRAFICA DE TOPOGRAFIA

    imagen_4 = arreglo_graficas[3].imshow(
        campo.topografia,
        cmap="terrain",
        origin="lower"
    )

    arreglo_graficas[3].scatter(
        coordenadas[:, 0],
        coordenadas[:, 1],
        color="red",
        marker="x",
        s=80
    )

    arreglo_graficas[3].set_title("Topografia")

    plt.colorbar(
        imagen_4,
        ax=arreglo_graficas[3],
        fraction=0.046,
        pad=0.04
    )

    plt.tight_layout()

    # GRAFICA 2

    figura2, grafica_convergencia = plt.subplots(figsize=(10, 5))

    colores = plt.cm.tab10(
        np.linspace(0, 1, len(resultados))
    )

    lista_costos = []

    contador = 0

    for dato in resultados:

        costo = dato[0]
        historial = dato[2]

        grafica_convergencia.plot(
            historial,
            color=colores[contador],
            linewidth=1.5,
            label="Corrida " + str(contador + 1)
        )

        lista_costos.append(costo)

        contador = contador + 1

    indice_mejor = np.argmin(lista_costos)

    mejor_historial = resultados[indice_mejor][2]

    grafica_convergencia.plot(
        mejor_historial,
        color="black",
        linewidth=2.5,
        linestyle="--",
        label="Mejor corrida"
    )

    grafica_convergencia.set_title(
        "Curva de Convergencia PSO"
    )

    grafica_convergencia.set_xlabel("Iteraciones")
    grafica_convergencia.set_ylabel("Costo")

    grafica_convergencia.legend()

    grafica_convergencia.grid(True)

    plt.tight_layout()

    # GRAFICA 3
    # ADECUACION HUMEDAD - CULTIVO

    figura3, grafica_barras = plt.subplots(figsize=(10, 4))

    lista_humedades = []
    lista_requerimientos = []
    lista_nombres = []

    for punto in coordenadas:

        x = punto[0]
        y = punto[1]

        humedad, suelo, elevacion, cultivo = campo.obtener_valores(x, y)

        requerimiento = campo.obtener_requerimiento_hidrico(cultivo)
        lista_humedades.append(humedad)
        lista_requerimientos.append(requerimiento)
        nombre_cultivo = campo.CULTIVOS[cultivo]["nombre"]
        lista_nombres.append(nombre_cultivo)

    posiciones_x = np.arange(len(coordenadas))

    grafica_barras.bar(
        posiciones_x - 0.2,
        lista_humedades,
        0.35,
        label="Humedad"
    )

    grafica_barras.bar(
        posiciones_x + 0.2,
        lista_requerimientos,
        0.35,
        label="Req cultivo"
    )

    etiquetas = []

    for i in range(len(coordenadas)):

        texto = "S" + str(i+1)
        etiquetas.append(texto)

    grafica_barras.set_xticks(posiciones_x)
    grafica_barras.set_xticklabels(etiquetas)

    grafica_barras.set_title(
        "Adecuacion Humedad-Cultivo"
    )

    grafica_barras.set_ylabel("Valor")
    grafica_barras.legend()
    grafica_barras.grid(True)
    plt.tight_layout()
    plt.show()


# MAIN

def main():

    print("INICIO DEL PROGRAMA")
    campo = CampoAgricola()
    numero_sensores = 10
    resultados = ejecutar_pruebas(
        campo,
        numero_sensores
    )

    costos = []

    for dato in resultados:
        costos.append(dato[0])
    indice_mejor = np.argmin(costos)
    mejor_costo = resultados[indice_mejor][0]
    mejor_posicion = resultados[indice_mejor][1]
    coordenadas_finales = mejor_posicion.reshape(
        numero_sensores,
        2
    )

    print("\nMEJOR RESULTADO")
    print("Costo:", mejor_costo)

    contador = 1

    for punto in coordenadas_finales:

        x = punto[0]
        y = punto[1]

        h, s, e, c = campo.obtener_valores(x, y)

        print(
            "Sensor",
            contador,
            "-> X:",
            round(x, 2),
            "Y:",
            round(y, 2),
            "H:",
            round(h, 3)
        )

        contador = contador + 1

    mostrar_graficas(
        campo,
        coordenadas_finales,
        resultados
    )


if __name__ == "__main__":
    main()