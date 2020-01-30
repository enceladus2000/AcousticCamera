import seaborn as sns
import numpy as np
X=np.arange(-1,125,0.25)
Y=np.arange(-1,1.25,0.25)
X,Y=np.arange(X,Y)
Z=my_3d_func(X,Y)
fig,ax1=plt.subplots(1,1)
g=sns.heat,ap(Z,ax=ax1)
g.set_xticklabels(np.arange(-1,1.25,0.25),rotation=0,fontsize=8)
g.set_yticklabels(['a','b','c','d','e','f','g','h','i'],rotation=0,fontsize=8)

