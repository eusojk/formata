# formata

A Python utility to convert global historical weather data (NetCDF) to .WTH format, which usable by DSSAT.
----------
Extract from a sample WTH:
```
*WEATHER DATA : 145_0001.agmerra.nc
@ INSI      LAT     LONG  ELEV   TAV   AMP REFHT WNDHT
    CI   53.875    0.125   -99   -99   -99   -99   -99
@DATE  SRAD  TMAX  TMIN  RAIN  WIND  RHUM  TAVG
80001   1.6   2.6  -1.1   0.8   6.8  73.9   0.8
80002   2.5   2.5  -0.9   0.0   5.0  71.5   0.7
80003   1.0   4.4  -1.6  22.6   6.0  88.9   0.8
80004   3.3   5.1   0.5   1.2   6.1  87.7   3.0
80005   2.4   5.4  -0.1   3.8   6.5  81.1   2.9
80006   1.5   5.4   2.3   1.1   5.9  79.5   3.8
```

* Period: 30 years (1980 - 2010)
* Weather Variables:
    * Precipitation
    * Relative Humidity
    * Solar radition
    * Average temperature
    * Temperature (min, max)
    * Wind speed

 * AgMerra climate datasets can be found on NASA GISS [website] (https://data.giss.nasa.gov/impacts/agmipcf/agmerra/)
