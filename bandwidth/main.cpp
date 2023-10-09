#include <fstream>
#include <string>
#include <stdlib.h>
#include <mpi.h>

#define master 0

typedef double scalar;
typedef int    integer;
typedef char   byte;

int main(int argc, char **argv)
{
    integer const step = 100;
    integer const maxSize = 1e6 / step;
    integer const toMKS = 1e6;
    integer const toMB  = 1024 * 1024;

    integer rank;    
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    integer const destination = 1u;
    integer const tag = 77u;

    for(unsigned int I = 0u; I < maxSize; ++I)
    {
        scalar messageWeight = sizeof(byte) * ((I + 1u) * step);

        byte *buffer = (byte*)malloc(sizeof(byte) * I);
     
        scalar timeTransfer = MPI_Wtime();   
        if(rank == master)
        { 
            MPI_Send(&buffer[0u], I, MPI_CHAR, destination, tag, MPI_COMM_WORLD);
            MPI_Recv(&buffer[0u], I, MPI_CHAR, destination, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
        else
        {
            MPI_Recv(&buffer[0u], I, MPI_CHAR, master, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            MPI_Send(&buffer[0u], I, MPI_CHAR, master, tag, MPI_COMM_WORLD);
        }
        timeTransfer = MPI_Wtime() - timeTransfer;

        free(buffer);
    
        if (rank == master)
        {
            std::cout << timeTransfer * toMKS                << "," 
                      << messageWeight / toMB / timeTransfer << ","
                      << messageWeight << "\n";         
        }
        else
        {
            std::cout << timeTransfer * toMKS                << "," 
                      << messageWeight / toMB / timeTransfer << ","
                      << messageWeight << "\n";          
        }   
    }

    MPI_Finalize();
    return 0;
}
