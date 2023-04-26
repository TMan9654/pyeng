import math as _math

import matplotlib.pyplot as plt
import unicodedata as _ud

import matplotlib.pyplot as _plt

import pyeng as _pyeng
import pyeng.engineer_data.resources as _resources


class Beam:
    __beam_count = 0

    def __init__(self, beam_element, profile: str, material: str):
        Beam.__beam_count += 1
        self.__instance = Beam.__beam_count
        self.beam_element = beam_element
        if isinstance(self.beam_element, (int, float)):
            self.start_node = (0, 0)
            self.end_node = (self.beam_element, 0)
            self.beam_element = (self.start_node, self.end_node)
        elif isinstance(self.beam_element, tuple):
            self.start_node = self.beam_element[0]
            self.end_node = self.beam_element[1]
        self.horizontal_dist = self.end_node[0] - self.start_node[0]
        self.vertical_dist = self.end_node[1] - self.start_node[1]
        self.length = _math.sqrt(self.horizontal_dist ** 2 + self.vertical_dist ** 2)
        self.profile = profile.upper()
        self.material = material.upper()
        self.section_properties = self.__get_section_properties()
        self.volume = _pyeng.convert_units(self.length * self.section_properties["Section Area"],
                                           f"{_pyeng.u_length.upper()}3",
                                           _ud.normalize("NFKD", _pyeng.u_volume))
        self.material_properties = self.__get_material_properties()
        self.info = f"Beam: {self.__instance} [{self.start_node}, {self.end_node}]\n" \
                    f"Length: {self.length} {_pyeng.u_length}\n" \
                    f"Width: {self.section_properties['Section Width']} {_pyeng.u_length}\n" \
                    f"Height: {self.section_properties['Section Height']} {_pyeng.u_length}\n" \
                    f"Profile: {self.profile}\n" \
                    f"Section Area: {self.section_properties['Section Area']} {_pyeng.u_area}\n" \
                    f"Beam Volume: {self.volume} {_pyeng.u_volume}\n" \
                    f"Ix: {self.section_properties['Ix']} {_pyeng.u_inertia}\n" \
                    f"Iy: {self.section_properties['Iy']} {_pyeng.u_inertia}\n" \
                    f"Beam Mass: {self.material_properties['Beam Mass']} {_pyeng.u_mass}\n" \
                    f"Tensile Strength: {self.material_properties['Tensile Strength']} {_pyeng.u_pressure}\n" \
                    f"Yield Strength: {self.material_properties['Yield Strength']} {_pyeng.u_pressure}\n" \
                    f"Elastic Modulus: {self.material_properties['Elastic Modulus']} {_pyeng.u_pressure}\n"
        self.supports = []
        self.p_loads = []
        self.u_loads = []
        self.q_loads = []

    def __repr__(self):
        return f"Beam({self.length:.2f}, {self.profile}, {self.material})"

    def __str__(self):
        return f"{_pyeng.unit_system} {self.profile.split(' ')[0]} BEAM " \
               f"({self.__instance}) - {self.material} - " \
               f"{self.length:.2f}x" \
               f"{self.section_properties['Section Width']}x" \
               f"{self.section_properties['Section Height']}"

    def __int__(self):
        return self.__instance

    def __get_section_properties(self):
        profile_type = self.profile.split(" ")[0]
        for profile_list in dir(_resources):
            if profile_type in profile_list:
                profile_list = getattr(_resources, profile_list)
                for profile in profile_list:
                    if profile == self.profile:
                        height, width, thickness = profile_list[profile]
                        corner_radius = 2 * thickness
                        section_area = (height * width - 4 * corner_radius ** 2 + _math.pi * corner_radius ** 2) - \
                                       ((height - corner_radius) * (width - corner_radius) - 4 *
                                        thickness ** 2 + _math.pi * thickness ** 2)
                        ix = ((width * height ** 3) / 12) - (
                                    ((width - corner_radius) * (height - corner_radius) ** 3) / 12)
                        iy = ((height * width ** 3) / 12) - (
                                    ((height - corner_radius) * (width - corner_radius) ** 3) / 12)
                        return {"Section Width": _pyeng.convert_units(float(self.profile.split(' ')[1].split('X')[1]),
                                                                      "IN",
                                                                      _pyeng.u_length),
                                "Section Height": _pyeng.convert_units(float(self.profile.split(' ')[1].split('X')[0]),
                                                                       "IN",
                                                                       _pyeng.u_length),
                                "Section Area": _pyeng.convert_units(section_area,
                                                                     "IN2",
                                                                     _ud.normalize("NFKD", _pyeng.u_area)),
                                "Ix": _pyeng.convert_units(ix, "IN4", _ud.normalize("NFKD", _pyeng.u_inertia)),
                                "Iy": _pyeng.convert_units(iy, "IN4", _ud.normalize("NFKD", _pyeng.u_inertia))
                                }

    def __get_material_properties(self):
        for material in _resources.STRUCTURAL_MATERIALS:
            if material == self.material:
                su, sy, density, elastic_modulus = _resources.STRUCTURAL_MATERIALS[material]
                mass = density * _pyeng.convert_units(self.volume, _ud.normalize("NFKD", _pyeng.u_volume), "IN3")
                return {"Beam Mass": _pyeng.convert_units(mass, "lb", _pyeng.u_mass),
                        "Tensile Strength": _pyeng.convert_units(su,
                                                                 "PSI", _ud.normalize("NFKD", _pyeng.u_pressure)),
                        "Yield Strength": _pyeng.convert_units(sy,
                                                               "PSI", _ud.normalize("NFKD", _pyeng.u_pressure)),
                        "Elastic Modulus": _pyeng.convert_units(elastic_modulus,
                                                                "PSI", _ud.normalize("NFKD", _pyeng.u_pressure))}


class Support:
    __support_count = 0

    def __init__(self, location, support_type: str, beam: object):
        Support.__support_count += 1
        self.__instance = Support.__support_count
        if not isinstance(beam, Beam):
            raise ValueError(f"Expected {Beam}, got {type(beam)} instead")
        if isinstance(location, (int, float)):
            self.node = (beam.start_node[0] + (location/beam.length * beam.horizontal_dist), beam.start_node[1] + (location/beam.length * beam.vertical_dist))
            self.location = location
        elif isinstance(location, tuple):
            self.node = location
            self.location = _math.sqrt(self.node[0] ** 2 + self.node[1] ** 2)
        if support_type.upper() not in _resources.STRUCTURAL_SUPPORTS:
            raise ValueError(f"{support_type} is not a valid support type, please use help for valid support types.")
        if beam.length < self.location or self.location < 0:
            raise ValueError("Location must be on a beam.")
        self.support_type = support_type.upper()
        self.beam = beam
        beam.supports.append(self)

    def __repr__(self):
        return f"Support({self.location}, {self.support_type}, Beam {int(self.beam)})"

    def __str__(self):
        return f"Beam {int(self.beam)} {self.support_type.lower()} " \
               f"support {self.__instance} at location {self.location} {_pyeng.u_length}"

    def __int__(self):
        return self.__instance


def show_structure(structure):
    struct_height = 0
    struct_length = 0
    for beam in structure:
        if abs(beam.vertical_dist) > struct_height:
            struct_height = abs(beam.vertical_dist)
        if abs(beam.horizontal_dist) > struct_length:
            struct_length = abs(beam.horizontal_dist)
    for beam in structure:
        if abs(beam.vertical_dist) > struct_height:
            struct_height = abs(beam.vertical_dist)
        if abs(beam.horizontal_dist) > struct_length:
            struct_length = abs(beam.horizontal_dist)
        beam_x = (beam.beam_element[0][0], beam.beam_element[1][0])
        beam_y = (beam.beam_element[0][1], beam.beam_element[1][1])
        _plt.plot(beam_x, beam_y, "-")
        _plt.annotate(f"Beam {int(beam)}",
                      xy=(beam_x[0] + beam.horizontal_dist / 2, beam_y[0] + beam.vertical_dist / 2),
                      xytext=(0 if beam.vertical_dist >= 0 else 5,
                              5 if beam.start_node[1] < struct_height and beam.end_node[1] < struct_height else -10),
                      textcoords="offset points", fontsize=8)
        if len(beam.supports) > 0:
            for support in beam.supports:
                if support.support_type == "PIN":
                    support_x = (support.node[0] - struct_length / 12,
                                 support.node[0],
                                 support.node[0] + struct_length / 12,
                                 support.node[0] - struct_length / 12)
                    support_y = (support.node[1] - struct_height / 10,
                                 support.node[1],
                                 support.node[1] - struct_height / 10,
                                 support.node[1] - struct_height / 10)
                    _plt.annotate(f"Support {int(support)}",
                                  xy=(support_x[1], support_y[1]),
                                  xytext=(15 if int(support) <= 1 else -55, -15),
                                  textcoords="offset points",
                                  fontsize=8)
                    _plt.plot(support_x, support_y, "o-", color="black")
                elif support.support_type == "FIX":
                    support_x = (support.node[0] - struct_length / 12,
                                 support.node[0],
                                 support.node[0] + struct_length / 12,
                                 support.node[0] - struct_length / 12)
                    support_y = (support.node[1] - struct_height / 10,
                                 support.node[1],
                                 support.node[1] - struct_height / 10,
                                 support.node[1] - struct_height / 10)
                    _plt.annotate(f"Support {int(support)}",
                                  xy=(support_x[1], support_y[1]),
                                  xytext=(15 if int(support) < 1 else -55, -15),
                                  textcoords="offset points",
                                  fontsize=8)
                    _plt.fill(support_x, support_y, "black")
                    _plt.plot(support_x, support_y, "-", color="black")
                elif support.support_type == "ROLLER":
                    support_x = (support.node[0] - struct_length / 12,
                                 support.node[0],
                                 support.node[0] + struct_length / 12,
                                 support.node[0] - struct_length / 12)
                    support_y = (support.node[1] - struct_height / 10,
                                 support.node[1],
                                 support.node[1] - struct_height / 10,
                                 support.node[1] - struct_height / 10)
                    _plt.annotate(f"Support {int(support)}",
                                  xy=(support_x[1], support_y[1]),
                                  xytext=(15 if int(support) < 1 else -55, -15),
                                  textcoords="offset points",
                                  fontsize=8)
                    _plt.plot(support_x, support_y, "o-", markerfacecolor="none", color="black")
                elif support.support_type == "SPRING":
                    support_x = (support.node[0] - struct_length / 12,
                                 support.node[0],
                                 support.node[0] + struct_length / 12,
                                 support.node[0] - struct_length / 12)
                    support_y = (support.node[1] - struct_height / 10, support.node[1],
                                 support.node[1] - struct_height / 10, support.node[1] - struct_height / 10)
                    _plt.annotate(f"Support {int(support)}",
                                  xy=(support_x[1], support_y[1]),
                                  xytext=(15 if int(support) < 1 else -55, -15),
                                  textcoords="offset points",
                                  fontsize=8)
                    _plt.plot(support_x, support_y, "--", markerfacecolor="none", color="black")
    _plt.xlabel(f"Length [{_pyeng.u_length}]")
    _plt.ylabel(f"Height [{_pyeng.u_length}]")
    _plt.show()
