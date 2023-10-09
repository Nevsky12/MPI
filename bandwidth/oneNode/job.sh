#!/bin/bash


#PBS -l walltime=00:10:00,nodes=1:ppn=2
#PBS -N bandwidth
#PBS -q batch


cd $(PBS_O_WORKDIR)/home/mpi202316/MPI/tasks/bandwidth/oneNode
export OMP_NUM_THREAD=$PBS_NUM_PPN
mpic++ main.cpp -o main
mpirun --hostfile $PBS_NODEFILE -np 2 ./main
