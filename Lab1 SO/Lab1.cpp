#include <iostream>
#include <string>
#include <fstream>
#include <dirent.h>
#include <vector>
#include <cstdio>
#include <cstdlib>
using namespace std;

int main(){
    string line, path="./archivos_deportes";
    DIR *direccion;
    vector<string> deporte;
    vector<string> categoria;
    direccion=opendir(path.c_str());
    while(dirent*i=readdir(direccion)){   
        string name = i->d_name;
        if(name!="." && name!=".."){
            string dep_aux,cat_aux, path_archivo="./archivos_deportes/"+name;                      //Recorre el directorio
            ifstream archivo(path_archivo);
            archivo.is_open();                          //Leer cada archivo
            int j=0;
            while(getline(archivo, line)){                      //Obtener las 3 lineas del archivo
                bool flag = false;
                if(j==0){//Deporte
                    dep_aux=line;
                    for(int k=0;k<deporte.size();k++){
                        if(deporte[k] == line){
                            flag = true;
                        }
                    }
                    if(flag==false){//Crear directorio
                        deporte.push_back(line);
                        string p="./"+line;
                        mkdir(p.c_str());
                    }
                }
                else if(j==1){//Categoría
                    cat_aux=line;
                    for(int k=0; k<categoria.size();k++){
                        if(categoria[k] == line){
                            flag = true;
                        }
                    }
                    if(flag==false){//Crear directorio y los dos directorios de medalla o no
                        categoria.push_back(line);
                        string p="./"+dep_aux+"/"+line;
                        mkdir(p.c_str());
                        p="./"+dep_aux+"/"+line+"/ConMedalla";
                        mkdir(p.c_str());
                        p="./"+dep_aux+"/"+line+"/SinMedalla";
                        mkdir(p.c_str());
                    }
                }
                else if(j==2){//Medalla
                    if(line=="Sin Medalla"){
                        string p="./"+dep_aux+"/"+cat_aux+"/SinMedalla/"+name;
                        //archivo guardarlo en....
                    }
                    else{
                        string p="./"+dep_aux+"/"+cat_aux+"/ConMedalla/"+name;
                        //system(("move "+path_archivo+" "+p+"/"+name).c_str());
                        cout<<p<<endl;
                        if(rename(path_archivo.c_str(),p.c_str())!=0){
                            cout<<"Todo mal"<<endl;
                        };
                    }
                }
                j++;
            }
            archivo.close();
        }
    }
    closedir(direccion);
    system("pause");
    return 0;
}