import json
import shutil
from pathlib import Path

import pandas as pd
from rdetoolkit.exceptions import StructuredError
from rdetoolkit.models.rde2types import RdeInputDirPaths, RdeOutputResourcePath

from eln.inputfile_handler import FileReader
from eln.meta_handler import MetaParser


class ELNProcessingCoordinator:
    """Coordinator class for managing custom processing modules.

    This class serves as a coordinator for custom processing modules, facilitating the use of
    various components such as file reading, metadata parsing, graph plotting, and structured
    data processing. It is responsible for managing these components and providing an organized
    way to execute the required tasks.

    Args:
        file_reader (FileReader): An instance of the file reader component.
        structured_processer (StructuredDataProcessor): An instance of the structured data
                                                        processing component.

    Attributes:
        file_reader (FileReader): The file reader component for reading input data.
        structured_processer (StructuredDataProcessor):
        The component for processing structured data.

    Example:
        module = ELNProcessingCoordinator(FileReader(), StructuredDataProcessor())
        # Note: The method 'execute_processing' hasn't been defined in the provided code,
        #       so its usage is just an example here.
        module.execute_processing(srcpaths, resource_paths)

    """

    def __init__(
        self,
        file_reader: FileReader,
        meta_parser: MetaParser,
    ):
        self.file_reader = file_reader
        self.meta_parser = meta_parser


def eln_module(
    srcpaths: RdeInputDirPaths, resource_paths: RdeOutputResourcePath,
) -> None:
    """Execute structured text processing, metadata extraction, and visualization.

    It handles structured text processing, metadata extraction, and graphing.
    Other processing required for structuring may be implemented as needed.

    Args:
        srcpaths (RdeInputDirPaths): Paths to input resources for processing.
        resource_paths (RdeOutputResourcePath): Paths to output resources for saving results.

    Returns:
        None

    Note:
        The actual function names and processing details may vary depending on the project.

    """
    module = ELNProcessingCoordinator(
        FileReader(), MetaParser(),
    )
    try:
        module.file_reader.check(srcpaths)
        invoice_meta_path = srcpaths.tasksupport / "invoicemeta.csv"
        df = pd.read_csv(invoice_meta_path)
        temp = df.query('category == "invoice"')
        rawfile = resource_paths.rawfiles[0]
        invoice_obj = module.file_reader.read_invoice(resource_paths.invoice_org)
        empty_meta_path = Path("/app/empty_metadata.json") if Path("/app").exists() else Path("./empty_metadata.json")
        if str(rawfile).endswith("_meta.json"):  # *_meta.jsonはdivide.pyで出力される1行分のデータ
            with open(str(rawfile), encoding="utf-8") as f:
                d = json.load(f)
            module.meta_parser.save_empty_meta(resource_paths)
            module.file_reader.overwrite_invoice(
                temp, d, invoice_obj, resource_paths.invoice.joinpath("invoice.json"),
            )
        else:
            shutil.copy(
                empty_meta_path, str(resource_paths.meta) + "/metadata.json",
            )
            module.file_reader.overwrite_invoice_for_original(
                invoice_obj, resource_paths.invoice.joinpath("invoice.json"),
            )
    except Exception as e:
        error_message = f"failed to analyze. failure reason is: {e}"
        raise StructuredError(error_message) from e


def dataset(srcpaths: RdeInputDirPaths, resource_paths: RdeOutputResourcePath) -> None:
    """Process the data using the ElnProcessingCoordinator.

    This function calls the `ELNProcessingCoordinator.get_object()` method to process structured text
    and generate the desired output. It takes in the source and resource paths, which
    contain information about the input data and output directories respectively.

    Args:
        srcpaths (RdeInputDirPaths): Paths to input resources for processing.
        resource_paths (RdeOutputResourcePath): Paths to output resources for saving results.

    Returns:
        None

    """
    eln_module(srcpaths, resource_paths)
