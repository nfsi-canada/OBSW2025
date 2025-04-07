## 2025 Ocean-Bottom Seismology Training Workshop


**Organizers**: [Pascal Audet](https://www.uogeophysics.com/authors/admin/) and [Martha Savage](https://people.wgtn.ac.nz/martha.savage)

**Instructor**: Pascal Audet

**When**: April 14-16, 2025, 8:30 AM to 4:30 PM (NZST) 

**Where**: Room 501 in the Cotton building, Victoria University of Wellington

**What**: This workshop will cover training in seismological methods and software for broadband OBS data analysis encompassing three broad themes: 1) Seismograph orientation and data cleaning, 2) Subsurface seismic velocity structure, and 3) Earthquake detection and location. The format of the workshop will include short lectures and extensive hands-on practice to process broadband ocean-bottom seismic data using various open-source Python software packages.  

**Program**: [PDF](PROGRAM/OBSW2025_Draft_Program.pdf)

---

### List of software packages

#### StDb

StDb is a package containing tools for building a database of station information from geophysical observatories. The code is used through command-line scripts and include several options for querying an online FDSN archive, list the content of an existing station database, merge existing databases, and manually append or edit station information (e.g., for stations not hosted on any FDSN archive). The resulting station dictionary is used in various seismic applications covered in this workshop, such as OrientPy, OBStools and RfPy.

- Git repository: https://github.com/schaefferaj/StDb

- Documentation: https://schaefferaj.github.io/StDb/

#### OrientPy

OrientPy is a toolbox to help determine seismometer orientation (i.e., azimuth of horizontal components) using automated or manual processing of earthquake data. These methods are particularly useful for broadband ocean-bottom seismograph (OBS) stations, but are also applicable to broadband land stations or shorter period instruments (depending on the method selected). 

- Git repository: https://github.com/nfsi-canada/OrientPy

- Documentation: https://nfsi-canada.github.io/OrientPy/

#### OBStools

OBStools is a package containing tools for processing data from broadband ocean-bottom seismograph (OBS) stations. Current functionalities include removing vertical-component noise from tilt and compliance effects, and calculating seafloor compliance. 

- Git repository: https://github.com/nfsi-canada/OBStools

- Documentation: https://nfsi-canada.github.io/OBStools/

#### RfPy 

RfPy is a software to calculate single event-station receiver functions from the spectral deconvolution technique. Methods are available to post-process the receiver function data to calculate H-k stacks, back-azimuth harmonics and common-conversion-point (CCP) imaging. 

- Git repository: https://github.com/paudetseis/RfPy

- Documentation: https://paudetseis.github.io/RfPy/

#### Telewavesim

Telewavesim contains Python and Fortran modules to synthesize teleseismic body-wave propagation through stacks of generally anisotropic and strictly horizontal layers using a matrix propagator approach. The code also properly models reverberations from an overlying column of water, effectively simulating recordings from ocean-bottom seismograph (OBS) stations. The code can be used in a variety of teleseismic receiver-based studies, such as receiver functions, long-period P-wave polarization, shear-wave splitting from core-refracted shear waves (i.e., SKS, SKKS), etc. 

- Git repository: https://github.com/paudetseis/Telewavesim

- Documentation: https://paudetseis.github.io/Telewavesim/

#### SeisBench

SeisBench is an open-source python toolbox for machine learning in seismology. It provides a unified API for applying deep learning models to seismic waveforms, and for accessing and training machine learning algorithms on seismic datasets. SeisBench has been built to alleviate traditional bottlenecks when applying machine learning techniques to seismic data, in particular the steps of data preparation, collection and labelling.

- Git repository: https://github.com/seisbench/seisbench/tree/main

- Documentation: https://seisbench.readthedocs.io/en/stable/index.html

#### GaMMA


GaMMA is an earthquake phase associator using a Bayesian Gaussian mixture model. It is designed to work with SeisBench and can be used to automatically build earthquake catalogues from raw waveforms using a Deep Learning picker.

- Git repository and Documentation: https://github.com/AI4EPS/GaMMA

#### PyOcto

PyOcto is a high-throughput seismic phase associator using the octotree structure for parameter search. It is designed to work with SeisBench and can be used to automatically build earthquake catalogues from raw waveforms using a Deep Learning picker.

- Git repository: https://github.com/yetinam/pyocto

- Documentation: https://pyocto.readthedocs.io/en/latest/

---

### Installing software packages

The open-source codes and tutorial instructions and data have been pre-installed on the workstations in Room Cotton 501, therefore there is no need to follow these steps for those attending the workshop in person. The following steps provide instructions to install the various software packages and required data on a personal computer. 

> **Warning!!** These instructions will work on a Linux or MacOS system, but have not been tested on Windows systems. We will not be able to troubleshoot installation problems on a personal computer during the workshop.

To install the packages, we strongly recommend installing and creating a `conda` environment (either from the [Anaconda](https://anaconda.org) distribution or [mini-conda](https://docs.conda.io/en/latest/miniconda.html)) where the codes can be installed alongside their dependencies. This **significantly reduces** the potential conflicts in package versions. In a bash (or zsh) terminal, follow these steps:

##### Creating a Conda environment:

- Create a conda environment (here we call it `obsw25`, short for "OBS Workshop 2025") and install `python` and some required packages directly:

```bash
conda create -n obsw25 -c conda-forge "python=3.10" "numpy<1.22" "setuptools=60" obspy jupyter fortran-compiler spectrum
```

- Activate the environment:

```bash
conda activate obsw25
```

Now you're ready to install the required packages used in the workshop. You might consider one of two options: 1) you are only interested in using the software and are not interested in the source code; 2) you want to look at the source code and are considering contributing (awesome!!)

##### 1) User mode: Installing wheels from the master branch on the GitHub repositories and PyPI:

> Note: Follow this sequence ***exactly*** (with Telewavesim installed first) to avoid version conflicts

```bash
pip install telewavesim@git+https://github.com/paudetseis/telewavesim
pip install stdb@git+https://github.com/schaefferaj/stdb
pip install obstools@git+https://github.com/nfsi-canada/obstools
pip install rfpy@git+https://github.com/paudetseis/rfpy
pip install orientpy@git+https://github.com/nfsi-canada/orientpy
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install seisbench
pip install git+https://github.com/wayneweiqiang/GaMMA.git
pip install pyocto
```

##### 2) Developer mode: Cloning and installing from source

- Navigate on the command line to a path where the software packages will be installed. **Note this should be different from your working directory**.

- Clone the required repositories ([fork](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) them first, if you are serious about contributing):

```bash
git clone https://github.com/paudetseis/Telewavesim.git
git clone https://github.com/schaefferaj/StDb.git
git clone https://github.com/nfsi-canada/OrientPy.git
git clone https://github.com/nfsi-canada/OBStools.git
git clone https://github.com/paudetseis/RfPy.git
```

- Install using `pip`:

```bash
pip install -e Telewavesim/.
pip install -e StDb/.
pip install -e OrientPy/.
pip install -e OBStools/.
pip install -e RfPy/.
```

- We then install SeisBench from PyPI (unless you want to contribute to those packages too!)

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install seisbench
```

- And finally, GaMMA from the GitHub repository and PyOcto from PyPI

```bash
pip install git+https://github.com/wayneweiqiang/GaMMA.git
pip install pyocto
```

### Getting the workshop material and data

Finally, download the tutorials and demo data provided on this repository by navigating to some work folder (where the data and results of the processing will be located) and typing:

```bash
git clone https://github.com/nfsi-canada/OBSW2025.git
cd OBSW2025
```

The TUTORIAL[1-6] folders should now be on your computer and you are ready to start the demonstrations.

### Testing your installation

If you want to make sure everything is installed properly, activate your conda environment (i.e., `conda activate obsw25`) and open a python window by typing in a terminal:

```bash
python
```

which, on a MacOS (darwin), will produce something like:

```bash
Python 3.10.16 | packaged by conda-forge | (main, Dec  5 2024, 14:12:04) [Clang 18.1.8 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

Then type:

```bash
>>> import telewavesim
>>> import stdb
>>> import orientpy
>>> import obstools
>>> import rfpy
>>> import seisbench
>>> import gamma
>>> import pyocto
```

If nothing happens, you're good to go! If you run into a problem, let us know by [raising an issue](https://github.com/nfsi-canada/OBSW2025/issues). 

