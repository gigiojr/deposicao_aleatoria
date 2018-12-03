import random
import math
import time
import logging
import numpy as np
from datetime import datetime
import threading

class ThreadPool(object):
    def __init__(self):
        super(ThreadPool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('Running: %s', self.active)
    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug('Running: %s', self.active)

class Depositor(threading.Thread):
    def __init__(self, l, t, i, s, pool):
        threading.Thread.__init__(self, name="Experimento %s Amostra %s" %(str(l), str(i)))
        self.name = "Experimento %s Amostra %s" %(str(l), str(i))
        self.s = s
        self.pool = pool
        self.l = l
        self.t = t

    def busca_lateral(self, vtr, idx):
        l = len(vtr)
        idx_left = (idx+l-1)%l
        idx_right = (idx+1)%l
        idx_choose = idx_right if vtr[idx_right] < vtr[idx_left] else idx_left
        return idx_choose if idx_choose < idx else idx

        # if idx == (len(vtr)-1):
        #     #avaliar apenas esquerda
        #     if vtr[idx] > vtr[idx-1]:
        #         return idx - 1
        #         # return self.busca_lateral(vtr, idx-1)
        #     elif vtr[idx] > vtr[0]:
        #         return 0
        #         # return self.busca_lateral(vtr, 0)
        #     else:
        #         return idx
        # elif idx == 0:
        #     #avaliar apenas direita
        #     if vtr[idx] > vtr[idx+1]:
        #         #return self.busca_lateral(vtr, idx+1)
        #         return idx + 1
        #     elif vtr[idx] > vtr[len(vtr) - 1]:
        #         # return self.busca_lateral(vtr, len(vtr) - 1)
        #         return len(vtr) - 1
        #     else:
        #         return idx
        # else:
        #     #avaliar os dois lados
        #     idx_left = idx-1
        #     idx_right = idx+1
        #     if vtr[idx_right] < vtr[idx_left]:
        #         #testar o atual com a direita
        #         idx_choose = idx_right
        #     elif vtr[idx_left] < vtr[idx_right]:
        #         #testar o atual com a esquerda
        #         idx_choose = idx_left
        #     else:
        #         idx_choose = idx_right if random.randint(0, 1) else idx_left

        #     if vtr[idx_choose] < vtr[idx]:
        #         # return self.busca_lateral(vtr, idx_choose)
        #         return idx_choose
        #     else:
        #         return idx

    def make_random_deposition(self, l, t):
        roughnesses = []
        vet = np.zeros(l, int)
        for i in range(t):
            for j in range(l):
                random_value = random.randint(0, l - 1)
                vet[random_value] += 1
            roughnesses.append(self.calcula_rugosidade(vet, l))
            print("%s rodando t=%s"%(self.name, i))
        return roughnesses

    def make_desposition_relaxation(self, l, t):
        self.roughnesses = []
        vtr = np.zeros(l, int)
        for i in range(t):
            for j in range(l):
                random_index = random.randint(0, l - 1)
                idx = self.busca_lateral(vtr, random_index)
                vtr[idx] += 1
            roughness = self.calcula_rugosidade(vtr, l)
            self.roughnesses.append(roughness)

    def calcula_rugosidade(self, vetor, L):
        hMedia = np.mean(vetor)
        somatorio = 0
        for i in vetor:
            somatorio += (i - hMedia) ** 2
        return np.sqrt(somatorio / L)

    def run(self):
        with self.s:
            print("Iniciando %s"%(self.name))
            self.pool.makeActive(self.name)
            a = datetime.now()
            self.make_desposition_relaxation(self.l, self.t)
            #self.make_random_deposition(self.l, self.t)
            b = datetime.now()
            print("Finalizando %s em %s"%(self.name,str(b-a)))
            self.pool.makeInactive(self.name)

class Executor:
    def __init__(self, l, t, N):
        self.l = l
        self.t = t
        self.N = N

    def get_mean_experiment(self):
        pool = ThreadPool()
        s = threading.Semaphore(100)
        experiments = {}
        for i in range(self.N):
            experiments[i] = Depositor(self.l, self.t, i, s, pool)
            experiments[i].start()

        while True:
            all_finish = True
            for i in experiments.values():
                if i.is_alive():
                    all_finish = False
            if all_finish:
                break
            time.sleep(60)

        mtx = [e.roughnesses for e in experiments.values()]
        mtx = np.array(mtx)
        self.mean = [np.mean(mtx[:,i]) for i in range(mtx.shape[1])]
        self.save_file(self.mean, self.l)
        return True

    def save_file(self, data, l):
        with open("data_RD_T2_"+str(l)+".txt", 'w+') as fp:
            fp.write(";".join(map(str, data)))
            fp.close()