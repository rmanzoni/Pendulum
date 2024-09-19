# Pendulum
ETH Praktikum example experiment  
manual https://ap.phys.ethz.ch/Anleitungen/Bilingual/Manual_v09Sept2024.pdf  
solution draft https://www.overleaf.com/project/66e11f87b49acdf3177e12a0  
Software requirements: [pandas]([url](https://pandas.pydata.org)), [uproot]([url](https://uproot.readthedocs.io/en/latest/index.html#how-to-install))  


## Convert PhyPhox data into ROOT

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


## Compute period of oscillation (simple counting)

For example, you can use the plot you produced earlier and count how many _maxima_ occur in a given time window.
To do this, enable "View -> Event Statusbar", then hover your pointer on the figure, as in the screenshots below

<img width="1512" alt="Screenshot 2024-09-19 alle 15 31 45" src="https://github.com/user-attachments/assets/b440d942-06cb-488a-8710-3849553a14dc">
<img width="1512" alt="Screenshot 2024-09-19 alle 15 31 25" src="https://github.com/user-attachments/assets/b0b54ad7-4c2e-4933-97ca-5ccfe3ecdefc">

the first maximum sits at $t_{0} = 4.3 \pm 0.1 s$, the second maximum at $t_{1}= 19.8 \pm 0.1 s$, total $\Delta t = 15.5 \pm 1.14 s$ and 13 periods in this time span, thus the period is $T = 15.5 \pm 0.14s/13 = 1.2 \pm 0.01 s$

**Q: estimate the uncertainty associating to reading the time off the graph**
Notice that the PhyPhox readings are discrete and relatively far in between. Thus, it's not easy to identify the maximum by eye.
Moving the pointer between to region that can be equally well considered as the local maximum gives a time difference of about $0.1s$

**Q: how many digits are appropriate?**
Given the estimated uncertainty, 1 digit is enough.

**Q: how can improve the _precision_ of this measurement?**  
Since the uncertainty on the time determination is constant, assume for example $0.1 s$, integrating over a longer period and thus more maxima, would reduce the impact of the uncertainty.

**Q: how much would precision improve if twice as many maxima are considered?**  

**Q: what is the difference between _precision_ and _accuracy_?**  
To guide the intuition, you could in principle integrate over a very large number of periods and improve precision indefinitely.
However, if your cronometer is, for example, systematically slow, such that when it displays $1s$ in fact $1.01s$ have elapsed, the accuracy would be limited to 1%

**Pro tip**  
The Taylor expansion of a cosine curve is a parabola. To better find the local maximum, can fit in the data with a parabola in the proximity of the maximum and read off the value returned by the fit (use sight click -> Fit Panel in ROOT)

<img width="1512" alt="Screenshot 2024-09-19 alle 16 03 57" src="https://github.com/user-attachments/assets/893774af-6fd3-4f5d-8849-503c204db37f">

## Verify that the period of oscillation does not depend on the mass
Need data.

**Q: discuss compatibility between measurements**
The central values will not be exactly the same, but will come with an uncertainty.  
Discuss compatibility between pairwise measurements (combine total uncertainty, anything correlated or simple sum in quadrature?)  

**Pro tip**
Put all measurements in a $T$ vs $m$ graph and also display the uncertainty on $T$.  
Run a $\chi^2$ fit with a flat function (constant), and compute the $p$-value corresponding to the normalized $\chi^2$.  

## Calculate $g$ and its associated error

Need $T$, $L$ and their uncertainties. Apply gaussian propagation

## plot $T^2$ vs $L$

## Compatibility between measured $g$ and $g_{Hoengg}$
Similar to before. Use the result of the chi2 fit with flat function.

## compute friction coefficient $\gamma$
Either single out maxima / minima and fit with an expo, or fit all points with the full PDF for dampen oscillations

For example, use `fitter.py` provided in this repo

<img width="1512" alt="Screenshot 2024-09-19 alle 17 11 39" src="https://github.com/user-attachments/assets/64cd8f12-ae0d-46ef-864d-cd3f1925d796">

```
****************************************
Minimizer is Minuit / Migrad
Chi2                      =      2.11946
NDf                       =          152
Edm                       =  1.37505e-06
NCalls                    =          205
A                         =     0.784725   +/-   0.0152518
gamma                     =    -0.115164   +/-   0.00248665
omega                     =      5.26108   +/-   0.00131206
alpha                     =     0.713192   +/-   0.0205958
```

