from __future__ import annotations

import os
import shutil
from pathlib import Path

from rdetoolkit.models.rde2types import RdeOutputResourcePath

from eln.interfaces import IMetaParser


class MetaParser(IMetaParser):
    """Template class for parsing and saving metadata.

    This class serves as a template for the development team to parse and save metadata.
    It implements the IMetaParser interface.
    Developers can use this template class as a foundation for adding
    specific parsing and saving logic for metadata based on the project's requirements.

    Args:
        data (MetaType): The metadata to be parsed and saved.

    Returns:
        tuple[MetaType, MetaType]: A tuple containing the parsed constant and repeated metadata.

    Example:
        meta_parser = MetaParser()
        parsed_const_meta, parsed_repeated_meta = meta_parser.parse(data)
        meta_obj = rde2util.Meta(metaDefFilePath='meta_definition.json')
        saved_info = meta_parser.save_meta('saved_meta.json', meta_obj,
                                        const_meta_info=parsed_const_meta,
                                        repeated_meta_info=parsed_repeated_meta)

    """

    def save_empty_meta(self, resource_paths: RdeOutputResourcePath) -> None:
        """Process raw files and metadata for the specified resource paths.

        This method checks if the raw file is a metadata file, and if so, moves it
        to the appropriate location and deletes the old raw file. If the raw file
        is not a metadata file, it copies a default empty metadata file to the target
        location.

        Args:
            resource_paths (RdeOutputResourcePath): An object containing paths to
                the raw files and metadata files.

        Returns:
            None

        """
        rawfile = resource_paths.rawfiles[0]
        empty_meta_path = Path("/app/empty_metadata.json") if Path("/app").exists() else Path("./empty_metadata.json")
        if str(rawfile).endswith("_meta.json"):
            shutil.move(
                str(resource_paths.rawfiles[0]), str(resource_paths.meta) + "/metadata.json",
            )
            os.remove(resource_paths.nonshared_raw / rawfile.name)
        else:
            shutil.copy(empty_meta_path, str(resource_paths.meta) + "/metadata.json")
