import numpy as np
from mpi4py import MPI


# Testando operações com dataset splitado
# np.sum = 27. Soma da 1a linha = 6 e da 2a = 15
X = np.array([[1, 2, 3], [4, 5, 6], [1, 1, 1], [1, 2, 3], [4, 5, 6], [1, 1, 1]])
newdata = []
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

print("%d of %d" % (comm.Get_rank(), comm.Get_size()))
a_size = len(X)
recvdata = np.empty(a_size, dtype=np.int64)
senddata = None
if rank == 0:
    senddata = X
    print('We will be scattering: ', senddata)
else:
    senddata = None

comm.Scatter(senddata, recvdata, root=0)
recvdata = np.sum(recvdata)
print('on task', rank, 'after Scatter: data = ', recvdata)

comm.Gather(recvdata, senddata, root=0)

if senddata is not None:
    newdata = np.sum(senddata)
    print(newdata)
