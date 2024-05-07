args = 20
contador = 0
palavra = 'Arthur'

while ((args > 0) or (contador < 20)):
    contador += 1
    args -= 1

if contador == 5:
    print(palavra)
    contador = 27

if contador == 3:
    print('Python')
    palavra = 'Python'