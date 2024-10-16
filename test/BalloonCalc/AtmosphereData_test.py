import unittest

from BalloonCalc import AtmosphereData

#print(GetAltitudeData(10))

class GetAltitudeDataTestCase(unittest.TestCase):

    def test_get_attitude(self):
        result = AtmosphereData.get_altitude_data(30, "../../AtmosphereDataStandardAtmosphere1976RawData.CSV")
        expected = [226.65, 1171.87, 0.0180119]
        for idx, expected_value in enumerate(expected):
            result_value = result[idx]
            self.assertEqual(expected_value, result_value)

