import numpy as np
import sys
import matplotlib.pylab as plt
from scipy import stats
from scipy.interpolate import interp1d
import scipy.integrate as integrate
from scipy.optimize import curve_fit
def func(x,b,c,d):
    return b*x+c*x*x+d*x**3# +e*x**4


data = np.loadtxt(sys.argv[1])
data2 = np.loadtxt(sys.argv[2])

P=data2[:,2]
T=data2[:,1]
PT=np.unique(np.vstack((P,T)),axis=1).T
#print(PT)
P=PT[:,0]
T=PT[:,1]
for P0, T0 in zip(P,T):
#    print(P0,T0)
    data = np.loadtxt(sys.argv[1])
    data2 = np.loadtxt(sys.argv[2])
    
    try:
        
        data=data[(P0==data[:,2])*(T0==data[:,1])]
        data2=data2[(P0==data2[:,2])*(T0==data2[:,1])]
        data=data[data[:,0].argsort()]
        data2=data2[data2[:,0].argsort()]
        
        # Integral variable
        x = data[:,0]
        
        # Integrand
        y = 2*(data2[:,3]-data[:,3])/x

    except:
        continue
#    data=data[data[:,0].argsort()]
#    data2=data2[data2[:,0].argsort()]
    
#    print(data,data2)



    x=np.append(0,x)
    y=np.append(0,y)
    yerror = np.append(0.00001,2*np.sqrt(data2[:,4]**2.+ data[:,4]**2.))
    fdtcv = interp1d(x, y,bounds_error=False,fill_value='extrapolate')#,kind='cubic')
    fdtcverror = interp1d(x, yerror,bounds_error=False,fill_value='extrapolate',)
    xnew = np.linspace(0, 1, num=111, endpoint=True)
    plt.plot(x, y, 'o', xnew, fdtcv(xnew))#, '-',xnew, fdtcv(xnew)-fdtcverror(xnew), '--',xnew, fdtcv(xnew)+fdtcverror(xnew), '--')
    #plt.legend(['data', 'linear'], loc='best')
    d2h273K = integrate.quad(lambda x: fdtcv(x), 1./np.sqrt(2.), 1)[0] # approximate value because the mass of oxygen is changed
    d2h273Kerror = integrate.quad(lambda x: fdtcverror(x), 0.7, 1)[0]

    #print(d2h273K, '+/-', d2h273Kerror)

    nqe273K = integrate.quad(lambda x: fdtcv(x), 0.0, 1)[0]
    nqe273Kerror = integrate.quad(lambda x: fdtcverror(x), 0.0, 1)[0]
 #   print(nqe273K, '+/-', nqe273Kerror)

    popt,  pcov = curve_fit(func, x, y,sigma=yerror)
    popt_err,  pcov = curve_fit(func, x, yerror,sigma=yerror)
#    plt.plot(xnew,func(xnew,*popt))
    print(T0,P0,integrate.simpson(y, x))#,nqe273Kerror)
    #plt.show()





popt2, pcov = curve_fit(func, data2[:,0],data2[:,3]/data2[:,0],sigma=data2[:,4])
data=data[data[:,0].argsort()]
data2=data2[data2[:,0].argsort()]
print(data)
print(data2)       
print(P0,T0)

y=np.linspace(0,1,100)

#plt.plot(data[:,0],data[:,3]/data[:,0])
y1   =  data[:,0]
y2   = data2[:,0]
int1 =  2*data[:,3]/y1
int2 = 2*data2[:,3]/y2

print(y1,y2)
popt,  pcov = curve_fit(func, y1, int2-int1)#,sigma=data[:,4])
#popt2, pcov = curve_fit(func, y2, int2)#,sigma=data2[:,4])


#plt.scatter(y1,int2-int1,label=sys.argv[1])#/data2[:,0])
#plt.scatter(y2,int2,label=sys.argv[2])#/data2[:,0])
#plt.plot(y,func(y,*popt))
#plt.plot(y,func(y,*popt2))
#plt.legend()

print(np.trapz(func(y,*popt2),x=y))#-np.trapz(func(y,*popt),x=y))

# print(T0,P0,2*(np.trapz(data[:,3]/data[:,0],x=data[:,0])-np.trapz(data2[:,3]/data2[:,0],x=data2[:,0])))
plt.show()





