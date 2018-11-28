import random
import matplotlib.pyplot as plt
import numpy as np


def buscaLateralVetor(lado, pos, vet, block):
    if lado:  # direita
        if pos < len(vet) - 1:
            if vet[pos] > vet[pos + 1]:
                pos += 1
            elif block:
                pos = buscaLateral(0, pos, vet, 0)
        else:
            if vet[pos] > vet[0]:
                pos = 0
            elif block:
                pos = buscaLateral(0, pos, vet, 0)
    else:  # esquerda
        if pos > 0:
            if vet[pos] > vet[pos - 1]:
                pos -= 1
            elif block:
                pos = buscaLateral(1, pos, vet, 0)
        else:
            if vet[pos] > vet[len(vet) - 1]:
                pos = len(vet) - 1
            elif block:
                pos = buscaLateral(1, pos, vet, 0)

    return pos


def buscaLateral(lado, pos, linha, block):
    if lado:  # direita
        if pos < len(linha) - 1:
            if linha[pos + 1] == 0:
                pos += 1
            elif pos+1 < len(linha) - 1:
                if linha[pos + 2] == 0:
                    pos += 2
                else:
                    if block:
                        pos = buscaLateral(0, pos, linha, 0)
            else:
                if block:
                    pos = buscaLateral(0, pos, linha, 0)
        else:
            if block:
                pos = buscaLateral(0, pos, linha, 0)
    else:  # esquerda
        if pos > 0:
            if linha[pos - 1] == 0:
                pos -= 1
            elif pos-1 > 0:
                if linha[pos - 2] == 0:
                    pos -= 2
                else:
                    if block:
                        pos = buscaLateral(1, pos, linha, 0)
            else:
                if block:
                    pos = buscaLateral(1, pos, linha, 0)
        else:
            if block:
                pos = buscaLateral(1, pos, linha, 0)
    return pos


def makeDA(maxAlt, l, t):  # Deposição Aleatória
    vet = np.zeros((maxAlt, l), int)
    for i in range(t):
        valRnd = random.randint(0, l - 1)
        for j in range(maxAlt):
            if vet[j][valRnd] == 0:
                vet[j][valRnd] = 1
                break
    return vet


# Deposição Aleatória com Relaxamento Superficial
def makeDARS(maxAlt, l, t):
    vet = np.zeros((maxAlt, l), int)
    for i in range(t):
        valRnd = random.randint(0, l - 1)
        for j in range(maxAlt):
            if vet[j][valRnd] == 0:
                vet[j][valRnd] = 1
                break
            else:
                lado = random.randint(0, 1)
                pos = buscaLateral(lado, valRnd, vet[j][:], 1)
                if pos != valRnd:
                    vet[j][pos] = 1
                    break
    return vet


vetDA = makeDA(200, 200, 10 ** 4)
vetDARS = makeDARS(200, 200, 10 ** 4)

plt.figure(0)
plt.imshow(vetDA, origin='lower')
plt.figure(1)
plt.imshow(vetDARS, origin='lower')
plt.show()
