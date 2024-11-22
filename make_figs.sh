#!/usr/bin/bash
python3 sphere.py
python3 discont.py
python3 plot_lattice.py
python3 plot_cooling.py -alg all -o charge
python3 autocorrelation_time.py -alg all
python3 autocorrelation_time.py -alg all -o charge
python3 autocorrelation_time.py -alg all -o magnetization
python3 plot_correlation_length.py -alg all