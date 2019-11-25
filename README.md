## CMU - PPLT Project Fall 2019
> Chenxiao Guan - chenxiag@andrew.cmu.edu

### Introduction
This is the program for the final project of the course Privacy Policy, Law and Technology at Carnegie Mellon University. The program collects data from different websites with different ad or tracker blockers installed. The purpose of the project is to compare different blockers performances based on the loading time changes, memory usage changes and number of trackers blocked on websites. Therefore, the script will collect these information for further data analysis. By running `measure.py`, it will collect data and one can use `Plotting.ipynb` for data visualization afterwards.

#### Currently supported blockers
1. AdBlock Plus
2. Ghostery
3. Adguard
4. Privacy Badger
5. uBlock Origin

### Dependencies
1. Python 3
2. Selenium
3. matplotlib

### Usage
```sh
$ python measure.py
```
One can change the list of websites in the urls folder. One can also change the list of blockers in `util.py`, but it is required to implement the method so that the script can get the number of trackers blocked. 
