######################################################################
#
# FUNC.PY
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
# de canales de EEG. Ademas de funciones para el manejo de las rutas
# de acceso a la base de datos.
########################################################################

import numpy as np
from scipy import fftpack
from matplotlib import pylab

# Grafica 4 canales con un mismo eje X en comun.
# Recibe los 4 canales como entrada, el vector de eje x,
# los titulos de los ejes y los canales.
# No retorna nada.
# Grafica el resultado por medio de matplotlib.
def graficar(canal1, canal2, canal3, canal4, tf, ejex, ejey, A, B, C, D):
	pylab.subplot(221)
	pylab.title(A) 
	#pylab.xlabel(ejex)
	pylab.ylabel(ejey)
	pylab.plot(tf, canal1 )

	pylab.suptitle(ejex)

	pylab.subplot(222)
	pylab.title(B) 
	#pylab.xlabel(ejex)
	pylab.ylabel(ejey)
	pylab.plot(tf, canal2 )

	pylab.subplot(223)
	pylab.title(C) 
	#pylab.xlabel(ejex)
	pylab.ylabel(ejey)
	pylab.plot(tf, canal3 )

	pylab.subplot(224)
	pylab.title(D) 
	#pylab.xlabel(ejex)
	pylab.ylabel(ejey)
	pylab.plot(tf, canal4 )

	pylab.show()

# Grafica la transformada rapida de fourier de 8 canales,
# con un mismo eje X en comun.
# Recibe los 8 canales como entrada.
# No retorna nada.
# Grafica el resultado por medio de matplotlib.
def graficarTF(canal1, canal2, canal3, canal4, canal5, canal6, canal7, canal8):
	FCC3hFT = fftpack.fft(canal1)
	FCC4hFT = fftpack.fft(canal2)
	FCC5hFT = fftpack.fft(canal3)
	FCC6hFT = fftpack.fft(canal4)
	CCP3hFT = fftpack.fft(canal5)
	CCP4hFT = fftpack.fft(canal6)
	CCP5hFT = fftpack.fft(canal7)
	CCP6hFT = fftpack.fft(canal8)

	FCC3hFT = FCC3hFT[0:2800]
	FCC4hFT = FCC4hFT[0:2800]
	FCC5hFT = FCC5hFT[0:2800]
	FCC6hFT = FCC6hFT[0:2800]
	CCP3hFT = CCP3hFT[0:2800]
	CCP4hFT = CCP4hFT[0:2800]
	CCP5hFT = CCP5hFT[0:2800]
	CCP6hFT = CCP6hFT[0:2800]

	NumberSamples = 5600
	SpaceSamples = 1.0 / 200

	tf = fftpack.fftfreq(NumberSamples, SpaceSamples)
	tf = tf[0:2800]

	graficar(np.abs(FCC3hFT), np.abs(FCC4hFT), np.abs(FCC5hFT), np.abs(FCC6hFT), tf, "Transformada de fourier", "Magnitud |Y(f)|", "FCC3h", "FCC4h", "FCC5h", "FCC6h")
	graficar(np.abs(CCP3hFT), np.abs(CCP4hFT), np.abs(CCP5hFT), np.abs(CCP6hFT), tf, "Transformada de fourier", "Magnitud |Y(f)|", "CCP3h", "CCP4h", "CCP5h", "CCP6h")

# Genera la ruta de acceso a la base de datos para las senales a trabajar.
# Recibe el numero de paciente y sesion a trabajar.
# Retorna un string con la ruta de acceso.
def FindPath1(paciente, sesion):
	inicio = '/home/vale/Documentos/Datos/CSV/cnt'
	path = inicio+paciente+'-'+sesion+'-x.csv'
	return path

# Genera la ruta de acceso a la base de datos para el tiempo de las senales.
# Recibe el numero de paciente y sesion a trabajar.
# Retorna un string con la ruta de acceso.
def FindPath2(paciente, sesion):
	inicio = '/home/vale/Documentos/Datos/CSV/mrk'
	path = inicio+paciente+'-'+sesion+'-time.csv'
	return path

# Genera la ruta de acceso a la base de datos para la intencion de movimiento.
# Recibe el numero de paciente y sesion a trabajar.
# Retorna un string con la ruta de acceso.
def FindPath3(paciente, sesion):
	inicio = '/home/vale/Documentos/Datos/CSV/mrk'
	path = inicio+paciente+'-'+sesion+'-event.csv'
	return path