from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import sqlite3
import re


def run_app():
    app.run(debug=True, host='0.0.0.0')


# Funções de sanitização:

def sanitize_string(value):
    return re.sub(r'[^a-zA-Z0-9\s]', '', value).strip()

def sanitize_query_params(query_params):
    sanitized_params = {}
    for key, value in query_params.items():
        sanitized_value = sanitize_string(value)
        sanitized_params[key] = sanitized_value
    return sanitized_params

# app flask com senha e objeto JWTManager:

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'Senha123@'
jwt = JWTManager(app)

# Banco de dados:

database = 'backend_test'

# Endpoint de autenticação:

@app.route('/auth', methods=['POST'])
def auth():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return (jsonify({'msg': 'Um nome de usuário válido é necessário.'}), 400)
    if not password:
        return (jsonify({'msg': 'Uma senha é necessária.'}), 400)
    
    if username == 'admin' and password == 'Senha123@':
        access_token = create_access_token(identity=username)
        return (jsonify({'access_token': access_token}), 200)
    
    return (jsonify({'msg': 'Usuário e/ou senha inválido(s)'}), 401)


# Endpoint -> clientes:

@app.route('/patients', methods=['GET'])
@jwt_required()
def get_patients():
        try:
            conn = sqlite3.connect('backend_test.db')
            cur = conn.cursor()

            query_params = sanitize_query_params(request.args.to_dict())
            where_clause = ""

            # Filtros por nome e sobrenome

            if 'nome' in query_params:
                nome = query_params['nome']
                where_clause += f"WHERE FIRST_NAME OR LAST_NAME LIKE '%{nome}%'"

            cur.execute (f"SELECT UUID,FIRST_NAME,LAST_NAME,DATE_OF_BIRTH FROM PATIENTS {where_clause}")
            
            rows = cur.fetchall()
            patients = []
            
            for row in rows:
                patient = {
                     'id':row[0],
                     'primeiro_nome':row[1],
                     'sobrenome': row[2],
                     'data_de_nascimento': row[3]
                }
                patients.append(patient)
            return (jsonify(patients), 200)
        except sqlite3.Error as err:
            return jsonify({'msg': 'Ocorreu um erro ao buscar o(s) paciente.'}), 500
        finally:
            cur.close()
            conn.close()

# Endpoint -> farmácias:

@app.route('/pharmacies', methods=['GET'])
@jwt_required()
def get_pharmacies():
        try:
            conn = sqlite3.connect('backend_test.db')
            cur = conn.cursor()

            query_params = sanitize_query_params(request.args.to_dict())
            where_clause = ""

             # Filtros por nome ou cidade

            if 'nome' in query_params:
                nome = query_params['nome']
                where_clause += f"WHERE NAME LIKE '%{nome}%'"
            
            if 'cidade' in query_params:
                nome = query_params['cidade']
                where_clause += f"WHERE CITY LIKE '%{nome}%'"

            cur.execute (f"SELECT UUID,NAME,CITY FROM PHARMACIES {where_clause}")

            rows = cur.fetchall()
            pharmacies = []

            for row in rows:
                pharmacie = {
                     'id':row[0],
                     'nome':row[1],
                     'cidade': row[2]
                }
                pharmacies.append(pharmacie)
            return (jsonify(pharmacies), 200)
        except sqlite3.Error as err:
            return (jsonify({'msg': 'Ocorreu um erro ao buscar a(s) farmácia(s).'}), 500)
        finally:
            cur.close()
            conn.close()

# Endpoint -> transações:

@app.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    try:
        conn = sqlite3.connect('backend_test.db')
        cur = conn.cursor()

        query_params = request.args.to_dict()
        where_clause = ""

        # Filtros por nome ou sobrenome do paciente e nome da farmácia
        if 'nome' in query_params:
            nome = query_params['nome']
            where_clause += f"WHERE patients.FIRST_NAME LIKE '%{nome}%' OR patients.LAST_NAME LIKE '%{nome}%'"

        if 'farmacia' in query_params:
            farmacia = query_params['farmacia']
            where_clause += f"WHERE pharmacies.NAME LIKE '%{farmacia}%'"

        cur.execute("""
            SELECT transactions.PATIENT_UUID, patients.FIRST_NAME, patients.LAST_NAME, patients.DATE_OF_BIRTH,
                   transactions.PHARMACY_UUID, pharmacies.NAME, pharmacies.CITY, transactions.UUID,
                   transactions.AMOUNT, transactions.TIMESTAMP
            FROM transactions
            JOIN pharmacies ON pharmacies.UUID = transactions.PHARMACY_UUID
            JOIN patients ON patients.UUID = transactions.PATIENT_UUID
            """ + where_clause)

        rows = cur.fetchall()
        transactions = []
        for row in rows:
            transaction = {
                'id_paciente': row[0],
                'nome_paciente': row[1],
                'sobrenome_paciente': row[2],
                'data_nascimento_paciente': row[3],
                'id_farmácia': row[4],
                'nome_farmácia': row[5],
                'cidade_farmácia': row[6],
                'id_transação': row[7],
                'quantidade_transação': row[8],
                'data_transação': row[9]
            }
            transactions.append(transaction)
        return jsonify(transactions), 200
    except sqlite3.Error as err:
        return jsonify({'msg': 'Ocorreu um erro ao buscar as transações.'}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    run_app()



