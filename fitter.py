'''
https://github.com/root-project/root/blob/master/bindings/pyroot/pythonizations/test/tf_pycallables.py
'''

import numpy as np
import uproot
import ROOT

# load data
tree = uproot.open('accelerations.root')['tree']

# user defined function, corresponding to dphi/dt in manual Eq 3
def f1(x, par):

    # t : time
    # par[0] : amplitude
    # par[1] : gamma
    # par[2] : omega
    # par[3] : alpha
    
    t = x[0]
    
    return - par[0] * np.exp(par[1]*t / 2.) * (par[1]/2. * np.cos(par[2]*t + par[3]) + par[2]*np.sin(par[2]*t + par[3]))

# define time range
tmin =  6. # clip initial noise
tmax = 40. # clip final noise

# number of free parameter in the damped oscillation equation, A, gamma, omega, alpha
npars = 4

# ROOT function
f = ROOT.TF1('damped_oscillations', f1, tmin, tmax, npars)


# plot
t  = np.array(tree['t' ].array())
ay = np.array(tree['ay'].array())

g1 = ROOT.TGraph(len(t), t, ay)
g1.SetTitle("Pendulum;t (s);d#phi/dt")
g1.Draw('AC*')

# Set the initial parameters to reasonable values to help the fit converge.
T = 1.2 # this is the perio
f.SetParameters(5, 0., 2*np.pi/1.2, 0.)
f.SetNpx(2000) # add more evaluation points, smoothen the function

# Give the parameters names.
f.SetParNames('A', 'gamma', 'omega', 'alpha')

# fit in a range (option 'R') and save results (option 'S')
fit_results = g1.Fit(f, 'SR')

