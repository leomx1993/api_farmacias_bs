import unittest
import json
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from flask.testing import FlaskClient
from projeto_teste_bluestorm import app


class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.access_token = None

        response = cls.app.post('/auth', json={'username': 'admin', 'password': 'Senha123@'})
        data = json.loads(response.data.decode('utf-8'))

        cls.access_token = data.get('access_token')

    # Pacientes:    

    def test_get_patients(self):
        self.assertIsNotNone(self.access_token)

        response = self.app.get('/patients', headers={'Authorization': 'Bearer ' + self.access_token})
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        # Verificação: Se cada item da lista possui as chaves esperadas
        expected_keys = ['id', 'primeiro_nome', 'sobrenome', 'data_de_nascimento']
        
        for patient in data:
            self.assertTrue(all(key in patient for key in expected_keys))

        # id -> string
        for patient in data:
            self.assertIsInstance(patient['id'], str)

    # Farmácias:    

    def test_get_pharamacies(self):
        self.assertIsNotNone(self.access_token)

        response = self.app.get('/pharmacies', headers={'Authorization': 'Bearer ' + self.access_token})
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        # Chaves esperadas
        expected_keys = ['id', 'nome', 'cidade']
        
        for patient in data:
            self.assertTrue(all(key in patient for key in expected_keys))

        # id -> string
        for patient in data:
            self.assertIsInstance(patient['id'], str)
    
    # Farmácias:    

    def test_get_transactions(self):
        self.assertIsNotNone(self.access_token)

        response = self.app.get('/transactions', headers={'Authorization': 'Bearer ' + self.access_token})
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        # Chaves esperadas
        expected_keys = [
            'id_paciente',
            'nome_paciente',
            'sobrenome_paciente',
            'data_nascimento_paciente',
            'id_farmácia',
            'nome_farmácia',
            'cidade_farmácia',
            'id_transação',
            'quantidade_transação',
            'data_transação'
        ]

        for transaction in data:
            self.assertTrue(all(key in transaction for key in expected_keys))

        # id_paciente', 'id_farmácia' e 'id_transação' -> strings
        for transaction in data:
            self.assertIsInstance(transaction['id_paciente'], str)
            self.assertIsInstance(transaction['id_farmácia'], str)
            self.assertIsInstance(transaction['id_transação'], str)
        
        # 'quantidade_transação' -> numéricos
        
        for transaction in data:
            self.assertIsInstance(transaction['quantidade_transação'], (int, float))


if __name__ == '__main__':
    unittest.main()