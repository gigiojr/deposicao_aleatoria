from Depositor import Depositor, Executor
import matplotlib.pyplot as plt
import numpy as np
import time
import gc

def main():
    # l = [200, 400, 800, 1600]
    for i in range(10):  
        e = Executor(800, 10**6, 10)
        e.get_mean_experiment(i)
        gc.collect()
    # threads = [Depositor(i) for i in l]
    # [thread.start() for thread in threads]
    #mtx_deposition = [a.make_random_deposition( l, a.t) for l in a.l]
    # a.repeat_experiment( 100, a.l[0], a.t)
    # plt.figure(0)
    # plt.loglog(range(len(a.mean)), a.mean)
    # plt.figure(1)
    # plt.loglog(range(len(a.wMedia)), a.wMedia)
    # plt.figure(1)
    # plt.plot(range(len(mtx_deposition)), mtx_deposition)
    # plt.show()


if __name__ == '__main__':
    main()