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
    integer const maxSize = 1e6;
    integer const toMKS = 1e6;
    integer const toMB  = 1024 * 1024;

    integer rank;    
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    integer const destination = 1u;
    integer const tag = 77u;

    integer const step = 100;
    for(unsigned int I = 0u; I <= maxSize / step; ++I)
    {
        integer const messageWeight = sizeof(byte) * I * step;
        byte *buffer = (byte*)malloc(messageWeight);
     
        scalar timeTransfer = MPI_Wtime();   
        if(rank == master)
        { 
            MPI_Bsend(&buffer[0u], messageWeight, MPI_CHAR, destination, tag, MPI_COMM_WORLD);
            MPI_Recv(&buffer[0u], messageWeight, MPI_CHAR, destination, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
        else
        {
            MPI_Recv(&buffer[0u], messageWeight, MPI_CHAR, master, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            MPI_Bsend(&buffer[0u], messageWeight, MPI_CHAR, master, tag, MPI_COMM_WORLD);
        }
        timeTransfer = MPI_Wtime() - timeTransfer;

        if (rank == master)
        {
            std::cout << timeTransfer * toMKS                        << "," 
                      << scalar(messageWeight) / toMB / timeTransfer << ","
                      << scalar(messageWeight) << "\n";         
        }
        else
        {
            std::cout << timeTransfer * toMKS                        << "," 
                      << scalar(messageWeight) / toMB / timeTransfer << ","
                      << scalar(messageWeight) << "\n";          
        } 

        free(buffer);  
    }

    MPI_Finalize();
    return 0;
}
