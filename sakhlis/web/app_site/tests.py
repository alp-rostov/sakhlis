from utils import *


assert set_coordinates_address('Руставели', 'Тбилиси'), 'Тест не пройден1'
assert set_coordinates_address('', 'Тбилиси'), 'Тест не пройден2'
assert set_coordinates_address(222, 222), 'Тест не пройден5'

assert set_coordinates_address(['Руставели'], 'Тбилиси'), 'Тест не пройден3'
assert set_coordinates_address('Руставели', {'Тбилиси'}), 'Тест не пройден4'