from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BlockType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GRASS: _ClassVar[BlockType]
    BRICK: _ClassVar[BlockType]
    STONE: _ClassVar[BlockType]
    WATER: _ClassVar[BlockType]

class RotationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UP: _ClassVar[RotationType]
    RIGHT: _ClassVar[RotationType]
    DOWN: _ClassVar[RotationType]
    LEFT: _ClassVar[RotationType]

class ObjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BULLET: _ClassVar[ObjectType]
GRASS: BlockType
BRICK: BlockType
STONE: BlockType
WATER: BlockType
UP: RotationType
RIGHT: RotationType
DOWN: RotationType
LEFT: RotationType
BULLET: ObjectType

class ConnectRequest(_message.Message):
    __slots__ = ("strategy_version", "author_name", "strategy_uuid")
    STRATEGY_VERSION_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_NAME_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_UUID_FIELD_NUMBER: _ClassVar[int]
    strategy_version: int
    author_name: str
    strategy_uuid: str
    def __init__(self, strategy_version: _Optional[int] = ..., author_name: _Optional[str] = ..., strategy_uuid: _Optional[str] = ...) -> None: ...

class ConnectReply(_message.Message):
    __slots__ = ("session_token", "team_id", "map", "units")
    SESSION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    session_token: str
    team_id: int
    map: GameMapInfo
    units: _containers.RepeatedCompositeFieldContainer[UnitInfo]
    def __init__(self, session_token: _Optional[str] = ..., team_id: _Optional[int] = ..., map: _Optional[_Union[GameMapInfo, _Mapping]] = ..., units: _Optional[_Iterable[_Union[UnitInfo, _Mapping]]] = ...) -> None: ...

class GameFieldState(_message.Message):
    __slots__ = ("current_tick", "teams", "blocks_delta", "objects")
    CURRENT_TICK_FIELD_NUMBER: _ClassVar[int]
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    BLOCKS_DELTA_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    current_tick: int
    teams: _containers.RepeatedCompositeFieldContainer[TeamInfo]
    blocks_delta: _containers.RepeatedCompositeFieldContainer[GameFieldBlocksDelta]
    objects: _containers.RepeatedCompositeFieldContainer[ObjectInfo]
    def __init__(self, current_tick: _Optional[int] = ..., teams: _Optional[_Iterable[_Union[TeamInfo, _Mapping]]] = ..., blocks_delta: _Optional[_Iterable[_Union[GameFieldBlocksDelta, _Mapping]]] = ..., objects: _Optional[_Iterable[_Union[ObjectInfo, _Mapping]]] = ...) -> None: ...

class GameMapInfo(_message.Message):
    __slots__ = ("width_blocks", "width_px", "height_blocks", "height_px", "teams_count", "blocks")
    WIDTH_BLOCKS_FIELD_NUMBER: _ClassVar[int]
    WIDTH_PX_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_BLOCKS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_PX_FIELD_NUMBER: _ClassVar[int]
    TEAMS_COUNT_FIELD_NUMBER: _ClassVar[int]
    BLOCKS_FIELD_NUMBER: _ClassVar[int]
    width_blocks: int
    width_px: int
    height_blocks: int
    height_px: int
    teams_count: int
    blocks: _containers.RepeatedScalarFieldContainer[BlockType]
    def __init__(self, width_blocks: _Optional[int] = ..., width_px: _Optional[int] = ..., height_blocks: _Optional[int] = ..., height_px: _Optional[int] = ..., teams_count: _Optional[int] = ..., blocks: _Optional[_Iterable[_Union[BlockType, str]]] = ...) -> None: ...

class TeamInfo(_message.Message):
    __slots__ = ("id", "is_active", "score", "total_units", "current_units", "units", "is_winner", "strategy_uuid", "strategy_version", "author_name")
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_UNITS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_UNITS_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    IS_WINNER_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_UUID_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_VERSION_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_NAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    is_active: bool
    score: int
    total_units: int
    current_units: int
    units: _containers.RepeatedCompositeFieldContainer[UnitInfo]
    is_winner: bool
    strategy_uuid: str
    strategy_version: int
    author_name: str
    def __init__(self, id: _Optional[int] = ..., is_active: bool = ..., score: _Optional[int] = ..., total_units: _Optional[int] = ..., current_units: _Optional[int] = ..., units: _Optional[_Iterable[_Union[UnitInfo, _Mapping]]] = ..., is_winner: bool = ..., strategy_uuid: _Optional[str] = ..., strategy_version: _Optional[int] = ..., author_name: _Optional[str] = ...) -> None: ...

class GameFieldBlocksDelta(_message.Message):
    __slots__ = ("x", "y", "old_type", "new_type")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    OLD_TYPE_FIELD_NUMBER: _ClassVar[int]
    NEW_TYPE_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    old_type: BlockType
    new_type: BlockType
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., old_type: _Optional[_Union[BlockType, str]] = ..., new_type: _Optional[_Union[BlockType, str]] = ...) -> None: ...

class PositionAndSpeed(_message.Message):
    __slots__ = ("x_px", "y_px", "rotation", "speed")
    X_PX_FIELD_NUMBER: _ClassVar[int]
    Y_PX_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    x_px: int
    y_px: int
    rotation: RotationType
    speed: int
    def __init__(self, x_px: _Optional[int] = ..., y_px: _Optional[int] = ..., rotation: _Optional[_Union[RotationType, str]] = ..., speed: _Optional[int] = ...) -> None: ...

class ObjectInfo(_message.Message):
    __slots__ = ("position_and_speed", "type", "team_id")
    POSITION_AND_SPEED_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    position_and_speed: PositionAndSpeed
    type: ObjectType
    team_id: int
    def __init__(self, position_and_speed: _Optional[_Union[PositionAndSpeed, _Mapping]] = ..., type: _Optional[_Union[ObjectType, str]] = ..., team_id: _Optional[int] = ...) -> None: ...

class UnitInfo(_message.Message):
    __slots__ = ("position_and_speed", "id", "is_alive", "shoot_cooldown")
    POSITION_AND_SPEED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ALIVE_FIELD_NUMBER: _ClassVar[int]
    SHOOT_COOLDOWN_FIELD_NUMBER: _ClassVar[int]
    position_and_speed: PositionAndSpeed
    id: int
    is_alive: bool
    shoot_cooldown: int
    def __init__(self, position_and_speed: _Optional[_Union[PositionAndSpeed, _Mapping]] = ..., id: _Optional[int] = ..., is_alive: bool = ..., shoot_cooldown: _Optional[int] = ...) -> None: ...

class StrategyReaction(_message.Message):
    __slots__ = ("current_tick", "units")
    CURRENT_TICK_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    current_tick: int
    units: _containers.RepeatedCompositeFieldContainer[StrategyReactionUnit]
    def __init__(self, current_tick: _Optional[int] = ..., units: _Optional[_Iterable[_Union[StrategyReactionUnit, _Mapping]]] = ...) -> None: ...

class StrategyReactionUnit(_message.Message):
    __slots__ = ("id", "rotation", "will_move", "will_shoot")
    ID_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    WILL_MOVE_FIELD_NUMBER: _ClassVar[int]
    WILL_SHOOT_FIELD_NUMBER: _ClassVar[int]
    id: int
    rotation: RotationType
    will_move: bool
    will_shoot: bool
    def __init__(self, id: _Optional[int] = ..., rotation: _Optional[_Union[RotationType, str]] = ..., will_move: bool = ..., will_shoot: bool = ...) -> None: ...
