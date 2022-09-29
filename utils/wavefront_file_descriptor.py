import re
import os
from dataclasses import dataclass
from typing import List, Optional, Tuple
from model.coordinate import Coordinate3D
from model.world_objects.displayable import Displayable
from model.world_objects.window import Window

@dataclass
class MaterialObject:
    name: str
    diffuse_color: Tuple[float, float, float]

@dataclass
class WavefrontObject:
    name: str
    vertices: List[Coordinate3D]
    material: MaterialObject
    vertices_idx: List[int]

class WavefrontFileDescriptor:
    """
    This class is responsible for importing and exporting Wavefront files.
    To fulfill that responsibility, it is capable of translating WorldObjects into Wavefront
    strings and vice versa.
    For .obj files, this class is capable of interpreting the following directives:
        - v (Geometric vertex)
        - o (Object name)
        - w (Window)
        - p (Point)
        - l (Line)
        - mtllib (Material Library)
        - usemtl (Material Name)
    For .mtl files, this class is capable of interpreting the following directives:
        - newmtl (New Material)
        - Kd (Diffuse Color)
    """

    @staticmethod
    def __parse_displayables(displayables: List[Displayable]) -> Tuple[List[WavefrontObject], List[MaterialObject]]:
        # generate unique material objects
        materials_dict = dict.fromkeys([displayable.get_color() for displayable in displayables])
        for hex_color in materials_dict:
            materials_dict[hex_color] = MaterialObject(
                hex_color,
                WavefrontFileDescriptor.__rgb_hex_to_float(hex_color)
            )
        # generate wavefront objects
        w_objects = []
        for displayable in displayables:
            coords = displayable.get_coordinates()
            w_objects.append(
                WavefrontObject(
                    name=displayable.get_name(),
                    vertices=[Coordinate3D(coord.x, coord.y, 0) for coord in coords],
                    material=materials_dict[displayable.get_color()],
                    vertices_idx=[]
                )
            )
        return w_objects, materials_dict.values()

    @staticmethod
    def __dump_material_file(materials: List[MaterialObject]) -> str:
        filename = 'materials.mtl'
        filepath = f'exported/{filename}'
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as material_file:
            for material in materials:
                material_file.write(f'newmtl {material.name}\n')
                material_file.write(f'Kd {" ".join(map(str, material.diffuse_color))}\n')
        return filename

    @staticmethod
    def __dump_wavefront_file(objects: List[WavefrontObject], mtllib: str) -> None:
        vertices_str = []
        obj_descriptions = []
        for obj in objects:
            cur_idx = len(vertices_str)
            last_idx = cur_idx + len(obj.vertices)
            obj.vertices_idx = list(range(cur_idx+1, last_idx+1))
            vertices_str.extend([f'v {" ".join(map(str, coord))}\n' for coord in obj.vertices])
            
            obj_descriptions.append(f'o {obj.name}\n')
            obj_descriptions.append(f'usemtl {obj.material.name}\n')
            obj_descriptions.append(f'{"p" if len(obj.vertices) == 1 else "l"} {" ".join(map(str, obj.vertices_idx))}\n')

        filename = 'drawables.obj'
        filepath = f'exported/{filename}'
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as wavefront_file:
            wavefront_file.writelines(vertices_str)
            wavefront_file.write(f'mtllib {mtllib}\n')
            # write window
            wavefront_file.writelines(obj_descriptions)

    @staticmethod
    def __rgb_hex_to_float(hex_str: str) -> Tuple[float, float, float]:
        if re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$').match(hex_str):
            div = 255.0
            if len(hex_str) <= 4:
                return tuple(int(hex_str[i]*2, 16) / div for i in (1, 2, 3))
            return tuple(int(hex_str[i:i+2], 16) / div for i in (1, 3, 5))
        raise ValueError(f'"{hex_str}" is not a valid HEX code.')

    @staticmethod
    def __rgb_float_to_hex(rgb_vals: Tuple[float, float, float]) -> str:
        int_rgb_vals = [max(0, min(int(val*255), 255)) for val in rgb_vals]
        return '#%02x%02x%02x' % int_rgb_vals
    
    @classmethod
    def import_file(cls, filepath: str) -> Tuple[List[Displayable], Optional[Window]]:
        pass

    @classmethod
    def export_file(cls, displayables: List[Displayable], window: Window) -> None:
        objects, materials = cls.__parse_displayables(displayables)
        mtllib_filename = cls.__dump_material_file(materials)
        cls.__dump_wavefront_file(objects, mtllib_filename)