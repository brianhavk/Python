import pygimli.physics.ert as ert

dataset = ert.load("simple.dat")

mgr = ert.ERTManager(dataset, verbose=True)
inversion = mgr.invert(robustData=True)
chi2 = (mgr.inv.chi2History)[-1]
print("Last Chi2 from chi2History: " + str(chi2))