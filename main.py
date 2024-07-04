import psycopg2
from faker import Faker
from random import randint, choice

# Crear una instancia de Faker
fake = Faker()

def connect_db():
    return psycopg2.connect(
        dbname='bddproyecto',
        user='postgres',
        password='1234',
        host='localhost',
        port='5432'
    )

def create_categoria(cursor):
    categorias = ['Entrante', 'Plato Principal', 'Postre', 'Bebida']
    cursor.executemany('''
    INSERT INTO Categoria (id_categoria, nombre) VALUES (%s, %s)
    ''', [(i, categorias[i]) for i in range(len(categorias))])

def create_persona(cursor, n):
    personas = []
    for _ in range(n):
        nombre_usuario = fake.user_name()[:20]
        nombre = fake.first_name()
        apellido = fake.last_name()
        pais = fake.country()[:20]
        sexo = choice(['M', 'F'])
        email = fake.email()[:30]
        password = fake.password()[:40]
        fechaNacimiento = fake.date_of_birth()

        personas.append((nombre_usuario, nombre, apellido, pais, sexo, email, password, fechaNacimiento))

    cursor.executemany('''
    INSERT INTO Persona (nombre_usuario, nombre, apellido, pais, sexo, email, password, fechaNacimiento)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', personas)
    
    return [p[0] for p in personas]

def create_usuario(cursor, n):
    persona_ids = create_persona(cursor, n)
    usuarios = [(i,) for i in persona_ids]
    cursor.executemany('''
    INSERT INTO Usuario (nombre_usuario)
    VALUES (%s)
    ''', usuarios)

def create_chef(cursor, n):
    especialidades = ['Italiana', 'Francesa', 'Japonesa', 'Peruana', 'Mexicana']
    persona_ids = create_persona(cursor, n)
    chefs = [(i, choice(especialidades)[:25], fake.sentence(nb_words=3)[:30]) for i in persona_ids]
    cursor.executemany('''
    INSERT INTO Chef (nombre_usuario, especialidad, premios)
    VALUES (%s, %s, %s)
    ''', chefs)

def create_receta(cursor, n):
    recetas = []
    for _ in range(n):
        nombre = fake.sentence(nb_words=3).replace('.', '')[:50]
        origen = fake.country()[:20]
        calorias_total = randint(100, 1000)
        id_categoria = randint(1, 4)  # Asumiendo que hay 4 categorías insertadas
        descripcion = fake.paragraph()[:1000]
        recetas.append((nombre, origen, calorias_total, id_categoria, descripcion))

    cursor.executemany('''
    INSERT INTO Receta (nombre, origen, calorias_total, id_categoria, descripcion)
    VALUES (%s, %s, %s, %s, %s)
    ''', recetas)

def create_ingrediente(cursor, n):
    ingredientes = []
    for _ in range(n):
        nombre = fake.word()[:20]
        calorias = randint(10, 200)
        origen = fake.country()[:20]
        cantidad = randint(1, 10)
        ingredientes.append((nombre, calorias, origen, cantidad))

    cursor.executemany('''
    INSERT INTO Ingrediente (nombre, calorias, origen, cantidad)
    VALUES (%s, %s, %s, %s)
    ''', ingredientes)

def clear_table(cursor, table_name):
    cursor.execute(f'DELETE FROM {table_name} CASCADE')

def main():
    conn = connect_db()
    cursor = conn.cursor()

    # Vaciar las tablas si es necesario
    clear_table(cursor, 'Valoracion')
    clear_table(cursor, 'Mira')
    clear_table(cursor, 'Tiene')
    clear_table(cursor, 'Toma')
    clear_table(cursor, 'Prepara')
    clear_table(cursor, 'Asociada')
    clear_table(cursor, 'Usuario')
    clear_table(cursor, 'Chef')
    clear_table(cursor, 'Receta')
    clear_table(cursor, 'Ingrediente')
    clear_table(cursor, 'Sabor')
    clear_table(cursor, 'Categoria')
    clear_table(cursor, 'Persona')

    # Crear datos
    create_categoria(cursor)
    create_usuario(cursor, 1000)
    create_chef(cursor, 1000)
    create_receta(cursor, 1000)
    create_ingrediente(cursor, 1000)

    # Confirmar los cambios
    conn.commit()

    # Cerrar la conexión
    cursor.close()
    conn.close()

    print("Datos generados y almacenados en la base de datos con éxito.")

if __name__ == '__main__':
    main()
