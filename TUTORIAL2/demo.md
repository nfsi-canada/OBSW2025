# Tutorial 2 Demonstration

In this demonstration we will attempt to determine the orientation of station
[7D.FN07A](https://ds.iris.edu/gmap/#network=7D&station=FN07A&planet=earth) from the Cascadia Initiative: 

We use this station because its orientation have been determined previously, so we can 
calibrate our results see [here](https://obsic.whoi.edu/wp-content/uploads/sites/6/2019/05/Cascadia_Horizontal_Orientation_Report_2011-2012_14_05_02.pdf). This station was also used to calculate and model receiver functions
(Audet, GJI, 2016), so this will provide an example of an end-to-end workflow for this
type of analysis.

First, ensure the `Conda` environment is activated:

```
conda activate obsw25
```

### Creating the StDb database

Simply type in the terminal:

```
query_fdsn_stdb -N 7D -S FN07A FN07A > logfile
```

This command will extract the metadata and store it in the StDb file `FN07A.pkl`. You can also
check the content of the database:

```
ls_stdb FN07A.pkl
```

Once we have the StDb file, we can run the scripts to automate the analysis and determine the station
orientation using OrientPy.

#### BNG analysis

#### Automated processing

We wish to use the entire deployment time of station FN07A to calculate the station orientation using teleseismic P-wave data. Since the file FN07A.pkl contains only one station, it is not necessary to specify a key. This option would be useful if the database contained several stations and we were only interested in downloading data for LOBS3. In this case, we would specify `--keys=FN07A` or `--keys=7D.FN07A`. We could use all the default paramaters to do automated processing for regional events. However, since we wish to analyze teleseismic data, we will edit a few of them to include more waveform data around the predicted P-wave arrival time. We also consider all earthquakes between 30 and 175 degrees, as the program will automatically use either the P or PP waves to extract the waveforms.

The parameters to edit in this case are: `--times=-5.,15.` to extract data from -5 to 15 seconds following P-wave arrival; `--window=60.` to include 60 seconds of data; `--minmax=6.` to limit the number of events to consider; `--mindist=30.` for the minimum epicentral distance for teleseismic P; and `--bp=0.04,0.1` to focus on the long-period P waves:

```
bng_calc_auto --times=-5.,15. --window=60. --bp=0.04,0.1 --min-mag=6. --min-dist=30. FN07A.pkl
```

You will notice that a folder called BNG_RESULTS/7D.FN07A/ has been created. This is where all processed files will be stored on your computer.

#### Averaging

Now that all events have been processed, we wish to produce an average value of station orientation. However, not all estimates have equal weight in the final average. In particular, Braunmiller et al. (2020) have shown how a combination of parameters can be used to exclude poorly constrained estimates to produce a more robust final estimate. Here we will use all default values in the script and specify arguments to plot and save final figures.

```
bng_average --plot --save FN07A.pkl
```

The first figure to pop up will show the various combinations of quality factors, highlighting the estimates that pass the selected (default) thresholds. The second figure displays the estimates according to three parameters:

- Signal-to-noise ratio (SNR)
- Cross-correlation coefficient (CC)
- Earthquake magnitude

The results for this method are not particularly great. We would need to tweak the parameters to try and improve the estimate, perhaps use regional earthquakes, and so on. Let's now look at the surface-wave analysis.

### DL analysis

#### Automated processing

We wish to use the entire deployment time of station FN07A to calculate the station orientation using Rayleigh-wave polarization data. Following the previous example, since the file FN07A.pkl contains only one station, it is not necessary to specify a key. Here we use default parameters, except for the minimum earthquake magnitude that we set to 7 (to speed up the calculations), and the maximum earthquake depth that we set to 30 km.

```
dl_calc --min-mag=7. --max-dep=30. FN07A.pkl
```

You will notice that a folder called DL_RESULTS/7D.FN07A/ has been created. This is where all processed files will be stored on your computer.

#### Averaging

Now that all events have been processed, we wish to produce an average value of station orientation. However, not all estimates have equal weight in the final average. In particular, Doran and Laske have shown how to specify a threshold cross-correlation (CC) value to exclude waveforms for which the CC between the radial and Hilbert-transformed vertical component is low. Here we use the default CC threshold of 0.8 and produce a final plot with the estimate.

```
dl_average --plot FN07A.pkl
```

The figure displays the estimates according to the CC value. You can change the default CC value based on this plot to estimate the H1 orientation:

```
dl_average --plot --cc=0.75 FN07A.pkl
```