import matplotlib.pyplot as plt
import numpy as np

def obtener_input():
    L = float(input("Ingrese la longitud de la viga: "))
    n_soportes = int(input("Ingrese el número de soportes (mínimo 2): "))
    soportes = []
    for i in range(n_soportes):
        pos = float(input(f"Ingrese la posición del soporte {i+1}: "))
        soportes.append(pos)
    
    n_cargas = int(input("Ingrese el número de cargas (mínimo 1): "))
    cargas = []
    for i in range(n_cargas):
        tipo = input(f"Ingrese el tipo de carga {i+1} (puntual/distribuida): ")
        pos = float(input(f"Ingrese la posición de la carga {i+1}: "))
        magnitud = float(input(f"Ingrese la magnitud de la carga {i+1}: "))
        if tipo == "distribuida":
            fin = float(input(f"Ingrese la posición final de la carga distribuida {i+1}: "))
            cargas.append((tipo, pos, fin, magnitud))
        else:
            cargas.append((tipo, pos, magnitud))
    
    return L, soportes, cargas

def calcular_reacciones(L, soportes, cargas):
    R1 = 0
    R2 = 0
    
    for carga in cargas:
        if carga[0] == "puntual":
            R1 += carga[2] * (L - carga[1]) / L
            R2 += carga[2] * carga[1] / L
        else:
            w = carga[3]
            a = carga[1]
            b = carga[2]
            R1 += w * (b - a) * (L - (a + b) / 2) / L
            R2 += w * (b - a) * ((a + b) / 2) / L
    
    return R1, R2

def calcular_cortante(x, L, soportes, cargas, R1, R2):
    V = 0
    
    if x >= soportes[0]:
        V += R1
    if x >= soportes[1]:
        V += R2
    
    for carga in cargas:
        if carga[0] == "puntual":
            if x >= carga[1]:
                V -= carga[2]
        else:
            a = carga[1]
            b = carga[2]
            w = carga[3]
            if x > b:
                V -= w * (b - a)
            elif x > a:
                V -= w * (x - a)
    
    return V

def graficar_diagrama_cortante(L, soportes, cargas):
    R1, R2 = calcular_reacciones(L, soportes, cargas)
    
    x = np.linspace(0, L, 1000)
    V = []
    
    for xi in x:
        v = calcular_cortante(xi, L, soportes, cargas, R1, R2)
        V.append(v)
    
    fig, ax1 = plt.subplots(figsize=(10, 5))
    
    # Diagrama de fuerza cortante
    ax1.plot(x, V)
    ax1.set_title("Diagrama de Fuerza Cortante")
    ax1.set_xlabel("Posición en la viga")
    ax1.set_ylabel("Fuerza Cortante")
    ax1.grid(True)
    
    plt.tight_layout()
    plt.show()

# Programa principal
L, soportes, cargas = obtener_input()
graficar_diagrama_cortante(L, soportes, cargas)