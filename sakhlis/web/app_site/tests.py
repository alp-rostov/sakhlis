# from utils import *
#
#
# assert set_coordinates_address('Руставели', 'Тбилиси'), 'Тест не пройден1'
# assert set_coordinates_address('', 'Тбилиси'), 'Тест не пройден2'
# assert set_coordinates_address(222, 222), 'Тест не пройден5'
#
# assert set_coordinates_address(['Руставели'], 'Тбилиси'), 'Тест не пройден3'
# assert set_coordinates_address('Руставели', {'Тбилиси'}), 'Тест не пройден4'
import itertools
from pprint import pprint



def grouper(iterable, n):
    args = [iter(iterable)]*n
    print(*args)
    return itertools.zip_longest(*args)

print(next(grouper((1,'cndf',3), 5)))
print(next(grouper((1,'cndf',3), 4)))