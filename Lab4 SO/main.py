import threading, time, random
from datetime import datetime

#Globales
TOTAL_JUGADORES = 256
JUGADORES_POR_GRUPO = 32
finalista1=''
finalista2=''
hebra1=''
hebra2=''
resultado=''
adelante=False

#Locks que verifican las 32 hebras
lock_validacion1 = threading.Lock()
lock_validacion2 = threading.Lock()
condicion_grupo1 = threading.Condition(lock_validacion1)
condicion_grupo2 = threading.Condition(lock_validacion2)

#Almacenan las Hebras
hebras_grupo1 = []
hebras_grupo2 = []
hebras_eliminatoria = []
hebras_repechaje=[]

#Lock que protege al contador (asigna el grupo)
lock_contador = threading.Lock()
contador_global = 0
contador=256

# Semáforos para permitir solo una hebra por grupo
semaforo_paso1 = threading.Semaphore(1)
semaforo_paso2 = threading.Semaphore(1)

#Lock y condicion para elimintorias
lock_eliminatoria = threading.Lock()
lock_eliminatoria2 = threading.Lock()
condicion_eliminatoria = threading.Condition(lock_eliminatoria2)

def iniciar_threads(validar): #Creación de las 256 hebras, estas se guardan en una lista
    lista=[]
    for i in range(TOTAL_JUGADORES):
        h=threading.Thread(name='H'+str(i+1), target=proceso, args=(("Hebra"+str(i+1)),validar,))
        h.start()
        lista.append(h)
    return lista

def cerrar_threads(hebras): 
    for hebra in hebras:
        hebra.join()

def validacion(hebra,validar):
    
    global hebras_grupo1, hebras_grupo2, contador_global

    #Asigna el grupo según orden de llegada
    with lock_contador:
        contador_global += 1
        if(contador_global%2==0):grupo=1
        else:grupo=2

    #Pasa el proceso a su grupo correspondiente
    if grupo==1:
        with condicion_grupo1:
            #Iniciar el tiempo de la hebra
            entrada = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            validar.write(hebra+" "+entrada+"\n")

            hebras_grupo1.append(hebra)
            if(len(hebras_grupo1)<JUGADORES_POR_GRUPO):
                condicion_grupo1.wait()

            else:
                #time.sleep(15)
                condicion_grupo1.notify_all()
                hebras_grupo1=[]
    elif grupo==2:
        with condicion_grupo2:
            #Iniciar el tiempo de la hebra
            entrada = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            validar.write(hebra+" "+entrada+"\n")

            hebras_grupo2.append(hebra)
            if(len(hebras_grupo2)<JUGADORES_POR_GRUPO):
                condicion_grupo2.wait()
            else:
                #time.sleep(15)
                condicion_grupo2.notify_all()
                hebras_grupo2=[]

def eliminacion_directa(hebra):
    global hebras_eliminatoria, hebras_repechaje, contador, finalista1, hebra1, hebra2, resultado
    flag = True
    while(flag):
        print(contador)
        with lock_eliminatoria:
            hebras_eliminatoria.append(hebra)
            if(len(hebras_eliminatoria) == 1): 
                hebra1 = hebra
                adelante = False
            if(len(hebras_eliminatoria) == 2):
                hebra2 = hebra
                hebras_eliminatoria.pop()
                hebras_eliminatoria.pop()
                resultado = batalla(hebra1, hebra2)
                #Comprobar si es perdedor o no
                if(resultado[1] == hebra):
                    contador-=1
                    hebras_repechaje.append(hebra)
                    adelante = True
                    return
                adelante = True
        if(hebra1 == hebra):
            while(adelante == False):
                pass
            #Comprobar si es perdedor o no
            if(resultado[1] == hebra):
                contador-=1
                hebras_repechaje.append(hebra)
                return
        if(contador == 1):
            finalista1 = hebra
            return

def batalla(hebra1, hebra2):
    ganador = random.choice([hebra1, hebra2])
    perdedor=''
    if(hebra1!=ganador):perdedor=hebra1
    else:perdedor=hebra2
    return [ganador,perdedor]        



def proceso(hebra,validar):
    global finalista1
    #Validación
    validacion(hebra,validar)
    #Eliminación directa
    eliminacion_directa(hebra)
    #Repechaje
    if(hebra==finalista1):print(hebra)

def main():
    #Abrir archivos
    validar = open("Validación.txt",'w')

    hebras = iniciar_threads(validar)

    cerrar_threads(hebras)

if __name__ == "__main__":
    main()