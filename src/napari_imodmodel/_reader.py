from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)
from pathlib import Path

import numpy as np

from imodmodel import ImodModel

if TYPE_CHECKING:
    from typing import Iterable
    from napari.types import LayerDataTuple


def napari_get_reader(path: Union[str, List[str]]) -> Optional[Callable]:
    if not isinstance(path, list):
        path = [path]
    print("getting reader")
    if not all(map(lambda p: p.endswith(".mod"), path)):
        return None
    return reader_function


def read_model(path: Path) -> "Iterable[LayerDataTuple]":
    model = ImodModel.from_file(path)
    meshes = list()
    for obj in model.objects:
        color = np.array([obj.header.red, obj.header.green, obj.header.blue])
        for mesh in obj.meshes:
            vertex_colors = np.broadcast_to(color, (len(mesh.vertices), 3))
            if mesh.face_values is None:
                yield (mesh.vertices, mesh.indices), dict(
                    vertex_colors=vertex_colors, shading="smooth"
                ), "surface"
            else:
                yield (mesh.vertices, mesh.indices, mesh.face_values), dict(
                    vertex_colors=vertex_colors, shading="smooth"
                ), "surface"


def reader_function(
    paths: Union[str, List[str]]
) -> List[Tuple[Any, Dict, str]]:
    if not isinstance(paths, list):
        paths = [paths]
    layers = list()
    for path in paths:
        layers += list(read_model(Path(path)))
    return layers
