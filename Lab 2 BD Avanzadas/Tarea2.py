from neo4j import GraphDatabase

class PonyDatabase:
    def __init__(self, uri, user, password, database_name):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database_name = database_name

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters = None):
        with self.driver.session(database=self.database_name) as session:
            session.run(query, parameters)
    
    def return_query(self, query, parameters = None):
        with self.driver.session(database=self.database_name) as session:
            result = session.run(query, parameters)
            return [record for record in result]

    def add_pony(self):
        nombre = input("Ingresa el nombre del pony: ")
        color = input("Ingresa el color del pony: ")
        tipo = input("Ingresa el tipo del pony: ")
        habilidad = input("Ingresa la habilidad del pony: ")
        cutiemark = input("Ingresa la cutiemark del pony: ")
        gusto = input("Ingresa los gustos del pony: ")
        bebida = input("Ingresa la bebida del pony: ")
        nodo = nombre.lower().replace(" ", "")
        query = '''
            MERGE ("'''+nodo+'''":Pony { nombre: '"'''+nombre+'''"', color: '"'''+color+'''"', tipo: '"'''+tipo+'''"', habilidad: '"'''+habilidad+'''"', cutiemark: '"'''+cutiemark+'''"', gustos: '"'''+gusto+'''"', bebida: '"'''+bebida+'''"' })
            MERGE ("'''+nodo+'''")-[:AMIGOS]->(vinyl)
        '''
        self.run_query(query)

    def cant_ponys(self):
        ciudad = input("Ingrese el nombre de la ciudad: ")
        query = '''
            MATCH ((pony)-[:VIVE_EN]->(ciudad:Ciudad{nombre:"'''+ciudad+'''"}))
            RETURN COUNT(pony) AS total_ponys
        '''
        result = self.return_query(query)
        print(result[0]['total_ponys'] if result else 0)

    def add_anexo(self):
        query = '''
            MATCH (p:Pony)
            OPTIONAL MATCH (p)-[:AMIGOS]->(a:Pony)
            WITH p, COUNT(a) AS total_amigos
            SET p.anexo = CASE
                WHEN p.tipo = "Unicornio" AND total_amigos >= 3 THEN "Sociable"
                WHEN p.tipo = "Unicornio" AND total_amigos = 2 THEN "Reservado"
                WHEN p.tipo = "Unicornio" AND total_amigos = 1 THEN "Solitario"
                WHEN p.tipo = "Pony terrestre" AND total_amigos >= 4 THEN "Hipersociable"
                WHEN p.tipo = "Pony terrestre" AND total_amigos <= 2 THEN "Reservado"
                WHEN p.tipo = "Alicornio" THEN "Realeza"
                ELSE "Por Completar"
            END
        '''
        self.run_query(query)

    def camino_corto(self):
        pony1 = input("Ingrese el nombre del primer pony: ")
        pony2 = input("Ingrese el nombre del segundo pony: ")
        query = '''
            MATCH path = shortestPath((pony1:Pony{nombre:"'''+pony1+'''"})-[:AMIGOS*]->(pony2:Pony{nombre:"'''+pony2+'''"}))
            RETURN nodes(path) AS path, length(path) AS length
         '''
        result = self.return_query(query)
        if result:
            short_path = (result[0]['path'] if result else None)
            length = result[0]['length']  
            print(f"Longitud del camino: {length}")
            print("Nodos en el camino:")
            for nodo in short_path:
                print(f"{nodo['nombre']} ({nodo['tipo']})")
        else:
            print("No existe relacion")

    def friend_of_friend(self):
        nombre = input("Ingrese nombre del pony: ")
        query = '''
            MATCH ((pony:Pony{nombre:"'''+nombre+'''"})-[:AMIGOS]->(amigo:Pony)-[:AMIGOS]->(amigo_de_amigo:Pony))
            WHERE amigo_de_amigo <> amigo AND amigo_de_amigo <> pony
            RETURN DISTINCT amigo_de_amigo.nombre AS amigo_de_amigo
        '''
        result = self.return_query(query)
        if result:
            print("Amigos de amigos:")
            for record in result:
                print(f"{record['amigo_de_amigo']}")
        else:
            print("No se encontraron amigos de amigos.")

    def magic_ponys(self):
        query = '''
            MATCH (pony:Pony)
            WHERE toLower(pony.habilidad) CONTAINS 'magia'
            RETURN pony.nombre AS pony
        '''
        result = self.return_query(query)
        if result:
            print("Lista de ponys con habilidades relacionadas a la magia:")
            for record in result:
                print(f"{record['pony']}")
        else:
            print("No se encontraron ponys.")

    def friend_uni(self):
        query = '''
        MATCH ((pony:Pony)-[:AMIGOS]->(amigo:Pony))
        WHERE NOT (amigo)-[:AMIGOS]->(pony)
        RETURN pony.nombre AS pony_amigo, amigo.nombre AS amigo_no_amigo
        '''
        result = self.return_query(query)
        if result:
            for record in result:
                print(f"{record['pony_amigo']} es amigo unidireccional de {record['amigo_no_amigo']}")
        else:
            print("No se encontraron ponys con amigos unidereccionales.")

    def ponys_pref(self):
        tipo = input("Ingresar el tipo de pony: ")
        query = '''
            MATCH (pony:Pony {tipo:"'''+tipo+'''"})
            WHERE pony.bebida IN ['Coca Cola', 'Sprite']
            RETURN pony.bebida AS bebida, COUNT(pony) AS cantidad
        '''
        result = self.return_query(query)
        suma = 0
        if result:
            print("Preferencias de bebida para ponis del tipo: "+ tipo)
            for record in result:
                bebida = record['bebida']
                cantidad = record['cantidad']
                suma += cantidad
                print(f"Bebida: {bebida}, Cantidad: {cantidad}")
            print(f"Cantidad total: {suma}")
        else:
            print("No se encontraron ponys.")
        
    def more_enemys(self):
        query = '''
            MATCH (pony:Pony)
            OPTIONAL MATCH (pony)-[:ENEMIGOS]->(enemigo:Pony)
            WITH pony, COUNT(enemigo) AS enemigos
            OPTIONAL MATCH (pony)-[:COLABORACION]->(colaborador:Pony)
            WITH pony, enemigos, COUNT(colaborador) AS colaboradores
            WHERE enemigos > colaboradores
            RETURN pony.nombre AS pony
        '''
        result = self.return_query(query)
        if result:
            print("Ponys que tienen mas enemigos que colaboraciones:")
            for record in result:
                print(f"{record['pony']}")
        else:
            print("No se encontraron ponys.")
        
    def pref_and_friend(self):
        query = '''
            MATCH ((pony:Pony {bebida:"Coca Cola"})-[:AMIGOS]->(amigo:Pony{tipo:"Pony terrestre", bebida:"Sprite"}))
            RETURN DISTINCT pony.nombre as pony
        '''
        result = self.return_query(query)
        if result:
            print("Ponys que prefieren Coca Cola y tienen al menos un amigo que prefiere Sprite:")
            for record in result:
                print(f"{record['pony']}")
        else:
            print("No se encontraron ponys.")


def opciones():
    print("(1) Agregar un pony a la base de datos y definir una relacion de amistad con el nodo de nombre Vinyl.")
    print("(2) Retornar la cantidad de pegasos, ponis terrestres y unicornios de una ciudad.")
    print("(3) Agregar un campo extra llamado anexo a los ponis segun el numero de amigos que tengan.")
    print("(4) Encontrar el camino mas corto entre ponis, considerando unicamente la relacion de amistad.")
    print("(5) Encontrar los amigos de los amigos de un pony, sin contar a los amigos directos.")
    print("(6) Retornar los ponis en los que el atributo habilidad este relacionado con la magia.")
    print("(7) Retornar nombres de los ponis que tienen relaciones de amistad unidireccionales, y con quien.")
    print("(8) Retornar la cantidad de pegasos, alicornios, ponis terrestres o unicornios que tienen preferencia por Coca Cola o Sprite.")
    print("(9) Retornar los ponis que tienen mas enemigos que colaboraciones con otros ponis.")
    print("(10) Encontrar los ponis que tienen preferencia por Coca Cola y que tengan al menos un amigo pony terrestre que prefiera Sprite.")
    print("(11) Salir.")

#Main
#Conexion DB
db = PonyDatabase("bolt://localhost:7687", "neo4j", "12345678", "ponydb")

flag = True
while(flag == True):
    opciones()
    opcion = input("Ingrese su opcion: ")
    if(opcion == '1'):
        db.add_pony()
    elif(opcion == '2'):
        db.cant_ponys()
    elif(opcion == '3'):
        db.add_anexo()
    elif(opcion == '4'):
        db.camino_corto()
    elif(opcion == '5'):
        db.friend_of_friend()
    elif(opcion == '6'):
        db.magic_ponys()
    elif(opcion == '7'):
        db.friend_uni()
    elif(opcion == '8'):
        db.ponys_pref()
    elif(opcion == '9'):
        db.more_enemys()
    elif(opcion == '10'):
        db.pref_and_friend()
    elif(opcion == '11'):
        flag = False

#Cerrar BD
db.close()