#!/usr/bin/python3
# import matplotlib.pyplot as plt
# import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

Algs = {
    "lexic_metropolis": "Lexicographical Metropolis",
    "random_metropolis": "Random Metropolis",
    "random_glauber": "Random Glauber",
    "lexic_glauber": "Lexicographical Glauber",
    "multi_cluster": "Multi Cluster",
}
obs = {
    "charge": {"label": r"$C_{QQ}(t)/C_{QQ}(0)$", "index": 1, "sym": "Q"},
    "magnet": {
        "label": r"$\frac{C_{M}(t)}{C_{M}(0)}$",
        "index": 2,
        "sym": "M"
    },
    "energy": {
        "label": r"$\frac{C_{\mathcal{H}}(t)}{C_{\mathcal{H}}(0)}$",
        "index": 0,
        "sym": "E",
    },
}


def correlation(X, t):
    X_mean = X.mean()
    N = X.size - t
    if t == 0:
        C = (X - X_mean) ** 2
    else:
        C = (X[0:-t] - X_mean) * (X[t:] - X_mean)
    C_mean = C.mean()
    C_Var = (C**2).mean() - C_mean**2
    C_Error = np.sqrt(C_Var / N)
    return t, C_mean, C_Error


def chi2_by_dof(y0, y, yerr, dof):
    ss = (y - y0) ** 2 / yerr
    return ss.sum() / dof


def fix(x, dx):
    before, after = str(dx).split(".")
    i = 0
    val = 0
    for d in after:
        i += 1
        if d != "0":
            val = round(float(d + "." + after[i:]))
            break
    y = round(x, i)
    if i > len(str(y).split(".")[1]):
        y = f"{y}{'0'*(i-len(str(y).split('.')[1]))}"
    return f"{y}({val})"


def f(x, a, b, c):
    return c + a / (x + b)


class fit:
    def __init__(self, xdata, ydata, yerr):
        self.xdata = xdata
        self.ydata = ydata
        self.yerr = yerr

    def fiting(self, func, args=dict()):
        self.func = func
        self.opt, self.cov = curve_fit(
            func, self.xdata,
            self.ydata,
            **args,
            #:sigma=self.yerr
        )
        residuals = self.ydata - func(self.xdata, *self.opt)
        dof = self.xdata.size - self.opt.size
        # self.error = np.diag(self.cov)
        sigma_err = abs(np.std(residuals))
        pfit = []
        for i in range(100):
            random_delta = np.random.normal(0, sigma_err, len(self.xdata))
            random_ydata = self.ydata+random_delta
            random_opt, random_cov = curve_fit(
                func,
                self.xdata,
                random_ydata,
                #sigma=self.yerr+sigma_err
            )
            pfit.append(random_opt)
        pfit = np.array(pfit)
        
        self.opt = np.mean(pfit, 0)
        self.error = 2*np.std(pfit, 0)

        residuals = self.ydata - func(self.xdata, *self.opt)
        chisq = ((residuals / self.yerr) ** 2).sum()
        dof = self.xdata.size - self.opt.size
        self.chisq_by_dof = np.round(chisq / dof, 2)
