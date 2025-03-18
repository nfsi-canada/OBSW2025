# Tutorial 4 Demonstration

In this demonstration we will attempt to calculate receiver functions for station
7D.FN07A from the Cascadia Initiative: https://ds.iris.edu/gmap/#network=7D&station=FN07A&planet=earth.


First, ensure the `Conda` environment is activated:

```
conda activate obsw25
```

### Creating and editing the StDb database

Simply type in the terminal:

```
query_fdsn_stdb -N 7D -S FN07A FN07A > logfile
```

As we already determined the station orientation using OrientPy, we need to edit the station file using one of the `StDb` scripts:

```
edit_stdb FN07A.pkl
```

This will open a GUI where you can manually edit any field. *Do not change important metadata information!* However, you can edit the second to last field, with corresponds to `azcorr` and stores the orientation of the H1 component.

