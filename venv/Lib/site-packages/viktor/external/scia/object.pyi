import abc
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

class _SciaObject:
    def __init__(self, object_id: int, name: str) -> None: ...
    @property
    def object_id(self) -> int: ...
    @property
    def name(self) -> str: ...

class Layer(_SciaObject):
    def __init__(self, object_id: int, name: str, comment: str = ..., structural_model_only: bool = ..., current_used_activity: bool = ...) -> None: ...

class Material(_SciaObject):
    def __init__(self, object_id: int, name: str) -> None: ...

class NonLinearFunction(_SciaObject):
    class Type(Enum):
        TRANSLATION: NonLinearFunction.Type
        ROTATION: NonLinearFunction.Type
        NONLINEAR_SUBSOIL: NonLinearFunction.Type
    class Support(Enum):
        RIGID: NonLinearFunction.Support
        FREE: NonLinearFunction.Support
        FLEXIBLE: NonLinearFunction.Support
    function_type: Any
    positive_end: Any
    negative_end: Any
    def __init__(self, object_id: int, name: str, function_type: Type, positive_end: Support, negative_end: Support, impulse: List[Tuple[float, float]]) -> None: ...
    @property
    def impulse(self) -> List[Tuple[float, float]]: ...

class Subsoil(_SciaObject):
    class C1z(Enum):
        FLEXIBLE: Subsoil.C1z
        NONLINEAR_FUNCTION: Subsoil.C1z
    c1x: Any
    c1y: Any
    c1z: Any
    stiffness: Any
    c2x: Any
    c2y: Any
    is_drained: Any
    water_air_in_clay_subgrade: Any
    specific_weight: Any
    fi: Any
    sigma_oc: Any
    c: Any
    cu: Any
    def __init__(self, object_id: int, name: str, stiffness: float, c1x: float = ..., c1y: float = ..., c1z: C1z = ..., nonlinear_function: NonLinearFunction = ..., c2x: float = ..., c2y: float = ..., is_drained: bool = ..., water_air_in_clay_subgrade: bool = ..., specific_weight: float = ..., fi: float = ..., sigma_oc: float = ..., c: float = ..., cu: float = ...) -> None: ...
    @property
    def nonlinear_function(self) -> Optional[NonLinearFunction]: ...

class Orthotropy(_SciaObject):
    class _Type(Enum):
        STANDARD: Orthotropy._Type
    thickness: Any
    D11: Any
    D22: Any
    D12: Any
    D33: Any
    D44: Any
    D55: Any
    d11: Any
    d22: Any
    d12: Any
    d33: Any
    kxy: Any
    kyx: Any
    def __init__(self, object_id: int, name: str, material: Material, thickness: float, D11: float = ..., D22: float = ..., D12: float = ..., D33: float = ..., D44: float = ..., D55: float = ..., d11: float = ..., d22: float = ..., d12: float = ..., d33: float = ..., kxy: float = ..., kyx: float = ...) -> None: ...

class CrossSection(_SciaObject, ABC, metaclass=abc.ABCMeta):
    material: Any
    @abstractmethod
    def __init__(self, object_id: int, name: str, material: Material): ...

class RectangularCrossSection(CrossSection):
    width: Any
    height: Any
    def __init__(self, object_id: int, name: str, material: Material, width: float, height: float) -> None: ...

class CircularCrossSection(CrossSection):
    diameter: Any
    def __init__(self, object_id: int, name: str, material: Material, diameter: float) -> None: ...

class CircularHollowCrossSection(CrossSection):
    diameter: Any
    thickness: Any
    def __init__(self, object_id: int, name: str, material: Material, diameter: float, thickness: float) -> None: ...

class ComposedCrossSection(CrossSection, ABC, metaclass=abc.ABCMeta):
    material_2: Any
    @abstractmethod
    def __init__(self, object_id: int, name: str, material: Material, material_2: Material): ...

class CircularComposedCrossSection(ComposedCrossSection):
    diameter: Any
    thickness: Any
    def __init__(self, object_id: int, name: str, material: Material, material_2: Material, diameter: float, thickness: float) -> None: ...

class NumericalCrossSection(CrossSection):
    A: Any
    Ay: Any
    Az: Any
    AL: Any
    AD: Any
    cYUCS: Any
    cZUCS: Any
    alpha: Any
    Iy: Any
    Iz: Any
    Wely: Any
    Welz: Any
    Wply: Any
    Wplz: Any
    Mply_plus: Any
    Mply_min: Any
    Mplz_plus: Any
    Mplz_min: Any
    dy: Any
    dz: Any
    It: Any
    Iw: Any
    beta_y: Any
    beta_z: Any
    def __init__(self, object_id: int, name: str, material: Material, *, A: float = ..., Ay: float = ..., Az: float = ..., AL: float = ..., AD: float = ..., cYUCS: float = ..., cZUCS: float = ..., alpha: float = ..., Iy: float = ..., Iz: float = ..., Wely: float = ..., Welz: float = ..., Wply: float = ..., Wplz: float = ..., Mply_plus: float = ..., Mply_min: float = ..., Mplz_plus: float = ..., Mplz_min: float = ..., dy: float = ..., dz: float = ..., It: float = ..., Iw: float = ..., beta_y: float = ..., beta_z: float = ...) -> None: ...

class LibraryCrossSection(CrossSection):
    class Section(Enum):
        I: LibraryCrossSection.Section
        RECTANGULAR_HOLLOW: LibraryCrossSection.Section
        CIRCULAR_HOLLOW: LibraryCrossSection.Section
        L: LibraryCrossSection.Section
        CHANNEL: LibraryCrossSection.Section
        T: LibraryCrossSection.Section
        FULL_RECTANGULAR: LibraryCrossSection.Section
        FULL_CIRCULAR: LibraryCrossSection.Section
        ASYMMETRIC_I: LibraryCrossSection.Section
        ROLLED_Z: LibraryCrossSection.Section
        GENERAL_COLD_FORMED: LibraryCrossSection.Section
        COLD_FORMED_ANGLE: LibraryCrossSection.Section
        COLD_FORMED_CHANNEL: LibraryCrossSection.Section
        COLD_FORMED_Z: LibraryCrossSection.Section
        COLD_FORMED_C: LibraryCrossSection.Section
        COLD_FORMED_OMEGA: LibraryCrossSection.Section
        COLD_FORMED_C_EAVES_BEAM: LibraryCrossSection.Section
        COLD_FORMED_C_PLUS: LibraryCrossSection.Section
        COLD_FORMED_ZED: LibraryCrossSection.Section
        COLD_FORMED_ZED_ASYMMETRIC_LIPS: LibraryCrossSection.Section
        COLD_FORMED_ZED_INCLINED_LIP: LibraryCrossSection.Section
        COLD_FORMED_SIGMA: LibraryCrossSection.Section
        COLD_FORMED_SIGMA_STIFFENED: LibraryCrossSection.Section
        COLD_FORMED_SIGMA_PLUS: LibraryCrossSection.Section
        COLD_FORMED_SIGMA_EAVES_BEAM: LibraryCrossSection.Section
        COLD_FORMED_SIGMA_PLUS_EAVES_BEAM: LibraryCrossSection.Section
        COLD_FORMED_ZED_BOTH_LIPS_INCLINED: LibraryCrossSection.Section
        COLD_FORMED_I_PLUS: LibraryCrossSection.Section
        COLD_FORMED_IS_PLUS: LibraryCrossSection.Section
        COLD_FORMED_SIGMA_ASYMMETRIC: LibraryCrossSection.Section
        COLD_FORMED_2C: LibraryCrossSection.Section
        RAIL_TYPE_KA: LibraryCrossSection.Section
        RAIL_TYPE_KF: LibraryCrossSection.Section
        RAIL_TYPE_KG: LibraryCrossSection.Section
        SFB: LibraryCrossSection.Section
        IFBA: LibraryCrossSection.Section
        IFBB: LibraryCrossSection.Section
        THQ: LibraryCrossSection.Section
        VIRTUAL_JOIST: LibraryCrossSection.Section
        MINUS_L: LibraryCrossSection.Section
    section: Any
    profile: Any
    def __init__(self, object_id: int, name: str, material: Material, section: Section, profile: str) -> None: ...

class Node(_SciaObject):
    x: Any
    y: Any
    z: Any
    def __init__(self, object_id: int, name: str, x: float, y: float, z: float) -> None: ...

class Beam(_SciaObject):
    lcs_rotation: Any
    def __init__(self, object_id: int, name: str, begin_node: Node, end_node: Node, cross_section: CrossSection, ez: float = ..., lcs_rotation: float = ..., layer: Layer = ...) -> None: ...
    @property
    def begin_node(self) -> Node: ...
    @property
    def end_node(self) -> Node: ...
    @property
    def cross_section(self) -> CrossSection: ...
    @property
    def ez(self) -> float: ...

class CrossLink(_SciaObject):
    beam_1: Any
    beam_2: Any
    def __init__(self, object_id: int, name: str, beam_1: Beam, beam_2: Beam) -> None: ...

class ArbitraryProfileSpan:
    class TypeOfCss(Enum):
        PRISMATIC: ArbitraryProfileSpan.TypeOfCss
        PARAM_HAUNCH: ArbitraryProfileSpan.TypeOfCss
        TWO_CSS: ArbitraryProfileSpan.TypeOfCss
    class Alignment(Enum):
        DEFAULT: ArbitraryProfileSpan.Alignment
        CENTER_LINE: ArbitraryProfileSpan.Alignment
        TOP_SURFACE: ArbitraryProfileSpan.Alignment
        BOTTOM_SURFACE: ArbitraryProfileSpan.Alignment
        LEFT_SURFACE: ArbitraryProfileSpan.Alignment
        RIGHT_SURFACE: ArbitraryProfileSpan.Alignment
        TOP_LEFT: ArbitraryProfileSpan.Alignment
        TOP_RIGHT: ArbitraryProfileSpan.Alignment
        BOTTOM_LEFT: ArbitraryProfileSpan.Alignment
        BOTTOM_RIGHT: ArbitraryProfileSpan.Alignment
    length: Any
    type_of_css: Any
    alignment: Any
    def __init__(self, length: float, type_of_css: TypeOfCss, cross_section_start: CrossSection, cross_section_end: CrossSection, alignment: Alignment) -> None: ...
    @property
    def cross_section_start(self) -> CrossSection: ...
    @property
    def cross_section_end(self) -> CrossSection: ...

class ArbitraryProfile(_SciaObject):
    class CDef(Enum):
        ABSOLUTE: ArbitraryProfile.CDef
        RELATIVE: ArbitraryProfile.CDef
    c_def: Any
    def __init__(self, object_id: int, name: str, beam: Beam, c_def: CDef, cross_section: CrossSection, spans: List[ArbitraryProfileSpan]) -> None: ...
    @property
    def beam(self) -> Beam: ...
    @property
    def cross_section(self) -> CrossSection: ...
    @property
    def spans(self) -> List[ArbitraryProfileSpan]: ...

class HingeOnBeam(_SciaObject):
    class Position(Enum):
        BEGIN: HingeOnBeam.Position
        END: HingeOnBeam.Position
        BOTH: HingeOnBeam.Position
    class Freedom(Enum):
        FREE: HingeOnBeam.Freedom
        RIGID: HingeOnBeam.Freedom
        FLEXIBLE: HingeOnBeam.Freedom
    position: Any
    def __init__(self, object_id: int, name: str, beam: Beam, position: Position, freedom_ux: Freedom = ..., freedom_uy: Freedom = ..., freedom_uz: Freedom = ..., freedom_fix: Freedom = ..., freedom_fiy: Freedom = ..., freedom_fiz: Freedom = ..., stiffness_ux: float = ..., stiffness_uy: float = ..., stiffness_uz: float = ..., stiffness_fix: float = ..., stiffness_fiy: float = ..., stiffness_fiz: float = ...) -> None: ...
    @property
    def beam(self) -> Beam: ...
    @property
    def freedom(self) -> Tuple[HingeOnBeam.Freedom, HingeOnBeam.Freedom, HingeOnBeam.Freedom, HingeOnBeam.Freedom, HingeOnBeam.Freedom, HingeOnBeam.Freedom]: ...
    @property
    def stiffness(self) -> Tuple[float, float, float, float, float, float]: ...

class HingeOnPlane(_SciaObject):
    class CDef(Enum):
        ABSOLUTE: HingeOnPlane.CDef
        RELATIVE: HingeOnPlane.CDef
    class Freedom(Enum):
        FREE: HingeOnPlane.Freedom
        RIGID: HingeOnPlane.Freedom
        FLEXIBLE: HingeOnPlane.Freedom
    class Origin(Enum):
        FROM_START: HingeOnPlane.Origin
        FROM_END: HingeOnPlane.Origin
    def __init__(self, object_id: int, name: str, edge: Union[Tuple[Plane, int], InternalEdge], ux: Freedom = ..., stiffness_ux: float = ..., uy: Freedom = ..., stiffness_uy: float = ..., uz: Freedom = ..., stiffness_uz: float = ..., fix: Freedom = ..., stiffness_fix: float = ..., c_def: CDef = ..., position_x1: float = ..., position_x2: float = ..., origin: Origin = ...) -> None: ...
    @property
    def plane(self) -> Plane: ...

class Plane(_SciaObject):
    class FEMModel(Enum):
        ISOTROPIC: Plane.FEMModel
        ORTHOTROPIC: Plane.FEMModel
    class Type(Enum):
        PLATE: Plane.Type
        WALL: Plane.Type
        SHELL: Plane.Type
    material: Any
    plane_type: Any
    thickness: Any
    def __init__(self, object_id: int, name: str, thickness: float, material: Material, *, plane_type: Type = ..., layer: Layer = ..., corner_nodes: List[Node] = ..., internal_nodes: List[Node] = ..., swap_orientation: bool = ..., lcs_rotation: float = ..., fem_model: FEMModel = ..., orthotropy: Orthotropy = ..., center_node: Node = ..., vertex_node: Node = ..., axis: Tuple[float, float, float] = ...) -> None: ...
    @property
    def corner_nodes(self) -> List[Node]: ...
    @property
    def internal_nodes(self) -> List[Node]: ...
    @property
    def swap_orientation(self) -> bool: ...
    @property
    def lcs_rotation(self) -> float: ...

class LineSupport(_SciaObject, ABC, metaclass=abc.ABCMeta):
    class Constraint(Enum):
        FIXED: LineSupport.Constraint
        HINGED: LineSupport.Constraint
        SLIDING: LineSupport.Constraint
        CUSTOM: LineSupport.Constraint
    class Type(Enum):
        LINE: LineSupport.Type
        FOUNDATION_STRIP: LineSupport.Type
        WALL: LineSupport.Type
    class Freedom(Enum):
        FREE: LineSupport.Freedom
        RIGID: LineSupport.Freedom
        FLEXIBLE: LineSupport.Freedom
        RIGID_PRESS_ONLY: LineSupport.Freedom
        RIGID_TENSION_ONLY: LineSupport.Freedom
        FLEXIBLE_PRESS_ONLY: LineSupport.Freedom
        FLEXIBLE_TENSION_ONLY: LineSupport.Freedom
        NONLINEAR: LineSupport.Freedom
    class CSys(Enum):
        GLOBAL: LineSupport.CSys
        LOCAL: LineSupport.CSys
    class CDef(Enum):
        ABSOLUTE: LineSupport.CDef
        RELATIVE: LineSupport.CDef
    class Extent(Enum):
        FULL: LineSupport.Extent
        SPAN: LineSupport.Extent
    class Origin(Enum):
        FROM_START: LineSupport.Origin
        FROM_END: LineSupport.Origin
    c_sys: Any
    c_def: Any
    position_x1: Any
    position_x2: Any
    origin: Any
    @abstractmethod
    def __init__(self, object_id: int, name: str, x: Freedom = ..., stiffness_x: float = ..., function_x: NonLinearFunction = ..., y: Freedom = ..., stiffness_y: float = ..., function_y: NonLinearFunction = ..., z: Freedom = ..., stiffness_z: float = ..., function_z: NonLinearFunction = ..., rx: Freedom = ..., stiffness_rx: float = ..., function_rx: NonLinearFunction = ..., ry: Freedom = ..., stiffness_ry: float = ..., function_ry: NonLinearFunction = ..., rz: Freedom = ..., stiffness_rz: float = ..., function_rz: NonLinearFunction = ..., c_sys: CSys = ..., c_def: CDef = ..., position_x1: float = ..., position_x2: float = ..., origin: Origin = ...): ...
    @property
    def constraint(self) -> LineSupport.Constraint: ...
    @property
    def freedom(self) -> Tuple[LineSupport.Freedom, LineSupport.Freedom, LineSupport.Freedom, LineSupport.Freedom, LineSupport.Freedom, LineSupport.Freedom]: ...
    @property
    def stiffness(self) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]: ...
    @property
    def function_x(self) -> Optional[NonLinearFunction]: ...
    @property
    def function_y(self) -> Optional[NonLinearFunction]: ...
    @property
    def function_z(self) -> Optional[NonLinearFunction]: ...
    @property
    def function_rx(self) -> Optional[NonLinearFunction]: ...
    @property
    def function_ry(self) -> Optional[NonLinearFunction]: ...
    @property
    def function_rz(self) -> Optional[NonLinearFunction]: ...

class LineSupportLine(LineSupport):
    extent: Any
    def __init__(self, object_id: int, name: str, beam: Beam, x: LineSupport.Freedom = ..., stiffness_x: float = ..., function_x: NonLinearFunction = ..., y: LineSupport.Freedom = ..., stiffness_y: float = ..., function_y: NonLinearFunction = ..., z: LineSupport.Freedom = ..., stiffness_z: float = ..., function_z: NonLinearFunction = ..., rx: LineSupport.Freedom = ..., stiffness_rx: float = ..., function_rx: NonLinearFunction = ..., ry: LineSupport.Freedom = ..., stiffness_ry: float = ..., function_ry: NonLinearFunction = ..., rz: LineSupport.Freedom = ..., stiffness_rz: float = ..., function_rz: NonLinearFunction = ..., c_sys: LineSupport.CSys = ..., extent: LineSupport.Extent = ..., c_def: LineSupport.CDef = ..., position_x1: float = ..., position_x2: float = ..., origin: LineSupport.Origin = ...) -> None: ...
    @property
    def beam(self) -> Beam: ...
    @property
    def spring_type(self) -> LineSupport.Type: ...

class LineSupportSurface(LineSupport):
    def __init__(self, object_id: int, name: str, edge: Union[Tuple[Plane, int], InternalEdge], x: LineSupport.Freedom = ..., stiffness_x: float = ..., y: LineSupport.Freedom = ..., stiffness_y: float = ..., z: LineSupport.Freedom = ..., stiffness_z: float = ..., rx: LineSupport.Freedom = ..., stiffness_rx: float = ..., ry: LineSupport.Freedom = ..., stiffness_ry: float = ..., rz: LineSupport.Freedom = ..., stiffness_rz: float = ..., c_sys: LineSupport.CSys = ..., c_def: LineSupport.CDef = ..., position_x1: float = ..., position_x2: float = ..., origin: LineSupport.Origin = ...) -> None: ...
    @property
    def plane(self) -> Plane: ...

class SurfaceSupportSurface(_SciaObject):
    def __init__(self, object_id: int, name: str, plane: Plane, subsoil: Subsoil) -> None: ...
    @property
    def plane(self) -> Plane: ...
    @property
    def subsoil(self) -> Subsoil: ...

class OpenSlab(_SciaObject):
    def __init__(self, object_id: int, name: str, plane: Plane, corner_nodes: List[Node]) -> None: ...
    @property
    def plane(self) -> Plane: ...
    @property
    def corner_nodes(self) -> List[Node]: ...

class InternalEdge(_SciaObject):
    def __init__(self, object_id: int, name: str, plane: Plane, node_1: Node, node_2: Node) -> None: ...
    @property
    def plane(self) -> Plane: ...
    @property
    def node_1(self) -> Node: ...
    @property
    def node_2(self) -> Node: ...

class PointSupport(_SciaObject):
    class Constraint(Enum):
        FIXED: PointSupport.Constraint
        HINGED: PointSupport.Constraint
        SLIDING: PointSupport.Constraint
        CUSTOM: PointSupport.Constraint
    class Type(Enum):
        STANDARD: PointSupport.Type
        PAD_FOUNDATION: PointSupport.Type
        COLUMN: PointSupport.Type
    class Freedom(Enum):
        FREE: PointSupport.Freedom
        RIGID: PointSupport.Freedom
        FLEXIBLE: PointSupport.Freedom
    class CSys(Enum):
        GLOBAL: PointSupport.CSys
        LOCAL: PointSupport.CSys
    spring_type: Any
    freedom: Any
    stiffness: Any
    default_size: Any
    c_sys: Any
    def __init__(self, object_id: int, name: str, node: Node, spring_type: Type, freedom: Tuple[Freedom, Freedom, Freedom, Freedom, Freedom, Freedom], stiffness: Tuple[float, float, float, float, float, float], c_sys: CSys, default_size: float = ..., angle: Tuple[float, float, float] = ...) -> None: ...
    @property
    def node(self) -> Node: ...
    @property
    def constraint(self) -> PointSupport.Constraint: ...

class PointSupportLine(_SciaObject):
    class Freedom(Enum):
        FREE: PointSupportLine.Freedom
        RIGID: PointSupportLine.Freedom
        FLEXIBLE: PointSupportLine.Freedom
    class CSys(Enum):
        GLOBAL: PointSupportLine.CSys
        LOCAL: PointSupportLine.CSys
    class CDef(Enum):
        ABSOLUTE: PointSupportLine.CDef
        RELATIVE: PointSupportLine.CDef
    class Origin(Enum):
        FROM_START: PointSupportLine.Origin
        FROM_END: PointSupportLine.Origin
    def __init__(self, object_id: int, name: str, beam: Beam, x: PointSupportLine.Freedom = ..., stiffness_x: float = ..., y: PointSupportLine.Freedom = ..., stiffness_y: float = ..., z: PointSupportLine.Freedom = ..., stiffness_z: float = ..., rx: PointSupportLine.Freedom = ..., stiffness_rx: float = ..., ry: PointSupportLine.Freedom = ..., stiffness_ry: float = ..., rz: PointSupportLine.Freedom = ..., stiffness_rz: float = ..., default_size: float = ..., c_sys: PointSupportLine.CSys = ..., c_def: PointSupportLine.CDef = ..., position_x: float = ..., origin: PointSupportLine.Origin = ..., repeat: int = ..., delta_x: float = ...) -> None: ...

class RigidArm(_SciaObject):
    hinge_on_master: Any
    hinge_on_slave: Any
    def __init__(self, object_id: int, name: str, master_node: Node, slave_node: Node, hinge_on_master: bool, hinge_on_slave: bool) -> None: ...
    @property
    def master_node(self) -> Node: ...
    @property
    def slave_node(self) -> Node: ...

class SectionOnBeam(_SciaObject):
    class CDef(Enum):
        ABSOLUTE: SectionOnBeam.CDef
        RELATIVE: SectionOnBeam.CDef
    class Origin(Enum):
        FROM_START: SectionOnBeam.Origin
        FROM_END: SectionOnBeam.Origin
    c_def: Any
    position_x: Any
    origin: Any
    repeat: Any
    delta_x: Any
    def __init__(self, object_id: int, name: str, beam: Beam, c_def: CDef, position_x: float, origin: Origin, repeat: int, delta_x: float) -> None: ...
    @property
    def beam(self) -> Beam: ...

class LoadGroup(_SciaObject):
    class LoadOption(Enum):
        PERMANENT: LoadGroup.LoadOption
        VARIABLE: LoadGroup.LoadOption
        ACCIDENTAL: LoadGroup.LoadOption
        SEISMIC: LoadGroup.LoadOption
    class RelationOption(Enum):
        STANDARD: LoadGroup.RelationOption
        EXCLUSIVE: LoadGroup.RelationOption
        TOGETHER: LoadGroup.RelationOption
    class LoadTypeOption(Enum):
        CAT_A: LoadGroup.LoadTypeOption
        CAT_B: LoadGroup.LoadTypeOption
        CAT_C: LoadGroup.LoadTypeOption
        CAT_D: LoadGroup.LoadTypeOption
        CAT_E: LoadGroup.LoadTypeOption
        CAT_F: LoadGroup.LoadTypeOption
        CAT_G: LoadGroup.LoadTypeOption
        CAT_H: LoadGroup.LoadTypeOption
        SNOW: LoadGroup.LoadTypeOption
        WIND: LoadGroup.LoadTypeOption
        TEMPERATURE: LoadGroup.LoadTypeOption
        RAIN_WATER: LoadGroup.LoadTypeOption
        CONSTRUCTION_LOADS: LoadGroup.LoadTypeOption
    load_option: Any
    def __init__(self, object_id: int, name: str, load_option: LoadOption, relation: RelationOption = ..., load_type: LoadTypeOption = ...) -> None: ...
    @property
    def relation(self) -> Optional[LoadGroup.RelationOption]: ...
    @property
    def load_type(self) -> Optional[LoadGroup.LoadTypeOption]: ...

class LoadCase(ABC, _SciaObject, metaclass=abc.ABCMeta):
    class ActionType(Enum):
        PERMANENT: LoadCase.ActionType
        VARIABLE: LoadCase.ActionType
    class PermanentLoadType(Enum):
        SELF_WEIGHT: LoadCase.PermanentLoadType
        STANDARD: LoadCase.PermanentLoadType
        PRIMARY_EFFECT: LoadCase.PermanentLoadType
    class VariableLoadType(Enum):
        STATIC: LoadCase.VariableLoadType
        PRIMARY_EFFECT: LoadCase.VariableLoadType
    class Specification(Enum):
        STANDARD: LoadCase.Specification
        TEMPERATURE: LoadCase.Specification
        STATIC_WIND: LoadCase.Specification
        EARTHQUAKE: LoadCase.Specification
        SNOW: LoadCase.Specification
    class Duration(Enum):
        LONG: LoadCase.Duration
        MEDIUM: LoadCase.Duration
        SHORT: LoadCase.Duration
        INSTANTANEOUS: LoadCase.Duration
    class Direction(Enum):
        NEG_Z: LoadCase.Direction
        POS_Z: LoadCase.Direction
        NEG_Y: LoadCase.Direction
        POS_Y: LoadCase.Direction
        NEG_X: LoadCase.Direction
        POS_X: LoadCase.Direction
    description: Any
    action_type: Any
    @abstractmethod
    def __init__(self, object_id: int, name: str, description: str, action_type: ActionType, load_group: LoadGroup): ...
    @property
    def load_group(self) -> LoadGroup: ...
    @property
    @abstractmethod
    def load_type(self) -> Union[LoadCase.PermanentLoadType, LoadCase.VariableLoadType]: ...
    @property
    @abstractmethod
    def direction(self) -> Optional[LoadCase.Direction]: ...
    @property
    @abstractmethod
    def specification(self) -> Optional[LoadCase.Specification]: ...
    @property
    @abstractmethod
    def duration(self) -> Optional[LoadCase.Duration]: ...
    @property
    @abstractmethod
    def master(self) -> Optional[str]: ...
    @property
    @abstractmethod
    def primary_effect(self) -> Optional[LoadCase]: ...

class PermanentLoadCase(LoadCase):
    def __init__(self, object_id: int, name: str, description: str, load_group: LoadGroup, load_type: LoadCase.PermanentLoadType, direction: LoadCase.Direction = ..., primary_effect: LoadCase = ...) -> None: ...
    @property
    def load_type(self) -> LoadCase.PermanentLoadType: ...
    @property
    def direction(self) -> Optional[LoadCase.Direction]: ...
    @property
    def specification(self) -> None: ...
    @property
    def duration(self) -> None: ...
    @property
    def master(self) -> None: ...
    @property
    def primary_effect(self) -> Optional[LoadCase]: ...

class VariableLoadCase(LoadCase):
    def __init__(self, object_id: int, name: str, description: str, load_group: LoadGroup, load_type: LoadCase.VariableLoadType, specification: LoadCase.Specification = ..., duration: LoadCase.Duration = ..., primary_effect: LoadCase = ..., master: str = ...) -> None: ...
    @property
    def load_type(self) -> LoadCase.VariableLoadType: ...
    @property
    def master(self) -> Optional[str]: ...
    @property
    def specification(self) -> Optional[LoadCase.Specification]: ...
    @property
    def duration(self) -> Optional[LoadCase.Duration]: ...
    @property
    def direction(self) -> None: ...
    @property
    def primary_effect(self) -> Optional[LoadCase]: ...

class LoadCombination(_SciaObject):
    class Type(Enum):
        ENVELOPE_ULTIMATE: LoadCombination.Type
        ENVELOPE_SERVICEABILITY: LoadCombination.Type
        LINEAR_ULTIMATE: LoadCombination.Type
        LINEAR_SERVICEABILITY: LoadCombination.Type
        EN_ULS_SET_B: LoadCombination.Type
        EN_ACC_ONE: LoadCombination.Type
        EN_ACC_TWO: LoadCombination.Type
        EN_SEISMIC: LoadCombination.Type
        EN_SLS_CHAR: LoadCombination.Type
        EN_SLS_FREQ: LoadCombination.Type
        EN_SLS_QUASI: LoadCombination.Type
        EN_ULS_SET_C: LoadCombination.Type
    combination_type: Any
    def __init__(self, object_id: int, name: str, combination_type: Type, load_cases: Dict[LoadCase, float], *, description: str = ...) -> None: ...
    @property
    def load_cases(self) -> Dict[LoadCase, float]: ...

class NonLinearLoadCombination(_SciaObject):
    class Type(Enum):
        ULTIMATE: NonLinearLoadCombination.Type
        SERVICEABILITY: NonLinearLoadCombination.Type
    combination_type: Any
    def __init__(self, object_id: int, name: str, combination_type: Type, load_cases: Dict[LoadCase, float], *, description: str = ...) -> None: ...
    @property
    def load_cases(self) -> Dict[LoadCase, float]: ...

class ResultClass(_SciaObject):
    def __init__(self, object_id: int, name: str, combinations: List[LoadCombination], nonlinear_combinations: List[NonLinearLoadCombination]) -> None: ...
    @property
    def combinations(self) -> List[LoadCombination]: ...
    @property
    def nonlinear_combinations(self) -> List[NonLinearLoadCombination]: ...

class IntegrationStrip(_SciaObject):
    class _EffectiveWidthGeometry(Enum):
        CONSTANT_SYMMETRIC: IntegrationStrip._EffectiveWidthGeometry
        CONSTANT_ASYMMETRIC: IntegrationStrip._EffectiveWidthGeometry
    class _EffectiveWidthDefinition(Enum):
        WIDTH: IntegrationStrip._EffectiveWidthDefinition
        NUMBER_OF_THICKNESS: IntegrationStrip._EffectiveWidthDefinition
    point_1: Any
    point_2: Any
    width: Any
    def __init__(self, object_id: int, name: str, plane: Plane, point_1: Tuple[float, float, float], point_2: Tuple[float, float, float], width: float, effective_width_geometry: _EffectiveWidthGeometry = ..., effective_width_definition: _EffectiveWidthDefinition = ...) -> None: ...
    @property
    def plane(self) -> Plane: ...

class SectionOnPlane(_SciaObject):
    class Draw(Enum):
        UPRIGHT_TO_ELEMENT: SectionOnPlane.Draw
        ELEMENT_PLANE: SectionOnPlane.Draw
        X_DIRECTION: SectionOnPlane.Draw
        Y_DIRECTION: SectionOnPlane.Draw
        Z_DIRECTION: SectionOnPlane.Draw
    point_1: Any
    point_2: Any
    def __init__(self, object_id: int, name: str, point_1: Tuple[float, float, float], point_2: Tuple[float, float, float], draw: SectionOnPlane.Draw = ..., direction_of_cut: Tuple[float, float, float] = ...) -> None: ...

class ProjectData(_SciaObject):
    name_: Any
    part: Any
    description: Any
    author: Any
    date: Any
    def __init__(self, *, name: str = ..., part: str = ..., description: str = ..., author: str = ..., date: str = ...) -> None: ...

class MeshSetup(_SciaObject):
    average_1d: Any
    average_2d: Any
    division_2d_1d: Any
    def __init__(self, *, average_1d: float = ..., average_2d: float = ..., division_2d_1d: int = ...) -> None: ...

class SolverSetup(_SciaObject):
    neglect_shear_force_deformation: Any
    bending_theory: Any
    solver_type: Any
    number_of_sections: Any
    reinforcement_coefficient: Any
    def __init__(self, *, neglect_shear_force_deformation: bool = ..., bending_theory: str = ..., solver_type: str = ..., number_of_sections: float = ..., reinforcement_coefficient: float = ...) -> None: ...

class Concrete(_SciaObject):
    class ECPart(Enum):
        GENERAL: Concrete.ECPart
        BRIDGES: Concrete.ECPart
    thermal_expansion: Any
    unit_mass: Any
    wet_density: Any
    e_modulus: Any
    poisson: Any
    g_modulus: Any
    log_decrement: Any
    specific_heat: Any
    thermal_conductivity: Any
    fck: Any
    def __init__(self, object_id: int, name: str, part: ECPart, thermal_expansion: float = ..., unit_mass: float = ..., wet_density: float = ..., e_modulus: float = ..., poisson: float = ..., g_modulus: float = ..., log_decrement: float = ..., specific_heat: float = ..., thermal_conductivity: float = ..., *, fck: float = ...) -> None: ...
    @property
    def ec_part(self) -> Concrete.ECPart: ...

class FreeLoad(_SciaObject, ABC, metaclass=abc.ABCMeta):
    class Direction(Enum):
        X: FreeLoad.Direction
        Y: FreeLoad.Direction
        Z: FreeLoad.Direction
    class Select(Enum):
        AUTO: FreeLoad.Select
        SELECT: FreeLoad.Select
    class Type(Enum):
        FORCE: FreeLoad.Type
    class Validity(Enum):
        ALL: FreeLoad.Validity
        NEG_Z: FreeLoad.Validity
        POS_Z: FreeLoad.Validity
        FROM_TO: FreeLoad.Validity
        ZERO_Z: FreeLoad.Validity
        NEG_Z_INCL_ZERO: FreeLoad.Validity
        POS_Z_INCL_ZERO: FreeLoad.Validity
    class CSys(Enum):
        GLOBAL: FreeLoad.CSys
        MEMBER_LCS: FreeLoad.CSys
        LOAD_LCS: FreeLoad.CSys
    class Location(Enum):
        LENGTH: FreeLoad.Location
        PROJECTION: FreeLoad.Location
    direction: Any
    @abstractmethod
    def __init__(self, object_id: int, name: str, load_case: LoadCase, direction: Direction, select: Select, validity: Validity = ..., load_type: Type = ..., c_sys: CSys = ...): ...
    @property
    def load_case(self) -> LoadCase: ...

class FreeLineLoad(FreeLoad):
    class Distribution(Enum):
        UNIFORM: FreeLineLoad.Distribution
        TRAPEZOIDAL: FreeLineLoad.Distribution
    point_1: Any
    point_2: Any
    magnitude_1: Any
    magnitude_2: Any
    def __init__(self, object_id: int, name: str, load_case: LoadCase, point_1: Tuple[float, float], point_2: Tuple[float, float], direction: FreeLoad.Direction, magnitude_1: float, magnitude_2: float, distribution: Distribution = ..., validity: FreeLoad.Validity = ..., load_type: FreeLoad.Type = ..., select: FreeLoad.Select = ..., system: FreeLoad.CSys = ..., location: FreeLoad.Location = ...) -> None: ...

class FreePointLoad(FreeLoad):
    magnitude: Any
    position: Any
    def __init__(self, object_id: int, name: str, load_case: LoadCase, direction: FreeLoad.Direction, magnitude: float, position: Tuple[float, float], load_type: FreeLoad.Type = ..., validity: FreeLoad.Validity = ..., select: FreeLoad.Select = ..., system: FreeLoad.CSys = ...) -> None: ...

class FreeSurfaceLoad(FreeLoad):
    class Distribution(Enum):
        UNIFORM: FreeSurfaceLoad.Distribution
        DIR_X: FreeSurfaceLoad.Distribution
        DIR_Y: FreeSurfaceLoad.Distribution
        POINTS: FreeSurfaceLoad.Distribution
    q1: Any
    def __init__(self, object_id: int, name: str, load_case: LoadCase, direction: FreeLoad.Direction, q1: float, q2: float = ..., q3: float = ..., points: List[Tuple[float, float]] = ..., distribution: Distribution = ..., load_type: FreeLoad.Type = ..., validity: FreeLoad.Validity = ..., system: FreeLoad.CSys = ..., location: FreeLoad.Location = ..., selection: List[Plane] = ...) -> None: ...
    @property
    def q2(self) -> Optional[float]: ...
    @property
    def q3(self) -> Optional[float]: ...
    @property
    def points(self) -> Optional[List[Tuple[float, float]]]: ...
    @property
    def distribution(self) -> FreeSurfaceLoad.Distribution: ...
    @property
    def selection(self) -> Optional[List[Plane]]: ...

class LineLoad(_SciaObject):
    class CSys(Enum):
        GLOBAL: LineLoad.CSys
        LOCAL: LineLoad.CSys
    class CDef(Enum):
        ABSOLUTE: LineLoad.CDef
        RELATIVE: LineLoad.CDef
    class Direction(Enum):
        X: LineLoad.Direction
        Y: LineLoad.Direction
        Z: LineLoad.Direction
    class Distribution(Enum):
        UNIFORM: LineLoad.Distribution
        TRAPEZOIDAL: LineLoad.Distribution
    class Origin(Enum):
        FROM_START: LineLoad.Origin
        FROM_END: LineLoad.Origin
    class Type(Enum):
        FORCE: LineLoad.Type
        SELF_WEIGHT: LineLoad.Type
    load_type: Any
    distribution: Any
    load_start: Any
    load_end: Any
    direction: Any
    c_sys: Any
    position_start: Any
    position_end: Any
    c_def: Any
    origin: Any
    ey: Any
    ez: Any
    def __init__(self, object_id: int, name: str, load_case: LoadCase, beam: Beam, load_type: Type, distribution: Distribution, load_start: float, load_end: float, direction: Direction, c_sys: CSys, position_start: float, position_end: float, c_def: CDef, origin: Origin, ey: float, ez: float) -> None: ...
    @property
    def beam(self) -> Beam: ...
    @property
    def load_case(self) -> LoadCase: ...

class LineMomentOnBeam(_SciaObject):
    class CDef(Enum):
        ABSOLUTE: LineMomentOnBeam.CDef
        RELATIVE: LineMomentOnBeam.CDef
    class Direction(Enum):
        X: LineMomentOnBeam.Direction
        Y: LineMomentOnBeam.Direction
        Z: LineMomentOnBeam.Direction
    class Origin(Enum):
        FROM_START: LineMomentOnBeam.Origin
        FROM_END: LineMomentOnBeam.Origin
    m1: Any
    m2: Any
    def __init__(self, object_id: int, name: str, beam: Beam, load_case: LoadCase, m1: float, m2: float = ..., direction: Direction = ..., c_def: CDef = ..., position_x1: float = ..., position_x2: float = ..., origin: Origin = ...) -> None: ...

class LineMomentOnPlane(_SciaObject):
    class CDef(Enum):
        ABSOLUTE: LineMomentOnPlane.CDef
        RELATIVE: LineMomentOnPlane.CDef
    class Direction(Enum):
        X: LineMomentOnPlane.Direction
        Y: LineMomentOnPlane.Direction
        Z: LineMomentOnPlane.Direction
    class Origin(Enum):
        FROM_START: LineMomentOnPlane.Origin
        FROM_END: LineMomentOnPlane.Origin
    m1: Any
    m2: Any
    def __init__(self, object_id: int, name: str, edge: Union[Tuple[Plane, int], InternalEdge], load_case: LoadCase, m1: float, m2: float = ..., direction: Direction = ..., c_def: CDef = ..., position_x1: float = ..., position_x2: float = ..., origin: Origin = ...) -> None: ...
    @property
    def plane(self) -> Plane: ...

class LineForceSurface(_SciaObject):
    class CSys(Enum):
        GLOBAL: LineForceSurface.CSys
        LOCAL: LineForceSurface.CSys
    class Direction(Enum):
        X: LineForceSurface.Direction
        Y: LineForceSurface.Direction
        Z: LineForceSurface.Direction
    class Distribution(Enum):
        UNIFORM: LineForceSurface.Distribution
        TRAPEZOIDAL: LineForceSurface.Distribution
    class Location(Enum):
        LENGTH: LineForceSurface.Location
        PROJECTION: LineForceSurface.Location
    class CDef(Enum):
        ABSOLUTE: LineForceSurface.CDef
        RELATIVE: LineForceSurface.CDef
    class Origin(Enum):
        FROM_START: LineForceSurface.Origin
        FROM_END: LineForceSurface.Origin
    direction: Any
    p1: Any
    p2: Any
    def __init__(self, object_id: int, name: str, edge: Union[Tuple[Plane, int], InternalEdge], load_case: LoadCase, p1: float, p2: float = ..., direction: Direction = ..., location: Location = ..., c_sys: CSys = ..., c_def: CDef = ..., position_x1: float = ..., position_x2: float = ..., origin: Origin = ...) -> None: ...
    @property
    def plane(self) -> Plane: ...
    @property
    def load_case(self) -> LoadCase: ...
    @property
    def c_sys(self) -> LineForceSurface.CSys: ...
    @property
    def location(self) -> LineForceSurface.Location: ...
    @property
    def distribution(self) -> LineForceSurface.Distribution: ...
    @property
    def c_def(self) -> LineForceSurface.CDef: ...
    @property
    def position_x1(self) -> Optional[float]: ...
    @property
    def position_x2(self) -> Optional[float]: ...
    @property
    def origin(self) -> LineForceSurface.Origin: ...

class PointLoadNode(_SciaObject):
    class CSys(Enum):
        GLOBAL: PointLoadNode.CSys
        LOCAL: PointLoadNode.CSys
    class Direction(Enum):
        X: PointLoadNode.Direction
        Y: PointLoadNode.Direction
        Z: PointLoadNode.Direction
    load: Any
    direction: Any
    c_sys: Any
    angle: Any
    def __init__(self, object_id: int, name: str, node: Node, load_case: LoadCase, load: float, direction: Direction = ..., c_sys: CSys = ..., angle: Tuple[float, float, float] = ...) -> None: ...
    @property
    def node(self) -> Node: ...
    @property
    def load_case(self) -> LoadCase: ...

class PointLoad(_SciaObject):
    class CSys(Enum):
        GLOBAL: PointLoad.CSys
        LOCAL: PointLoad.CSys
    class CDef(Enum):
        ABSOLUTE: PointLoad.CDef
        RELATIVE: PointLoad.CDef
    class Direction(Enum):
        X: PointLoad.Direction
        Y: PointLoad.Direction
        Z: PointLoad.Direction
    class Distribution(Enum):
        UNIFORM: PointLoad.Distribution
        TRAPEZOIDAL: PointLoad.Distribution
    class Origin(Enum):
        FROM_START: PointLoad.Origin
        FROM_END: PointLoad.Origin
    class Type(Enum):
        FORCE: PointLoad.Type
    direction: Any
    load_type: Any
    load_value: Any
    c_sys: Any
    c_def: Any
    position_x: Any
    origin: Any
    repeat: Any
    ey: Any
    ez: Any
    angle: Any
    def __init__(self, object_id: int, name: str, load_case: LoadCase, beam: Beam, direction: Direction, load_type: Type, load_value: float, c_sys: CSys = ..., c_def: CDef = ..., position_x: float = ..., origin: Origin = ..., repeat: int = ..., ey: float = ..., ez: float = ..., *, angle: Tuple[float, float, float] = ...) -> None: ...
    @property
    def beam(self) -> Beam: ...
    @property
    def load_case(self) -> LoadCase: ...

class PointMomentNode(_SciaObject):
    class CSys(Enum):
        GLOBAL: PointMomentNode.CSys
        LOCAL: PointMomentNode.CSys
    class Direction(Enum):
        X: PointMomentNode.Direction
        Y: PointMomentNode.Direction
        Z: PointMomentNode.Direction
    load: Any
    direction: Any
    c_sys: Any
    def __init__(self, object_id: int, name: str, node: Node, load_case: LoadCase, load: float, direction: Direction, c_sys: CSys) -> None: ...
    @property
    def node(self) -> Node: ...
    @property
    def load_case(self) -> LoadCase: ...

class SurfaceLoad(_SciaObject):
    class Direction(Enum):
        X: SurfaceLoad.Direction
        Y: SurfaceLoad.Direction
        Z: SurfaceLoad.Direction
    class Type(Enum):
        FORCE: SurfaceLoad.Type
        SELF_WEIGHT: SurfaceLoad.Type
    class CSys(Enum):
        GLOBAL: SurfaceLoad.CSys
        LOCAL: SurfaceLoad.CSys
    class Location(Enum):
        LENGTH: SurfaceLoad.Location
        PROJECTION: SurfaceLoad.Location
    direction: Any
    load_type: Any
    load_value: Any
    c_sys: Any
    location: Any
    def __init__(self, object_id: int, name: str, load_case: LoadCase, plane: Plane, direction: Direction, load_type: Type, load_value: float, c_sys: CSys, location: Location) -> None: ...
    @property
    def plane(self) -> Plane: ...
    @property
    def load_case(self) -> LoadCase: ...

class ThermalLoad(_SciaObject):
    class Distribution(Enum):
        CONSTANT: ThermalLoad.Distribution
        LINEAR: ThermalLoad.Distribution
    class CDef(Enum):
        ABSOLUTE: ThermalLoad.CDef
        RELATIVE: ThermalLoad.CDef
    class Origin(Enum):
        FROM_START: ThermalLoad.Origin
        FROM_END: ThermalLoad.Origin
    distribution: Any
    delta: Any
    left_delta: Any
    right_delta: Any
    top_delta: Any
    bottom_delta: Any
    c_def: Any
    position_start: Any
    position_end: Any
    origin: Any
    def __init__(self, object_id: int, name: str, load_case: LoadCase, beam: Beam, distribution: Distribution, delta: float, left_delta: float, right_delta: float, top_delta: float, bottom_delta: float, position_start: float, position_end: float, c_def: CDef, origin: Origin) -> None: ...
    @property
    def beam(self) -> Beam: ...
    @property
    def load_case(self) -> LoadCase: ...

class ThermalSurfaceLoad(_SciaObject):
    class Distribution(Enum):
        CONSTANT: ThermalSurfaceLoad.Distribution
        LINEAR: ThermalSurfaceLoad.Distribution
    delta: Any
    top_delta: Any
    bottom_delta: Any
    def __init__(self, object_id: int, name: str, load_case: LoadCase, plane: Plane, delta: float = ..., top_delta: float = ..., bottom_delta: float = ...) -> None: ...
