import unittest
from parrucchieria_prova.Model.parrucchiere import parrucchiere  # Importa la classe Parrucchiere dal tuo modulo

class TestParrucchiere(unittest.TestCase):

    def test_to_dict(self):
        # Creare un'istanza di Parrucchiere per il test
        parrucchier = parrucchiere('john_doe', 'password123')

        # Chiamare il metodo to_dict() e ottenere il risultato
        result = parrucchier.to_dict()

        # Definire il risultato atteso
        expected = {
            'username': 'john_doe',
            'password': 'password123',
            'user_type': 'Parrucchiere'
        }

        # Assert che il risultato sia uguale al risultato atteso
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()