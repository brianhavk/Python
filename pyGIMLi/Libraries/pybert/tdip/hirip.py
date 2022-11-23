"""Class for managing HIRIP data based on TDIP data."""
import numpy as np
import matplotlib.pyplot as plt
import pygimli as pg
import pygimli.meshtools as mt
import pybert as pb
from .tdipdata import TDIP
from pybert.tdip.mipmodelling import DCIPMModelling


class HIRIP(TDIP):
    """Manager for HIRIP (high-resolution induced polarasation) data.

    A HIRIP survey usually consists of a separated transmitter (Tx) and
    receiver (Rx) line, typically with a distance of several electrode spacings
    like 50-100m whereas electrode spacing is usually 10-20m.
    The class uses the TDIPdata class to hold the data, and can therefore be
    initialized by any supported data format.
    """

    def __init__(self, *args, **kwargs):
        """Initialize with possible data file."""
        super().__init__(*args, **kwargs)
        if max(self.data["a"]) < 0:  # all remote
            self.data.set('a', self.data('b'))  # take a for b
            self.data.set('b', self.data('b') * 0 - 1)  # set b to zero

        self.fitDataDecays()
        self.mesh2d = None
        self.A = np.array([[1, 0], [0, 1]])
        self.origin = [0, 0]
        self.remotePole = [-1000, -1000]
        self.irx = np.unique(self.data["a"])
        if "positions" in kwargs:
            self.loadPositions(kwargs["positions"],
                               rotate=kwargs.pop("rotate", True),
                               topo=kwargs.pop("topo", False),
                               angle=kwargs.pop("angle", None))

    # def __repr__(self):
    #     """Readable representation of class instance."""
    #     return "\n".join([super().__repr__(), "full"+self.datag.__str__()])

    def loadPositions(self, xlsfile=None, rotate=True, topo=0, angle=None):
        """Set positions from Excel file."""
        import pandas as pd
        self.data2d = pg.DataContainerERT(self.data)  # make a copy
        A = pd.read_excel(xlsfile)  # consider using openpyxl
        ex = np.array(A["UTM_east"])
        ey = np.array(A["UTM_north"])
        if "elevation" in A:
            ez = A["elevation"]
        elif "z" in A:
            ez = A["z"]
        else:
            raise ImportError("no elevation found")

        self.ez = np.array(ez)
        self.irx = np.nonzero(pg.y(self.data) == 0)[0]
        self.itx = np.nonzero(pg.y(self.data))[0]
        for i, ir in enumerate(self.irx):
            self.data.setSensor(ir, pg.Pos(ex[i], ey[i], self.ez[i]))

        for i, it in enumerate(self.itx):
            j = len(self.irx) + 1 + i
            self.data.setSensor(it, pg.Pos(ex[j], ey[j], self.ez[j]))

        irp = len(self.irx)
        self.remotePole = [ex[irp], ey[irp], self.ez[irp]]
        self.data.createSensor([hirip.remotePole[0], hirip.remotePole[1], 0])
        self.data["b"] = pg.Vector(self.data.size(), self.data.sensorCount()-1)

        # INCLUDE REMOTE POLE!!!!!
        self.data.set('k', pg.core.geometricFactors(self.data))

        self.data["rhoa"] = self.data["u"] / self.data["i"] * self.data["k"]
        self.exG = ex
        self.eyG = ey
        if rotate:
            self.rotateCoordinates(topo=topo, angle=angle)

    def electrodePositions(self, original=False):
        """Retrieve electrode positions in rotated or original cordinates."""
        ex = pg.x(self.data)
        ey = pg.y(self.data)
        if original:
            ex, ey = np.transpose(self.A).dot(np.vstack((ex, ey)))
            ex += self.origin[0]
            ey += self.origin[1]

        return ex, ey

    def showPositions(self, original=False, save=False, ext="pdf", ax=None):
        """Show positions."""
        ex, ey = self.electrodePositions(original=original)
        rx, ry = self.remotePole[0:2]
        if original:
            rx, ry = np.transpose(self.A).dot(np.vstack((rx, ry)))
            rx += self.origin[0]
            ry += self.origin[1]

        if ax is None:
            fig, ax = plt.subplots()

        ax.plot(ex[self.irx], ey[self.irx], "r+-", label="Rx")
        ax.plot(ex[self.itx], ey[self.itx], "bx", label="Tx")
        ax.plot(rx, ry, "go", label="remote")
        ax.set_aspect(1.0)
        ax.grid(True)
        ax.legend()
        if save:
            outname = self.basename+"-position"
            if original:
                outname += "Org"

            ax.figure.savefig(outname+"."+ext, bbox_inches="tight", dpi=300)

        return ax

    def rotateCoordinates(self, topo=0, angle=None):
        """Rotate the coordinates to quasi-2D.

        Parameters
        ==========
        topo : float
            Topographical factor for amplification (0 for flat)
        angle : float | None
            angle for rotation of coordinate system (None: fitting line)
        """
        ex = pg.x(self.data)[self.irx]
        ey = pg.y(self.data)[self.irx]
        self.origin = np.array([ex[0], ey[0]])  # first electrode of rx line
        ex -= ex[0]
        ey -= ey[0]

        if angle is not None:
            ang = angle * np.pi / 180
        else:
            # ang = np.arctan2(sum(ex*ey)/sum(ex*ex), 1)  # rad
            ang = np.median(np.arctan2(ey, ex))

        self.A = np.array([[np.cos(ang), np.sin(ang)],
                           [-np.sin(ang), np.cos(ang)]])
        ex1, ey1 = self.A.dot([ex[1], ey[1]])
        if ex1 < 0:
            ang += np.pi
            self.A = np.array([[np.cos(ang), np.sin(ang)],
                               [-np.sin(ang), np.cos(ang)]])

        pos = np.vstack((pg.x(self.data)-self.origin[0],
                         pg.y(self.data)-self.origin[1]))
        ex, ey = self.A.dot(pos)
        rx, ry = self.A.dot(np.array(self.remotePole[:2])-self.origin)
        self.remotePole[:2] = rx, ry
        self.ez = pg.z(self.data)
        ez = self.ez * topo
        for i in range(len(ex)):
            self.data.setSensorPosition(i, pg.Pos(ex[i], ey[i], ez[i]))

        self.ex = ex

    def reduceDataNotAnymore(self):
        """Set or load data as TDIP data."""
        self.data.set('rhoa', pg.abs(self.data('r') * self.data('k')))
        # make sure apparent resistivity is positive
        self.dataOrg = pg.DataContainerERT(self.data)  # make a copy
        # holds local (survey) coordinate system
        data = self.data  # save typing (no copy!)
        data.set('a', data('b'))  # take a for b
        data.set('b', data('b') * 0 - 1)  # set b to zero
        data.removeUnusedSensors()  # get rid of
        for i, pos in enumerate(data.sensorPositions()):
            data.setSensorPosition(i, [pos.x(), 0])  # use only x value

        # make electrode positions unique
        ex = pg.x(data).array()
        ux, ii, jj = np.unique(ex, return_index=True, return_inverse=True)
        for tok in ['a', 'm', 'n']:
            data.set(tok, jj[[int(ai) for ai in data(tok)]])

        for i, xi in enumerate(ux):
            data.setSensor(i, [xi, 0])

        data.removeUnusedSensors()
        data.set('k', pg.core.geometricFactors(data))

    def showGeometricEffect(self):
        """Show geometric effect, i.e. relation of 2D/3D geometric factor."""
        geomeffect = pg.abs(self.data2d('k')/self.data('k'))
        pb.show(self.data, geomeffect)

    def filter(self, **kwargs):
        """Filter some data. See documentation of pybert.TDIPdata.

        Parameters
        ----------
        tmin, tmax : double
            minimum/maximum time (gate center) in s
        rmin, rmax : double
            minimum/maximum apparent resistivity in Ohmm
        kmax : double
            maximum (absolute) geometric factor in m
        emax : double
            maximum error in percent
        m0min, m0max : double
            minimum/maximum (fitted) initial chargeability
        taumin, taumax : double
            minimum/maximum (fitted) time constant
        fitmax : double
            maximum exponential fit
        electrode : int
            electrode to be removed completely
        a/b/m/n : int
            delete data with specific current or potential electrode
        ab/mn : int
            delete data with specific current or potential dipole lengths
        corrSID: int [1]
            correct sensor index (like in data files)
        nr : iterable of ints []
            data indices to delete
        forward : bool
            keep only forward-directed measurements
        """
        ind = super().filter(**kwargs)  # do filtering also on 2d datacontainer
        if 0:
            self.data2d.set('valid', pg.Vector(self.data2d.size()))
            self.data2d.markValid(pg.find(ind))  # something wrong
            self.data2d.removeInvalid()
        print(self.data, self.data2d)

    def create2DMesh(self, **kwargs):
        """Create 2D mesh."""
        ex = pg.x(self.data)[self.irx]
        ez = pg.z(self.data)[self.irx]
        pos = [pg.Pos(ex[i], ez[i]) for i in range(len(ex))]
        # ez = pg.z(self.data)[np.argsort(ex)]
        # ex = np.sort(ex)
        self.mesh2d = pg.meshtools.createParaMesh(pos, **kwargs)
        self.ERT = pg.physics.ERTManager()
        self.ERT.data = self.data2d
        self.ERT.setMesh(self.mesh2d)
        self.ERT.fop.region(1).setBackground(True)
        self.ERT.fop.createConstraints()
        self.pd = self.ERT.fop.paraDomain
        if kwargs.pop('show', False):
            pg.show(self.mesh2d)

    def create3DMesh(self, mesh2d=None, y=None):
        """Create 3D triangular prism mesh."""
        if mesh2d is None:
            if self.ERT is not None:
                self.mesh2d = pg.Mesh(self.ERT.mesh)
            else:
                if self.mesh2d is None:
                    self.create2DMesh()
        else:
            self.mesh2d = pg.Mesh(mesh2d)  # make a copy
        # remove all electrode marker (becoming edges)
        for node in self.mesh2d.nodes():
            node.setMarker(0)  # remove electrode marker

        if max(self.mesh2d.cellMarkers()) < 3:
            ma = 1
            # self.fop2d = pg.core.DCSRMultiElectrodeModelling(
            #     self.mesh2d, self.data2d)
            for cell in self.mesh2d.cells():
                if cell.marker() == 2:
                    ma += 1
                    cell.setMarker(ma)
                else:
                    cell.setMarker(1)

        # self.pd = pg.Mesh(2)
        # self.pd.createMeshByMarker(self.mesh2d, 2, 9999)
        # prolong 2D mesh into third dimension
        self.maxMarker = ma
        if y is None:
            dy = pg.median(np.diff(pg.x(self.data))) * 0.5  # de*paraDX
            yPos = np.unique(pg.y(self.data))
            # dist = min(np.diff(yPos))
            yVec = np.arange(yPos[0]-dy, yPos[-1]+dy+.1, dy)
            prol = pg.utils.niceLogspace(dy, dy*40, 4)
            y = np.hstack((yVec[0]-np.flipud(prol), yVec, yVec[-1]+prol))
        elif len(y) < 4:  # just a few values
            plc3d = pg.core.createMesh3D(
                self.mesh2d, y, pg.core.MARKER_BOUND_MIXED,
                pg.core.MARKER_BOUND_MIXED)

            self.mesh3d = mt.createMesh(plc3d)
            self.mesh3d.swapCoordinates(1, 2)  # make y to z and vice versa
            print(self.mesh3d)

        self.mesh3d = pg.core.createMesh3D(
            self.mesh2d, y, pg.core.MARKER_BOUND_MIXED,
            pg.core.MARKER_BOUND_MIXED)

        self.mesh3d.swapCoordinates(1, 2)  # make y to z and vice versa
        print(self.mesh3d)
        nout = 0
        for cell in self.mesh3d.cells():
            cy = cell.center().y()
            if cy > yVec[-1] or cy < yVec[0]:
                cell.setMarker(1)
                nout += 1

        self.mesh3d.exportVTK('mesh3d.vtk')

    def invert3d(self, **kwargs):
        """Carry out hybrid inversion using 2D inverse and 3D forward mesh."""
        # define a 3D forward modelling operator with 3D data
        self.fop3d = pg.core.DCSRMultiElectrodeModelling(self.mesh3d,
                                                         self.data)
        self.tM = pg.trans.RTransLog()
        if "limits" in kwargs:
            self.tM = pg.trans.RTransLogLU(*kwargs["limits"])

        self.tD = pg.trans.TransLog()
        if kwargs.pop("dataLinear", False):
            self.tD = pg.trans.Trans()

        self.inv3d = pg.core.RInversion(self.data('rhoa'), self.fop3d,
                                        self.tD, self.tM, True, False)
        self.fop3d.region(1).setBackground(True)
        self.fop3d.createRefinedForwardMesh(False, False)
        if 'C' in kwargs:
            C = kwargs['C']
        else:
            C = self.ERT.fop.createConstraints()
            C = self.ERT.fop.constraints()
            print(C.rows(), C.cols(), C.nVals())

        self.fop3d.setConstraints(C)
        self.cW = pg.Vector(C.rows(), 1.0)
        self.inv3d.setCWeight(self.cW)
        # self.inv3d.setConstraintsH(self.cW*0)
        self.inv3d.setRelativeError(kwargs.pop('err', 0.03))
        startModel = pg.Vector(C.cols(), pg.median(self.data('rhoa')))
        self.inv3d.setModel(startModel)
        self.inv3d.setRobustData(kwargs.pop('robustData', False))
        self.inv3d.setBlockyModel(kwargs.pop('blockyModel', False))
        self.inv3d.setLambda(kwargs.pop('lam', 30))
        self.fop3d.regionManager().setZWeight(kwargs.pop('zWeight', 0.5))
        self.res = self.inv3d.run()
        pg.info("ERT chi^2={:.1f}, rrms={:.1f}%".format(self.inv3d.chi2(),
                                                        self.inv3d.relrms()))

    def invertMa(self, *args, **kwargs):
        """Invert single apparent chargeability."""
        super().invertMa(*args, fop=self.fop3d, mesh=self.pd,
                         **kwargs)

    def invertMa3d(self, nr=0, *args, **kwargs):
        """Invert single apparent chargeability."""
        res = self.inv3d.model()
        fIP = DCIPMModelling(self.fop3d, self.pd, res)
        if nr > 0:
            ma = self.MA[:, nr-1]
        else:
            ma = self.data["m0"] / 1000

        maerr = kwargs.pop('maerr', 0.01)
        fIP.regionManager().setZWeight(kwargs.pop('zWeight', 1.0))
        fIP.createRefinedForwardMesh(False)
        tD, tM = pg.trans.TransLog(), pg.core.RTransLogLU(0, 0.99)
        INV = pg.core.RInversion(ma, fIP, tD, tM, True, False)
        mstart = pg.Vector(len(res), pg.median(ma))
        INV.setModel(mstart)
        INV.setAbsoluteError(maerr)
        INV.setLambda(kwargs.pop('lam', 100))
        INV.setRobustData(kwargs.pop('robustData', False))
        INV.setBlockyModel(kwargs.pop('blockyModel', False))
        self.m = INV.run()
        self.mafwd = INV.response()

    def showDataFit(self, **kwargs):
        """Show apparent resistivity/chargeability data, response & misfit."""
        rmin = kwargs.pop("rmin", min(self.data["rhoa"]))
        rmax = kwargs.pop("rmax", max(self.data["rhoa"]))
        fig, ax = pg.plt.subplots(nrows=3, ncols=2, figsize=(12, 12))
        rkw = dict(cMin=rmin, cMax=rmax, logScale=True, am=1,
                   cMap="Spectral_r", label=r"$\rho_a$ ($\Omega$m)")
        pb.show(self.data, ax=ax[0, 0], **rkw)
        pb.show(self.data, self.inv3d.response(), ax=ax[1, 0], **rkw)
        misfit = self.inv3d.response() / self.data["rhoa"] * 100 - 100
        mm = np.max(np.abs(misfit))
        pb.show(self.data, misfit, ax=ax[2, 0], cMin=-mm, cMax=mm, cMap="bwr",
                am=1, label="misfit (%)")
        mdata = self.data["m0"]
        mresp = self.mafwd*1000
        mmin = kwargs.pop("rmin", min(mdata))
        mmax = kwargs.pop("rmax", max(mresp))
        mkw = dict(cMin=mmin, cMax=mmax, logScale=False, am=1, cMap="plasma",
                   label=r"$m_a$ (mV/V)")
        pb.show(self.data, mdata, ax=ax[0, 1], **mkw)
        pb.show(self.data, mresp, ax=ax[1, 1], **mkw)
        misfit = mresp - mdata
        mm = np.max(np.abs(misfit))
        pb.show(self.data, misfit, ax=ax[2, 1], cMin=-mm, cMax=mm,
                cMap="bwr", am=1, label="misfit (mV/V)")

        pg.info("ERT chi^2={:.1f}, rrms={:.1f}%".format(self.inv3d.chi2(),
                                                        self.inv3d.relrms()))
        pg.info("IP RMS={:.1f} mV/V".format(np.sqrt(np.mean(misfit**2))))
        return ax

    def simultaneousInversion_(self, *args, **kwargs):
        """Invert single apparent chargeability."""
        super().simultaneousInversion(*args, fop=self.fop3d, **kwargs)

    def paraDomainTopo(self):
        """Return parameter domain with topography."""
        pd = pg.Mesh(self.pd)
        mx = pg.x(pd.positions())
        mz = pg.y(pd.positions())
        if np.isclose(max(mz), 0):
            mt = np.interp(mx, self.ex[self.irx], self.ez[self.irx])
            for i, node in enumerate(pd.nodes()):
                node.setPos(node.pos() + pg.Pos(0, mt[i]))

        return pd

    def saveResults(self, *args, **kwargs):
        """Save result to file."""
        if self.M is None:
            self.M = np.reshape(self.m, (-1, 1))

        super(*args, **kwargs)

    def export3DVTK(self, pd=None, topo=0, method=None):
        """Export VTK using 3D coordinates.

        Parameters
        ----------
        The shift and rotate matrix is used to project the result
        """
        if pd is None:
            if topo:
                pd = self.paraDomainTopo()
            else:
                pd = self.pd

        pd3d = pg.Mesh(pd)
        pd3d.setDimension(3)
        mx2 = pg.x(pd.positions())
        mz = pg.y(pd.positions())
        if method == "Rx":  # interpolate on Rx line
            exG, eyG = self.electrodePositions(original=True)
            ex = pg.x(self.data)
            mx = np.interp(mx2, ex[self.irx], exG[self.irx])
            my = np.interp(mx2, ex[self.irx], eyG[self.irx])
        else:  # use rotation matrix and offset generating a line
            mx, my = np.transpose(self.A).dot(np.vstack((
                mx2, np.zeros_like(mx2))))
            mx += self.origin[0]
            my += self.origin[1]

        for i in range(pd.nodeCount()):
            pd3d.node(i).setPos(pg.Pos(mx[i], my[i], mz[i]))

        pd3d["res"] = self.res
        pd3d["m"] = self.m*1000
        pd3d.exportVTK(self.basename+'-result3d.vtk')

    def exportASCII(self, method=""):
        """Export to some ascii format containing: E, N, z, res, ip."""
        pd = self.paraDomainTopo()
        mx2 = pg.x(pd.cellCenters())
        mz = pg.y(pd.cellCenters())
        if method == "Rx":  # interpolate on Rx line
            exG, eyG = self.electrodePositions(original=True)
            ex = pg.x(self.data)
            mx = np.interp(mx2, ex[self.irx], exG[self.irx])
            my = np.interp(mx2, ex[self.irx], eyG[self.irx])
        else:  # use rotation matrix and offset generating a line
            mx, my = np.transpose(self.A).dot(np.vstack((
                mx2, np.zeros_like(mx2))))
            mx += self.origin[0]
            my += self.origin[1]
        A = np.column_stack((mx2, mz, mx, my, self.res, self.m*1000))
        np.savetxt(self.basename+'.csv', A, delimiter="\t", fmt="%.2f",
                   header="x2d(m)\tz_(m)\tx_(m)\ty_(m)\tres(Ohmm)\tm(mV/V)")


if __name__ == '__main__':
    hirip = HIRIP('datafile.bin')
    # hirip.generateDataPDF(showFit=True, ylim=[1, 50], basename='')
    print(hirip)
    hirip.filter(fitmax=0.3, rmin=20)
    hirip.invertRhoa(err=0.03)  # , maxIter=1)
    rdict = dict(label='resistivity', cMap='Spectral_r', cMin=100, cMax=3000)
    ax2, cb = hirip.showResistivity(**rdict)
    # ax2.figure.savefig('inv2d.pdf', bbox_inches='tight')
    hirip.create3DMesh()  # mesh2d=hirip.ERT.mesh)
    model = hirip.invert3d()
    ax3, cb = pg.show(hirip.pd, model, **rdict)
    # ax3.figure.savefig('inv3d.pdf', bbox_inches='tight')
    # hirip.invertMa_(show=True)
    hirip.simultaneousInversion_()

    hirip.saveResults()
    hirip.fitModelDecays(useColeCole=True)
    hirip.showColeColeResults(rlim=(50, 3000), mlim=(5, 50),
                              tlim=(0.5, 4.0), clim=(0, 1))
