import pyeng as _pyeng
import pyeng.engineer_data.units as _units
import pyeng.engineer_data.resources as _resources


def set_units(set_to: str):
    for unit_system in _resources.UNIT_SYSTEMS:
        if unit_system == set_to.upper():
            _pyeng.unit_system = unit_system
            _pyeng.u_length = _resources.UNIT_SYSTEMS[unit_system][0]
            _pyeng.u_area = _resources.UNIT_SYSTEMS[unit_system][1]
            _pyeng.u_volume = _resources.UNIT_SYSTEMS[unit_system][2]
            _pyeng.u_inertia = _resources.UNIT_SYSTEMS[unit_system][3]
            _pyeng.u_mass = _resources.UNIT_SYSTEMS[unit_system][4]
            _pyeng.u_pressure = _resources.UNIT_SYSTEMS[unit_system][5]
            _pyeng.u_pload = _resources.UNIT_SYSTEMS[unit_system][6]
            _pyeng.u_dload = _resources.UNIT_SYSTEMS[unit_system][7]


def convert_units(value: float, convert_from: str, convert_to: str):
    from_type, to_type = None, None
    for unit_type in dir(_units)[:-8]:
        if "CONSTANTS" not in unit_type:
            for unit_system in getattr(_units, unit_type):
                for unit in getattr(_units, unit_type)[unit_system]:
                    if convert_from.upper() == unit:
                        from_type = unit_type
                        if from_type == "TEMPERATURE":
                            return convert_temp(value, convert_from.upper(), convert_to.upper())
                        from_constant = getattr(_units, unit_type)[unit_system][unit]
                        if from_constant != 1:
                            from_constant = 1/from_constant
                    if convert_to.upper() == unit:
                        to_type = unit_type
                        to_constant = getattr(_units, unit_type)[unit_system][unit]
    if from_type is None or to_type is None:
        raise ValueError("A unit does not exist, more units are being added")
    if from_type != to_type:
        raise ValueError(f"Unit types must be of the same type. {from_type} converts to {from_type}, not {to_type}")
    return round(value * from_constant * to_constant, 9)


def convert_temp(value, convert_from, convert_to):
    if convert_from == "F":
        if convert_to == "C":
            return (value - 32) * 5 / 9
        elif convert_to == "R":
            return value + 459.67
        elif convert_to == "K":
            return (value + 459.67) * 5 / 9
        else:
            return value
    elif convert_from == "C":
        if convert_to == "F":
            return value * 9 / 5 + 32
        elif convert_to == "R":
            return (value + 273.15) * 9 / 5
        elif convert_to == "K":
            return value + 273.15
        else:
            return value
    elif convert_from == "R":
        if convert_to == "F":
            return value - 459.67
        elif convert_to == "C":
            return (value - 491.67) * 5 / 9
        elif convert_to == "K":
            return value * 5 / 9
        else:
            return value
    elif convert_from == "K":
        if convert_to == "F":
            return value * 9 / 5 - 459.67
        elif convert_to == "C":
            return value - 273.15
        elif convert_to == "R":
            return value * 9 / 5
        else:
            return value
    else:
        return value
