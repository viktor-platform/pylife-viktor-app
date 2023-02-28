from viktor import ViktorController
from viktor.parametrization import ViktorParametrization


class Parametrization(ViktorParametrization):
    pass


class Controller(ViktorController):
    viktor_enforce_field_constraints = True  # Resolves upgrade instruction https://docs.viktor.ai/sdk/upgrades#U83

    label = 'My Entity Type'
    parametrization = Parametrization
