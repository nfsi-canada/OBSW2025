# Getting Seismic data and metadata

All codes in this workshop are designed to use the [FDSN web services](https://www.fdsn.org/webservices/) to get station information, earthquake catalogues, and waveform data. These are implemented in `ObsPy` as dedicated "clients" that interact with the web services under the hood. For instance:

```
from obspy.clients.fdsn import Client

client = Client('IRIS')
```

In `ObsPy`, one can either specify a key string that points to a public archive or use the corresponding URL. For instance, the two "clients" below are identical and point to the same archive:

```
client1 = Client('GEONET')
client2 = Client('http://service.geonet.org.nz')
```

To be more specific, I encourage you to use the appropriate `base_url` keyword argument when defining a "client", which makes it explicit:

```
client = Client(base_url='http://service.geonet.org.nz')
```

We can then use these "clients" to get [station information](https://docs.obspy.org/master/packages/autogen/obspy.clients.fdsn.client.Client.get_stations.html#obspy.clients.fdsn.client.Client.get_stations), [event catalogues](https://docs.obspy.org/master/packages/autogen/obspy.clients.fdsn.client.Client.get_events.html#obspy.clients.fdsn.client.Client.get_events), and [waveform data](https://docs.obspy.org/master/packages/autogen/obspy.clients.fdsn.client.Client.get_waveforms.html#obspy.clients.fdsn.client.Client.get_waveforms):

```
inv = client.get_stations(...)
cat = client.get_events(...)
stream = client.get_waveforms(...)
```

### FDSN web services for local data with `SeisComP`

Oftentimes, the dataset we wish to use is not available publicly and only exists on a local (maybe external) computer drive. Due to the many different ways the data can be formatted and sorted, adapting every codes to be as flexible as possible is a huge task. Instead, it is possible to (re)format the data in a structured way that is coherent with the way FDSN services access the data on remote archives, and run `SeisComP` locally to enable FDSN web services on the same computer on a local port (e.g., http://localhost:8080), such that we can use the usual `ObsPy` "client":

```
client = Client(base_url='http://localhost:8080')

client.get_stations(...)
```

`SeisComP` is already installed on one of the geophysics servers in room CO-501, such that anyone with properly formatted seismic data will be able to load it into `SeisComP` and use the FDSN web services for their data set.

### Formatting the seismic data archive

To enable the FDSN web services and load local data sets, `SeisComP` uses the station XML standard for station metadata and the "SeisComP Data Structure" (SDS) for archiving miniSEED waveform data. 

#### Station XML

The metadata should be formatted as a [stationXML](https://www.fdsn.org/xml/station/). The corresponding `ObsPy` documentation is [here](https://docs.obspy.org/packages/obspy.core.inventory.html). If you don't have a station `.xml` file but you have a dataless SEED file, you can convert it to `.xml` using [this tools](https://seiscode.iris.washington.edu/projects/stationxml-converter).

#### Waveform (`.mseed`) data

The SDS folder containing the waveform data has the structure:

```
archive
  + year
    + network code
      + station code
        + channel code
          + one file per day and location, e.g. NET.STA.LOC.CHAN.D.YEAR.DOY
```

For the ELVES data, this is, for example:

```
SDS/
  2023/ (+ 2024/ 2025/)
    3O/
      EL23A/ (+ EL23B/ EL23C/ ...)
        CH1.D/ (+ CH2.D/ CH3.D/)
          3O.EL23A..CH1.D.2023.332
          ...
```

Note, the filename does not include the extension `.mseed`, and the characters `.D` that appear in both the channel code and the filename. Note also the two dots (`..`). If there is a location code, it should appear between those dots (e.g., for a location code `10`, the corresponding filename should be `3O.EL23A.10.CH1.D.2023.332`). There is no location code for the ELVES data, and this field is simply absent from the filenames. Finally, the day-of-year (DOY) field must be zero-padded to be exactly 3 characters.

### Bringing data to the OBS workshop

If you wish to work on your own data set at the workshop, you will need to bring, on a single drive (or share via secure file transfer):

```
drive/
  station_metadata.xml
  SDS/
    ...
```

If you are not sure of your setup, please send us a smaller copy (subset of data) as soon as possible so we can test it before the workshop. 


### Working with ELVES data

The ELVES data will be available via an FDSN web service set up for the workshop through `SeisComP`. To access the data, you will need to be connected to the local domain (geo.vuw.ac.nz) and use the full URL that points to the `SeisComP` server, as well as a user name and password. In a Python environment, you can access the ELVES data using the `ObsPy` tools by specifying

```
client = Client(base_url='http://seiscomp.geo.vuw.ac.nz', user='xxxx', password='xxxx')
client.get_stations(...)
client.get_waveforms(...)
```

For most of the codes we will use during the workshop, you will be able to define the URL as well as the authentication fields using command-line options `--server='http://seiscomp.geo.vuw.ac.nz'` and `--user-auth='xxxx:xxxx'`. We will provide username and password information and examples during the workshop.