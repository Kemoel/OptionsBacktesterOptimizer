import scipy
from input.initialization import *
from scipy.optimize import minimize

from lib.account_metrics import shrp_ratio

def optimizer(data):
    max_shrp = scipy.optimize.minimize(shrp_ratio)
    return