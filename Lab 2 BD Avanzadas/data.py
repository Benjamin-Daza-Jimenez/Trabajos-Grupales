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

    def create_constraints(self):
        constraint_queries = [
            "CREATE CONSTRAINT pony_name_unique IF NOT EXISTS FOR (p:Pony) REQUIRE p.nombre IS UNIQUE",
            "CREATE CONSTRAINT location_name_unique IF NOT EXISTS FOR (l:Location) REQUIRE l.nombre IS UNIQUE"
        ]
        
        for query in constraint_queries:
            self.run_query(query)

    def clear_database(self):
        self.run_query("MATCH (n) DETACH DELETE n")

    def create_ponys(self):
        query = """
            MERGE (twilight:Pony { nombre: 'Twilight Sparkle', color: 'Morado', tipo: 'Alicornio', habilidad: 'Magia avanzada', cutiemark: 'Estrella de seis puntas', gusto: 'Libros y conocimiento', bebida: 'Coca Cola' })
            MERGE (rarity:Pony { nombre: 'Rarity', color: 'Blanco', tipo: 'Unicornio', habilidad: 'Diseño de moda', cutiemark: 'Tres diamantes', gusto: 'Moda y lujo', bebida: 'Sprite' })
            MERGE (applejack:Pony { nombre: 'Applejack', color: 'Naranja', tipo: 'Pony terrestre', habilidad: 'Recolección de manzanas', cutiemark: 'Manzana', gusto: 'Familia y trabajo duro', bebida: 'Coca Cola' })
            MERGE (fluttershy:Pony { nombre: 'Fluttershy', color: 'Amarillo', tipo: 'Pegaso', habilidad: 'Comunicación con animales', cutiemark: 'Mariposa', gusto: 'Cuidado de animales', bebida: 'Sprite' })
            MERGE (pinkie:Pony { nombre: 'Pinkie Pie', color: 'Rosa', tipo: 'Pony terrestre', habilidad: 'Organización de fiestas', cutiemark: 'Globos', gusto: 'Fiestas y diversión', bebida: 'Sprite' })
            MERGE (rainbow:Pony { nombre: 'Rainbow Dash', color: 'Cyan', tipo: 'Pegaso', habilidad: 'Velocidad y vuelo', cutiemark: 'Rayo de colores', gusto: 'Carreras y adrenalina', bebida: 'Coca Cola' })
            MERGE (celestia:Pony { nombre: 'Princess Celestia', color: 'Blanco', tipo: 'Alicornio', habilidad: 'Control del sol', cutiemark: 'Sol', gusto: 'Paz y justicia', bebida: 'Sprite' })
            MERGE (luna:Pony { nombre: 'Princess Luna', color: 'Azul', tipo: 'Alicornio', habilidad: 'Control de la luna', cutiemark: 'Luna', gusto: 'Sueños y noche', bebida: 'Sprite' })
            MERGE (shining:Pony { nombre: 'Shining Armor', color: 'Blanco', tipo: 'Unicornio', habilidad: 'Magia de escudo', cutiemark: 'Escudo', gusto: 'Protección y familia', bebida: 'Coca Cola' })
            MERGE (trixie:Pony { nombre: 'Trixie Lulamoon', color: 'Azul', tipo: 'Unicornio', habilidad: 'Ilusionismo', cutiemark: 'Estrella mágica', gusto: 'Espectáculos y atención', bebida: 'Sprite' })
            MERGE (starlight:Pony { nombre: 'Starlight Glimmer', color: 'Lavanda', tipo: 'Unicornio', habilidad: 'Manipulación de magia', cutiemark: 'Cero y uno', gusto: 'Cambio y control', bebida: 'Sprite' })
            MERGE (tempest:Pony { nombre: 'Tempest Shadow', color: 'Gris oscuro', tipo: 'Unicornio', habilidad: 'Magia de relámpago', cutiemark: 'Rayo', gusto: 'Independencia y fuerza', bebida: 'Coca Cola' })
            MERGE (cadance:Pony { nombre: 'Princess Cadance', color: 'Rosa', tipo: 'Alicornio', habilidad: 'Amor y felicidad', cutiemark: 'Corazón', gusto: 'Unión y familia', bebida: 'Coca Cola' })
            MERGE (sour:Pony { nombre: 'Sour Sweet', color: 'Amarillo y verde', tipo: 'Pony terrestre', habilidad: 'Cambios de personalidad', cutiemark: 'Caramelo', gusto: 'Sorpresas y diversión', bebida: 'Sprite' })
            MERGE (sunset:Pony { nombre: 'Sunset Shimmer', color: 'Naranja', tipo: 'Unicornio', habilidad: 'Magia de transformación', cutiemark: 'Sol naciente', gusto: 'Redención y amistad', bebida: 'Coca Cola' })
            MERGE (moondancer:Pony { nombre: 'Moondancer', color: 'Púrpura', tipo: 'Unicornio', habilidad: 'Magia de protección', cutiemark: 'Estrella', gusto: 'Estudio y tranquilidad', bebida: 'Sprite' })
            MERGE (sweetie:Pony { nombre: 'Sweetie Belle', color: 'Blanco', tipo: 'Pony terrestre', habilidad: 'Canto', cutiemark: 'N/A', gusto: 'Música y amigos', bebida: 'Sprite' })
            MERGE (applebloom:Pony { nombre: 'Apple Bloom', color: 'Amarillo', tipo: 'Pony terrestre', habilidad: 'Creatividad', cutiemark: 'N/A', gusto: 'Aventuras y amistad', bebida: 'Sprite' })
            MERGE (scootaloo:Pony { nombre: 'Scootaloo', color: 'Naranja', tipo: 'Pony terrestre', habilidad: 'Vuelo', cutiemark: 'N/A', gusto: 'Carreras y diversión', bebida: 'Coca Cola' })
            MERGE (diamond:Pony { nombre: 'Diamond Tiara', color: 'Rosa', tipo: 'Pony terrestre', habilidad: 'Manipulación social', cutiemark: 'Corona', gusto: 'Poder y estatus', bebida: 'Sprite' })
            MERGE (silver:Pony { nombre: 'Silver Spoon', color: 'Gris', tipo: 'Pony terrestre', habilidad: 'Estrategia', cutiemark: 'Cuchara', gusto: 'Amistad superficial', bebida: 'Sprite' })
            MERGE (zecora:Pony { nombre: 'Zecora', color: 'Negro y blanco', tipo: 'Pony terrestre', habilidad: 'Herboristería', cutiemark: 'Luna', gusto: 'Sabiduría y naturaleza', bebida: 'Coca Cola'  })
            MERGE (vinyl:Pony { nombre: 'Vinyl Scratch', color: 'Blanco y azul', tipo: 'Unicornio', habilidad: 'Música electrónica', cutiemark: 'Nota musical', gusto: 'Fiestas y música', bebida: 'Coca Cola'  })
            MERGE (octavia:Pony { nombre: 'Octavia Melody', color: 'Gris', tipo: 'Pony terrestre', habilidad: 'Tocar el chelo', cutiemark: 'Nota musical', gusto: 'Música clásica', bebida: 'Coca Cola' })
            MERGE (twirly:Pony { nombre: 'Twirly Treats', color: 'Rosa claro', tipo: 'Pony terrestre', habilidad: 'Repostería', cutiemark: 'Cupcake', gusto: 'Dulces y diversión', bebida: 'Coca Cola' })
            MERGE (soaringWind:Pony { nombre: 'Soaring Wind', color: 'Azul claro', tipo: 'Pegaso', habilidad: 'Control del viento', cutiemark: 'Rayo de viento', gusto: 'Aventura y exploración', bebida: 'Coca Cola' })
            MERGE (cloudBurst:Pony { nombre: 'Cloud Burst', color: 'Gris oscuro', tipo: 'Pegaso', habilidad: 'Nubes de tormenta', cutiemark: 'Nube oscura', gusto: 'Intensidad y fuerza', bebida: 'Sprite' })
            MERGE (mistySky:Pony { nombre: 'Misty Sky', color: 'Lavanda', tipo: 'Pegaso', habilidad: 'Creación de niebla', cutiemark: 'Niebla mágica', gusto: 'Tranquilidad y misterio', bebida: 'Sprite' })
            MERGE (goldenFeather:Pony { nombre: 'Golden Feather', color: 'Amarillo dorado', tipo: 'Pegaso', habilidad: 'Vuelo brillante', cutiemark: 'Pluma dorada', gusto: 'Brillo y alegría', bebida: 'Sprite' })


            MERGE (twilight)-[:AMIGOS]->(rarity)
            MERGE (rarity)-[:AMIGOS]->(twilight)
            MERGE (twilight)-[:AMIGOS]->(applejack)
            MERGE (applejack)-[:AMIGOS]->(twilight)
            MERGE (twilight)-[:AMIGOS]->(fluttershy)
            MERGE (fluttershy)-[:AMIGOS]->(twilight)
            MERGE (twilight)-[:AMIGOS]->(pinkie)
            MERGE (pinkie)-[:AMIGOS]->(twilight)
            MERGE (twilight)-[:AMIGOS]->(rainbow)
            MERGE (rainbow)-[:AMIGOS]->(twilight)
            MERGE (rarity)-[:AMIGOS]->(applejack)
            MERGE (applejack)-[:AMIGOS]->(rarity)
            MERGE (applejack)-[:AMIGOS]->(fluttershy)
            MERGE (fluttershy)-[:AMIGOS]->(applejack)
            MERGE (fluttershy)-[:AMIGOS]->(pinkie)
            MERGE (pinkie)-[:AMIGOS]->(fluttershy)
            MERGE (rainbow)-[:AMIGOS]->(pinkie)
            MERGE (pinkie)-[:AMIGOS]->(rainbow)
            MERGE (celestia)-[:AMIGOS]->(luna)
            MERGE (luna)-[:AMIGOS]->(celestia)
            MERGE (cadance)-[:AMIGOS]->(shining)
            MERGE (scootaloo)-[:AMIGOS]->(applebloom)
            MERGE (applebloom)-[:AMIGOS]->(scootaloo)
            MERGE (applebloom)-[:AMIGOS]->(sweetie)
            MERGE (sunset)-[:AMIGOS]->(starlight)
            MERGE (starlight)-[:AMIGOS]->(sunset)
            MERGE (rarity)-[:AMIGOS]->(sour)
            MERGE (sour)-[:AMIGOS]->(rarity)
            MERGE (sweetie)-[:AMIGOS]->(fluttershy)
            MERGE (shining)-[:AMIGOS]->(moondancer)
            MERGE (moondancer)-[:AMIGOS]->(shining)
            MERGE (tempest)-[:AMIGOS]->(trixie)
            MERGE (silver)-[:AMIGOS]->(celestia)
            MERGE (diamond)-[:AMIGOS]->(silver)
            MERGE (cadance)-[:AMIGOS]->(sour)
            MERGE (trixie)-[:AMIGOS]->(starlight)
            MERGE (sour)-[:AMIGOS]->(scootaloo)
            MERGE (scootaloo)-[:AMIGOS]->(sour)
            MERGE (rainbow)-[:AMIGOS]->(diamond)
            MERGE (diamond)-[:AMIGOS]->(rainbow)
            MERGE (sunset)-[:AMIGOS]->(applejack)
            MERGE (moondancer)-[:AMIGOS]->(sunset)
            MERGE (sunset)-[:AMIGOS]->(moondancer)
            MERGE (sour)-[:AMIGOS]->(twilight)
            MERGE (sour)-[:AMIGOS]->(zecora)
            MERGE (zecora)-[:AMIGOS]->(sour)
            MERGE (zecora)-[:AMIGOS]->(octavia)
            MERGE (twirly)-[:AMIGOS]->(applejack)
            MERGE (vinyl)-[:AMIGOS]->(octavia)
            MERGE (octavia)-[:AMIGOS]->(vinyl)
            MERGE (vinyl)-[:AMIGOS]->(trixie)
            MERGE (trixie)-[:ENEMIGOS]->(twilight)
            MERGE (tempest)-[:ENEMIGOS]->(twilight)
            MERGE (tempest)-[:ENEMIGOS]->(octavia)
            MERGE (tempest)-[:ENEMIGOS]->(trixie)
            MERGE (tempest)-[:ENEMIGOS]->(celestia)
            MERGE (tempest)-[:ENEMIGOS]->(twilight)
            MERGE (diamond)-[:ENEMIGOS]->(applebloom)
            MERGE (silver)-[:ENEMIGOS]->(scootaloo)
  
            MERGE (twilight)-[:COLABORACION]->(pinkie)
            MERGE (rarity)-[:COLABORACION]->(sunset)
            MERGE (fluttershy)-[:COLABORACION]->(pinkie)
            MERGE (rainbow)-[:COLABORACION]->(celestia)
            MERGE (shining)-[:COLABORACION]->(twilight)
            MERGE (tempest)-[:COLABORACION]->(starlight)
            MERGE (applejack)-[:COLABORACION]->(sweetie)
            MERGE (applebloom)-[:COLABORACION]->(scootaloo)
            MERGE (sour)-[:COLABORACION]->(diamond)
            MERGE (silver)-[:COLABORACION]->(rarity)
            MERGE (moondancer)-[:COLABORACION]->(fluttershy)
            MERGE (cadance)-[:COLABORACION]->(luna)
            MERGE (twilight)-[:COLABORACION]->(starlight)
            MERGE (sunset)-[:COLABORACION]->(tempest)
            MERGE (rainbow)-[:COLABORACION]->(fluttershy)
            MERGE (scootaloo)-[:COLABORACION]->(twilight)
            MERGE (applebloom)-[:COLABORACION]->(rarity)

            MERGE (ponyville:Ciudad { nombre: 'Ponyville', tipo: 'Ciudad', poblacion: 1000 })
            MERGE (canterlot:Ciudad { nombre: 'Canterlot', tipo: 'Ciudad', poblacion: 5000 })
            MERGE (cloudsdale:Ciudad { nombre: 'Cloudsdale', tipo: 'Ciudad', poblacion: 2000 })
            MERGE (everfree:Ciudad { nombre: 'Everfree Forest', tipo: 'Bosque', poblacion: 100 })
            MERGE (manehattan:Ciudad { nombre: 'Manehattan', tipo: 'Ciudad', poblacion: 8000 })

            MERGE (twilight)-[:VIVE_EN]->(ponyville)
            MERGE (applejack)-[:VIVE_EN]->(ponyville)
            MERGE (fluttershy)-[:VIVE_EN]->(ponyville)
            MERGE (pinkie)-[:VIVE_EN]->(ponyville)
            MERGE (rainbow)-[:VIVE_EN]->(cloudsdale)
            MERGE (rarity)-[:VIVE_EN]->(ponyville)
            MERGE (celestia)-[:VIVE_EN]->(canterlot)
            MERGE (luna)-[:VIVE_EN]->(canterlot)
            MERGE (shining)-[:VIVE_EN]->(canterlot)
            MERGE (cadance)-[:VIVE_EN]->(canterlot)
            MERGE (starlight)-[:VIVE_EN]->(canterlot)
            MERGE (sunset)-[:VIVE_EN]->(canterlot)
            MERGE (moondancer)-[:VIVE_EN]->(canterlot)
            MERGE (zecora)-[:VIVE_EN]->(everfree)
            MERGE (vinyl)-[:VIVE_EN]->(manehattan)
            MERGE (octavia)-[:VIVE_EN]->(manehattan)
            MERGE (twirly)-[:VIVE_EN]->(ponyville)
            MERGE (trixie)-[:VIVE_EN]->(ponyville)
            MERGE (tempest)-[:VIVE_EN]->(everfree)
            MERGE (sour)-[:VIVE_EN]->(canterlot)
            MERGE (diamond)-[:VIVE_EN]->(manehattan)
            MERGE (silver)-[:VIVE_EN]->(manehattan)
            MERGE (scootaloo)-[:VIVE_EN]->(ponyville)
            MERGE (sweetie)-[:VIVE_EN]->(ponyville)
            MERGE (applebloom)-[:VIVE_EN]->(ponyville)
            MERGE (soaringWind)-[:VIVE_EN]->(cloudsdale)
            MERGE (cloudBurst)-[:VIVE_EN]->(cloudsdale)
            MERGE (mistySky)-[:VIVE_EN]->(cloudsdale)
            MERGE (goldenFeather)-[:VIVE_EN]->(cloudsdale)
        """
        self.run_query(query)


if __name__ == "__main__":
    # en la siguiente linea se conecta a la base de datos
    # es poco probable que este no sea el puerto en donde se está ejecutando, pero pueden revisar haciendo click en
    # el nombre del proyecto Ponydb, a la derecha aparecen los diversos puertos, en este caso nos interesa el que dice bolt
    # el usuario por defecto es neo4j, la contraseña deben cambiarla por la que hayan puesto, yo puse 12345678.
    db = PonyDatabase("bolt://localhost:7687", "neo4j", "12345678", "ponydb")
    db.create_constraints()
    db.clear_database() 
    db.create_ponys()

    db.close()
