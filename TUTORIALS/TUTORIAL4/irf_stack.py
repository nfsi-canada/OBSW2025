# python stack_invert.py --no-outlier --bp=0.05,0.5 --stacked --trange=-5.,10. MMPY.pkl

# Import modules and functions
# Seismo-related 
import stdb
from obspy import Stream, UTCDateTime
from rfpy import binning
from telewavesim import utils as ut

# System interaction
from pathlib import Path
from argparse import ArgumentParser
from os.path import exists as exist
from joblib import Parallel, delayed
import multiprocessing
import time

# I/O and visuals
import matplotlib.pyplot as plt
import pickle

# Computation
import numpy as np
import scipy.optimize as spo
from scipy.special import comb
from scipy.linalg import toeplitz
from sklearn.neighbors import KernelDensity as KDE


def get_arguments(argv=None):
    """
    Get command-line arguments from :class:`~argparse.ArgumentParser` objects.

    """

    parser = ArgumentParser(
        usage="%(prog)s [arguments] <station database>",
        description="Script used to plot receiver function data ")

    # General Settings
    parser.add_argument(
        "indb",
        help="Station Database to process from.",
        type=str)
    parser.add_argument(
        "--keys",
        action="store",
        type=str,
        dest="stkeys",
        default="",
        help="Specify a comma separated list of station keys for " +
        "which to perform the analysis. These must be " +
        "contained within the station database. Partial keys will " +
        "be used to match against those in the dictionary. For " +
        "instance, providing IU will match with all stations in " +
        "the IU network [Default processes all stations in the database]")
    parser.add_argument(
        "-v", "-V", "--verbose",
        action="store_true",
        dest="verb",
        default=False,
        help="Specify to increase verbosity.")
    parser.add_argument(
        "-L", "--long-name",
        action="store_true",
        dest="lkey",
        default=False,
        help="Force folder names to use long-key form (NET.STN.CHN). " +
        "Default behaviour uses short key form (NET.STN) for the folder " +
        "names, regardless of the key type of the database.")

    PreGroup = parser.add_argument_group(
        title='Pre-processing Settings',
        description="Options for pre-processing of receiver function " +
        "data before plotting")
    PreGroup.add_argument(
        "--snr",
        action="store",
        type=float,
        dest="snr",
        default=-9999.,
        help="Specify the vertical component SNR threshold for " +
        "extracting receiver functions. [Default 5.]")
    PreGroup.add_argument(
        "--snrh",
        action="store",
        type=float,
        dest="snrh",
        default=-9999.,
        help="Specify the horizontal component SNR threshold for " +
        "extracting receiver functions. [Default None]")
    PreGroup.add_argument(
        "--cc",
        action="store",
        type=float,
        dest="cc",
        default=-1.,
        help="Specify the CC threshold for extracting receiver functions. " +
        "[Default None]")
    PreGroup.add_argument(
        "--no-outlier",
        action="store_true",
        dest="no_outl",
        default=False,
        help="Set this option to delete outliers based on the MAD " +
        "on the variance. [Default False]")
    PreGroup.add_argument(
        "--bp",
        action="store",
        type=str,
        dest="bp",
        default=None,
        help="Specify the corner frequencies for the bandpass filter. " +
        "[Default 0.05, 0.5]")
    PreGroup.add_argument(
        "--phase",
        action="store",
        type=str,
        dest="phase",
        default='allP',
        help="Specify the phase name to plot.  " +
        "Options are 'P', 'PP', 'allP', 'S', 'SKS' or 'allS'. " +
        "[Default 'allP']")

    ModelGroup = parser.add_argument_group(
        title='Model and estimation Settings',
        description="Model parameters, ensemble size and available CPUs " +
        "for the calculations")
    ModelGroup.add_argument(
        "--nlay",
        action="store",
        type=int,
        dest="nlay",
        default=30,
        help="Number of layers in model. [Default 20]")
    ModelGroup.add_argument(
        "--zmax",
        action="store",
        type=float,
        dest="zmax",
        default=60.,
        help="Maximum depth of model. [Default 100.]")
    ModelGroup.add_argument(
        "--nens",
        action="store",
        type=int,
        dest="nens",
        default=20,
        help="Number of inversions in the ensemble. [Default 20]")
    ModelGroup.add_argument(
        "--ncores",
        action="store",
        type=int,
        dest="ncores",
        default=None,
        help="Number of cores to use. [Default total number of " + 
        "CPUs on computer]")

    PlotGroup = parser.add_argument_group(
        title='Plot Settings',
        description="Options for plot format")
    PlotGroup.add_argument(
        "--trange",
        action="store",
        default=None,
        type=str,
        dest="trange",
        help="Specify the lag range for the x-axis (sec). Negative lags " +
        "are allowed [Default -5., 25.]")
    PlotGroup.add_argument(
        "--save",
        action="store_true",
        dest="saveplot",
        default=False,
        help="Set this option if you wish to save the figure. [Default " +
        "does not save figure]")

    args = parser.parse_args(argv)

    # Check inputs
    if not exist(args.indb):
        parser.error("Input file " + args.indb + " does not exist")

    if args.phase not in ['P', 'PP', 'allP', 'S', 'SKS', 'allS']:
        parser.error(
            "Error: choose between 'P', 'PP', 'allP', 'S', 'SKS' and 'allS'.")
    if args.phase == 'allP':
        args.listphase = ['P', 'PP']
    elif args.phase == 'allS':
        args.listphase = ['S', 'SKS']
    else:
        args.listphase = [args.phase]

    if args.bp is not None:
        args.bp = [float(val) for val in args.bp.split(',')]
        args.bp = sorted(args.bp)
        if (len(args.bp)) != 2:
            parser.error(
                "Error: --bp should contain 2 " +
                "comma-separated floats")
    else:
        args.bp = [0.05, 0.5]

    if args.trange is None:
        args.trange = [-5., 25.]
    else:
        args.trange = [float(val) for val in args.trange.split(',')]
        args.trange = sorted(args.trange)
        if (len(args.trange)) != 2:
            parser.error(
                "Error: --trange should contain 2 " +
                "comma-separated floats")

    # create station key list
    if len(args.stkeys) > 0:
        args.stkeys = args.stkeys.split(',')

    return args


def pred_rf(vs, depth, vp, slow, f1, f2, npts, dt):

    # Model parameters
    nlay = len(vp)
    thick = np.ones(nlay)*(depth[1] - depth[0]) # Constant thickness layers
    dens = 2350. + 36.*(vp - 3.)**2 # Density parameterization from Tkalčić et al. (2006)
    flags = []; [flags.append('iso') for i in range(nlay)]

    # Telewavesim Model
    model = ut.Model(thick, dens, vp, vs, flags)

    # Calculate xyz traces
    trxyz = ut.run_plane(model, slow, npts, dt)

    # Get radial transfer function
    rf_pred = ut.tf_from_xyz(trxyz, pvh=False)[0]

    # Receiver functions (filtered transfer functions)
    rf_pred.filter('bandpass', freqmin=f1, freqmax=f2, zerophase=True, corners=2)

    return rf_pred


def misfit(vs, stack, Cerr, depth, vp, slow, f1, f2):

    # Trace parameters
    npts = stack.stats.npts
    dt = stack.stats.delta

    # degrees of freedom
    dof = npts - len(vp)

    # Get predicted RF
    rf_pred = pred_rf(vs, depth, vp, slow, f1, f2, npts, dt)

    # Extract quantities for cost function
    y_pred = rf_pred.data
    y_obs = stack.data
    y_err = np.sqrt(np.diag(Cerr))
    resid = y_obs - y_pred

    # Cost function 
    cost = np.sum(resid**2/y_err)/dof

    return cost


def smoothstep(x, x_min=0, x_max=1, N=1):
    x = np.clip((x - x_min) / (x_max - x_min), 0, 1)

    result = 0
    for n in range(0, N + 1):
         result += comb(N + n, n) * comb(2 * N + 1, N - n) * (-x) ** n

    result *= x ** (N + 1)

    return result


def minimize_parallel(stack, Cerr, depth, vp, slow, f1, f2, nn, dt, i):

    print('Loop #', i)

    nlay = len(depth)

    # Small random perturbations to Vp (std = 0.2 km/s)
    vp_ = vp + np.random.normal(scale=0.2, size=nlay)

    # Starting Vs model: scaled vp 
    vs_start = vp_/1.78 

    # Bounds on Vs
    bnds = tuple([(1., 4.5) for i in range(nlay)])

    # Constraint on deep Vs
    def con(t):
        return t[-1] - 7.8/1.76
    cons = {'type': 'eq', 'fun': con}

    # Minimize the misfit
    res = spo.minimize(misfit, vs_start, 
        args=(stack, Cerr, depth, vp_, slow, f1, f2), 
        bounds=bnds, constraints=cons,
        method='SLSQP')
    
    # Global optimization - very slow!!
    # res = spo.shgo(misfit, bnds, 
    #     args=(stack, Cerr, depth, vp_, slow, f1, f2))

    # Predict RF from best fit solution
    rf_pred = pred_rf(res.x, depth, vp_, slow, f1, f2, nn, dt)

    vpvs = vp_/res.x

    return res.x, vpvs, rf_pred.data


def main():

    # Run Input Parser
    args = get_arguments()

    # Load Database
    db, stkeys = stdb.io.load_db(fname=args.indb, keys=args.stkeys)

    # Path to folder containing plots
    plotpath = Path('PLOTS')
    if args.saveplot and not plotpath.is_dir():
        plotpath.mkdir(parents=True)
    respath = Path('RESULTS')
    if args.saveplot and not respath.is_dir():
        respath.mkdir(parents=True)

    # Loop over station keys
    for stkey in list(stkeys):

        # Extract station information from dictionary
        sta = db[stkey]

        # Construct Folder Name
        stfld = stkey
        if not args.lkey:
            stfld = stkey.split('.')[0]+"."+stkey.split('.')[1]

        # Define path to see if it exists
        if args.phase in ['P', 'PP', 'allP']:
            datapath = Path('P_DATA') / stfld
        elif args.phase in ['S', 'SKS', 'allS']:
            datapath = Path('S_DATA') / stfld
        if not datapath.is_dir():
            print('Path to ' + str(datapath) + ' doesn`t exist - continuing')
            continue

        # Temporary print locations
        tlocs = sta.location
        if len(tlocs) == 0:
            tlocs = ['']
        for il in range(0, len(tlocs)):
            if len(tlocs[il]) == 0:
                tlocs[il] = "--"
        sta.location = tlocs

        # Update Display
        print(" ")
        print("|===============================================|")
        print("|                   {0:>8s}                    |".format(
            sta.station))
        print("|===============================================|")
        print("|  Station: {0:>2s}.{1:5s}                            |".format(
            sta.network, sta.station))
        print("|      Channel: {0:2s}; Locations: {1:15s}  |".format(
            sta.channel, ",".join(tlocs)))
        print("|      Lon: {0:7.2f}; Lat: {1:6.2f}                |".format(
            sta.longitude, sta.latitude))
        print("|-----------------------------------------------|")

        # Initialize empty stream to store the RFs - only radial here
        rfRstream = Stream()

        # March down data folders
        datafiles = [x for x in datapath.iterdir() if x.is_dir()]
        for folder in datafiles:

            # Skip hidden folders
            if folder.name.startswith('.'):
                continue

            # Load meta data
            filename = folder / "Meta_Data.pkl"
            if not filename.is_file():
                continue
            metafile = open(filename, 'rb')
            meta = pickle.load(metafile)
            metafile.close()

            # Skip data not in list of phases
            if meta.phase not in args.listphase:
                continue

            # QC Thresholding
            if meta.snrh < args.snrh:
                continue
            if meta.snr < args.snr:
                continue
            if meta.cc < args.cc:
                continue

            # If everything passed, load the RF data
            filename = folder / "RF_Data.pkl"
            if filename.is_file():
                file = open(filename, "rb")
                rfdata = pickle.load(file)
                if args.phase in ['P', 'PP', 'allP']:
                    Rcmp = 1
                    Tcmp = 2
                elif args.phase in ['S', 'SKS', 'allS']:
                    Rcmp = 1
                    Tcmp = 2
                rfRstream.append(rfdata[Rcmp])
                file.close()

        if len(rfRstream) == 0:
            continue

        # Outlier removal based on total variance within selected time range
        if args.no_outl:

            varR = []
            for i in range(len(rfRstream)):
                taxis = rfRstream[i].stats.taxis
                tselect = (taxis > args.trange[0]) & (taxis < args.trange[1])
                varR.append(np.var(rfRstream[i].data[tselect]))
            varR = np.array(varR)

            # Remove outliers wrt variance within time range
            medvarR = np.median(varR)
            madvarR = 1.4826*np.median(np.abs(varR-medvarR))
            robustR = np.abs((varR-medvarR)/madvarR)
            outliersR = np.arange(len(rfRstream))[robustR > 2.5]
            for i in outliersR[::-1]:
                rfRstream.remove(rfRstream[i])

        else:
            taxis = rfRstream[0].stats.taxis

        print('')
        print(datapath)
        print("Number of radial RF data: " + str(len(rfRstream)))
        print('')

        # Filtering
        rfRstream.filter('bandpass', freqmin=args.bp[0],
                         freqmax=args.bp[1], corners=2,
                         zerophase=True)

        # Time axis parameters
        nn = rfRstream[0].stats.npts
        dt = rfRstream[0].stats.delta
        time = np.arange(-nn/2+1, nn/2+1)*dt

        # Stack of all radial traces 
        stack = binning.bin_all(rfRstream, rfRstream, pws=False)[0]

        # Mean of slowness
        slow = np.mean([rf.stats.slow for rf in rfRstream])

        # Residuals
        resid = np.array([tr.data - stack.data for tr in rfRstream])

        # 2-sigma error
        stde = 2.*np.std(resid, ddof=1, axis=0)/np.sqrt(len(rfRstream))

        # Diagonal matrix of stde
        sig = np.diag(stde)

        # Normalized auto-correlation
        rcoeff = [np.correlate(resid[i], resid[i], mode='same') for i in range(resid.shape[0])]
        rcoeff = [rcoeff[i]/np.max(rcoeff[i]) for i in range(resid.shape[0])]

        # Take mean of normalized auto-correlations
        rcoeff = np.mean(rcoeff, axis=0)
        rcoeff = np.fft.fftshift(rcoeff)
        # rcoeff[rcoeff<0.] = 1.e-10

        # Store into Toeplitz matrix
        Rx = toeplitz(rcoeff, rcoeff)

        # Error covariance
        Cerr = sig*Rx*sig

        # Background model
        nlay = args.nlay
        zmax = args.zmax
        depth = np.linspace(0., zmax, nlay)

        # Define Vp as smooth gradient between 15 and 50 km
        vp = smoothstep(depth, x_min=15., x_max=50., N=1)*1.46 + 6.54

        # Ensemble of Vs models
        nens = args.nens
        vs_ensemble = np.empty((nens, nlay))
        vpvs_ensemble = np.empty((nens, nlay))
        stack_ensemble = np.empty((nens, nn))

        # Initiate multi-processing
        if not args.ncores:
            num_cores = multiprocessing.cpu_count()
            print('Number of cores available', num_cores)
        else:
            num_cores = args.ncores

        # Run nested for loop in parallel
        results = Parallel(n_jobs=num_cores)(delayed(minimize_parallel) \
            (stack, Cerr, depth, vp, slow, args.bp[0], args.bp[1], nn, dt, i) \
            for i in range(nens))

        for k, res in enumerate(results):
            vs_ensemble[k] = res[0]
            vpvs_ensemble[k] = res[1]
            stack_ensemble[k] = res[2]

        # Plot individual velocity models and ensemble mean
        f = plt.figure(figsize=(5, 5))
        ax1 = f.add_subplot(121)
        for ens in range(nens):
            ax1.step(vs_ensemble[ens], depth, 'k', alpha=0.3)
        ax1.step(np.mean(vs_ensemble, axis=0), depth, 'r')
        ax1.set_xlabel('Vs (km/s)')
        ax1.set_ylabel('Depth (km)')
        ax1.grid()
        ax1.invert_yaxis()
        # Vp/Vs
        ax2 = f.add_subplot(122)
        for ens in range(nens):
            ax2.step(vpvs_ensemble[ens], depth, 'k', alpha=0.3, where='pre')
        ax2.step(np.mean(vpvs_ensemble, axis=0), depth, 'r', where='pre')
        ax2.set_xlabel('Vp/Vs')
        ax2.grid()
        ax2.invert_yaxis()
        plt.tight_layout()
        # Save or show
        if args.saveplot:
            plt.savefig(plotpath / (sta.station+'_Vs_ensemble.png'))
        else:
            plt.show()

        # Get Vs from piecewise density of ensemble models
        nvs = 100
        vs_plot = np.linspace(2., 5., nvs).reshape(-1, 1)
        vpvs_plot = np.linspace(1.4, 2.5, nvs).reshape(-1, 1)
        vs_kde = np.empty((nlay, nvs))
        vpvs_kde = np.empty((nlay, nvs))
        vs_map = np.empty(nlay)
        vpvs_map = np.empty(nlay)
        for ilay in range(nlay):
            vs_kde_layer = np.exp(KDE(bandwidth=0.1).fit(vs_ensemble[:,ilay].reshape(-1, 1)).score_samples(vs_plot))
            vs_kde[ilay] = vs_kde_layer
            vs_map[ilay] = vs_plot[vs_kde_layer==np.max(vs_kde_layer)][0][0]
            vpvs_kde_layer = np.exp(KDE(bandwidth=0.1).fit(vpvs_ensemble[:,ilay].reshape(-1, 1)).score_samples(vpvs_plot))
            vpvs_kde[ilay] = vpvs_kde_layer
            vpvs_map[ilay] = vpvs_plot[vpvs_kde_layer==np.max(vpvs_kde_layer)][0][0]

        # Show ensemble as distribution (KDE)
        f = plt.figure(figsize=(5, 5))
        ax1 = f.add_subplot(121)
        ax1.imshow(vs_kde[:-1,:], extent=[2., 5., np.max(depth), 0.], aspect='auto', cmap='GnBu')
        ax1.step(vs_map, depth, 'w', where='pre')
        # ax1.stairs(vs_map, depth, c='w', orientation='horizontal', baseline=None)
        ax1.set_xlabel('Vs (km/s)')
        ax1.set_ylabel('Depth (km)')
        ax2 = f.add_subplot(122)
        ax2.imshow(vpvs_kde[:-1,:], extent=[1.4, 2.5, np.max(depth), 0.], aspect='auto', cmap='GnBu')
        ax2.step(vpvs_map, depth, 'w', where='pre')
        ax2.set_xlabel('Vp/Vs')
        plt.tight_layout()
        if args.saveplot:
            plt.savefig(plotpath / (sta.station+'_Vs_ensemble_dist.png'))
        else:
            plt.show()

        # Plot fit to data
        f = plt.figure(figsize=(5, 5))
        err = stde
        plt.fill_between(time, stack.data + err, stack.data - err, fc='r', alpha=0.3)
        plt.plot(time, stack.data, 'r', label='RF stack $\pm$ 1-$\sigma$')
        for ens in range(nens):
            plt.plot(time, stack_ensemble[ens], 'k', alpha=0.1)
        plt.plot(time, stack_ensemble[0], 'k', alpha=0.1, label='synthetic RF')
        plt.xlim(args.trange[0], args.trange[1])
        plt.xlabel('Time lag (s)')
        plt.ylabel('RF amplitude')
        plt.legend()
        plt.tight_layout()
        if args.saveplot:
            plt.savefig(plotpath / (sta.station+'_RF_ensemble.png'))
        else:
            plt.show()

        if args.saveplot:
            np.savetxt(respath / (sta.station+'_results.txt'), np.array([depth, vs_map, vpvs_map]).T)


if __name__ == "__main__":

    # Run main program
    main()
