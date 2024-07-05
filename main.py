import psycopg2
from faker import Faker
from random import randint, choice
import sys

# Crear una instancia de Faker
fake = Faker()

def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="bddproyecto",
        user="postgres",
        password="1234"
    )

def create_categoria(cursor):
    categorias = ['Entrada', 'Plato Principal', 'Postre', 'Bebida']
    cursor.executemany('''
    INSERT INTO Categoria (id_categoria, nombre) VALUES (%s, %s)
    ''', [(i+1, categorias[i]) for i in range(len(categorias))])

def create_persona(cursor, n):
    personas = []
    for i in range(n):
        id_persona = i + 1  # Usar un contador para garantizar unicidad
        nombre_usuario = fake.user_name()[:20]
        nombre = fake.first_name()
        apellido = fake.last_name()
        pais = fake.country()[:20]
        sexo = choice(['M', 'F'])
        email = fake.email()[:30]
        password = fake.password()[:40]
        fechaNacimiento = fake.date_of_birth()

        personas.append((id_persona, nombre_usuario, nombre, apellido, pais, sexo, email, password, fechaNacimiento))

    cursor.executemany('''
    INSERT INTO Persona (id_persona, nombre_usuario, nombre, apellido, pais, sexo, email, password, fechaNacimiento)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', personas)

    return [p[0] for p in personas]

def create_usuario(cursor, persona_ids):
    usuarios = [(i, fake.state_abbr()[:10]) for i in persona_ids]
    cursor.executemany('''
    INSERT INTO Usuario (id_persona, estado)
    VALUES (%s, %s)
    ''', usuarios)

def create_chef(cursor, persona_ids):
    especialidades = ['Italiana', 'Francesa', 'Japonesa', 'Peruana', 'Mexicana']
    chefs = [(i, choice(especialidades)[:25], randint(1, 10)) for i in persona_ids]
    cursor.executemany('''
    INSERT INTO Chef (id_persona, especialidad, nro_premios)
    VALUES (%s, %s, %s)
    ''', chefs)

def create_receta(cursor, n):
    recetas = []
    for i in range(n):
        id_receta = i + 1  # Usar un contador para garantizar unicidad
        nombre = fake.sentence(nb_words=3).replace('.', '')[:50]
        origen = fake.country()[:20]
        calorias_total = randint(100, 1000)
        id_categoria = randint(1, 4)  # Asumiendo que hay 4 categorías insertadas
        descripcion = fake.paragraph()[:1000]
        recetas.append((id_receta, nombre, origen, calorias_total, id_categoria, descripcion))

    cursor.executemany('''
    INSERT INTO Receta (id_receta, nombre, origen, calorias_total, id_categoria, descripcion)
    VALUES (%s, %s, %s, %s, %s, %s)
    ''', recetas)

    return [r[0] for r in recetas]

def create_ingrediente(cursor, n):
    ingredientes = []
    for i in range(n):
        id_ingrediente = i + 1  # Usar un contador para garantizar unicidad
        nombre = fake.word()[:20]
        calorias = randint(10, 200)
        origen = fake.country()[:20]
        cantidad = randint(1, 10)
        ingredientes.append((id_ingrediente, nombre, calorias, origen, cantidad))

    cursor.executemany('''
    INSERT INTO Ingrediente (id_ingrediente, nombre, calorias, origen, cantidad)
    VALUES (%s, %s, %s, %s, %s)
    ''', ingredientes)

    return [i[0] for i in ingredientes]

def create_valoracion(cursor, n, persona_ids, receta_ids):
    valoraciones = []
    for i in range(n):
        id_valoracion = i + 1  # Usar un contador para garantizar unicidad
        comentarios = fake.text(max_nb_chars=255)
        calificacion = randint(1, 5)
        facilidad = randint(1, 5)
        id_persona = choice(persona_ids)
        id_receta = choice(receta_ids)
        valoraciones.append((id_valoracion, comentarios, calificacion, facilidad, id_persona, id_receta))

    cursor.executemany('''
    INSERT INTO Valoracion (id_valoracion, comentarios, calificacion, facilidad, id_persona, id_receta)
    VALUES (%s, %s, %s, %s, %s, %s)
    ''', valoraciones)

def create_sabor(cursor):
    sabores = [
        (1, 'Dulce', 'Media', 'Dulce'),
        (2, 'Salado', 'Alta', 'Salado'),
        (3, 'Acido', 'Baja', 'Acido'),
        (4, 'Picante', 'Muy Alta', 'Picante')
    ]
    cursor.executemany('''
    INSERT INTO Sabor (id_sabor, nombre, intensidad, tipo_sabor)
    VALUES (%s, %s, %s, %s)
    ''', sabores)

def create_mira(cursor, n, persona_ids, receta_ids):
    miras = []
    used_combinations = set()
    for i in range(n):
        while True:
            id_persona = choice(persona_ids)
            id_receta = choice(receta_ids)
            if (id_persona, id_receta) not in used_combinations:
                used_combinations.add((id_persona, id_receta))
                break
        NrVistas = randint(1, 100)
        miras.append((id_persona, NrVistas, id_receta))

    cursor.executemany('''
    INSERT INTO Mira (id_persona, NrVistas, id_receta)
    VALUES (%s, %s, %s)
    ''', miras)

def create_tiene(cursor, n, receta_ids, ingrediente_ids):
    tiene = []
    used_combinations = set()
    for i in range(n):
        while True:
            id_receta = choice(receta_ids)
            id_ingrediente = choice(ingrediente_ids)
            if (id_receta, id_ingrediente) not in used_combinations:
                used_combinations.add((id_receta, id_ingrediente))
                break
        tiene.append((id_receta, id_ingrediente))

    cursor.executemany('''
    INSERT INTO Tiene (id_receta, id_ingrediente)
    VALUES (%s, %s)
    ''', tiene)

def create_toma(cursor, n, receta_ids):
    toma = []
    used_combinations = set()
    for i in range(n):
        while True:
            id_receta = choice(receta_ids)
            id_sabor = randint(1, 4)
            if (id_receta, id_sabor) not in used_combinations:
                used_combinations.add((id_receta, id_sabor))
                break
        toma.append((id_receta, id_sabor))

    cursor.executemany('''
    INSERT INTO Toma (id_receta, id_sabor)
    VALUES (%s, %s)
    ''', toma)

def create_asociada(cursor):
    asociada = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4)
    ]
    cursor.executemany('''
    INSERT INTO Asociada (id_categoria, id_sabor)
    VALUES (%s, %s)
    ''', asociada)

def create_prepara(cursor, n, chef_ids, receta_ids):
    prepara = []
    used_combinations = set()
    for i in range(n):
        while True:
            id_chef = choice(chef_ids)
            id_receta = choice(receta_ids)
            if (id_chef, id_receta) not in used_combinations:
                used_combinations.add((id_chef, id_receta))
                break
        prepara.append((id_chef, id_receta))

    cursor.executemany('''
    INSERT INTO Prepara (id_chef, id_receta)
    VALUES (%s, %s)
    ''', prepara)

def clear_table(cursor, table_name):
    cursor.execute(f'DELETE FROM {table_name} CASCADE')

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <num_registros>")
        sys.exit(1)

    num_registros = int(sys.argv[1])

    conn = connect_db()
    cursor = conn.cursor()

    # Vaciar las tablas si es necesario
    tables = ['Valoracion', 'Mira', 'Tiene', 'Toma', 'Prepara', 'Asociada', 'Usuario', 'Chef', 'Receta', 'Ingrediente', 'Sabor', 'Categoria', 'Persona']
    for table in tables:
        clear_table(cursor, table)

    # Crear datos
    create_categoria(cursor)
    # Confirmar los cambios después de insertar las categorías
    conn.commit()

    persona_ids = create_persona(cursor, num_registros)
    create_usuario(cursor, persona_ids)
    create_chef(cursor, persona_ids)
    receta_ids = create_receta(cursor, num_registros)
    ingrediente_ids = create_ingrediente(cursor, num_registros)
    create_valoracion(cursor, num_registros, persona_ids, receta_ids)
    create_sabor(cursor)
    create_mira(cursor, num_registros, persona_ids, receta_ids)
    create_tiene(cursor, num_registros, receta_ids, ingrediente_ids)
    create_toma(cursor, num_registros, receta_ids)
    create_asociada(cursor)
    create_prepara(cursor, num_registros, persona_ids, receta_ids)

    # Confirmar los cambios
    conn.commit()

    # Cerrar la conexión
    cursor.close()
    conn.close()

    print(f"{num_registros} registros generados y almacenados en la base de datos con éxito.")

if __name__ == "__main__":
    main()