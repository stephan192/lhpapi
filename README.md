# lhpapi
Python client to retrieve data provided by the 16 German federal state flood information centers jointly known as [Länderübergreifendes Hochwasser Portal (LHP)](https://www.hochwasserzentralen.de)

## Install
```
pip install lhpapi
```

## Usage

### Quickstart example
Get values for the Isar in Munich
```
from lhpapi import HochwasserPortalAPI, LHPError

try:
    api = HochwasserPortalAPI("BY_16005701")
    
    print(f"ident:\t\t{api.ident}")
    print(f"name:\t\t{api.name}")
    print(f"url:\t\t{api.url}")
    print(f"hint:\t\t{api.hint}")
    print(f"level:\t\t{api.level} cm")
    print(f"stage:\t\t{api.stage}")
    print(f"flow:\t\t{api.flow} m³/s")
    print(f"last_update:\t{api.last_update}")
except LHPError as err:
    print("Something went wrong!")
```

Result
```
ident:          BY_16005701
name:           München / Isar
url:            https://www.hnd.bayern.de/pegel/isar/muenchen-16005701
hint:           None
level:          120.0 cm
stage:          0
flow:           73.6 m³/s
last_update:    2024-03-01 21:15:00+00:00
```

### Detailed description
**Methods:**
- **`__init__(ident: str)`**  
  Create a new LHP API class instance
  
  The `ident` must be one of the stream gauges (`Pegel`) listed in [pegel.md](https://github.com/stephan192/lhpapi/blob/master/docs/pegel.md). Some stream gauges are listed twice or even more often in [pegel.md](https://github.com/stephan192/lhpapi/blob/master/docs/pegel.md), because they are listed on more than one state portal. Select the one of your choice.
  
  Method `update()` is automatically called at the end of a successfull init.

- **`update()`**  
  Update data by querying the LHP servers and parsing the result
  
  Function should be called regularly, e.g. every 15minutes, to update the data stored in the class attributes.

**Attributes (read only):**
- **`ident : str`**  
  The identifier of the selected stream gauge

- **`name : str`**  
  The name of the selected stream gauge

- **`url : str`**  
  An URL pointing to additional information about the selected stream gauge

- **`hint : str`**  
  A hint reported for the the selected stream gauge

- **`level : float`**  
  The actual water level (in German *Pegelstand* or colloquially *Wasserstand*). A value in centimetres, starting from 0 cm = *Pegelnullpunktshöhe*.
  
- **`stage : int`**  
  The actual warning stage (in German depending on ferderal state e.g. *Meldestufe* in Bavaria, *Alarmstufe* in Brandenburg). A number between 0 (=no flood) and 4 (= very large flood).

- **`flow : float`**  
  The actual flow rate (in German *Abfluss* or *Durchfluss*). A value in m³/s.

- **`last_update : datetime`**  
  A datetime object representing the last update


### List of supported values
* :heavy_check_mark: Value mostly available. Check individual state portal because not all stream gauges report all values, values not avaiable are reported as `None`.
* :x: Value generally yet not available.

| Prefix | State                  | Level              | Stage              | Flow               | Portal |
|--------|------------------------|--------------------|--------------------|--------------------|--------|
| BB     | Brandenburg            | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | [Pegelportal Brandenburg](https://pegelportal.brandenburg.de) |
| BE     | Berlin                 | :heavy_check_mark: | :x:                | :heavy_check_mark: | [Wasserportal Berlin](https://wasserportal.berlin.de) |
| BW     | Baden-Württemberg      | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | [Hochwasservorhersagezentrale Baden-Württemberg](https://www.hvz.baden-wuerttemberg.de) |
| BY     | Bayern                 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | [Hochwassernachrichtendienst Bayern](https://www.hnd.bayern.de) |
| HB     | Bremen                 | :heavy_check_mark: | :heavy_check_mark: | :x:                | [Pegelstände Bremen](https://geoportale.dp.dsecurecloud.de/pegelbremen) |
| HE     | Hessen                 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | [Hochwasserportal Hessen](https://www.hochwasser-hessen.de) |
| HH     | Hamburg                | :heavy_check_mark: | :heavy_check_mark: | :x:                | [Warndienst Binnenhochwasser Hamburg](https://www.wabiha.de/karte.html) |
| MV     | Mecklenburg-Vorpommern | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | [Pegelportal Mecklenburg-Vorpommern](https://pegelportal-mv.de) |
| NI     | Niedersachsen          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | [NLWKN Pegelonline](https://www.pegelonline.nlwkn.niedersachsen.de) |
| NW     | Nordrhein-Westfalen    | :heavy_check_mark: | :heavy_check_mark: | :x:                | [Hochwassermeldedienst NRW](https://www.hochwasserportal.nrw.de)|
| RP     | Rheinland-Pfalz        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | [Hochwasservorhersagedienst - Landesamt für Umwelt Rheinland-Pfalz](https://hochwasser.rlp.de)|
| SH     | Schleswig-Holstein     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | [Hochwasser-Sturmflut-Information Schleswig-Holstein](https://hsi-sh.de) |
| SL     | Saarland               | :heavy_check_mark: | :heavy_check_mark: | :x:                | [Pegel Saarland](https://www.saarland.de/mukmav/DE/portale/wasser/informationen/hochwassermeldedienst/wasserstaende_warnlage/wasserstaende_warnlage_node.html) |
| SN     | Sachsen                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | [Landeshochwasserzentrum Sachsen](https://www.umwelt.sachsen.de/umwelt/infosysteme/hwims/portal/web/wasserstand-uebersicht) |
| ST     | Sachsen-Anhalt         | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | [Landesportal Sachsen-Anhalt](https://hochwasservorhersage.sachsen-anhalt.de) |
| TH     | Thüringen              | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | [Hochwassernachrichtenzentrale Thüringen](https://hnz.thueringen.de/hw-portal) |
