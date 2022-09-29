from typing import List, Optional, Tuple
from model.world_objects.displayable import Displayable
from model.world_objects.window import Window


class WavefrontFileDescriptor:
    """
    This class is responsible for importing and exporting Wavefront files.
    To fulfill that responsibility, it is capable of translating WorldObjects into Wavefront
    strings and vice versa.
    """

    @staticmethod
    def import_file(filepath: str) -> Tuple[List[Displayable], Optional[Window]]:
        pass

    @staticmethod
    def export_file(displayables: List[Displayable]) -> None:
        pass