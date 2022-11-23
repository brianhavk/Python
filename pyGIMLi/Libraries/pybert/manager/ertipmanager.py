#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 09:43:42 2015
"""

from __future__ import print_function, division
import sys
import numpy as np
import pygimli as pg
#import pybert as pb
import matplotlib.pyplot as plt
from pygimli.utils.base import interperc
from pybert.manager.resistivity import Resistivity
from pygimli.utils import getSavePath
from pygimli.viewer.mpl import drawModel, CellBrowser, createColorbar, plotLines

TOLERANCE = 1e-12


class ERTIPManager(ERTManager):
    """
    Class for managing an IP inversion. This also requires having the result
    from a resistivity inversion.
    """

    def __init__(self, *args, **kwargs):
        """
        Supply a filename to load.
        """
        super(ERTIPManager, self).__init__(*args, **kwargs)

        try:
            self.rhoai = pg.Vector(np.abs(self.data("rhoa") *
                                   np.sin(self.data("ip") / 1000.0)))
        except KeyError as e:
            raise(e)
#        try:
#            self.res_obj = kwargs.pop("resistivity")
#        except KeyError:
#            self.res_obj = Resistivity(*args, **kwargs)
#        except:
#            print("Unexpected error: {}".format(sys.exc_info()[0]))

    def createFOP(self, refine=True):
        """
        Create forward operator working on refined mesh.
        """

        super(ERTIPManager, self).createFOP(refine=refine)

        self.f_IP = pg.LinearModelling(self.pd, self.f.jacobian(), True)
        self.f_IP.regionManager().setConstraintType(1)
        self.f_IP.regionManager().region(1).setBackground(True)
        self.f_IP.createRefinedForwardMesh(refine) #TODO: not done in C++


    def estimateError(self, absoluteError=1.0, relativeError=0.03):
        """
        If the data file contains the error estimate it will be used as
        a relative error. Otherwise an absolute error will be used instead.
        Default is 1.0 mrad.
        """

#        if relativeError > 1:  # obviously in %
#            relativeError /= 100.
        self.error_is_rel = False

        if self.data.haveData("iperr"): #this is assumed to be relative error
            self.error_IP = np.abs(np.asarray(self.data("iperr")) / np.asarray(self.data("ip")))
            self.error_is_rel = True
        else: #otherwise we use absolute error
            self.error_IP = np.abs(self.rhoai) / (np.abs(self.data("ip")) +\
                            TOLERANCE) * absoluteError

        super(ERTIPManager, self).estimateError()
#        if hasattr(self, 'INV'):
#            self.INV.setRelativeError(self.error)

    def createInv(self, verbose=True, dosave=False):
        """
        Create inversion instance.
        """
        super(ERTIPManager, self).createInv(verbose=verbose, dosave=dosave)

        if not hasattr(self, "f_IP"):
            self.createFOP()
        if not hasattr(self, "error_IP"):
            self.estimateError()

#        self.tD_IP = pg.trans.TransLog()
        self.tM_IP = pg.trans.TransLog()
        self.INV_IP = pg.core.RInversion(self.rhoai, self.f_IP,
                                    verbose=verbose, dosave=dosave)
#        self.INV.setTransData(self.tD_IP)
        self.INV_IP.setTransModel(self.tM_IP)

        self.INV_IP.setRecalcJacobian(False)
        self.INV_IP.stopAtChi1(False)

        if self.error_is_rel:
            self.INV_IP.setRelativeError(self.error_IP)
        else:
            self.INV_IP.setAbsoluteError(self.error_IP)

    def run(self, zweight=0.7, lam=30., max_iter=20):
        """Run resistivity and IP inversion."""
        if not hasattr(self, "INV_IP"):
            self.createInv()

        super(ERTIPManager, self).run(zweight, lam, max_iter)
        self.start_IP = self.createStartModel(self.rhoai, self.pd, model_type="median")
        self.f_IP.setStartModel(self.start_IP)
        self.f_IP.regionManager().setZWeight(zweight)
        self.INV_IP.setLambda(lam)
        self.INV_IP.setModel(self.start_IP)
        self.INV_IP.setMaxIter(max_iter)
        self.im_resistivity = self.INV_IP.run()
        resistivity = np.asarray(self.INV.response())#np.asarray(self.resistivity)
        self.phase = np.angle(self.im_resistivity, resistivity) * 1000.0

    def _show_data(self, data, ax=None, cMin=None, cMax=None, logScale=True,
                   **kwargs):

        if cMin is None or cMax is None:
            cMin, cMax = interperc(data, 3, islog=True)
        if ax is None:
            ax, cbar = pg.show(self.pd, data=data, logScale=logScale,
                               colorBar=True, cMin=cMin, cMax=cMax, **kwargs)
        else:
            gci = drawModel(ax, self.pd, data=data, logScale=logScale,
                            colorBar=True, cMin=cMin, cMax=cMax, **kwargs)
            cbar = createColorbar(gci, **kwargs)
            browser = CellBrowser(self.mesh, data, ax)
            browser.connect()
            plt.show()  # block=False)

        if kwargs.has_key('lines'):
            plotLines(ax, kwargs['lines'])
        return ax, cbar

    def _show_im_res(self, ax=None, cMin=None, cMax=None, logScale=True,
                   **kwargs):
        """
        Method to draw the imaginary resistivity.
        """
        return self._show_data(self.im_resistivity, ax, cMin, cMax,
                               logScale, **kwargs)

    def _show_phase(self, ax=None, cMin=None, cMax=None, logScale=True,
                   **kwargs):
        """
        Show the phase.
        """
        return self._show_data(self.phase, ax, cMin, cMax, logScale, **kwargs)

    def showResult(self, ax=None, cMin=None, cMax=None,
                   logScale=True, **kwargs):
        """
        Show resulting resistivity and IP vectors.
        """

        fig1, ax1 = self._show_im_res(ax, cMin, cMax, logScale, **kwargs)
        fig2, ax2 = self._show_phase(ax, cMin, cMax, logScale, **kwargs)

        return (fig1, fig2), (ax1, ax2)

    def saveResult(self, folder=None, size=(16, 20), **kwargs):
        """
        Saves the results in the specified folder.

        Saved items are:
            Inverted profile
            Resistivity vector
            Coverage vector
            Standardized coverage vector
            Mesh (bms and vtk with results)
        """
#        TODO: How to extract the chi2 etc. from each iteration???

        subfolder = '/' + self.__class__.__name__
        path = getSavePath(folder, subfolder)

        print('Saving resistivity and IP data to: {}'.format(path))

#        np.savetxt(path + '/resistivity.vector',
#                   self.resistivity)
#        np.savetxt(path + '/resistivity-cov.vector',
#                   self.coverageDC())
#        np.savetxt(path + '/resistivity-scov.vector',
#                   self.standardizedCoverage())
        np.savetxt(path + '/im_resistivity.vector',
                   self.im_resistivity)
        np.savetxt(path + '/phase.vector', self.phase)

        self.pd.addExportData('Im. Resistivity', self.im_resistivity)
        self.pd.addExportData('Phase', self.phase)
#        self.pd.addExportData('Resistivity', self.resistivity)
#        self.pd.addExportData('Coverage', self.coverageDC())
#        self.pd.addExportData('S_Coverage', self.standardizedCoverage())
#        self.pd.exportVTK(path + 'resistivity')
#        self.mesh.save(path + 'resistivity-mesh')
#        self.pd.save(path + 'resistivity-pd')

        fig1, ax1 = plt.subplots()
        self._show_im_res(ax=ax1, **kwargs)
        fig1.set_size_inches(size)
        fig1.savefig(path + '/im_resistivity.pdf')

        fig2, ax2 = plt.subplots()
        self._show_phase(ax=ax2, **kwargs)
        fig2.set_size_inches(size)
        fig2.savefig(path + '/phase.pdf')

        blah, fig3, ax3 = super(ResistivityIP, self).saveResult(folder=folder)
        return path, (fig1, fig2, fig3), (ax1, ax2, ax3)

if __name__ == '__main__':
    datafile = sys.argv[1]
    res_ip = ERTIPManager(datafile)
    print(res_ip)
    pg.showLater(True)
    res_ip.showData()
    res_ip.makeMesh(quality=34.7, max_cell_area=0.0)
    res_ip.showMesh()
    res_ip.run(zweight=0.7, lam=20.0, max_iter=15)
#    ax, cbar = res_ip.showResult()
    res_ip.saveResult()
    pg.showNow()
