import csv
import sys

ALTITUDE = 0
AIR_TEMPERATURE = 1
AIR_PRESSURE = 2
AIR_DENSITY = 3

def get_altitude_data(altitude, atmosphere_raw_data_file):
    with open(atmosphere_raw_data_file,  newline='') as csvfile:
        air_density_to_altitude = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        for row in air_density_to_altitude:
            if row[ALTITUDE] >= altitude:
                return [row[AIR_TEMPERATURE], row[AIR_PRESSURE], row[AIR_DENSITY]]
    sys.exit("Flughöhe nicht in den Atmosphärendaten gefunden!")
