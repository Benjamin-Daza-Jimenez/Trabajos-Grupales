#include<iostream>
#include<algorithm>
#include<random>
#include<fstream>
#include<vector>
#include<string>
#include<sys/types.h>
#include<sys/shm.h>
#include<unistd.h>
#include<sys/wait.h>
#include<sys/mman.h>
#include<fcntl.h> 
using namespace std;

void create_mazo(vector<vector<string>>&vec){
    vector<string> aux;
    for(int i=0;i<10;i++){//Cartas de color entre 0 y 9
        if(i!=0){
            for(int j=0;j<2;j++){
                aux.push_back(to_string(i));
                aux.push_back("rojo");
                vec.push_back(aux);
                aux.clear();
                aux.push_back(to_string(i));
                aux.push_back("azul");
                vec.push_back(aux);
                aux.clear();
                aux.push_back(to_string(i));
                aux.push_back("amarillo");
                vec.push_back(aux);
                aux.clear();
                aux.push_back(to_string(i));
                aux.push_back("azul");
                vec.push_back(aux);
                aux.clear();
            }
        }
        else{//i==0
            aux.push_back(to_string(i));
            aux.push_back("rojo");
            vec.push_back(aux);
            aux.clear();
            aux.push_back(to_string(i));
            aux.push_back("azul");
            vec.push_back(aux);
            aux.clear();
            aux.push_back(to_string(i));
            aux.push_back("amarillo");
            vec.push_back(aux);
            aux.clear();
            aux.push_back(to_string(i));
            aux.push_back("azul");
            vec.push_back(aux);
            aux.clear();
        }
    }
    for(int i=0;i<2;i++){//Cambio de sentido
        aux.push_back("Cambio de sentido");
        aux.push_back("rojo");
        vec.push_back(aux);
        aux.clear();
        aux.push_back("Cambio de sentido");
        aux.push_back("azul");
        vec.push_back(aux);
        aux.clear();
        aux.push_back("Cambio de sentido");
        aux.push_back("amarillo");
        vec.push_back(aux);
        aux.clear();
        aux.push_back("Cambio de sentido");
        aux.push_back("azul");
        vec.push_back(aux);
        aux.clear();
    }
    for(int i=0;i<2;i++){//Salta
        aux.push_back("Salta");
        aux.push_back("rojo");
        vec.push_back(aux);
        aux.clear();
        aux.push_back("Salta");
        aux.push_back("azul");
        vec.push_back(aux);
        aux.clear();
        aux.push_back("Salta");
        aux.push_back("amarillo");
        vec.push_back(aux);
        aux.clear();
        aux.push_back("Salta");
        aux.push_back("azul");
        vec.push_back(aux);
        aux.clear();
    }
    for(int i=0;i<2;i++){//Roba Dos
     aux.push_back("Roba Dos");
        aux.push_back("rojo");
        vec.push_back(aux);
        aux.clear();
        aux.push_back("Roba Dos");
        aux.push_back("azul");
        vec.push_back(aux);
        aux.clear();
        aux.push_back("Roba Dos");
        aux.push_back("amarillo");
        vec.push_back(aux);
        aux.clear();
        aux.push_back("Roba Dos");
        aux.push_back("azul");
        vec.push_back(aux);
        aux.clear();
    }
    for(int i=0;i<4;i++){//Comodín
        aux.push_back("Comodin");
        aux.push_back("negro");
        vec.push_back(aux);
        aux.clear();
    }
    for(int i=0;i<4;i++){//Comodín Roba Cuatro
        aux.push_back("Comodin Roba Cuatro");
        aux.push_back("negro");
        vec.push_back(aux);
        aux.clear();
    }
    //Desordena el mazo
    random_device dv;
    mt19937 g(dv());
    shuffle(vec.begin(),vec.end(),g);
}

void tirar_carta(vector<string>&carta,vector<vector<string>>&descarte){
    vector<string>carta_ds=descarte[descarte.size()-1];
    if(carta[1]=="negro"){//Comodines
        if(carta[0]=="Comodin"){
            //Hacer lo que deba hacer
        }
        else if(carta[0]=="Comodin Roba Cuatro"){
            //Hacer lo que deba hacer
        }
    }
    else if(carta[0]=="Roba Dos"&&carta[1]==carta_ds[1]){//Roba 2
        //Hacer lo que deba hacer
    }
    else if(carta[0]=="Salta"&&carta[1]==carta_ds[1]){//Salta
        //Hacer lo que deba hacer
    }
    else if(carta[0]=="Cambio de sentido"&&carta[1]==carta_ds[1]){//Cambio de sentido
        //Hacer lo que deba hacer
    }
    else if(carta[0]==carta_ds[0]||carta[1]==carta_ds[1]){//Tira una carta numerica
        //Hacer lo que deba hacer
    }
}

int main(){
    //Inicio del mazo
    vector<vector<string>> mazo;
    create_mazo(mazo);
    vector<vector<string>> pila_descarte;
    pila_descarte.push_back(mazo[0]);
    mazo.erase(mazo.begin());

    //Crear memoria compartida
    int mem = shm_open("/memoria", O_CREAT | O_RDWR, 0666);
    
    //Establecer tamanio memoria
    size_t total_size = (mazo.size() + pila_descarte.size()) * sizeof(vector<vector<string>>);
    ftruncate(mem, total_size);
    
    //Mapear memoria compartida
    vector<vector<string>>* shared_memory = (vector<vector<string>>*)mmap(NULL, total_size, PROT_READ | PROT_WRITE, MAP_SHARED, mem, 0);

    //Copiar elementos
    for (size_t i = 0; i < mazo.size(); ++i) {
        shared_memory[i].push_back(mazo[i]); // Copiar el primer vector
    }
    for (size_t i = 0; i < pila_descarte.size(); ++i) {
        shared_memory[mazo.size() + i].push_back(pila_descarte[i]); // Copiar el segundo vector
    }
    
    //Crear forks
    int id1,id2,id3,id4;
    id1 = fork();
    if(id1==0){
        //Mano1
        vector<vector<string>> mano_jugador;
        for(int i = 0; i < 7; i++){
            mano_jugador.push_back(mazo[0]);
            mazo.erase(mazo.begin());
        }
        id2 = fork();
    }
    if(id2==0){
        //Mano2
        id3 = fork();
    }
    if(id3==0){
        //Mano3
        id4 = fork();
    }
    if(id4==0){
        //Mano4
    }
    else{
        wait(NULL);
    }

    //Crear mano

    //Crear turnos

    
    return 0;
}