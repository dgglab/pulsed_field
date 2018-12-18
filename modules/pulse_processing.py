import numpy as np
import signal_processing as sp
from itertools import product
from nptdms import TdmsFile

def import_shot(fname, params):
    """
    This function loads in the noted parameters for a given shot. 
    B and B dot may or may not be sampled at a lower frequnecy. 
    Therefore, NaNs are removed on import to make this clear.
    This function takes a tmds file as its input.
    
    Arguments:
        fname: path to TDMS data
        params: list of tuples strings of variable names to import with their 
                appropriate gains
    """
        
    shot = dict()
    shot['params'] = params
        
    tdms_file = TdmsFile(fname)
    for p, g in params:
        if p == 'B':
            shot[p] = tdms_file.object('p','Field_fixed').data / g
        else:
            shot[p] = tdms_file.object('p',p).data / g
    return shot



def import_shot_ascii(fname, params, cols):
    """
    This function loads in the noted parameters for a given shot. 
    B and B dot may or may not be sampled at a lower frequnecy. 
    Therefore, NaNs are removed on import to make this clear
        
    Arguments:
        fname: path to ASCII data
        params: list of tuples strings of variable names to import with their 
                appropriate gains
    """
    
    with open(fname, 'r') as f:
        data = np.genfromtxt(f,delimiter ='\t')

    shot = dict()
    shot['params'] = params
    shot['cols'] = cols
    for (p, g), c in zip(params, cols):
        if p == 'B' or p == 'Bdot':
            shot[p] = data[~np.isnan(data[:,c]),c] / g
        else:
            shot[p] = data[:,c] / g
    return shot


def downsample(shot, keys, n):
    """
    Used to down sample data by averaging over n data points
    
    Arguments:
        shot: shot containing data to be down sampled
        keys: dict keys of variables to down sample
        n: factor to down sample by
    """
    
    for key in keys:
        shot[key] = sp.linAve(shot[key],n)[n-1::n]
    return shot

    
def smooth(shot, keys, n, window = 'hanning'):
    """
    Smooths data according to a given windowed average
    
    Arguments:
        shot: shot containing data to be smoothed
        keys: dict keys of variables to smooth
        n: size of windowed average
        window: type of window to use with smoothing
    """
    
    for key in keys:
        shot[key] = sp.smooth(shot[key], window_len=n, window=window)
    return shot
    
    
def rise_fall(shot, params, thresh=0.05):
    """
    Find the peak field of the shot and separatly return the rising and falling
    portions of the data. The data is truncated at thresh to prevent
    long tails
    
    Arguments:
        shot: shot containing data
        params: list of tuples strings of variable names to with their 
                appropriate gains
        thresh: cutoff B for truncating data
    """
    
    shot['B_max'] = np.max(np.abs(shot['B']))
    index_max = np.argmax(np.abs(shot['B']))
    shot['index_max'] = index_max
    
    threshind_rising = np.argmin(np.abs(shot['B'][:index_max]-thresh))
    threshind_falling = np.argmin(np.abs(shot['B'][index_max:]-thresh))
    
    for p,_ in params:
        shot[p+'_rising'] = shot[p][threshind_rising:index_max]
        shot[p+'_falling'] = shot[p][index_max:index_max+threshind_falling]
    
    shot['Rxx_rising'] = shot['Vxx_rising']/shot['I_rising']
    shot['Rxx_falling'] = shot['Vxx_falling']/shot['I_falling']
    
    shot['Rxy_rising'] = shot['Vxy_rising']/shot['I_rising']
    shot['Rxy_falling'] = shot['Vxy_falling']/shot['I_falling']
    
    return shot
    

def interp_shots(shots, params):
    """
    This function interpolates all parameters to the B field of the shot with 
    the lowest peak field. B is interpolated last so that it cannot mess
    up the interpolation of other variables
    
    Arguments:
        shots: list containing shots to interpolate to same field
        params: list of tuples strings of variable names to import with their 
                appropriate gains
    """
    
    B_max_store = []
    for shot in shots:
        B_max_store.append(shot['B_max'])
    
    minB_shot = np.argmin(B_max_store)
    
    for (i,shot),(p,_) in product(enumerate(shots),params):
        if i == minB_shot:
            pass 
        else:
            if p == 'B':
                pass
            else:
                shot[p+'_rising'] = np.interp(
                    np.abs(shots[minB_shot]['B_rising']),np.abs(shot['B_rising']),
                    shot[p + '_rising'])
                    
                shot[p+'_falling'] = np.interp(
                    np.abs(shots[minB_shot]['B_falling']),np.abs(np.flip(shot['B_falling'])),
                    np.flip(shot[p + '_falling']))
     
    
    for i,shot in enumerate(shots):
        if i == minB_shot:
            shot['B_rising'] = np.abs(shot['B_rising'])
            shot['B_falling'] = np.abs(shot['B_falling'])
            pass
        else:
            shot['B_rising'] = np.interp(
                np.abs(shots[minB_shot]['B_rising']),np.abs(shot['B_rising']),
                np.abs(shot['B_rising']))
                
            shots[i]['B_falling'] = np.interp(
                np.abs(shots[minB_shot]['B_falling']),np.abs(np.flip(shot['B_falling'])),
                np.abs(np.flip(shot['B_falling'])))
                
            shot['Rxx_rising'] = shot['Vxx_rising']/shot['I_rising']
            shot['Rxx_falling'] = shot['Vxx_falling']/shot['I_falling']
            
            shot['Rxy_rising'] = shot['Vxy_rising']/shot['I_rising']
            shot['Rxy_falling'] = shot['Vxy_falling']/shot['I_falling']
    
    return shots
    

    
    
