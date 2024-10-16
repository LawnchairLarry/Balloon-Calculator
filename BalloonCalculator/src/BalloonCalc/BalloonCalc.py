#from BalloonCalc import AtmosphereData

import AtmosphereData
import SphereCalc
import CylinderCalc
import sys

#Konstanten definieren:
HELIUM = 1
HYDROGEN = 2
AIR_TEMPERATURE = 0
AIR_PRESSURE = 1
AIR_DENSITY = 2
HELIUM_SPECIFIC_GAS_CONSTANT = 2077.1
HYDROGEN_SPECIFIC_GAS_CONSTANT = 4124.2
PE_DENSITY = 925 # kg/m³

def main():
    print("Willkommen beim Balloon Calculator V0.3.0")
    print("Dieses Programm ermöglicht die Berechnung des Benötigten Volumens und Oberfläche eines Ballons.")
    print("Dieser Rechner kann nur für nicht elastisches Material angewandt werden.")

    max_altitude = float(input("Bitte die maximale Flughöhe in km angeben: "))
    lifting_gas = 0
    while lifting_gas < 1 or lifting_gas > 2:
        lifting_gas = int(input('''Bitte wählen sie das zu verwendende Traggas.
                                1. Helium
                                2. Wasserstoff
                                Geben Sie 1 für Helium oder 2 für Wasserstoff ein: '''))
    atmosphere_data_file = sys.argv[1]
#    atmosphere_data_file = "../../AtmosphereData/AtmosphereDataStandardAtmosphere1976RawData.CSV"          # Hardcoded Dateipfad für Testzwecke
    conditions_at_max_altitude = AtmosphereData.get_altitude_data(max_altitude, atmosphere_data_file)

    # Traggasdichte auf Maximalhöhe berechnen:
    if lifting_gas == 1:
        specific_gas_constant = HELIUM_SPECIFIC_GAS_CONSTANT
    elif lifting_gas == 2:
            specific_gas_constant = HYDROGEN_SPECIFIC_GAS_CONSTANT
    rho_lifting_gas_at_max_altitude = conditions_at_max_altitude[AIR_PRESSURE] / (specific_gas_constant * conditions_at_max_altitude[AIR_TEMPERATURE])

    # Ballonhüllendaten abfragen
    d = float(input("Bitte die Stärke der Ballonhülle in Millimeter eingeben: "))
    d = d / 1000 # in m umwandeln
    user_input = 0
    while user_input < 1 or user_input > 2:
        user_input = int(input('''Wählen Sie ein Ballonhüllenmaterial:
        1. Polyethylen (PE-LD)
        2. Manuelle Eingabe
        Bitte Nummer eingeben: '''))
    if user_input == 1:
        rho_hull = PE_DENSITY
    elif user_input == 2:
        rho_hull = float(input("Bitte die Dichte des Ballonhüllenmaterials in kg/m³ eingeben: "))

    # Nutzlast oder Volumen gegeben?
    payload_to_volume_calc = 0
    while payload_to_volume_calc < 1 or payload_to_volume_calc > 2:
        payload_to_volume_calc = int(input('''Was möchten Sie berechnen?
        1. Nutzlast mit gegebenen Balonvolumen
        2. Ballonvolumen, Durchmesser und Oberfläche mit gegebener Nutzlast
        Bitte Nummer eingeben: '''))
    if payload_to_volume_calc == 1:
        v_bal = float(input("Bitte Ballonvolumen in m³ eingeben: "))
    if payload_to_volume_calc == 2:
        payload = float(input("Bitte Nutzlast in kg eingeben: "))

    # Kugelförmiger oder Zylindrischer Ballon?
    user_input = 0
    while user_input < 1 or user_input > 2:
        user_input = int(input('''Was möchten Sie berechnen?
            1. Kugelförmiger Ballon
            2. Zylindrischer Ballon
            Bitte Nummer eingeben: '''))
    if user_input == 1:
        if payload_to_volume_calc == 1:
            print_atmosphere_conditions(conditions_at_max_altitude,rho_lifting_gas_at_max_altitude)
            print(f"Nutzlast: {SphereCalc.calculate_payload(conditions_at_max_altitude, rho_lifting_gas_at_max_altitude, d, rho_hull, v_bal)}")
        if payload_to_volume_calc == 2:
            balloon_data = SphereCalc.approximate_v_bal(payload, conditions_at_max_altitude, rho_lifting_gas_at_max_altitude, d, rho_hull)
            print_atmosphere_conditions(conditions_at_max_altitude, rho_lifting_gas_at_max_altitude)
            print(f"Ballonvolumen: {balloon_data[0]} m³")
            print(f"Ballondurchmesser: {balloon_data[1]} m")
            print(f"Ballonoberfläche: {balloon_data[2]} m²")
    if user_input == 2:
        if payload_to_volume_calc == 1:
            print_atmosphere_conditions(conditions_at_max_altitude, rho_lifting_gas_at_max_altitude)
            print(f"Nutzlast: {CylinderCalc.calculate_payload(conditions_at_max_altitude, rho_lifting_gas_at_max_altitude, d, rho_hull, v_bal)} kg")
        if payload_to_volume_calc == 2:
            print_atmosphere_conditions(conditions_at_max_altitude, rho_lifting_gas_at_max_altitude)
            balloon_data = CylinderCalc.approximate_v_bal(payload, conditions_at_max_altitude, rho_lifting_gas_at_max_altitude, d, rho_hull)
            print(f"Ballonvolumen: {balloon_data[0]} m³")
            print(f"Ballondurchmesser: {balloon_data[1]} m")
            print(f"Ballonhöhe: {balloon_data[2]} m")
            print(f"Ballonoberfläche: {balloon_data[3]} m²")

def print_atmosphere_conditions(atmospheric_conditions, rho_lifting_gas):
    print("------------------------------------------------------")
    print("Atmosphärenbedingungen auf maximaler Höhe:")
    print(f"Temperatur: {atmospheric_conditions[AIR_TEMPERATURE]} K")
    print(f"Druck: {atmospheric_conditions[AIR_PRESSURE]} Pascal")
    print(f"Luftdichte: {atmospheric_conditions[AIR_DENSITY]} kg/m³")
    print(f"Traggasdichte: {rho_lifting_gas} kg/m³")
    print("------------------------------------------------------")

if __name__ == "__main__":
    main()

