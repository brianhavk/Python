import numpy as np
import matplotlib.pyplot as plt
import pygimli as pg

class FunctionModelling(pg.core.ModellingBase):
    def __init__(self, nc, xvec, verbose=False):
        pg.core.ModellingBase.__init__(self, verbose)
        self.x_ = xvec
        self.nc_ = nc
        nx = len(xvec)
        self.regionManager().setParameterCount(nc)
        self.jacobian().resize(nx, nc)
        for i in range(self.nc_):
            self.jacobian().setCol(i, pg.math.pow(self.x_, i))

    def response(self, model):
        return self.jacobian() * model

    def responseDirect(self, model):
        y = pg.Vector(len(self.x_), model[0])

        for i in range(1, self.nc_):
            y += pg.math.pow(self.x_, i) * model[i]

        return y

    def createJacobian(self, model):
        pass  # if J depends on the model you should work here

    def startModel(self):
        return pg.Vector(self.nc_, 0.5)

x = np.array([8.92065, 8.97057, 8.93661, 9.21454, 9.24524, 9.26204])
y = np.array([6.93674, 6.15386, 6.01189, 5.44065, 5.27785, 5.1701])
noise = 0.5

print(len(x))
fop = FunctionModelling(3, x)

inv = pg.core.Inversion(y, fop)

inv.setAbsoluteError(noise)

inv.setLambda(0)

plt.plot(x, y, 'rx')
plt.plot(x, inv.response(), 'b-')
plt.show()
