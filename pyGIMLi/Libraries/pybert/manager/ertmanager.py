#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resistivity manager for administrating ERT data, modelling and inversion
"""

import sys

import numpy as np
import matplotlib.pyplot as plt

import pygimli as pg
from pygimli.viewer.mpl import drawModel, drawMesh, plotLines
from pygimli.viewer.mpl import CellBrowser
from pygimli.utils.base import interperc, getSavePath

import pybert as pb
# from pybert.data import drawDataAsMatrix, Pseudotype, plotERTData
from pybert.data import Pseudotype, plotERTData

try:
    from pygimli.manager import MeshMethodManager
except ImportError:
    from pygimli.frameworks import MeshMethodManager

try:
    from pygimli.physics.ert import ERTManager  # pg 1.1
except ImportError:
    ERTManager = Resistivity  # pg 1.0

def simulate(mesh, res, scheme, verbose=False, **kwargs):
    """Convenience function of you like it static"""
    sr = kwargs.pop('sr', True)
    ert = ERTManager(verbose=verbose)
    ert.setSingularityRemoval(sr)

    if isinstance(mesh, str):
        mesh = pg.load(mesh)

    if isinstance(scheme, str):
        scheme = pb.load(scheme)

    return ert.simulate(mesh, res=res, scheme=scheme, verbose=verbose, **kwargs)


class Resistivity(MeshMethodManager):
    """
    Class for managing a resistivity inversion.

    Takes care of the standard setup logistics.
    """
    def __init__(self, filename=None, verbose=True, debug=False, **kwargs):
        """Init function with optional data load."""

        super(Resistivity, self).__init__(verbose=verbose,
                                         debug=debug, **kwargs)  # py2
        # better MeshMethodManager.__init__?
        self.schemetype = kwargs.pop('schemetype', Pseudotype.Gradient)

        # self.data = None  # we hold a onw data container .. necessary? NO
        self.dataToken_ = 'rhoa'  # shouldn't this be a static member?
        self._sr = True

        if filename is not None:
            if isinstance(filename, str):
                self.loadData(filename)
            elif isinstance(filename, pg.DataContainerERT):
                self.setData(filename)

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()

    def __str__(self):
        """Human readable string representation of the class."""
        out = self.__class__.__name__ + " object"
        if hasattr(self, 'data'):
            out += "\n" + self.data.__str__()
        if hasattr(self, 'mesh'):
            out += "\n" + self.mesh.__str__()
        return out

    def setSingularityRemoval(self, sr=True):
        """Turn on singularity removal (should only be used when
        initializing)."""
        self._sr = sr
        self.fop = ERTManager.createFOP(verbose=self.fop.verbose(), sr=sr)

    @staticmethod
    def createFOP(verbose=False, sr=True):
        """ Create forward operator working on refined mesh.

        Parameters
        ----------
        verbose : bool, optional
            Turn verbose output on/off. Is propagated to the fop object.
            Default: False
        sr : bool, optional
            Return a forward operator with singularity removal turned on or
            off. Default: True

        Returns
        -------
        fop: :bertapi:`Bert::DCSRMultiElectrodeModelling` |
        :bertapi:`Bert::pb.DCMultiElectrodeModelling`

        """
        if sr:
            fop = pb.DCSRMultiElectrodeModelling(verbose=verbose)
        else:
            fop = pb.DCMultiElectrodeModelling(verbose=verbose)

        try:
            import psutil  # thread count
            fop.setThreadCount(psutil.cpu_count(logical=False))
        except ImportError:
            pg.warn("Module ps psutil not found.")

        return fop

    def model(self):
        """Return resistivity model (for compatibility)."""
        return self.resistivity

    def createInv(self, fop, verbose=True, dosave=False):
        """ create inversion instance """

        self.tD = pg.trans.TransLog()
        self.tM = pg.trans.TransLogLU()

        inv = pg.core.RInversion(verbose, dosave)
        inv.setTransData(self.tD)
        inv.setTransModel(self.tM)
        inv.setForwardOperator(fop)
        return inv

    def createApparentData(self, data):  # what the hack is this?
        return data('rhoa')

    def loadData(self, filename):
        """" load data from file """
        # check for file formats and import if necessary
        self.setData(pg.DataContainerERT(filename))
        return self.data

    def getDepth(self):
        """ get typical investigation depth """
        return pb.DCParaDepth(self.data)

    def createMesh(self, depth=None, quality=34.3, maxCellArea=0.0,
                   paraDX=0.3, plc=None):
        """ create (inversion)
        WRITEME
        """
        if depth is None:
            depth = self.getDepth()

        if plc is None:
            self.poly = pg.meshtools.createParaMeshPLC(
                self.data.sensorPositions(), paraDepth=depth, paraDX=paraDX,
                paraMaxCellSize=maxCellArea, paraBoundary=2, boundary=2)
        else:
            self.poly = plc

        if self.verbose:
            print("creating mesh...")
        mesh = pg.meshtools.createMesh(self.poly, quality=quality,
                                       smooth=(1, 10))
        mesh.createNeighbourInfos()
        # print(mesh)
        self.setMesh(mesh, refine=True)

        if self.verbose:
            print(self.mesh)
        return mesh

    def setMesh(self, mesh, refine=True, refineP2=False, omitBackground=False):
        """
        -> maybe in base
        """
        if isinstance(mesh, str):
            mesh = pg.load(mesh)

        self.mesh = pg.Mesh(mesh)
        self.mesh.createNeighbourInfos()

        if self.verbose:
            print(mesh)

        self.fop.setMesh(self.mesh)
        self.fop.regionManager().setConstraintType(1)

        if not omitBackground:
            if self.fop.regionManager().regionCount() > 1:
                self.fop.regionManager().region(1).setBackground(True)
#            self.fop.regionManager().regions().begin().second.setBackground(1)

        self.fop.createRefinedForwardMesh(refine, refineP2)
        self.paraDomain = self.fop.regionManager().paraDomain()
        self.inv.setForwardOperator(self.fop)  # necessary?

    def showMesh(self, all=False, ax=None, marker=False):
        """ show mesh in given axes or in a new figure """
        if ax is None:
            fig, ax = plt.subplots()
        if marker:
            drawModel(ax, self.mesh, data=self.mesh.cellMarkers())

        if not all:
            drawMesh(ax, self.paraDomain)
        else:
            drawMesh(ax, self.mesh)
#        plt.show(block=False)

    def setData(self, data):
        """ set data container from outside

        base api

        """
        self.data = data

        # better self.checkData()?
        oldsize = self.data.size()
#        TODO: Set criteria for marking datapoints invalid.
#        self.data.markInvalid(pg.abs(self.data('s') - self.data('g')) < 1)
#        self.data.markInvalid(self.data('t') <= 0.)

        self.data.removeInvalid()
        newsize = self.data.size()
        if newsize < oldsize:
            print('Removed ' + str(oldsize-newsize) + ' values.')

        # prohibit 3D downhole measurements
        # if self.mesh.dim() == 2:

        #     maxYabs = max(pg.abs(pg.y(self.data)))
        #     maxZabs = max(pg.abs(pg.z(self.data)))

        #     if maxZabs > 0 and maxYabs == 0:
        #         pg.info("swapping z to y coordinats for 2d data.")
        #         for i in range(self.data.sensorCount()):
        #             pos = self.data.sensorPosition(i).rotateX(-pi/2)
        #             self.data.setSensorPosition(i, pos)

        if not self.data.allNonZero('rhoa'):
            raise BaseException("No or partial rhoa values.")

        if self.data.allNonZero('err'):
            self.error = self.data('err')
        else:
            pg.info("estimate data error")
            self.error = ERTManager.estimateError(self.data)

        # TODO don't create the mesh here
        # TODO the function calles .. setDate
        # self.createMesh()
        # this forces fallback mode if run is called without prior createMesh
#        self.mesh = None  # very big bullshit
        self.fop.setData(self.data)

    def setPrimPot(self, pot):
        """ set primary potential (string or matrix) and check size """
        if isinstance(pot, str):
            self.fop.setPrimaryPotFileBody(pot)  # workaround
#            self.pot = pg.Matrix(pot)  # somehow not working
        else:
            self.pot = pot
            if self.pot.cols() == self.fop.mesh().nodeCount():
                self.fop.setPrimaryPotential(self.pot)
            else:
                raise Exception('Warning: potential size does not match mesh!')

    def setMeshPot(self, mesh='mesh/mesh.bms', pot=None):
        """ set mesh and potential from outside (mesh/matrix or filename) """
        self.setMesh(mesh)
        if pot is None:
            if self.mesh.dimension() == 3:
                pot = 'primaryPot/pot.bmat'
            else:
                pot = 'primaryPot/pot_s.bmat'
        self.setPrimPot(pot)

    @staticmethod
    def estimateError(data, absoluteError=0.001, relativeError=0.03,
                      absoluteUError=None, absoluteCurrent=0.1):
        """ Estimate error composed of an absolute and a relative part.
        This is a static method and will not alter any member of the Manager

        Parameters
        ----------
        absoluteError : float [0.001]
                Absolute data error in Ohm m. Need 'rhoa' values in data.

        relativeError : float [0.03]
                relative error level in %/100

        absoluteUError : float [0.001]
                Absolute potential error in V. Need 'u' values in data. Or
                calculate them from 'rhoa', 'k' and absoluteCurrent if no 'i'
                is given

        absoluteCurrent : float [0.1]
                Current level in A for reconstruction for absolute potential V

        Returns
        -------
        error : Array
        """

        if relativeError >= 0.5:
            print("relativeError set to a value > 0.5 .. assuming this "
                  "is a percentage Error level dividing them by 100")
            relativeError /= 100.0

        if absoluteUError is None:
            if not data.allNonZero('rhoa'):
                raise BaseException("We need apparent resistivity values "
                                    "(rhoa) in the data to estimate a "
                                    "data error.")
            error = relativeError + absoluteError / data('rhoa')
        else:
            u = None
            i = absoluteCurrent
            if data.haveData("i"):
                i = data('i')

            if data.haveData("u"):
                u = data('u')
            else:
                if data.haveData("r"):
                    u = data('r') * i
                elif data.haveData("rhoa"):
                    if data.haveData("k"):
                        u = data('rhoa') / data('k') * i
                    else:
                        raise BaseException("We need (rhoa) and (k) in the"
                                            "data to estimate data error.")

                else:
                    raise BaseException("We need apparent resistivity values "
                                        "(rhoa) or impedances (r) "
                                        "in the data to estimate data error.")

            error = pg.abs(absoluteUError / u) + relativeError

        return error

    def run(self, **kwargs):  # just for backward-compat (move to MethodMan.)
        """Run inversion. deprecated, use invert instead."""
        self.invert(**kwargs)

    def invert(self, data=None, rhoa=None, err=None, mesh=None, **kwargs):
        """Run the full inversion.

        The data and error needed to be set before.
        The meshes will be created if necessary.

        Parameters
        ----------
        data : pg.DataContainerERT
            The data scheme with 'rhoa' and 'err' data array.
        rhoa : iterable
            Will overwrite data('rhoa')
        err : iterable
            Will overwrite data('err')
        mesh : pg.Mesh
            Inversion mesh, may need the different regions.
            Only 1 region for Neumann domains(no Boundary).
            Two regions (marker 1 and 2) one for the background region and
            one for the inversion domain.

        **kwargs
            * lam : float [20]
                regularization parameter
            * zWeight : float [0.7]
                relative vertical weight
            * maxIter : int [20]
                maximum iteration number
            * robustData : bool [False]
                robust data reweighting using an L1 scheme (IRLS reweighting)
            * blockyModel : bool [False]
                blocky model constraint using L1 reweighting roughness vector
            * startModel : array-like
                starting model
            * startModelIsReference : bool [False]
                startmodel is the reference model for the inversion

            Forwarded to createMesh:

            * depth
            * quality
            * paraDX
            * maxCellArea
        """
        if 'verbose' in kwargs:
            self.setVerbose(kwargs.pop('verbose'))

        if data is not None:
            # setDataContainer would be better
            if rhoa is not None:
                data.set('rhoa', rhoa)
            self.setData(data)

        if rhoa is not None:
            self.data.set('rhoa', rhoa)

        if err is not None:
            self.error = err

        if mesh is not None:
            self.setMesh(mesh,
                         refine=kwargs.pop('refineMesh', True),
                         refineP2=kwargs.pop('refineP2', False),
                         omitBackground=kwargs.pop('omitBackground', False)
                         )

        if self.mesh is None or 'depth' in kwargs or 'paraDX' in kwargs:
            self.createMesh(depth=kwargs.pop('depth', None),
                            quality=kwargs.pop('quality', 34.0),
                            maxCellArea=kwargs.pop('maxCellArea', 0.0),
                            paraDX=kwargs.pop('paraDX', 0.3))

        self.inv.setData(self.data('rhoa'))
        self.inv.setRelativeError(self.error)

        zWeight = kwargs.pop('zWeight', 0.7)
        if 'zweight' in kwargs:
            zWeight = kwargs.pop('zweight', 0.7)
            print("zweight option will be removed soon. Please use zWeight.")

        self.fop.regionManager().setZWeight(zWeight)

        self.inv.setLambda(kwargs.pop('lam', 20))
        self.inv.setMaxIter(kwargs.pop('maxIter', 20))
        self.inv.setRobustData(kwargs.pop('robustData', False))
        self.inv.setBlockyModel(kwargs.pop('blockyModel', False))
        self.inv.setRecalcJacobian(kwargs.pop('recalcJacobian', True))

        # TODO: ADD MORE KWARGS
        pc = self.fop.regionManager().parameterCount()

        startModel = kwargs.pop('startModel',
                                pg.Vector(pc, pg.median(self.data('rhoa'))))

        self.inv.setModel(startModel)

        if kwargs.pop('startModelIsReference', False):
            self.inv.setReferenceModel(startModel)

        # Run the inversion
        if len(kwargs) > 0:
            print(kwargs)
            pg.warn("Warning! There are unknown kwargs arguments.", kwargs)

        model = self.inv.run()
        self.resistivity = model(self.paraDomain.cellMarkers())

        return self.resistivity

    def echoStatus(self):
        """Echo inversion status as known from pygimli core (invisible)."""
        print("Inversion status - iteration number {}".format(self.inv.iter()))
        print("Model: min={:6f} max={:6f}".format(min(self.inv.model()),
                                                  max(self.inv.model())))
        print("Response: min={:6f} max={:6f}".format(min(self.inv.response()),
                                                     max(self.inv.response())))
        print("chi^2={:.3f} rrms={:.2f}".format(self.inv.chi2(),
                                                self.inv.relrms()))

    def coverageDC(self):
        """
        Return coverage vector considering the logarithmic transformation.
        """
        covTrans = pg.coverageDCtrans(self.fop.jacobian(),
                                      1.0/self.inv.response(),
                                      1.0/self.inv.model())
        return np.log10(covTrans / self.paraDomain.cellSizes())

    def standardizedCoverage(self, threshhold=0.01):
        """
        Return standardized coverage vector (0|1) using thresholding.
        """

        coverage = self.coverageDC()
        return 1.0*(np.absolute(coverage) > threshhold)

    def simulate(self, mesh, res, scheme, verbose=False, **kwargs):
        r"""Simulate an ERT measurement.

        Perform the forward task for a given mesh, a resistivity distribution
        (per cell) and return data (apparent resistivity) for a measurement
        scheme.

        This is a static method since it does not interfere with the Managers
        inversion approaches.

        This function can also operate on complex resistivity models, thereby
        computing complex apparent resistivities.

        Parameters
        ----------
        mesh : :gimliapi:`GIMLI::Mesh`
            Mesh to calculate for.

        res : array(mesh.cellCount()) | array(N, mesh.cellCount())
            Resistivity distribution for the given mesh cells can be:
                * single array of len mesh.cellCount()
                * matrix of N resistivity distributions of len mesh.cellCount()
                * res map as [[marker0, res0], [marker1, res1], ...]

        scheme : :bertapi:`Bert::DataContainerERT`
            data measurement scheme

        **kwargs :
            * sr : bool [True]
                Calculate with singularity removal. Recommended only for
                meshes with topography beacause the primary potential must be
                known.

            * calcOnly : bool [False]
                Use fop.calculate instead of fop.response. Usefull if you want
                to force the caluclation of impedances for homogeneous models.
                No noise handling. Solution is put in scheme('u') and
                a dataMap instance will be returned.

            * noiseLevel : float[0.0]
                add normal distributed noise based on
                scheme('err') or on noiseLevel if scheme did not contain 'err'

            * noiseAbs : float[0.0]
                Absolute voltage error in V

            * returnArray : bool [False]
                Return array instead of datacontainer

            * returnFields : bool [False]
                Return matrix of all potential values per injection electrodes.

        Returns
        -------
        rhoa : DataContainerERT | array(N, data.size()) | pg.Matrix(N, nodes)
            Data container with resulting data and errors with noisify = True.
            Matrix of rhoa values (case of resistivity matrix noisify = False).
            In case of a complex valued resistivity model, phase values will be
            returned in the DataContainerERT (see example below), or as an
            additional returned array.

        Examples
        --------
        >>> world = pg.meshtools.createWorld(start=[-20, 0], end=[20, -10],
        >>>                                  layers=[-1,-3])
        >>> mesh = pg.meshtools.createMesh(world, quality=33, area=0.1,
        >>>                                smooth=[1,2])
        >>> rhoMap = [[1, 1.0], [2, 10.0], [3, 1.0]]
        >>> ax, _ = pg.show(mesh, pg.solver.parseArgToArray(rhoMap,
        >>>                 mesh.cellCount(), mesh),
        >>>                 label=r'Resistivity ($\Omega$m)')
        >>> pg.show(mesh, axes=ax)
        >>> scheme = pb.createData(np.linspace(0, 10., 11), schemeName='dd')
        >>> rhoa1 = ERTManager.simulate(mesh, res=rhoMap, scheme=scheme)
        >>> rhoa2 = ERTManager.simulate(mesh, res=pg.solver.parseArgToArray(
        >>>     rhoMap, mesh.cellCount(), mesh), scheme=scheme)
        >>> np.testing.assert_array_equal(rhoa1, rhoa2)
        >>> pb.show(scheme, vals=rhoa1)

        >>> import pybert as pb
        >>> import pygimli as pg
        >>> import pygimli.meshtools as mt
        >>> world = mt.createWorld(start=[-50, 0], end=[50, -50],
        ...                        layers=[-1, -5], worldMarker=True)
        >>> scheme = pb.createData(
        ... elecs=pg.utils.grange(start=-10, end=10, n=21), schemeName='dd')
        >>> for pos in scheme.sensorPositions():
        ... world.createNode(pos)
        ... world.createNode(pos + pg.Pos(0, -0.1))
        >>> mesh = mt.createMesh(world, quality=34)
        >>> rhomap = [
        ...    [1, 100. + 0j],
        ...    [2, 50. + 0j],
        ...    [3, 10.+ 0j],
        ... ]
        >>> ert = pb.ERTManager()
        >>> data = ert.simulate(mesh, res=rhomap, scheme=scheme, verbose=True)
        >>> rhoa = data.get('rhoa').array()
        >>> phia = data.get('phia').array()
        """
        # A local copy of fop is better here so it does not interfere with the
        # Forward operator for any inversion tasks

        useFOPCalculate = kwargs.pop('calcOnly', False)

        fop = self.fop
        fop.setData(scheme)
        fop.setMesh(mesh, ignoreRegionManager=True)

        rhoa = None
        phia = None

        isArrayData = False
        # parse the given res into mesh-cell-sized array
        if hasattr(res[0], '__iter__'):  # ndim == 2
            if len(res[0]) == 2:  # res seems to be a map
                res = pg.solver.parseArgToArray(res, mesh.cellCount(), mesh)
            else:  # probably nData x nCells array
                # better check for array data here
                isArrayData = True

        if not scheme.allNonZero('k') and not useFOPCalculate:
            scheme.set('k', fop.calcGeometricFactor(scheme))

        if isArrayData:
            rhoa = np.zeros((len(res), scheme.size()))
            for i, r in enumerate(res):
                rhoa[i] = fop.response(r)
                if verbose:
                    print(i, "/", len(res), " : ", pg.dur(), "s",
                          "min r:", min(r), "max r:", max(r),
                          "min r_a:", min(rhoa[i]), "max r_a:", max(rhoa[i]))
        else:  # res is single resistivity array
            if len(res) == mesh.cellCount():
                if isinstance(res, pg.CVector):
                    fop.setComplex(1)
                    res = pg.cat(pg.real(res), -pg.abs(pg.imag(res)))
                elif isinstance(res[0], np.complex):
                    fop.setComplex(1)
                    res = pg.cat(res.real, -abs(res.imag))

                if useFOPCalculate:
                    fop.mesh().setCellAttributes(res)
                    dMap = pg.DataMap()
                    fop.calculate(dMap)
                    scheme.set("u", dMap.data(scheme))

                    if kwargs.pop("returnFields", False):
                        return pg.Matrix(fop.solution())
                    return dMap
                else:
                    resp = fop.response(res)

                if fop.complex():
                    rhoa = pg.abs(resp(0, scheme.size()))
                    phia = pg.abs(resp(scheme.size(), -1))
                    # print(min(phia), max(phia))
                else:
                    rhoa = resp
            else:
                print(mesh)
                print("res: ", res)
                raise BaseException("Simulate with wrong resistivity array.")

        ret = pg.DataContainerERT(scheme)
        if not isArrayData:
            ret = pg.DataContainerERT(scheme)
            ret.set('rhoa', rhoa)

            if phia is not None:
                ret.set('phia', phia)
        else:
            ret.set('rhoa', rhoa[0])
            if phia is not None:
                ret.set('phia', phia[0])

        if kwargs.pop("returnFields", False):
            return pg.Matrix(fop.solution())

        noiseLevel = kwargs.pop('noiseLevel', 0)

        if noiseLevel > 0:  # if errors in data noiseLevel=1 just triggers
            if not ret.allNonZero('err'):
                # 1A  and #100µV
                ret.set('err', ERTManager.estimateError(
                    ret,
                    relativeError=noiseLevel,
                    absoluteUError=kwargs.pop('noiseAbs', 1e-4),
                    absoluteCurrent=1)
                )
                print("Data error estimate (min:max) ",
                      min(ret('err')), ":", max(ret('err')))

            rhoa *= 1. + pg.randn(ret.size()) * ret('err')
            ret.set('rhoa', rhoa)

            ipError = None
            if phia is not None:
                if scheme.allNonZero('iperr'):
                    ipError = scheme('iperr')
                else:
                    # np.abs(self.data("phia") +TOLERANCE) * 1e-4absoluteError
                    if noiseLevel > 0.5:
                        noiseLevel /= 100.

                    ipError = ret("phia") * noiseLevel

                    if verbose:
                        print("Data IP abs error estimate (min:max) ",
                              min(ipError), ":", max(ipError))

                phia *= (1. + pg.randn(ret.size()) * noiseLevel)
                ret.set('iperr', ipError)
                ret.set('phia', phia)

        # check what needs to be setup and returned

        if kwargs.pop('returnArray', False):
            if phia is not None:
                return rhoa, phia
            else:
                return rhoa

        return ret

    def show(self, mesh, model):
        """
        Show data in form of apparent resistivity.
        """

    def showData(self, vals=None, ax=None, name='data', **kwargs):
        """
        Show data in form of apparent resistivity.
        """

        if ax is None:
            self.figs[name], ax = plt.subplots()

        if vals is None:
            vals = self.data('rhoa')
        elif type(vals) is str:
            vals = self.data(vals)

#        im = drawDataAsMatrix(ax, self.data, vals, pseudotype=self.schemetype)
        ax = plotERTData(self.data, vals=vals, ax=ax, **kwargs)
#        if 'clim' in kwargs:
#            im.set_clim(kwargs.pop('clim'))

        plt.show(block=False)
        return ax

    def showModel(self, vals=None, ax=None, **kwargs):
        """ Show any vector in new or existing axis.

        Parameters
        ----------

        adjustWorldAxes : bool [True]
            Adjust world axes to y-Depth and x (m) if y max <= 0.
        """
        if vals is None:
            vals = self.resistivity
        logScale = kwargs.pop('logScale', True)
        cMinP, cMaxP = interperc(vals, kwargs.pop('interperc', 3),
                                 islog=logScale)
        cMin = kwargs.pop('cMin', cMinP)
        cMax = kwargs.pop('cMax', cMaxP)

        label = kwargs.pop('label', r"Resistivity ($\Omega$m)")

#        if ax is not None:
#            gci = drawModel(ax, self.paraDomain, data=vals, colorBar=True,
#                            logScale=logScale, cMin=cMin, cMax=cMax, **kwargs)
#
#            labels = ['cMin', 'cMax', 'nLevs', 'orientation']
#            subkwargs = {key: kwargs[key] for key in labels if key in kwargs}
#            cbar = createColorBar(gci, label=label, **subkwargs)
#            browser = CellBrowser(self.paraDomain, vals, ax)
#            browser.connect()
#            plt.show(block=False)
#        else:
#            ax, cbar = pg.show(self.paraDomain, vals, cMin=cMin, cMax=cMax,
#                               logScale=logScale, label=label,
#                               coverage=self.coverageDC(), **kwargs)
#            browser = CellBrowser(self.paraDomain, vals, ax)
#            browser.connect()
        coverage = kwargs.pop('coverage', self.coverageDC())
        ax, cbar = pg.show(self.paraDomain, vals, cMin=cMin, cMax=cMax,
                           logScale=logScale, label=label, ax=ax,
                           coverage=coverage, **kwargs)
        if kwargs.pop('cellBrowser', False):
            browser = CellBrowser(self.paraDomain, vals, ax)
            browser.connect()
        # add axe labels

        if kwargs.pop('adjustWorldAxes', True):
            if self.paraDomain.ymax() <= 0:
                pg.viewer.mpl.adjustWorldAxes(ax)
            else:
                ax.set_xlabel("$x$ (m)")
                ax.set_ylabel("$z$ (m)")
                pg.plt.tight_layout()

        if 'lines' in kwargs:
            plotLines(ax, kwargs['lines'])

        return ax, cbar

    def showResult(self, ax=None, name='result', **kwargs):
        """ Show resulting resistivity vector. """

        if ax is None:
            self.figs[name], ax = plt.subplots()

        return self.showModel(vals=self.resistivity, ax=ax, **kwargs)

    def showCoverage(self, ax=None, name='result', **kwargs):
        """ Show resulting resistivity vector. """

        if ax is None:
            self.figs[name], ax = plt.subplots()

        return self.showModel(ax, self.coverageDC(), **kwargs)

    def showResultAndFit(self, figsize=(10, 15), **kwargs):
        """Show resstivity distribution with data and forward response."""
        fig, ax = plt.subplots(nrows=3, figsize=figsize)  # , sharex=True)
        _, cb = self.showModel(vals=self.resistivity, ax=ax[2], **kwargs)

        clim = cb.get_clim()
        cmap = kwargs.pop('cMap', 'viridis')
        for i, vals in enumerate([self.data('rhoa'), self.inv.response()]):
            self.showData(ax=ax[i], vals=vals, cMin=clim[0], cMax=clim[1],
                          colorBar=False, cMap=cmap)
        fig.tight_layout()
        self.figs['resultFit'] = fig
        pg.plt.pause(0.1)

    def saveResult(self, folder=None, size=(16, 10), **kwargs):
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

        pg.info('Saving resistivity data to: {}'.format(path))

        np.savetxt(path + '/resistivity.vector',
                   self.resistivity)
        np.savetxt(path + '/resistivity-cov.vector',
                   self.coverageDC())
        np.savetxt(path + '/resistivity-scov.vector',
                   self.standardizedCoverage())

        self.paraDomain.addExportData('Resistivity', self.resistivity)
        self.paraDomain.addExportData('Resistivity (log10)',
                                      np.log10(self.resistivity))
        self.paraDomain.addExportData('Coverage', self.coverageDC())
        self.paraDomain.addExportData('S_Coverage',
                                      self.standardizedCoverage())
        self.paraDomain.exportVTK(path + 'resistivity')
        self.mesh.save(path + 'resistivity-mesh')
        self.paraDomain.save(path + 'resistivity-pd')

        if self.paraDomain.dim() == 2:
            fig, ax = plt.subplots()
            fig.set_size_inches(size)

            self.showModel(vals=self.resistivity, ax=ax, **kwargs)
            fig.savefig(path + '/resistivity.pdf')

            return path, fig, ax
        return path


def test():
    """ run some test that checks the functionality """
    pass


def main(argv):
    """Main function for direct calling with data file (and options)."""

    # if len(argv) == 1:
    # datafile = 'ESSnotopo.data'
    # else:
    # datafile = argv[1]

    parser = ERTManager.createArgParser(dataSuffix='dat')
    options = parser.parse_args()
    kwargs = options.__dict__

    verbose = not kwargs.pop('quiet')

    if verbose:
        print(options.__dict__)

    ert = ERTManager(verbose=verbose, debug=pg.debug())

    ert.loadData(kwargs.pop('dataFileName'))
    ert.invert(**kwargs)

#    print(res)
#    res.showData()

#    res.createMesh(quality=34.8, maxCellArea=50.0)
#    res.showMesh(all=False)

    ert.saveResult()
#    ert.showResultAndFit()
#    ax, cbar = ert.showResult(cMin=10, cMax=1000, logScale=True)


if __name__ == '__main__':
    main(sys.argv)
    pg.wait()
