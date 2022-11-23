import pygimli as pg

data = pg.load("resistivity.dat")
ert = pg.physics.ert.ERTManager(data, sr=False, useBert=True, debug=False, verbose=True)
ert.invert(lam=0.42, maxIter=2)
ert.showResult()