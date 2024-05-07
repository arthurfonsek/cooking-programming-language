numero = input("Digite um número inteiro:  \n")

numero = int(numero)

if numero/2 == 0:
    print("O número é divisível por 2")
else:
    print("O número é ímpar")


while numero > 0:
    print(numero)
    numero -= 1