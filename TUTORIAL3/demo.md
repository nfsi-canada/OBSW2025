# Tutorial 2 Demonstration

In this demonstration we will show how to calculate and apply tilt and compliance corrections for station
[7D.FN07A](https://ds.iris.edu/gmap/#network=7D&station=FN07A&planet=earth) from the Cascadia Initiative.

First, ensure the `Conda` environment is activated:

```
conda activate obsw25
```

### Download daylong (mostly noise) data

We wish to download one month of data for the station FN07A for March 2012. The various options above allow us to select the additional channels to use (e.g., -C 12,P for both horizontal and pressure data - which is the default setting). Default frequency settings for data pre-processing match those of the Matlab ATaCR software and can be ignored when calling the program. Since the file FN07A.pkl contains only one station, it is not necessary to specify a key. This option would be useful if the database contained several stations and we were only interested in downloading data for FN07A. In this case, we would specify `--keys=FN07A` or `--keys=7D.FN07A`. The only required options at this point are the `--start` and `--end` options to specify the dates for which data will be downloaded.

If you change your mind about the pre-processing options, you can always re-run the following line with the option `-O`, which will overwrite the data saved to disk.

To download all broadband seismic and pressure data, simply type in a terminal:

```
atacr_download_data --start=2012-03-01 --end=2012-04-01 FN07A.pkl
```

Once this is done, you will notice that a folder called DATA/7D.FN07A/ has been created. This is where all day-long files will be stored on your computer.

### QC for daily spectral averages

In the next step, we wish to generate daily averages of the components' power spectrum for quality control. For this step, there are several Parameter Settings that can be tuned. Once again, the default values are the ones used to reproduce the results of the Matlab ATaCR software and can be left un-changed. The Time Search Settings can be used to look at a subset of the available day-long data files. Here these options can be ignored since we wish to look at all the availble data that we just downloaded. We can therefore type in a terminal:

```
atacr_daily_spectra FN07A.pkl
```

The code stores the `obstools.atacr.classes.DayNoise` objects to a newly created folder called SPECTRA/7D.FN07A/. To produce figures for visualization, we can re-run the above script but now use the plotting options to look at one day of the month (March 04, 2012). In this case we need to overwrite the previous results (option `-O`) and specify the date of interest:


```
atacr_daily_spectra -O --figQC --figAverage --start=2012-03-04 --end=2012-03-05 FN07A.pkl > logfile
```

The script will produce several figures, iwhich show all the raw data and the window classification into good and bad windows for subsequent analysis.

### Clean station averages

Now that we have processed daily spectra for all available components, it is possible to further average the spectra over multiple days to produce a "clean station average". It is still possible to specify a date range over which to average the spectra, thus giving flexibility in the production of the station averages. Parameter settings are similar to those used in `atacr_daily_spectra` but further include the option of plotting the averaged cross-spectral properties. To calculate a single station average for the entire month of March 2012 (and therefore using all available data) and plot the results, we can type in a terminal:

```
atacr_clean_spectra --figQC --figAverage --figCoh --figCross FN07A.pkl
```

 All `DayNoise` objects are averaged into a `StaNoise` object, which is saved to a newly created folder called AVG_STA/7D.FN07A/.

> Note: If you don’t specify the options `--start` and `--end`, the object will be saved with a filename that corresponds to the entire deployment time of the station, but in fact the object contains the average spectra of all daily spectra available on disk, and not necessarily the average over the entire deployment time. We recommend using the `--start` and `--end` options if you want to produce time-limited spectral averages (e.g., an average per week or per month, etc.). For example:

```
atacr_clean_spectra --start=2012-03-01 --end=2012-03-08 -O FN07A.pkl
```

This step produces all the cross-spectral quantities of interest across all possible (or useful) component pairs. Those are used in the subsequent analysis to produce the transfer functions used to correct the vertical component waveforms.

### Transfer function calculation

Once the `StaNoise` objects have been produced and saved to disk, the transfer functions across all available components can be calculated. By default the software will calculate the ones for which the spectral averages are available.

For compliance only (i.e., only `?HZ` and `?DH?`` components are available), the only transfer function possible is:

- `ZP`

For tilt only (i.e., all of `?HZ,1,2` components are available, but not `?DH`), the transfer functions are:

- `Z1`
- `Z2-1`

For both tilt and compliance (i.e., all four components are available), the following transfer functions are possible:

- `Z1`
- `Z2-1`
- `ZP`
- `ZP-21`

If you are using a `DayNoise` object to calculate the transfer functions (as opposed to averaged quantities over several days), the following may also be possible:

- `ZH`
- `ZP-H`

In this example we calculate all available transfer functions for all available data. In this case we do not need to specify any option and type in a terminal:

```
atacr_transfer_functions FN07A.pkl
```

Note how the `DayNoise` objects are read randomly from disk, followed by the `StaNoise` object. The result is a `TFNoise` object that is saved to a newly created folder called TF_STA/7D.FN07A/.

We can produce a figure of the transfer functions by re-running the previous command with the options `-O --figTF`:

```
atacr_transfer_functions -O -figTF FN07A.pkl
```

### Download earthquake data

Now we need to download the earthquake data, for which we wish to clean the vertical component using the transfer functions just calculated. This script `atacr_download_event` is very similar to `atacr_download_data`, with the addition of the Event and Geometry Settings.

> Warning: Be careful with the Frequency Settings, as these values need to be exactly the same as those used in `atacr_download_data`, but won’t be checked against.

To download the seismograms that recorded the March 9, 2012, magnitude 6.6 Vanuatu earthquake (be conservative with the options), type in a terminal:

```
atacr_download_event --min-mag=6.3 --max-mag=6.7 --start=2012-03-08 --end=2012-03-10 FN07A.pkl
```

The data are stored as an `EventStream` object, saved to disk in the newly created folder EVENTS/7D.FN07A/.

### Correct/clean earthquake data

The final step in the analysis is the application of the transfer functions to the raw earthquake seismograms to clean up the vertical component. Once again, the default settings can be used. The corrected seismograms will be saved to disk in a new folder called EVENTS/7D.FN07A/CORRECTED. To show some figures, specify the `--figRaw` and `--figClean` options:

```
atacr_correct_event --figRaw --figClean FN07A.pkl
```

Results are saved both as updated `EventStream` objects and as .SAC files that now contain the corrected vertical components.
