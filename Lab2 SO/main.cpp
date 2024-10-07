#include<iostream>
#include<vector>
#include<string>
#include<sys/types.h>
#include<unistd.h>
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
    
}

int main(){
    vector<vector<string>> mazo;
    create_mazo(mazo);
    vector<vector<string>> pila_descarte;
    //Crear forks
    int id1,id2,id3,id4;
    id1 = fork();
    if(id1=!0){
        id2 = fork();
    }
    if(id2!=0){
        id3 = fork();
    }
    if(id3!=0){
        id4 = fork();
    }
    //Crear mano

    //Crear turnos

    
    return 0;
}