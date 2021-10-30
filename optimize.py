from input.initialization import *
import scipy as sp

from lib.account_metrics import shrp_ratio

def optimizer(data):
    max_shrp = sp.optimize.minimize(shrp_ratio)
    return