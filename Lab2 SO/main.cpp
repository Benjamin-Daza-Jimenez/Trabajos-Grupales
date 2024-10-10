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

struct Game{
    vector<vector<string>> mazo;
    vector<vector<string>> pila_descarte;
    vector<vector<string>> mano_jugador;
    vector<vector<string>> mano_bot1;
    vector<vector<string>> mano_bot2;
    vector<vector<string>> mano_bot3;
    bool cambio_sentido;
    int roba;
};

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
                aux.push_back("verde");
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
            aux.push_back("verde");
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
        aux.push_back("verde");
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
        aux.push_back("verde");
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
        aux.push_back("verde");
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

void create_hand(vector<vector<string>>&vec, Game* shared_game){
    for(int i = 0; i < 7; i++){
        vec.push_back(shared_game->mazo[0]);
        shared_game->mazo.erase(shared_game->mazo.begin());
    }
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
    cout<<"--- Bienvenido a Uno ---"<<endl<<endl;
    
    //Crear memoria compartida
    int mem = shmget(IPC_PRIVATE, sizeof(Game), IPC_CREAT|0666);
    
    //Mapear memoria compartida
    Game* shared_game = (Game*)shmat(mem, nullptr, 0);

    //Inicio del mazo/juego
    create_mazo(shared_game->mazo);
    cout<<"✓ Mazo creado"<<endl<<"✓ Mazo revuelto"<<endl<<endl;
    shared_game->pila_descarte.push_back(shared_game->mazo[0]);
    shared_game->mazo.erase(shared_game->mazo.begin());
    shared_game->cambio_sentido = false;
    shared_game->roba = 0;

    //Crear forks
    int ids[4];

    for(int i=0;i<4;i++){
        ids[i]=fork();
        if(ids[i]==0){
            if(ids[i]==0&&i==0){//Mano jugador
                cout<<"✓ Mano del jugador creada"<<endl;
                create_hand(shared_game->mano_jugador,shared_game);
                break;
            }
            else if(ids[i]==0&&i==1){//Mano bot1
                cout<<"✓ Mano del bot1 creada"<<endl;
                create_hand(shared_game->mano_bot1,shared_game);
                break;
            }
            else if(ids[i]==0&&i==2){//Mano bot2
                cout<<"✓ Mano del bot2 creada"<<endl;
                create_hand(shared_game->mano_bot2,shared_game);
                break;
            }
            else if(ids[i]==0&&i==3){//Mano bot3
                cout<<"✓ Mano del bot3 creada"<<endl;
                create_hand(shared_game->mano_bot3,shared_game);
                break;
            }
        }
    }
    for (int i=0;i<4;i++){
        wait(NULL);
    }

    //Crear turnos
    return 0;
}