def somme(a, b):
    resultat = a + b
    return resultat

def my_min(a, b):
    return a - b

# TEST
if somme(5, 6) == 11:
    print('PASS')
else:
    print('FAIL')

if somme(2, 6) == 8:
    print('PASS')
else:
    print('FAIL')


def test_somme():
    assert somme(5, 6) == 12
    assert somme(-5, 5) == 0
    assert somme(0, 8) == 8

def test_somme_aaa():
    a = 5
    b = 7
    result = somme(a, b)
    assert result == 12

def test_my_min():
    assert my_min(8, 5) == 3
    assert my_min(8, 8) == 0
    assert my_min(10, 8) == 2
