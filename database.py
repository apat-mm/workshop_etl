import psycopg2
from pandas import DataFrame
import json

#Lectura archivo json con credenciales
with open('./db_config.json', 'r') as archivo:
    datos = json.load(archivo)

#Conexión con la base de datos 
try:
    conn = psycopg2.connect(
        host = 'localhost',
        user = datos['user'],
        password = datos['password'],
        database = datos['database']
    )
    print('¡Conexion exitosa!!')
    cursor = conn.cursor()


#Cración de tabla en postgres
    sql = '''
           CREATE TABLE candidates
           (first_name varchar, 
           last_name varchar,
           email varchar,
           application_date date,
           country varchar,
           YOE INT,
           seniority varchar,
           technology varchar,
           code_challenge_score INT,
           technical_interview_score INT
           );
           '''   
    cursor.execute(sql)
    conn.commit()
    print('¡Tabla creada!')


#Inserción de datos del csv a la tabla creada previamente
    sql = '''
            COPY candidates(first_name, last_name, email, application_date, country, YOE, seniority, technology, code_challenge_score, technical_interview_score)
            FROM 'C:/datac/candidates.csv' DELIMITER ';' CSV HEADER;
          '''
    cursor.execute(sql)
    conn.commit()
    print('¡Registros ingresados!')


#Creación de una columna vacía para almacenar los canditos contratados por medio de datos boolenaos 
    sql = '''
            ALTER TABLE candidates
            ADD COLUMN hired boolean;
          '''
    cursor.execute(sql)
    conn.commit()
    print('¡Columna hired creada')


#Condición para que un candidato sea contratado y actualización de la columna hired
    sql = '''
            UPDATE candidates SET hired = (code_challenge_score >= 7) AND (technical_interview_score >= 7); 
          '''
    cursor.execute(sql)
    conn.commit()
    print('¡Columna hired creada')


except Exception as ex:
    print(ex)
    
finally:
    conn.close()
    print('conexion finalizada!')