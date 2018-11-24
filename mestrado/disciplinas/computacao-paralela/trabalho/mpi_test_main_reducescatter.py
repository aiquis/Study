import numpy as np
from mpi4py import MPI


# Testando operações com dataset splitado
# np.sum = 27. Soma da 1a linha = 6 e da 2a = 15
X = np.array([[1, 2, 3], [4, 5, 6], [1, 1, 1], [1, 2, 3], [4, 5, 6], [1, 1, 1]])

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
print("%d of %d" % (comm.Get_rank(), comm.Get_size()))

a_size = 3
recvdata = np.zeros(size, dtype=np.int)
senddata = X
print('on task: ', rank, 'senddata = ', senddata)
# comm.Reduce_scatter_block(senddata, recvdata, op=MPI.SUM)
# print('on task: ', rank, 'recvdata = ', recvdata)