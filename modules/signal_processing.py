import numpy as np


"""
    reduceMat
    This function takes a windowed average of the input
    and returns the averaged 
"""
def reduceMat(A, Nave, axis=0):
    
    
    shpA = np.shape(A) # Find the shape of the input array

    listflag = 0
    if len(shpA) == 1:
        A = np.reshape(A,(-1,1))
        shpA = np.shape(A)
        listflag = 1

    # Create array of size of array along average direction
    r = np.arange(0,shpA[axis],Nave)
    
    # If the array cannot be divided into even windows
    if r[-1]+Nave>shpA[axis]:
        r=r[0:(np.shape(r)[0] - 1)] # Take out the last window
        
        
    # Averaging along rows
    if axis == 0:
        out=np.zeros((np.size(r),shpA[1-axis])) # Generate output array
        k=0 # Counter for storing
        for i in r:
            out[k,:]=np.mean(A[i+np.arange(0,Nave),:],axis)
            k=k+1;
    
    # Averaging along columns        
    if axis == 1:
        out=np.zeros((shpA[1-axis],np.size(r))) # Generate output
        k=0 # Counter for storing
        for i in r:
            out[:,k]=np.mean(A[:,i+np.arange(0,Nave)],axis)
            k=k+1;
            
    if listflag == 1:
        out = np.reshape(out,(-1))
    return out
	
	
	
def gaussAve(data, n, sigma = None):
	""" Returns data smoothed by a Gaussian window of size n """
	""" n is the number points on each side of the original point to include"""
	
	if n == 0:
		dataAve = data
		
	else:
		if not sigma:
			sigma = (float(n)/2)**(1/2)
		
		n = int(n)
		x= np.arange(-n,n+1)
		g = np.exp(-(x**2/(2*sigma**2)))
		g = g/g.sum()
		dataAve = np.convolve(data,g, mode='same')
			
		
	return dataAve
	
	
def linAve(data, n):
	""" Returns a linear average of the data over a window """
	dataAve = np.convolve(data, np.ones((2*n+1,))/(2*n+1), mode='same')
	return dataAve


# window :  ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']
def smooth(x,window_len=11,window='hanning'):
    
    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y


# Returns the symmetric and asymmetric components of y about the given zero
def symmetrize(x,y,zero=0):
    idx = (np.abs(x-zero)).argmin()
    xsym = np.zeros(2*np.minimum(idx,len(x)-(idx+1))+1)
    symtemp = np.zeros(np.minimum(idx,len(x)-(idx+1)))
    asymtemp = np.zeros(np.minimum(idx,len(x)-(idx+1)))
    xsym[idx] = x[idx]
    for i in range(len(symtemp)):
        xsym[idx+i+1] = x[idx+i+1]
        xsym[idx-i-1] = x[idx-i-1]
        symtemp[i] = (y[idx+i+1]+y[idx-i-1])/2
        asymtemp[i] = (y[idx+i+1]-y[idx-i-1])/2
    
    args = (symtemp[::-1],np.array([y[idx]]),symtemp)
    sym = np.concatenate(args,axis=0)
    args = (-asymtemp[::-1],np.array([0]),asymtemp)
    asym = np.concatenate(args,axis=0)
    return [xsym,sym,asym]