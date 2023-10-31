import GPB
import unittest
import data_process

import unittest

class TestNotebook(unittest.TestCase):
    
    def good_test_address(self):
        address = ['CRA', '70', '#', '26A', '-', '33']
        self.assertEqual(data_process.alternate_address(address)[0], 'Carrera 70 # 26A 33')

    def good_test_address2(self):
        address = ['CRA', '70', '#', '26A', '-', '33']
        self.assertEqual(data_process.alternate_address(address)[1], 'Carrera 70 Nro 26A - 33')

    def good_test_address2(self):
        address = ['CRA', '70', '#', '26A', '-', '33']
        self.assertEqual(data_process.alternate_address(address)[2], 'Carrera 70 Numero 26A - 33')    


unittest.main(argv=[''], verbosity=2, exit=False)