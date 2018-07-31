######################################################################
#
# IMAGE_PROCESSING.PY
#
# AUTOR: Juan Jose Delgado Quesada
# Correo: juanjose.dq@gmail.com
#
# Proyecto de graduacion 
# Universidad de Costa Rica
# Escuela de Ingenieria Electrica
# 2018
########################################################################

########################################################################
# El presente codigo contiene funciones utiles para la graficacion
# del porcentaje de intensidad de ERD/ERS para 8 canales, en una
# plantilla.
########################################################################

import cv2
import numpy as np

# Modifica la imagen de plantilla para graficar el porcentaje de
# intensidad de cada electrodo.
# Recibe el vector con los porcentajes de intensidad de cada canal.
# El resultado lo guarda en la imagen: result.png
def PaintMarks(porcentajes):
    img = cv2.imread('plantilla.png', cv2.IMREAD_COLOR)
    clas = []
    for i in porcentajes:
        if i >= 80.0:
            clas.append((2,4,212))
        elif i >= 60.0:
            clas.append((0,92,255))
        elif i >= 40.0:
            clas.append((54,229,255))
        elif i >= 20.0:
            clas.append((255,161,0))
        else:
            clas.append((255,0,0))

    cv2.circle(img,(417,333),18,clas[5],-1) #Derecha-(derecha-abajo)
    cv2.circle(img,(417,282),18,clas[1],-1) #Derecha-(derecha-arriba)
    cv2.circle(img,(365,282),18,clas[3],-1) #Derecha-(izquierda-arriba)
    cv2.circle(img,(365,333),18,clas[7],-1) #Derecha-(izquierda-abajo)
    cv2.circle(img,(207,282),18,clas[2],-1) #Izquierda-(derecha-arriba)
    cv2.circle(img,(155,335),18,clas[4],-1) #Izquierda-(izquierda-abajo)
    cv2.circle(img,(155,282),18,clas[0],-1) #Izquierda-(izquierda-arriba)
    cv2.circle(img,(207,335),18,clas[6],-1) #Izquierda-(derecha-abajo)

    cv2.imwrite('result.png', img)

# Calcula el porcentaje de intensidad de cada canal a partir del valor
# de ERD/ERS.
# Recibe un vector con los valores de ERD/ERS por canal.
# Retorna un vector con el resultado.
def CalMarks(porcentajes):
    graf = []
    comp = np.amin(porcentajes)
    for i in porcentajes:
        graf.append(i + (2*abs(comp)))

    graf2 = []
    comp = np.amax(graf)
    for i in graf:
        graf2.append((i*100)/comp)
    return graf2

