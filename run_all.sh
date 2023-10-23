#!/bin/bash
N="1e5"
alg="single,cluster"
./sigmaModel -cool 4,0,10 -c "$N" -alg "$alg" 
./sigmaModel -cool 4,0,20 -c "$N" -alg "$alg" 
./sigmaModel -cool 4,0,30 -c "$N" -alg "$alg" 
./sigmaModel -cool 4,0,40 -c "$N" -alg "$alg" 
