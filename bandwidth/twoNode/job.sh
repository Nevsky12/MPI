#!/bin/bash


#PBS -l walltime=00:05:00,nodes=2:ppn=2
#PBS -N bandwidth
#PBS -q batch


cd $(PBS_O_WORKDIR)/home/mpi202316/MPI/tasks/bandwidth/twoNode
export OMP_NUM_THREAD=$PBS_NUM_PPN
mpirun --hostfile $PBS_NODEFILE -np 4 ./main
