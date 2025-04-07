# Tutorial 4 Demonstration

In this demonstration we will attempt to calculate receiver functions for station
[7D.FN07A](https://ds.iris.edu/gmap/#network=7D&station=FN07A&planet=earth) from the Cascadia Initiative.


First, ensure the Conda environment is activated:

```
conda activate obsw25
```

Then, copy the StDb file `FN07A.pkl` from TUTORIAL2/ to TUTORIAL4/

```
cp ../TUTORIAL2/FN07A.pkl .
```

### Editing the StDb database

As we already determined the station orientation using OrientPy, we need to edit the station file using one of the StDb scripts to specify the azimuth of the H1 component:

```
edit_stdb FN07A.pkl
```

This will open a GUI where you can manually edit any field. *Do not change important metadata information!* However, you can edit the second to last field, with corresponds to `azcorr` and stores the orientation of the H1 component. You can check that the database has been updated:

```
ls_stdb FN07A.pkl
```

### Calculating receiver functions

The script to calculate receiver functions is called `rfpy_calc`. By default, this script processes data for all teleseismic P-waves from earthquakes with magnitudes between 6 and 9 and with epicentral distances between 30 and 90 degrees that occurred during the station deployment time. The default component alignment is ZRT and the default deconvolution method is the wiener filter. This is almost what is needed to reproduce the results in Audet (2016) - we only need to change the minimum magnitude to 5.8: 

```
rfpy_calc --minmag=5.8 FN07A.pkl
```

> **Local data**
>
> To use the ELVES data, we need to specify a few more options. First, use the `--server` and `--user-auth` options to get waveform data. Second, use the `--zcomp=3` option. For example,
> ```
> rfpy_calc --server='http://seiscomp.geo.vuw.ac.nz' --user-auth='xxxx:xxxx' --zcomp='3' --minmag=5.8 EL23A.pkl
> ```

Note that we could use a different deconvolution method (e.g., `method=multitaper`), select a shorter time range for the analysis, or align the waveforms along a different coordinate system (e.g., `LQT`, `PVH`). After running `rfpy_calc`, you should have a new folder named P_DATA/7D.FN07A containing all event folders, each of them containing the meta data, station data, raw data, and receiver function data:

```
ls -R * | head
```

Once this step is done, you can still re-calculate the receiver functions using different processing options (see below). If you want to change those parameters, run the previous command with `-O` to override anything that exists on disk. However, some parameters cannot be changed easily without re-downloading the raw data (e.g., length of processing window, sampling rate). 

Note that you can get more data by either specifying a new phase to analyze (e.g., `--phase=PP`), going to lower magnitudes (e.g., `--minmag=5. --maxmag=5.8`), by running `rfpy_calc` with those additional arguments.

### Re-calculating with different options

If later on you decide you want to try a different deconvolution method, component alignment or maybe try some pre-filtering options, you can always simply use the `rfpy_recalc` script to do so.

> **Note**: Re-calculating the receiver functions for different options will override any existing receiver function data. Be mindful of this when using this script.

This can be done by typing in the terminal:

```
rfpy_recalc --align=ZRT --method=multitaper FN07A.pkl
```

### Plotting receiver functions

Now that we have our data set of receiver functions, we can plot it! There are two types of plots: the "Back-azimuth" panels and the "Slowness" panels. In the first case the receiver functions are sorted by back-azimuth and all slowness information is lost (i.e., averaged out). In the other case it is the opposite and the receiver fuuntions are sorted by slowness and all back-azimuth information is lost. 

When plotting, you can decide whether to include all data, or set some quality control thresholds based on 1) the signal-to-noise ratio (SNR, in dB) calculated on the vertical component, 2) the correlation coefficient (CC) value of predicted and observed radial components, and 3) outliers. If you don’t specify any thresholding, by default the script `rfpy_plot` will use all data to make the plots. You also want to set corner frequencies for filterig, otherwise it will be difficult to see anything. Typically you would choose a frequency band that encompasses the dominant frequencies of teleseismic P waves (i.e., 0.05 to 1 Hz). Let’s examine the two types of plots with examples:

#### Back-azimuth panel

Below we make a plot of all P receiver functions, filtered between 0.1 and 0.5 Hz, using 72 back-azimuth bins (i.e., bin width of 5 degrees). We select receiver functions for which the raw waveform SNR is greater than 5 dB measured on the vertical component. We plot the receiver functions from 0. to +20 seconds following the zero-lag (i.e., P-wave arrival) time, stack all traces to produce an averaged receiver function, and normalize all traces to that of the stack.

```
rfpy_plot --snr=5 --bp=0.1,0.5 --nbaz=72 --normalize --stack --trange=0.,20. FN07A.pkl
```

This approximately reproduces Figure 10b in Audet (2016). Details may differ due to the use of different window lengths and pre-processing, etc.

#### Slowness panel

Now let’s make a plot of all receiver functions, this time sorted by slowness using 40 bins (bin width of approximately 0.001 s/km). 

```
rfpy_plot --snr=5 --bp=0.1,0.5 --nslow=40 --normalize --stack --trange=0.,20. FN07A.pkl
```

#### Save RFs to disk

The previous commands only create the RF figures and perhaps saves them to disk (e.g., `--save-fig='figname.png`). We can also save the RFs that went into creating the figure with the option `--save-rfs='folder_name'`, where you can choose a folder name that suits you. If you select both `--save-fig` and `--save-rfs`, the figure and RFs will be saved in the same `'folder_name'` folder; if only `--save-rfs` is specified, only the RFs will be saved. This folder will then contain the stacked (over all back-azimuths and slowness values) and binned (into back-azimuth or slowness bins) radial and transverse receiver functions as SAC files. It will also contain a `.csv` file containing the (baz, slow) pairs that the RFs represent. It also contains a hidden `.proc.json` file containing the command-line arguments that were specified when calling `rfpy_plot`, so you know how each figure was created. This will be useful in the next tutorial.
