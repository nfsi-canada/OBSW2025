## 2025 Ocean-Bottom Seismology Training Workshop


**Instructors**: [Pascal Audet](https://www.uogeophysics.com/authors/admin/)

**When**: April 14-16, 2025, 9:00 AM to 4:00 PM (NZDT) 

**Where**: Room 5XX in Cotton building, Victoria University of Wellington

**What**: This workshop will cover training in seismological methods and software for broadband OBS data analysis encompassing three broad themes: 1) Seismograph orientation and data cleaning, 2) Subsurface seismic velocity structure, and 3) Earthquake detection and location. The format of the workshop will include short lectures and extensive hands-on practice to process broadband ocean-bottom seismic data using various open-source Python software packages.  

---

### List of software packages

#### StDb

StDb is a package containing tools for building a database of station information from geophysical observatories. The code is used through command-line scripts and include several options for querying an online FDSN archive, list the content of an existing station database, merge existing databases, and manually append or edit station information (e.g., for stations not hosted on any FDSN archive). The resulting station dictionary is used in various seismic applications covered in this workshop, such as `OrientPy`, `OBStools` and `RfPy`.

- Git repository: https://github.com/schaefferaj/StDb

- Documentation: https://schaefferaj.github.io/StDb/

#### OrientPy

`OrientPy` is a toolbox to help determine seismometer orientation (i.e., azimuth of horizontal components) using automated or manual processing of earthquake data. These methods are particularly useful for broadband ocean-bottom seismograph (OBS) stations, but are also applicable to broadband land stations or shorter period instruments (depending on the method selected). The code uses the `StDb` package for querying and building a station database and can be used through command-line scripts.

- Git repository: https://github.com/nfsi-canada/OrientPy

- Documentation: https://nfsi-canada.github.io/OrientPy/

#### OBStools

`OBStools` is a package containing tools for processing data from broadband ocean-bottom seismograph (OBS) stations. Current functionalities include removing vertical-component noise from tilt and compliance effects, and calculating seafloor compliance. The code uses the `StDb` package for querying and building a station database and can be used through command-line scripts.

- Git repository: https://github.com/nfsi-canada/OBStools

- Documentation: https://nfsi-canada.github.io/OBStools/

#### RfPy 

`RfPy` is a software to calculate single event-station receiver functions from the spectral deconvolution technique. Methods are available to post-process the receiver function data to calculate H-k stacks, back-azimuth harmonics and common-conversion-point (CCP) imaging. The code uses the StDb package for querying and building a station database and can be used through command-line scripts.

- Git repository: https://github.com/paudetseis/RfPy

- Documentation: https://paudetseis.github.io/RfPy/

#### Telewavesim

`Telewavesim` contains Python and Fortran modules to synthesize teleseismic body-wave propagation through stacks of generally anisotropic and strictly horizontal layers using a matrix propagator approach. The code also properly models reverberations from an overlying column of water, effectively simulating recordings from ocean-bottom seismograph (OBS) stations. The code will be useful in a variety of teleseismic receiver-based studies, such as P or S receiver functions, long-period P-wave polarization, shear-wave splitting from core-refracted shear waves (i.e., SKS, SKKS), etc. It may also be used as a forward simulator in inverse methods. The main algorithm is written in Fortran with Python wrappers.

- Git repository: https://github.com/paudetseis/Telewavesim

- Documentation: https://paudetseis.github.io/Telewavesim/

---

### Installing software packages

The open-source codes have been pre-installed on the workstations in Room Cotton5XX, therefore there is no need to follow these steps for those attending the workshop in person. The following steps provide instructions to install the various software packages on a personal computer.

To install `obstools`, we strongly recommend installing and creating a `conda` environment (either from the [Anaconda](https://anaconda.org) distribution or [mini-conda](https://docs.conda.io/en/latest/miniconda.html)) where the code can be installed alongside its dependencies. This **significantly reduces** the potential conflicts in package versions. In a bash (or zsh) terminal, follow these steps:

- Create a conda environment (here we call it `mss` for the name of the symposium) and install `python=3.8` and `obspy`:

```bash
conda create -n msw python=3.8 obspy -c conda-forge
```

- Activate the environment:

```bash
conda activate msw
```

- Install the required [`stdb`](https://github.com/schaefferaj/StDb) package using `pip`:

```bash
pip install stdb
```

Now you're ready to install `obstools`. You might consider one of two options: 1) you want to look at the source code and are considering contributing (awesome!!); 2) you are only interested in using the software and are not interested in the source code.

##### 1) Developer mode: Installing from source

- Navigate on the command line to a path where the software will be installed

- Clone the OBStools repository ([fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) it first, if you are serious about contributing):

```bash
git clone https://github.com/paudetseis/OBStools.git
cd OBStools
```

- Install using `pip`:

```bash
pip install -e .
```

##### 2) User mode: Installing from the Python Package Index (PyPI):

```bash
pip install obstools
```

### Getting the demo data

Finally, download the demo data provided on this github repository by navigating to some work folder (where the data and results of the processing will be located) and typing:

```bash
git clone https://github.com/nfsi-canada/MSW2023.git
cd MSW2023
```

The `DATA` and `EVENTS` folders should now be on your computer and you are ready to start the tutorial.

### Testing your installation

If you want to make sure everything is installed properly, make sure your conda environment has been activated and open a python window by typing in a terminal:

```bash
python
```

which will produce something like:

```bash
Python 3.8.16 (default, Feb  1 2023, 16:05:36) 
[Clang 14.0.6 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

Then type:

```bash
>>> import stdb
>>> import obstools
```

If nothing happens, you're good to go! If you run into a problem, let us know by [raising an issue](https://github.com/nfsi-canada/OBSW2025/issues). 

