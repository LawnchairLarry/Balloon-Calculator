from math import pi

AIR_DENSITY = 2

def approximate_v_bal(payload,conditions_at_max_altitude,rho_lifting_gas_at_max_altitude,d,rho_hull):
    # V_bal aproximieren:
    v_bal = 0
    approximation_increment = 1
    first_approximation = True
    previous_approx_lower_then_target = False
    previous_approximated_payload_difference = 0
    while True:
        approximated_payload = calculate_payload(conditions_at_max_altitude,rho_lifting_gas_at_max_altitude,d,rho_hull,v_bal)
#        print(f"approximated_payload {approximated_payload}")                          für debugging
#        print(f"v_bal {v_bal}")
        approximated_payload_difference = payload - approximated_payload
#        print(f"approximated_payload_difference: {approximated_payload_difference}")   für debugging
#        print("------------------------------")

        # Bei Vorzeichenänderung wurde der Zielwert überschritten
        if approximated_payload_difference * previous_approximated_payload_difference  < 0:
            approximation_increment = approximation_increment / 2           # Annäherungsschrittweite ändern
        previous_approximated_payload_difference = approximated_payload_difference

        if first_approximation:
            if approximated_payload_difference < 0:
                first_approximation = False
            else:
                v_bal = v_bal + approximation_increment                 ####
                approximation_increment = approximation_increment * 2

        if not first_approximation:
            if approximated_payload_difference < -0.0001:
               v_bal = v_bal - approximation_increment
            elif approximated_payload_difference > 0.0001:
                v_bal = v_bal + approximation_increment
            else:
                break   # BREAK THE TRUTH!!!!

    # Durchmesser berechnen:
    diameter = ((v_bal * 6)/pi)**(1/3)

    # Oberfläche berechnen:
    surface = pi * diameter**2
    return [v_bal, diameter, surface]

def calculate_payload(conditions_at_max_altitude,rho_lifting_gas_at_max_altitude,d,rho_hull,v_bal):
    displaced_air = v_bal * conditions_at_max_altitude[AIR_DENSITY]
    mass_balloon_hull = 4 * pi * (((3 / 4) * (v_bal / pi)) ** (2 / 3) * d * rho_hull)
    mass_lifting_gas = v_bal * rho_lifting_gas_at_max_altitude
    return displaced_air - mass_balloon_hull - mass_lifting_gas