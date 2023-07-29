from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from pathlib import Path

import numpy as np

from imodmodel.models import ImodModel


def napari_get_reader(path: Union[str, List[str]]) -> Optional[Callable]:
    if not isinstance(path, list):
        path = [path]
    print('getting reader')
    if not all(map(lambda p: p.endswith('.mod'), path)):
        return None
    return reader_function

def read_model(path: Path) -> List[Tuple[np.ndarray, np.ndarray]]:
    model = ImodModel.from_file(path)
    meshes = list()
    for object in model.objects:
        for mesh in object.meshes:
            meshes.append((mesh.vertices, mesh.reshaped_indices(), mesh.extra_values()))
    return meshes

def reader_function(paths: Union[str, List[str]]) -> List[Tuple[Any, Dict, str]]:
    if not isinstance(paths, list):
        paths = [paths]
    layers = list()
    for path in paths:
        for mesh in read_model(Path(path)):
            layers.append((mesh, {}, "surface"))
    return layers
