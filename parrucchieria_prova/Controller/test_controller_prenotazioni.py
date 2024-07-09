import unittest
from unittest import TestCase

from controller_prenotazioni import controller_prenotazioni
from parrucchieria_prova.Model.prenotazioni import prenotazioni


class TestControllerPrenotazioni(unittest.TestCase):
    def setUp(self):
        # Initialize a controller_prenotazioni instance with some sample bookings
        self.controller = controller_prenotazioni()
        self.controller.initialize_prenotazioni()
        self.controller.add_prenotazione(prenotazioni('alice', '2023-07-10', '10:00', 'Mario', 'Haircut'))
        self.controller.add_prenotazione(prenotazioni('bob', '2023-07-11', '11:00', 'Luigi', 'Shave'))
        self.controller.add_prenotazione(prenotazioni('alice', '2023-07-12', '12:00', 'Mario', 'Color'))

    def test_get_bookings(self):
        # Test for user 'alice'
        alice_bookings = self.controller.get_bookings('alice')
        expected_alice_bookings = [
            {'username': 'alice', 'data': '2023-07-10', 'ora': '10:00', 'parrucchiere': 'Mario', 'servizio': 'Haircut'},
            {'username': 'alice', 'data': '2023-07-12', 'ora': '12:00', 'parrucchiere': 'Mario', 'servizio': 'Color'},
        ]
        self.assertEqual(alice_bookings, expected_alice_bookings)

        # Test for user 'bob'
        bob_bookings = self.controller.get_bookings('bob')
        expected_bob_bookings = [
            {'username': 'bob', 'data': '2023-07-11', 'ora': '11:00', 'parrucchiere': 'Luigi', 'servizio': 'Shave'},
        ]
        self.assertEqual(bob_bookings, expected_bob_bookings)

        # Test for a user with no bookings
        no_bookings = self.controller.get_bookings('charlie')
        expected_no_bookings = []
        self.assertEqual(no_bookings, expected_no_bookings)


if __name__ == '__main__':
    unittest.main()

