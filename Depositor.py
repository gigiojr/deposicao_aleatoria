import random
import math
import time
import logging
import numpy as np
import gc
import os
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

    def save_file(self, data, name):
        with open("data_"+name+".txt", 'w+') as fp:
            fp.write(";".join(map(str, data)))
            fp.close()

    def busca_lateral(self, vtr, idx):
        l = len(vtr)
        idx_left = (idx+l-1)%l
        idx_right = (idx+1)%l
        idx_choose = idx_right if vtr[idx_right] < vtr[idx_left] else idx_left
        return idx_choose if vtr[idx_choose] < vtr[idx] else idx
        # if vtr[idx_right] < vtr[idx_left]:
        #     #testar o atual com a direita
        #     idx_choose = idx_right
        # elif vtr[idx_left] < vtr[idx_right]:
        #     #testar o atual com a esquerda
        #     idx_choose = idx_left
        # else:
        #     idx_choose = idx_right if random.randint(0, 1) else idx_left
        # if vtr[idx_choose] < vtr[idx]:
        #     # return self.busca_lateral(vtr, idx_choose)
        #     return idx_choose
        # else:
        #     return idx


    def make_random_deposition(self, l, t):
        mtx = []
        vet = np.zeros(l, int)
        vet_1 = np.zeros(l, int)+1
        for i in range(t):
            random_value = np.random.randint(l, size=l)
            np.add.at(vet,random_value,vet_1)
            mtx.append(vet)
        del vet
        del vet_1
        roughnesses=[self.calcula_rugosidade(vet, l) for vet in mtx]
        del mtx
        gc.collect()
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
            print("%s passo %s"%(self.name,i))
            self.roughnesses.append(roughness)

    def calcula_rugosidade(self, vtr, L):
        vtr = np.array(vtr)
        mean = np.mean(vtr)
        vtr = (vtr-mean)**2
        return np.sqrt(vtr / L)

    def run(self):
        with self.s:
            print("Iniciando %s"%(self.name))
            self.pool.makeActive(self.name)
            a = datetime.now()
            self.make_desposition_relaxation(self.l, self.t)
            #self.roughnesses = self.make_random_deposition(self.l, self.t)
            # gc.collect()
            # self.save_file(self.roughnesses, self.name)
            gc.collect()
            b = datetime.now()
            print("Finalizando %s em %s"%(self.name,str(b-a)))
            self.pool.makeInactive(self.name)

class Executor:
    def __init__(self, l, t, N):
        self.l = l
        self.t = t
        self.N = N

    def get_mean_experiment(self, process_part=0):
        pool = ThreadPool()
        s = threading.Semaphore(100)
        experiments = {}
        for i in range(self.N):
            experiments[i] = Depositor(self.l, self.t, i, s, pool)
            experiments[i].start()
        gc.collect()
        for e in experiments.values():
            e.join()
        gc.collect()
        print("Pegando a matriz")
        mtx = [e.roughnesses for e in experiments.values()]
        print("Transformando a matriz")
        mtx = np.array(mtx)
        print("Média da matriz")
        self.mean = [np.mean(mtx[:,i]) for i in range(mtx.shape[1])]
        print("Salvando arquivo final")
        self.save_file(self.mean, self.l, process_part)
        return True

    def save_file(self, data, l, process_part):
        name = "data%sdata_RDSR_%s_%s.txt"%(os.sep, str(l), str(process_part))
        with open(name, 'w+') as fp:
            fp.write(";".join(map(str, data)))
            fp.close()