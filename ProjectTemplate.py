import os
import imp
import subprocess
INPUT_SERVER_PORT = 10000
plaxis_path = r'c:\Program Files (x86)\Plaxis\Plaxis 2D'


class SimpleProject(object):
    """
    Class that provides a way to quickly setup a project for example purposes.
    """

    def __init__(self, g_input):
        # Import module from plaxis_path. This enables us to store this script
        # anywhere we want to.
        found_module = imp.find_module('plxscripting', [plaxis_path])
        plxscripting = imp.load_module('plxscripting', *found_module)

        from plxscripting.easy import new_server
        self._new_server = new_server

        args = [os.path.join(plaxis_path, "Plaxis2DXInput.exe"),
                "--AppServerPort={}".format(INPUT_SERVER_PORT)]
        self._input_process = subprocess.Popen(args)

        self._s_input, self._g_input = self._new_server(
                'localhost', 10000, timeout=10.0)

    def gather_results(self):
        raise NotImplementedError("Override gather_results in subclass.")

    def output_results(self):
        raise NotImplementedError("Override output_results in subclass.")

    def close_input(self):
        self._input_process.kill()

    @property
    def g_input(self):
        return self._g_input

    def add_soil_layers(self):
        raise NotImplementedError("Override add_soil_layers in subclass.")

    def apply_soil_material(self):
        SAND_PARAMETERS = [
            ('MaterialName', 'Sand'),
            ('Colour', 10676870),
            ('SoilModel', 3),  # Hardening soil
            ('DrainageType', 'Drained'),
            ('gammaUnsat', 17),
            ('gammaSat', 20),
            ('E50ref', 43000),
            ('EoedRef', 28000),
            ('EurRef', 129000),
            ('powerm', 0.5),
            ('cref', 1),
            ('phi', 34.0),
            ('psi', 4.0),
            ('nu', 0.2),
            ('Rinter', 0.7),
            ('K0NC', 0.5),
            ('OCR', 1.0),
            ('POP', 0.0)
        ]
        sand = self._g_input.soilmat(*SAND_PARAMETERS)

        for soil_layer in self._g_input.SoilLayers:
            self._g_input.setmaterial(soil_layer, sand)

    def add_structures(self):
        pass  # Not adding any plates is fine too.

    def apply_plate_materials(self):
        DIAPHRAGM_WALL_PARAMETERS = [
            ('MaterialName', 'Wall'),
            ('Colour', 16711680),
            ('Elasticity', 0),  # Elastic
            ('IsIsotropic', True),
            ('IsEndBearing', True),
            ('EA', 12000000),
            ('EI', 120000),
            ('nu', 0.15),
            ('d', 0.34641),
            ('w', 8.3),
            ('Mp', 1000000000000000.0),
            ('Np', 10000000000.0),
            ('Np2', 10000000000.0),
            ('RayleighAlpha', 0),
            ('RayleighBeta', 0),
            ('Gref', 15061311)
        ]
        diaphragm_wall_material = \
            self._g_input.platemat(*DIAPHRAGM_WALL_PARAMETERS)

        for plate in self._g_input.Plates:
            self._g_input.setmaterial(plate, diaphragm_wall_material)

    def mesh(self):
        self._g_input.gotomesh()
        self._g_input.mesh(0.06)

    def select_curve_points(self):
        pass  # Not selecting any curve-points is fine too.

    def configure_phases(self):
        raise NotImplementedError("Override configure_phases in subclass.")

    def make_project(self):
        self.add_soil_layers()
        self.apply_soil_material()
        self.add_structures()
        self.apply_plate_material()
        self.mesh()
        self.select_curve_points()
        self.configure_phases()
        self._g_input.calculate()

    def run(project_class):
        # Replace with the path to your PLAXIS installation.
        project = project_class(r"c:\Program Files (x86)\Plaxis\PLAXIS 2DX")
        project.make_project()
        project.gather_results()
        project.output_results()
        project.close_input()
