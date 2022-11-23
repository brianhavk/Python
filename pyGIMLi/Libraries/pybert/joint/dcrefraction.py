#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 12:51:21 2015

@author: Marcus
"""

# general modules to import according to standards
import sys
import numpy as np
import matplotlib.pyplot as plt
import pygimli as pg
from pygimli.viewer.mpl import drawMesh
from pygimli.utils import getSavePath
from pygimli.physics.traveltime import Refraction
from pybert.manager import Resistivity


def getcweight(vec, a=0.1, b=0.1, c=1.0):
    """
    Structural constraint weight as function of roughness.
    """
    return np.minimum((a / (np.absolute(vec) + a) + b)**c, 1.0)


class DCRefraction():
    """Class for managing a structurally coupled DC resistivity and
    refraction inversion. Takes care of the standard setup logistics."""
    def __init__(self, filename_dc=None, filename_ra=None,
                 verbose=True, **kwargs):
        """
        Init function with optional data load.
        """
        if filename_dc is not None and filename_ra is not None:
            self.load(filename_dc, filename_ra)

        self.statistics = dict(ra=dict(), dc=dict())  # saving chi2 rrms etc
        self.figs = {}
        self.axs = {}

    def __repr__(self):
        """
        String representation of the class.
        """

        return self.__str__()

    def __str__(self):
        """
        Human readable string representation of the class.
        """

        out = "Resistivity and refraction object"
        if hasattr(self, 'mesh'):
            out += "\n" + self.mesh.__str__()
        if hasattr(self, 'dc'):
            out += "\n" + self.dc.__str__()
        if hasattr(self, 'ra'):
            out += "\n" + self.ra.__str__()
        return out

    def load(self, filename_dc, filename_ra):
        """
        Load data from files.
        """
        # check for file formats and import if necessary
        self.ra = Refraction(filename_ra)
        self.dc = Resistivity(filename_dc)

        print(self.dc)
        print(self.ra)

    def showData(self, ax=None):
        """
        Show data in form of apparent resistivities and apparent velocoties.
        """

        if ax is None:
            fig, ax = plt.subplots(nrows=2, ncols=1)

        self.dc.showData(ax=ax[0])
        self.ra.showData(ax=ax[1])
        plt.show(block=False)

    def getDepth(self):
        """
        Return the maximum (roughly estimated) depth of investigation
        of the two methods.
        """
        return max(self.ra.getDepth(), self.dc.getDepth())

    def makeMesh(self, depth=None, quality=34.3, max_cell_area=0.0):
        """ create (inversion) """
        if depth is None:
            depth = self.getDepth()

        self.dc.makeMesh(depth, quality, max_cell_area)
        self.mesh = self.dc.mesh
        newmesh = pg.Mesh()
        newmesh.createMeshByMarker(self.dc.mesh, 2, 99)
        self.ra.setMesh(newmesh)

    def setMesh(self, mesh):
        """ set mesh from outside (e.g. load from bert mesh folder) """
        if isinstance(mesh, str):
            self.mesh = pg.Mesh(mesh)
        else:
            self.mesh = mesh
        self.dc.setMesh(self.mesh)
        newmesh = pg.Mesh()
        newmesh.createMeshByMarker(self.mesh, 2, 99)
        self.ra.setMesh(newmesh)

    def showMesh(self, ax=None):
        """ show mesh in given axes or in a new figure """
        if ax is None:
            fig, ax = plt.subplots()

        drawMesh(ax, self.mesh)
        plt.show(block=False)

    def createFOP(self, refine=True):  # Dijkstra, later FMM
        """ create forward operator working on refined mesh """
        if not hasattr(self, 'mesh'):  # self.mesh is None:
            self.makeMesh()

        self.dc.createFOP(refine=refine)
        self.ra.createFOP(refine=refine)
        self.ra.fop.regionManager().region(1).setBackground(True)

    def estimateError(self, absoluteError=0.001, relativeError=0.03):
        """ estimate error composed of an absolute and a relative part """

# TODO: Make sure that the errors are estimated correctly. Particularly DC!

        self.dc.estimateError(absoluteError, relativeError)
        self.ra.estimateError(absoluteError, relativeError)

    def createInv(self, verbose=True, dosave=False):
        """ create inversion instance """

        self.dc.createInv(verbose=verbose, dosave=dosave)
        self.ra.createInv(verbose=verbose)

    def run(self, zweight_dc=0.7, zweight_ra=0.7,
            lambda_dc=30., lambda_ra=30.,
            a=0.1, b=0.1, c=1.0, max_iter=10, sep_iter=2,
            vel_top=500., vel_bottom=5000., verbose=False):
        """
        Run a structurally coupled inversion with an optional separate
        preparatory inversion.
        """

        self.ra.inv.setVerbose(verbose)
        self.dc.createInv(verbose=verbose)
        if sep_iter > 0:
            print('Running initial separate inversions. ({} iterations.)'
                  .format(sep_iter))
        print("Doing initial DC inversion")
        self.dc.run(zweight=zweight_dc, lam=lambda_dc, max_iter=sep_iter)
        if not self.dc.INV.verbose():
            self.dc.INV.echoStatus()
        print("Doing initial Ra inversion")
        self.ra.run(vtop=vel_top, vbottom=vel_bottom,
                    zweight=zweight_ra, lam=lambda_ra, max_iter=sep_iter)
        if not self.ra.inv.verbose():
            self.ra.inv.echoStatus()

        print('Running structurally coupled inversions. ({} iterations)'
              .format(max_iter-sep_iter))

        self.statistics['dc']['chi2'] = []
        self.statistics['ra']['chi2'] = []
        self.statistics['dc']['rrms'] = []
        self.statistics['ra']['rrms'] = []
        self.statistics['dc']['rms'] = []
        self.statistics['ra']['rms'] = []
        self.statistics['dc']['iter'] = []
        self.statistics['ra']['iter'] = []

        doLikeCPP = False  # if True then same cweights like dc_tt_jointinv
        if a == 0:
            doLikeCPP = True  # using "old" scheme if a == 0

        if doLikeCPP:
            flat_weight = self.dc.f.regionManager().createConstraintsWeight()

        chi2_thresh = 1.2
        stop = False  # main stop criterion
        while not stop:
            # TODO: Create nicer way of logging this stuff.
            self.statistics['dc']['chi2'].append(self.dc.INV.getChi2())
            self.statistics['ra']['chi2'].append(self.ra.inv.getChi2())
            self.statistics['dc']['rrms'].append(self.dc.INV.relrms())
            self.statistics['ra']['rrms'].append(self.ra.inv.relrms())
            self.statistics['dc']['rms'].append(self.dc.INV.absrms())
            self.statistics['ra']['rms'].append(self.ra.inv.absrms())
            self.statistics['dc']['iter'].append(self.dc.INV.iter())
            self.statistics['ra']['iter'].append(self.ra.inv.iter())

            do_ra_step = self.ra.inv.getChi2() > chi2_thresh
            do_dc_step = self.dc.INV.getChi2() > chi2_thresh

            if not doLikeCPP:
                self.ra.fop.region(2).fillConstraintsWeightWithFlatWeight()
                self.dc.f.region(2).fillConstraintsWeightWithFlatWeight()

                roughness_dc = self.dc.INV.roughness()
                roughness_ra = self.ra.inv.roughness()
                cweight_ra = getcweight(roughness_dc, a, b, c)
                cweight_dc = getcweight(roughness_ra, a, b, c)
            else:
                cweight_ra = self.dc.INV.getIRLS()*flat_weight
                cweight_dc = self.ra.inv.getIRLS()*flat_weight

            if do_dc_step:
                if do_ra_step:
                    self.dc.INV.setCWeight(cweight_dc)
                print("Doing DC inversion")
                self.dc.INV.oneStep()
                if not self.dc.INV.verbose():
                    self.dc.INV.echoStatus()

            if do_ra_step:
                if do_dc_step:
                    self.ra.inv.setCWeight(cweight_ra)
                print("Doing Ra inversion")
                self.ra.inv.oneStep()
                if not self.ra.inv.verbose():
                    self.ra.inv.echoStatus()

            ra_iter = self.ra.inv.iter() >= max_iter
            dc_iter = self.dc.INV.iter() >= max_iter

            stop = (not (do_ra_step or do_dc_step)) or ra_iter or dc_iter

        self.dc.resistivity = self.dc.INV.model()
        self.ra.velocity = 1.0 / self.ra.inv.model()

    def standardizedCoverage(self, threshhold=0.01):
        """
        Return standardized coverage vector (0|1) using threshholding.

        Coverage is where we have cells adequately covered by both methods.
        """

        coverage_dc = self.dc.standardizedCoverage(threshhold)
        coverage_ra = self.ra.standardizedCoverage()
        return coverage_dc * coverage_ra

    def showResult(self, c_min_dc=None, c_max_dc=None,
                   c_min_ra=None, c_max_ra=None,
                   log_scale_dc=True, log_scale_ra=False, **kwargs):
        """Show resulting resistivity and velocity vectors."""
        self.figs['result'], ax = plt.subplots(nrows=2, sharex=True)
        self.axs['res'], rcbar = self.dc.showResult(
            ax=ax[0], cMin=c_min_dc, cMax=c_max_dc, logScale=log_scale_dc,
            **kwargs)
        self.axs['vel'], vcbar = self.ra.showResult(
            ax=ax[1], cMin=c_min_ra, cMax=c_max_ra, logScale=log_scale_ra,
            **kwargs)
        return self.figs['result']

    def showResults(self, folder=None, size=(16, 20), **kwargs):
        """show all results in one figure"""
        fig, ax = plt.subplots(nrows=2, ncols=1)
        self.showResult(ax=ax, **kwargs)
        fig.set_size_inches(size)
        return fig, ax

    def saveResults(self, folder=None, fig=None, **kwargs):
        """Saves the results in the specified folder.

        Saved items are:
            Inverted profiles
            Resistivity vector
            Velocity vector
            Coverage vectors
            Standardized coverage vectors

            Joint standardized coverage vector
            Mesh (bms and vtk with results)
        """
        subfolder = '/' + self.__class__.__name__
        path = getSavePath(folder, subfolder)

        print('Saving joint resistivity/refraction data to: {}'.format(path))

#        self.ra.saveResult(folder=path, cMin=kwargs['c_min_ra'],
#                           cMax=kwargs['c_max_ra'])
#        self.dc.saveResult(folder=path, cMin=kwargs['c_min_dc'],
#                           cMax=kwargs['c_max_dc'])
        self.ra.saveResult(folder=path, **kwargs)
        self.dc.saveResult(folder=path, **kwargs)

        joint_scov = self.standardizedCoverage()
        np.savetxt(path + '/joint-scov.vector', joint_scov)

        with open(path + '/chi2.log', 'w') as out:
            ra_stats = self.statistics['ra']
            dc_stats = self.statistics['dc']

            keys = ra_stats.keys()
            n_iter = len(ra_stats['chi2'])

            for i in range(n_iter):
                out.write('DC[{}]'.format(str(i).zfill(2)))
                for k in keys:
                    out.write('\t' + k + ': {}'.format(dc_stats[k][i]))
                out.write('\nRA[{}]'.format(str(i).zfill(2)))
                for k in keys:
                    out.write('\t' + k + ': {}'.format(ra_stats[k][i]))
                out.write('\n')

        pd = pg.Mesh(2)
        pd.createMeshByMarker(self.mesh, 2)
        pd.addExportData('Resistivity', self.dc.resistivity)
        pd.addExportData('DC coverage', self.dc.coverageDC())
        pd.addExportData('DC S-coverage', self.dc.standardizedCoverage())
        pd.addExportData('Velocity', self.ra.velocity)
        pd.addExportData('Slowness', 1.0/self.ra.velocity)
        pd.addExportData('Refr. coverage', self.ra.rayCoverage())
        pd.addExportData('Refr. S-coverage', self.ra.standardizedCoverage())
        pd.addExportData('Joint S-coverage', joint_scov)
        pd.exportVTK(path + 'DCRefraction')
        if fig is not None:
            fig.savefig(path + '/dcra.pdf')
        return path


if __name__ == '__main__':
    datafile_dc = sys.argv[1]
    datafile_ra = sys.argv[2]
    dcra = DCRefraction(datafile_dc, datafile_ra)
    dcra.ra.data.markInvalid(dcra.ra.data('s') > 222)
    dcra.ra.data.removeInvalid()

    print(dcra)
    pg.showLater(True)
    dcra.showData()
    dcra.makeMesh(quality=34.5, max_cell_area=0)

    dcra.showMesh()
    dcra.run(sep_iter=2, max_iter=20)
    fig, ax = dcra.showResults(c_min_dc=10, c_max_dc=1000, c_min_ra=500,
                               c_max_ra=5000)
    dcra.saveResults(size=(16, 20))
    pg.showNow()
