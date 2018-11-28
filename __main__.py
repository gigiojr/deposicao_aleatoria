from Depositor import Depositor
import matplotlib.pyplot as plt
import numpy as np
import time


def main():
    a = Depositor()
    mtx_deposition = [a.make_random_deposition( l, a.t) for l in a.l]
    #mtx_deposition = a.make_desposition_relaxation( a.l[0], a.t)
    # print(mtx_deposition)
    # plt.figure(0)
    # plt.loglog(range(len(mtx_deposition)), mtx_deposition)
    # plt.figure(1)
    # plt.plot(range(len(mtx_deposition)), mtx_deposition)
    # plt.show()
    #a.start()


if __name__ == '__main__':
    main()