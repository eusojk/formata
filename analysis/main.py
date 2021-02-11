from formata import maker, utils, parser
import xarray as xr
inp = 'D:/ddrive/agmerra_net_files'
prate = 'D:/ddrive/agmerra_net_files/AgMERRA_1980_prate_corrected_range.nc4'

out = "D:/ddrive/wth_files"
country = "Canada"
converter = maker.NCToWTHConverter(inp, country)
converter.to_WTH(out)

# obj = parser.WeatherDataNC(inp)
