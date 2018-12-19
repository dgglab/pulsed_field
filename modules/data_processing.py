import numpy as np


def gaussAve(data, n, sigma = None):
    """
    Returns data smoothed by a Gaussian window of size n 
    n is the number points on each side of the original point to include
    """
    if n == 0:
        dataAve = data
    else:
        if not sigma:
            sigma = (n/2.0)**(1/2)

        x= np.arange(-n, n + 1)
        g = np.exp(-(x**2 / (2*sigma**2)))
        g = g / g.sum()
        dataAve = np.convolve(data, g, mode='same')
    
    return dataAve


def linAve(data, n):
    """
    Returns a windowed linear average of the data where the window is of
    size n
    """
    return np.convolve(data, np.ones((2*n + 1,))/(2*n + 1), mode='same')


def smooth(x, window_len=11, window='hanning'):
    """
    Windowed smoothing of data with a choice of the type of window
    window :  ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']
    """
    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    
    if window == 'flat':
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')
    
    return np.convolve(w / w.sum(), s, mode='valid')