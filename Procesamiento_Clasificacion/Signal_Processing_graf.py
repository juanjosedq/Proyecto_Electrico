######################################################################
#
# SIGNAL_PROCESSING_GRAF.PY
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
# El presente codigo realiza las etapas de procesamiento y clasificacion
# de las senales de EEG, basadas en imageneria motora.
########################################################################

import numpy as np
import csv
from scipy import signal
from func import FindPath1, FindPath2
from image_processing import PaintMarks, CalMarks
import socket

newIP = raw_input("Introduzca la IP / default = 0   :")
if newIP == '0':
    newIP = '192.168.0.113'

s = socket.socket()
s.connect((newIP, 9999))

while True:
    paciente = raw_input("Seleccione el paciente [1-29]")
    sesion = raw_input("Seleccione la seccion (1, 3 o 5)")
    tarea = raw_input("Seleccione la tarea [0-19]")

    if(paciente+sesion+tarea == '999'):
        break

    ##########################################################
    #Leer archivo CSV
    ##########################################################
    csv_data = []
    path = FindPath1(paciente, sesion)
    with open(path) as File:
        line = csv.reader(File, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        for row in line:
            csv_data.append(row)

    csv_time = []
    path = FindPath2(paciente, sesion)
    with open(path) as File:
	line = csv.reader(File, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	for row in line:
		csv_time = row

    time = []
    for i in csv_time:
        time.append(float(i))
    time = map(lambda x: x/1000, time)
    time = map(lambda x : x*200, time)

    csvT = []
    for num in xrange(32):
        new_row = []
        for line in csv_data:
            new_row.append(line[num])
        csvT.append(new_row)

    #########################################################################################
    #Seleccionando datos de interes (FCC5H, FCC3H, CCP5H, CCP3H, FCC4H, FCC6H, CCP4H y CCP6H)
    #########################################################################################
    cs = []
    for num in xrange (12, 16):
        cs.append(csvT[num])

    for num in xrange (24, 28):
        cs.append(csvT[num])

    time.append(float(len(cs[0])))

    #############################################################################
    #Seleccionando la tarea deseada
    #############################################################################
    tarea = int(tarea)
    task = xrange(int(time[tarea]),int(time[tarea+1]))
    FCC3h = []
    FCC4h = []
    FCC5h = []
    FCC6h = []
    CCP3h = []
    CCP4h = []
    CCP5h = []
    CCP6h = []
    for num in task:
        FCC3h.append(float(cs[1][num]))
        FCC4h.append(float(cs[4][num]))
        FCC5h.append(float(cs[0][num]))
        FCC6h.append(float(cs[5][num]))
        CCP3h.append(float(cs[3][num]))
        CCP4h.append(float(cs[6][num]))
        CCP5h.append(float(cs[2][num]))
        CCP6h.append(float(cs[7][num]))

    #################################################################################
    # FIltro chebyshev tipo 2 pasabanda
    #################################################################################

    N, Wn = signal.cheb2ord([0.08, 0.15], [0.03, 0.20], 1, 60)
    b, a = signal.cheby2(N, 60, Wn, 'bandpass')

    FCC3hfilt = signal.filtfilt(b, a, FCC3h)
    FCC4hfilt = signal.filtfilt(b, a, FCC4h)
    FCC5hfilt = signal.filtfilt(b, a, FCC5h)
    FCC6hfilt = signal.filtfilt(b, a, FCC6h)
    CCP3hfilt = signal.filtfilt(b, a, CCP3h)
    CCP4hfilt = signal.filtfilt(b, a, CCP4h)
    CCP5hfilt = signal.filtfilt(b, a, CCP5h)
    CCP6hfilt = signal.filtfilt(b, a, CCP6h)

    #############################################################################################
    # Clasificacion
    #############################################################################################

    fF3base, Pxx_F3base = signal.welch(FCC3hfilt[2400:len(FCC3h)], 200, nperseg=200)
    fF4base, Pxx_F4base = signal.welch(FCC4hfilt[2400:len(FCC3h)], 200, nperseg=200)
    fF5base, Pxx_F5base = signal.welch(FCC5hfilt[2400:len(FCC3h)], 200, nperseg=200)
    fF6base, Pxx_F6base = signal.welch(FCC6hfilt[2400:len(FCC3h)], 200, nperseg=200)
    fC3base, Pxx_C3base = signal.welch(CCP3hfilt[2400:len(FCC3h)], 200, nperseg=200)
    fC4base, Pxx_C4base = signal.welch(CCP4hfilt[2400:len(FCC3h)], 200, nperseg=200)
    fC5base, Pxx_C5base = signal.welch(CCP5hfilt[2400:len(FCC3h)], 200, nperseg=200)
    fC6base, Pxx_C6base = signal.welch(CCP6hfilt[2400:len(FCC3h)], 200, nperseg=200)

    potf3base = np.average(abs(Pxx_F3base[9:13]))
    potf4base = np.average(abs(Pxx_F4base[9:13]))
    potf5base = np.average(abs(Pxx_F5base[9:13]))
    potf6base = np.average(abs(Pxx_F6base[9:13]))
    potc3base = np.average(abs(Pxx_C3base[9:13]))
    potc4base = np.average(abs(Pxx_C4base[9:13]))
    potc5base = np.average(abs(Pxx_C5base[9:13]))
    potc6base = np.average(abs(Pxx_C6base[9:13]))

    potf3 = []
    potf4 = []
    potf5 = []
    potf6 = []
    potc3 = []
    potc4 = []
    potc5 = []
    potc6 = []

    for i in xrange(2,14):
        fFCC3h, Pxx_FCC3h = signal.welch(FCC3hfilt[i*200:(i*200)+200], 200, nperseg=200)
        fFCC4h, Pxx_FCC4h = signal.welch(FCC4hfilt[i*200:(i*200)+200], 200, nperseg=200)
        fFCC5h, Pxx_FCC5h = signal.welch(FCC5hfilt[i*200:(i*200)+200], 200, nperseg=200)
        fFCC6h, Pxx_FCC6h = signal.welch(FCC6hfilt[i*200:(i*200)+200], 200, nperseg=200)
        fCCP3h, Pxx_CCP3h = signal.welch(CCP3hfilt[i*200:(i*200)+200], 200, nperseg=200)
        fCCP4h, Pxx_CCP4h = signal.welch(CCP4hfilt[i*200:(i*200)+200], 200, nperseg=200)
        fCCP5h, Pxx_CCP5h = signal.welch(CCP5hfilt[i*200:(i*200)+200], 200, nperseg=200)
        fCCP6h, Pxx_CCP6h = signal.welch(CCP6hfilt[i*200:(i*200)+200], 200, nperseg=200)

        Presf3 = (Pxx_FCC3h - potf3base)
        Presf4 = (Pxx_FCC4h - potf4base)
        Presf5 = (Pxx_FCC5h - potf5base)
        Presf6 = (Pxx_FCC6h - potf6base)
        Presc3 = (Pxx_CCP3h - potc3base)
        Presc4 = (Pxx_CCP4h - potc4base)
        Presc5 = (Pxx_CCP5h - potc5base)
        Presc6 = (Pxx_CCP6h - potc6base)

        Prom_FCC3h = np.average(Presf3[9:13])
        Prom_FCC4h = np.average(Presf4[9:13])
        Prom_FCC5h = np.average(Presf5[9:13])
        Prom_FCC6h = np.average(Presf6[9:13])
        Prom_CCP3h = np.average(Presc3[9:13])	
        Prom_CCP4h = np.average(Presc4[9:13])
        Prom_CCP5h = np.average(Presc5[9:13])
        Prom_CCP6h = np.average(Presc6[9:13])

        potf3.append(Prom_FCC3h)
        potf4.append(Prom_FCC4h)
        potf5.append(Prom_FCC5h)
        potf6.append(Prom_FCC6h)
        potc3.append(Prom_CCP3h)
        potc4.append(Prom_CCP4h)
        potc5.append(Prom_CCP5h)
        potc6.append(Prom_CCP6h)

    maxp = []
    minp = []

    minp.append(np.amin(potf3))
    minp.append(np.amin(potf4))
    minp.append(np.amin(potf5))
    minp.append(np.amin(potf6))
    minp.append(np.amin(potc3))
    minp.append(np.amin(potc4))
    minp.append(np.amin(potc5))
    minp.append(np.amin(potc6))

    maxp.append(np.amax(potf3))
    maxp.append(np.amax(potf4))
    maxp.append(np.amax(potf5))
    maxp.append(np.amax(potf6))
    maxp.append(np.amax(potc3))
    maxp.append(np.amax(potc4))
    maxp.append(np.amax(potc5))
    maxp.append(np.amax(potc6))

    resultimpar = []
    resultpar = []

    for i in xrange(0, 8, 2):
        valor = (abs(minp[i]) - abs(maxp[i]))/(abs(maxp[i])*100)
        resultimpar.append(valor)

    for i in xrange(1, 8, 2):
        valor = (abs(minp[i]) - abs(maxp[i]))/(abs(maxp[i])*100)
        resultpar.append(valor)

    graf = []
    graf.append(resultimpar[0])
    graf.append(resultimpar[1])
    graf.append(resultimpar[2])
    graf.append(resultimpar[3])
    graf.append(resultpar[0])
    graf.append(resultpar[1])
    graf.append(resultpar[2])
    graf.append(resultpar[3])

    #Generador de imagen
    graf2 = CalMarks(graf)
    PaintMarks(graf2)

    manoderecha = 0
    manoizquierda = 0

    for num in xrange(4):
        if resultimpar[num] < resultpar[num]:
            manoizquierda = manoizquierda + 1
        else:
            manoderecha = manoderecha + 1

    if manoizquierda < manoderecha:
        s.send('3')
    elif manoderecha < manoizquierda:
		s.send('1')
    else:
		if np.amax(resultimpar) > np.amax(resultpar):
			s.send('3')
		else:
			s.send('1')
    print('------------------------------------------')
    
s.close()