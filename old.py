import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import datetime

"""
Instead of getting the data set manually in our browser we can adapt the URL to any coordinates that we want:
This was the original one:
    http://aa.usno.navy.mil/cgi-bin/aa_rstablew.pl?ID=AA&year=2018&task=0&place=Greenwich+%28UK%29&lon_sign=-1&lon_deg=0&lon_min=00&lat_sign=1&lat_deg=51&lat_min=28&tz=&tz_sign=-1
    
"""

inFile = r'.\GreenwichUK.txt'
year = 2018

# The problem with loading this with np.loadtxt() is that there are a different numbe of columns when you get to the end of each month:
##A = np.loadtxt(inFile, skiprows=9) # Gives "ValueError: Wrong number of columns at line 38"

# (1)
# Let's try a pandas-based approach first:
##df = pd.read_csv(inFile, skiprows=range(7) + [7, 8], header=None, infer_datetime_format=True)
##print df
# This is currently a collection of rows, where each row is a long string. It has not split the row strings into columns yet:
##print df.shape


# (2)
# Let's try a different way:
##df = pd.read_csv(inFile, skiprows=range(7) + [7, 8], header=None, delim_whitespace=True, infer_datetime_format=True)
##print df
# This fails, because now February has 31 days! The columns are being shifted by the 

# This is currently a collection of rows, where each row is a long string. It has not split the row strings into columns yet:
##print df.shape


# (3)
# try pandas "fixed with" feature by spcifying colspec tuples that correspond to start and stop of columns. 

# This will choose the first and seconf columns according to their column numbers in the un-split text file:
eg = pd.read_fwf(inFile, colspecs=[(0,2), (4,8)], skiprows=9, header=None)

# We can loop over this for all months and we might as well split it into sunset and sunrise at the same time.
# This also makes it easier because the different months are separated by two spaces while the sunrise and sunset columns are separated by just one space. 
##sunrise = pd.read_fwf(inFile, colspecs=[(0,2)] + [(i, i+4) for i in range(4,132,11)], skiprows=9, header=None)
##sunset  = pd.read_fwf(inFile, colspecs=[(0,2)] + [(i, i+4) for i in range(9,137,11)], skiprows=9, header=None)
# Now without the day number:
sunrise = pd.read_fwf(inFile, colspecs=[(i, i+4) for i in range(4,132,11)], skiprows=9, header=None).values.T.flatten()
sunset  = pd.read_fwf(inFile, colspecs=[(i, i+4) for i in range(9,137,11)], skiprows=9, header=None).values.T.flatten()

# Remove all NaNs from the flattened lists to leave just the days that exist: https://stackoverflow.com/questions/11620914/removing-nan-values-from-an-array
sunrise = sunrise[~np.isnan(sunrise)].astype('int').tolist()
sunset = sunset[~np.isnan(sunset)].astype('int').tolist()


print sunrise, len(sunrise)
print sunset, len(sunset)


"""
Now we want to convert our float values to datetimes.
We can do this using Python's datetime module but we will need to give it integer values for hours, minutes and seconds. 
"""
sunrise = [datetime.time(int(str(a)[:-2]), int(str(a)[-2:]), 0) for a in sunrise]
sunset = [datetime.time(int(str(a)[:-2]), int(str(a)[-2:]), 0) for a in sunset]

print sunrise, len(sunrise)
print sunset, len(sunset)

# OK You might have noticed that the columns containing NaNs have been converted to floats while the months with 31 days are integers. 

# Anyway, what we want to do is generate one (365,1) shaped array with a the date, another with sunrise times and another with sunset. 
##date =    ['2018-01']* 31 + ['2018-02']* 28 + ['2018-03']* 31 \
##        + ['2018-04']* 30 + ['2018-05']* 31 + ['2018-06']* 30 \
##        + ['2018-07']* 31 + ['2018-08']* 31 + ['2018-09']* 30 \
##        + ['2018-10']* 31 + ['2018-11']* 30 + ['2018-12']* 31 
### Take care of leap years! :)
##print date, len(date)

##datelist = pd.date_range(pd.datetime.today(), periods=365).tolist()

# Creates a datetime list from any specific day:
##datelist = pd.date_range(pd.to_datetime('20180101', format='%Y%m%d', errors='ignore'), periods=365).tolist()

# But we don't want the time, we want a "period":
##periodlist = pd.period_range(start='2018-01-01', end='2018-12-31', freq='D')
periodlist = pd.date_range(start='%s-01-01' % year, end='%s-12-31' % year, freq='D')
##print periodlist

datelist = [pd.to_datetime(date, format='%Y-%m-%d').date() for date in periodlist]
##print datelist

plt.figure()
plt.plot(datelist, sunrise, label='sunrise')
plt.plot(datelist, sunset, label='sunset')
plt.legend()
plt.show()

















# Converting to a numpy array with dtype of 16-bit integer means that the 
##A = np.array(df, dtype=np.int16)
##print A

