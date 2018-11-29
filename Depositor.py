import random
import math
import numpy as np
from datetime import datetime
from threading import Thread


class Depositor(Thread):
    def __init__(self):
        self.l = [200, 400, 800, 1600]
        self.t = 10 ** 6

    def save_file(self, data, l):
        with open("data_"+str(l)+".txt", 'w+') as fp:
            for row in data:
                str_data = map(str, row)
                fp.write(";".join(str_data))
            fp.close()

    def busca_lateral(self, vtr, idx):
        if idx == (len(vtr)-1):
            #avaliar apenas esquerda
            if vtr[idx] > vtr[idx-1]:
                return idx - 1
                # return self.busca_lateral(vtr, idx-1)
            elif vtr[idx] > vtr[0]:
                return 0
                # return self.busca_lateral(vtr, 0)
            else:
                return idx
        elif idx == 0:
            #avaliar apenas direita
            if vtr[idx] > vtr[idx+1]:
                #return self.busca_lateral(vtr, idx+1)
                return idx + 1
            elif vtr[idx] > vtr[len(vtr) - 1]:
                # return self.busca_lateral(vtr, len(vtr) - 1)
                return len(vtr) - 1
            else:
                return idx
        else:
            #avaliar os dois lados
            idx_left = idx-1
            idx_right = idx+1
            if vtr[idx_right] < vtr[idx_left]:
                #testar o atual com a direita
                idx_choose = idx_right
            elif vtr[idx_left] < vtr[idx_right]:
                #testar o atual com a esquerda
                idx_choose = idx_left
            else:
                idx_choose = idx_right if random.randint(0, 1) else idx_left

            if vtr[idx_choose] < vtr[idx]:
                # return self.busca_lateral(vtr, idx_choose)
                return idx_choose
            else:
                return idx

    def make_random_deposition(self, l, t):
        """ Make Random Deposition - Deposição Aleatória
        "
        " Keyword arguments:
        "
        " max_height -- Altura máxima
        " l          -- Locais para deposição
        " t          -- Count of number times step
        """
        w = []
        vet = np.zeros(l, int)
        for i in range(t):
            for j in range(l):
                random_value = random.randint(0, l - 1)
                vet[random_value] += 1
            w.append(self.calcula_rugosidade(vet, l))
        return w

    def make_desposition_relaxation(self, l, t):
        """ Make Random Deposition surface relaxation - Deposição Aleatória com Relaxamento Superficial
        "
        " Keyword arguments:
        "
        " max_height -- Altura máxima
        " l          -- Locais para deposição
        " t          -- Count of number times step
        """

        # data = []
        wMatriz = []
        for amostras in range(100):
            w = []
            vtr = np.zeros(l, int)
            for i in range(t):
                for j in range(l):
                    random_index = random.randint(0, l - 1)
                    idx = self.busca_lateral(vtr, random_index)
                    vtr[idx] += 1
                wlocal = self.calcula_rugosidade(vtr, l)
                w.append(wlocal)

            wMatriz.append(w)

        wMedia = []
        for i in range(t):
            soma = 0
            for w in wMatriz:
                soma += w[i]
            wMedia.append(soma / len(wMatriz))

        return wMedia

    def calcula_rugosidade(self, vetor, L):
        hMedia = np.mean(vetor)
        somatorio = 0
        for i in vetor:
            somatorio += (i - hMedia) ** 2
        return np.sqrt(somatorio / L)

    def run(self):
        a = datetime.now()
        self.vet_rd_200 = self.make_random_deposition_vet(200, 10 ** 6)
        self.vet_rdsr_200 = self.make_DARS_vet(200, 10 ** 6)
        self.vet_rd_400 = self.make_random_deposition_vet(400, 10 ** 6)
        self.vet_rdsr_400 = self.make_DARS_vet(400, 10 ** 6)
        self.vet_rd_800 = self.make_random_deposition_vet(800, 10 ** 6)
        self.vet_rdsr_800 = self.make_DARS_vet(800, 10 ** 6)
        self.vet_rd_1600 = self.make_random_deposition_vet(1600, 10 ** 6)
        self.vet_rdsr_1600 = self.make_DARS_vet(1600, 10 ** 6)
        b = datetime.now()
        print(b-a)
        print(self.vet_rd_200)
        print(self.vet_rdsr_200)
        print(self.vet_rd_400)
        print(self.vet_rdsr_400)
        print(self.vet_rd_800)
        print(self.vet_rdsr_800)
        print(self.vet_rd_1600)
        print(self.vet_rdsr_1600)
