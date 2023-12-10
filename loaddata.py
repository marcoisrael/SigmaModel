import matplotlib.pyplot as plt
import numpy as np
import os
text_kwargs = dict(ha='center', va='center', fontsize=14)
def fit(x,y):
    cof = np.polyfit(x, y, deg=1, cov=True)
    error = np.sqrt(cof[1][0][0]/5), np.sqrt(cof[1][1][1]/5)
    return cof[0],error
def tempName(start, end):
    name = f"{float(start)}-{float(end)}".replace('.','p')
    return name
class loadData:
    def __init__(self, method, algorithm, startTemp, endTemp, path, dest):
        self.algorithm = algorithm
        self.method = method
        self.path = path
        self.dest = dest
        self.name = f"{method} {algorithm}".replace("Lexic", "Lexicographical") 
        self.startTemp =  startTemp
        self.endTemp = endTemp
        if self.algorithm == "Metropolis" or  self.algorithm == "Glauber":
            self.update = "#Sweep"
            self.ar = "Aceptance Rate"
        else:
            self.update = "#Update"
            self.ar = "Cluster Size"
    def plot(self, tau_q):
        fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,dpi=140,figsize=(16,9))
        tauQf, chif,chifError = [],[],[]
        for n in tau_q:
            pathFile = f"{self.path}/{self.method.lower()}_{self.algorithm.lower()} {n}.csv"
            tauQ,T,chi,chiError,ar,arError = np.loadtxt(pathFile, delimiter=',',skiprows=1).transpose()
            tauQf.append(tauQ[-1])
            chif.append(chi[-1])
            chifError.append(chiError[-1])
            ax1.errorbar(tauQ, chi, yerr=chiError, ls='', marker='o', alpha=0.6, label=r'$\tau_Q=$'+f'{n}')
            ax1.set_xlabel(self.update, fontsize=14)
            ax1.set_ylabel(r'$\chi_f$', fontsize=14)
            ax2.errorbar(T ,chi, yerr=chiError, ls='', marker='o', alpha=0.6)
            ax2.set_xlabel(r'$T$', fontsize=14)
            ax2.set_ylabel(r'$\chi_t$', fontsize=14)
            ax4.errorbar(T, ar, yerr=arError, ls='', marker='o', alpha=0.6)
            ax4.set_xlabel(r'$T$', fontsize=14)
            ax4.set_ylabel(self.ar ,fontsize=14)
        tauQf,chif,chifError = np.array(tauQf),np.array(chif),np.array(chifError)
        x, y = np.log(tauQf),np.log(chif)
        cof, err = fit(x,y)
        t = np.log(np.linspace(3,15))
        ax3.plot(t, np.polyval(cof,t),linewidth=0.8)
        ax3.errorbar(x,y,yerr=chifError/chif,ls='',marker='o',alpha=0.6)
        ax3.set_xlabel(r'$\log\left(\tau_{Q_f}\right)$',fontsize=14)
        ax3.set_ylabel(r'$\log\left(\chi_{t_f}\right)$',fontsize=14)
        text = f'$\zeta = {-cof[0].round(3)}\pm {err[0].round(3)}$'
        ax3.text(0.7, 0.7, text,transform=ax3.transAxes, **text_kwargs) 
        title = f"{self.name}"+r", $V=64 \times 64$"+ f", $T \in ({self.startTemp},{self.endTemp})$"
        fig.suptitle(title,fontsize=14)
        lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
        lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
        ax1.grid(True)
        ax2.grid(True)
        ax3.grid(True)
        ax4.grid(True)
        fig.legend(lines, labels)
        #fig.tight_layout()
        if not os.path.isdir(self.dest):
            os.makedirs(self.dest)
        fig.savefig(f'{self.dest}/{self.method.lower()}_{self.algorithm.lower()}')   