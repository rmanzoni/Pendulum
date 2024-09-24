# Pendulum
ETH Praktikum example experiment  
manual https://ap.phys.ethz.ch/Anleitungen/Bilingual/Manual_v09Sept2024.pdf  
solution draft https://www.overleaf.com/project/66e11f87b49acdf3177e12a0  

[Scientific python quickstart](https://gist.github.com/rmanzoni/97674876b8130cc8220a2b7bf1fd8ec9)  

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
Using [data]([url](https://docs.google.com/spreadsheets/d/1I12oOLVPvXleMpLRMuvfgdFlY8O9UW1Aj1d4Rn_-vhk/edit?usp=sharing)) collected and preprocessed by Marina 

|L (cm)                    |  41     |  31     |  21.3  |   Unc. (cm)  | 0.1|
|--------------------------|---------|---------|--------|--------------|----|
|T (s) for 10 oscillations |  12.87  |  11.54  |  9.34  |   Unc. (s)   | 0.14|
|                          |  13.07  |  11.15  |  9.21  |              | 0.14|
|                          |  13.1   |  11.06  |  9.2   |              | 0.14|
|                          |  13.15  |  11.36  |  9.35  |              | 0.14|
|                          |  12.97  |  10.89  |  9.21  |              | 0.14|


compute the mean periods over 10 oscillations

```
import numpy as np

nperiods = 10

# for L=41 cm
data = np.array([12.87, 13.07, 13.1, 13.15, 12.97])
print(np.mean(data) / nperiods)
# ==> 1.3032 s

# for L=31 cm
data = np.array([11.54, 11.15, 11.06, 11.36, 10.89])
print(np.mean(data) / nperiods)
# ==> 1.12 s

# for L=21.3 cm
data = np.array([9.34, 9.21, 9.2, 9.35, 9.21])
print(np.mean(data) / nperiods)
# ==> 0.9262 s
```

and now the associated uncertainties.  

There are two components to the uncertainty. 

The first one is statistical (precision), and it is the standard error of the mean, calculated as the standard deviation divided by the square root of the number of measurements in the set, minus one

```
np.std(data) / np.sqrt(len(data)-1)

# for L=41 cm    ==> sem = 0.050 s
# for L=31 cm    ==> sem = 0.114 s
# for L=21.3 cm  ==> sem = 0.034 s
```

The second component accounts for systematic effects, for example the uncertainty associated to reading the time stamp off of the "wavy" graph shown above.
We need to do two readings for initial and final time, and we estimated an error of $0.1 s$ each time we identify a maximum in the cosine function.
Since the $0.1 s$ error could either be an over or under estimation, and, ideally, the two readings are independent of each other (as in, we don't necessarily _always_ over/underestimate), the total systematic uncertainty *for a N periods measurement* is $\sqrt{0.1^{2}+0.1^{2}} = 0.14s$. If they were correlated, the sum would be linear.
Therefore, for our case, given `nperiods=10`, this results in a systematic uncertainty of $0.14/10=0.014s$.
The statistical and systematic uncertainties can be summed in quadrature to obtain the total uncertainty.

Wrapping it up, these are the different period mesurements:

```
for L=41 cm    ==> T = (1.303 +/- 0.050 (stat) +/- 0.014 (syst)) s = (1.303 +/- 0.052) s
for L=31 cm    ==> T = (1.120 +/- 0.114 (stat) +/- 0.014 (syst)) s = (1.120 +/- 0.115) s
for L=21.3 cm  ==> T = (0.926 +/- 0.034 (stat) +/- 0.014 (syst)) s = (0.926 +/- 0.037) s
```

Let's now compute the corresponding gravitational acceleration $g = 4\pi^{2} L / T^{2}$

```
# Be careful with units, use metres not centimetres
def g(L, T):
    return 4 * (np.pi**2) * L / (T**2)
```

which returns

```
for L=41 cm    ==> g = 9.531 m/s^2
for L=31 cm    ==> g = 9.756 m/s^2
for L=21.3 cm  ==> g = 9.807 m/s^2
```

And now... uncertainties!
Gaussian error propagation, eveything is uncorrelated, partial derivatives... for you to play.

**Pro Tip: use the `uncertainty` python library. It computes gaussian error propagation for you**

```
L1 = u(0.41, 0.001)
T1 = u(1.3032, 0.052)
g(L1,T1)
9.530626515716135+/-0.7609330698411599

L2 = u(0.31, 0.001)
T2 = u(1.12, 0.115)
g(L2,T2)
9.75630537097481+/-2.003774165621949

L3 = u(0.213, 0.001)
T3 = u(0.926, 0.037)
g(L3,T3)
9.80657528575509+/-0.7850300446735916
```

As you can see, the uncertainties are quite large.  
Since you've calculated the error propagation piece by piece, derivative by derivative, which uncertiany impacts the measurement the most? Period or length?  


Can obtain the final value of $g$ either by doing a weighed average (some tips [here]([url](https://physics.stackexchange.com/questions/15197/how-do-you-find-the-uncertainty-of-a-weighted-average))) 

```
values = np.array([9.530626515716135, 9.75630537097481, 9.80657528575509])
uncs = np.array([0.7609330698411599, 2.003774165621949, 0.7850300446735916])

# using the uncertainty package again, u stands for ufloat, look at the link above to know how to compute the uncertainty of the weighted average
a = u(9.530626515716135, 0.7609330698411599)
b = u(9.75630537097481, 2.003774165621949)
c = u(9.80657528575509, 0.7850300446735916)

result = np.average([a,b,c], weights=1./uncs**2)
9.670668051617165+/-0.527135792579251
```

or by putting the three values with their uncertainties on a graph and fitting it with a flat line, aka `pol0` in ROOT (weighed $\chi^2$ fit, include uncertainties!)

```
gr = ROOT.TGraphErrors(3, array('d', [1,2,3]), array('d', values), array('d',[0.,0.,0.]), array('d', uncs))
gr.Draw('AP')
```

![g_graph](https://github.com/user-attachments/assets/f07fe000-b8db-4069-b3d6-328a0c6ab908)

Notice that the fitted value is (as it should!) exactly the same as that obtained from the weighted average.  

The normalized $\chi^2$ value can be interpreted as the probability that the three measurements are compatible with each other, giving the quoted uncertainties.  

```
from scipy import stats

chi2 = 0.06567
ndof = 2

prob = (1. - stats.chi2.cdf(chi2, ndof)) 

print(prob)
0.9676982166227073
```

The three measurements are compatible at 97% confidence level. Phew, physics ain't broken...


**Q: Which uncertainty dominates? How can you reduce it?**

**Q: discuss compatibility between measurements**
The central values will not be exactly the same, but will come with an uncertainty.  
Discuss compatibility between pairwise measurements (combine total uncertainty, anything correlated or simple sum in quadrature?)   

**Pro tip**
Put all measurements in a $T$ vs $m$ graph and also display the uncertainty on $T$.  
Run a $\chi^2$ fit with a flat function (constant), and compute the $p$-value corresponding to the normalized $\chi^2$.  

## plot $T^2$ vs $L$
![t2_vs_l](https://github.com/user-attachments/assets/769067d9-14a8-4b95-8754-9a7600efa7de)

Linear relation $T^{2} = 4\pi / g \cdot L$.  

The coefficient of the linear regression can be used to extract $g = 4\pi / 4.081 = 9.67 m/s^{2}$ (leave error computation to you)

## Compatibility between measured $g$ and $g_{Hoengg}$
$g_{\rm{Hoengg}} = (9.807 \pm 0.0)m/s^{2}$, $g_{\rm{meas}} = (9.67 \pm 0.53)m/s^{2}$, the measured value agrees within less than one standard deviation with the theoretical value.

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

The friction coefficient $\gamma = -0.115 \pm 0.002 s^{-1}$.  

**Bonus point: we can reverse engineer $T$ from the fitted $\omega$**
From this fit we get $T = 2\pi / \omega = 1.19 s$, to be compared with $1.2s$ obtained from a simple counting. 

