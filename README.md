# Pendulum
ETH Praktikum example experiment  
manual https://ap.phys.ethz.ch/Anleitungen/Bilingual/Manual_v09Sept2024.pdf  
solution draft https://www.overleaf.com/project/66e11f87b49acdf3177e12a0  
Software requirements: [pandas]([url](https://pandas.pydata.org)), [uproot]([url](https://uproot.readthedocs.io/en/latest/index.html#how-to-install))  


### Convert PhyPhox data into ROOT

This creates a [ROOT]([url](https://root.cern)) TTree saved in `accelerations.root`
```
ipython -i  converter.py
```

Now open the file and inspect it interactively
```
root -l accelerations.root --web=off
```
open a `TBrowser`
```
TBrowser l
```
and plot, for example, the acceleration in the y direction `ay` as a function of time `t`  

```
tree->Draw("a_y:t", "", "LP")
```
result

<img width="1512" alt="Screenshot 2024-09-19 alle 15 26 30" src="https://github.com/user-attachments/assets/2802f188-74b0-4cb2-ad32-bc104787ea39">


