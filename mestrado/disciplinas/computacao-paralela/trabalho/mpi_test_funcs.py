import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def scatter_data(X):
    # print("%d of %d" % (comm.Get_rank(), comm.Get_size()))
    a_size = len(X)
    recvdata = np.empty(a_size, dtype=np.int64)
    senddata = None

    if rank == 0:
        senddata = X

    comm.Scatter(senddata, recvdata, root=0)
    recvdata = recvdata * 2

    data_processed = gather_data(senddata, recvdata)

    return data_processed


def gather_data(senddata, recvdata):
    comm.Gather(recvdata, senddata, root=0)
    if rank == 0 and senddata is not None:
        return senddata
