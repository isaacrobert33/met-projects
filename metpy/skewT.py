import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units
import matplotlib.pyplot as plt

# Example sounding data (Temperature, Dewpoint, and Pressure levels)
pressure = [1000, 925, 850, 700, 500, 300, 200] * units.hPa
temperature = [20, 18, 12, 4, -10, -35, -60] * units.degC
dewpoint = [17, 16, 10, 0, -15, -40, -70] * units.degC

# Create a SkewT plot
skew = SkewT()

# Plot the temperature and dewpoint data
skew.plot(pressure, temperature, 'r')
skew.plot(pressure, dewpoint, 'g')

# Add wind barbs or other analyses as needed
plt.show()
