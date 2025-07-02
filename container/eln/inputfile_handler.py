import json
import pathlib
from pathlib import Path

import pandas as pd
from rdetoolkit.exceptions import StructuredError
from rdetoolkit.models.rde2types import MetaType, RdeInputDirPaths

from eln.interfaces import IInputFileParser


class FileReader(IInputFileParser):
    """Template class for reading and parsing input data.

    This class serves as a template for the development team to read and parse input data.
    It implements the IInputFileParser interface. Developers can use this template class
    as a foundation for adding specific file reading and parsing logic based on the project's
    requirements.

    Args:
        srcpaths (tuple[Path, ...]): Paths to input source files.

    Returns:
        Any: The loaded data from the input file(s).

    Example:
        file_reader = FileReader()
        loaded_data = file_reader.read(('file1.txt', 'file2.txt'))
        file_reader.to_csv('output.csv')

    """

    def check(self, srcpaths: RdeInputDirPaths) -> Path:
        """Check metadata-def.json.

        Checks if the 'metadata-def.json' file exists in the 'tasksupport' directory
        and if there are any .xlsx files present.

        Args:
            srcpaths (RdeInputDirPaths): An object containing paths to the source directories.

        Returns:
            Path: The path to the 'metadata-def.json' file in the 'tasksupport' directory.

        Raises:
            StructuredError: If the 'metadata-def.json' file
            does not exist in the specified directory.

        """
        metadata_file_path = srcpaths.tasksupport.joinpath("metadata-def.json")
        if not metadata_file_path.exists():
            error_message = f"No such file or directory: '{metadata_file_path}'"
            raise StructuredError(error_message)
        return metadata_file_path

    def read_invoice(self, raw_file_path: Path) -> dict[str, str]:
        """Read invoice file.

        Args:
            raw_file_path (Path): invoice file path

        Returns:
            invoice_obj (dict[str, str]): invoice data

        """
        with open(raw_file_path, encoding="utf-8") as f:
            invoice_obj: dict[str, str] = json.load(f)
        return invoice_obj

    def _overwrite_original(self, invoice_obj: dict, dst_invoice_json: Path) -> None:
        """Overwrite the common_data_type.

        Args:
            invoice_obj (dict): invoice data
            dst_invoice_json (Path): Path to the metadata list JSON file,
            which may include definitions or schema information.

        """
        invoice_obj["basic"]["dataName"] = "${filename}"
        with open(dst_invoice_json, "w", encoding="utf-8") as f_out:
            json.dump(invoice_obj, f_out, indent=4, ensure_ascii=False)

    def overwrite_invoice(
        self, df: pd.DataFrame, d: dict[str, dict], invoice_obj: dict, dst_invoice_json: Path,
    ) -> None:
        """Overwrite the invoice data if necessary.

        This method checks if the invoice data needs to be overwritten and updates
        it accordingly. It performs the necessary operations to write the modified
        data to the specified JSON file.

        Args:
            df (pd.DataFrame): The DataFrame containing data that will be used
                to update the invoice.
            d (dict[str, dict]): A dictionary of the data structure that may be
                used to overwrite parts of the invoice data.
            invoice_obj (dict): The original invoice data that will be overwritten.
            dst_invoice_json (Path): The path to the `invoice.json` file where the
                updated invoice data will be written.

        Returns:
            None

        """
        for row in df.itertuples():
            key = row.key.split("/")
            invoice_obj[key[0]][key[1]] = d["constant"][row.value]["value"]
        target_dir = pathlib.Path("data/inputdata")
        files = list(target_dir.glob("**/*.xlsx"))
        invoice_obj["custom"]["eln_filename"] = str(files[0].name)
        with open(dst_invoice_json, "w", encoding="utf-8") as f_out:
            json.dump(invoice_obj, f_out, indent=4, ensure_ascii=False)

    def overwrite_invoice_for_original(
        self, invoice_obj: dict, dst_invoice_json: Path,
    ) -> None:
        """Overwrite the invoice data if necessary.

        This method checks if the invoice data needs to be overwritten and updates
        it accordingly. It performs the necessary operations to write the modified
        data to the specified JSON file.

        Args:
            invoice_obj (dict): The original invoice data that will be overwritten or updated.
            dst_invoice_json (Path): The path to the invoice JSON file where the updated
                invoice data will be written.

        Returns:
            None

        """
        # custom.common_data_type
        self._overwrite_original(invoice_obj, dst_invoice_json)

    def read(self, srcpath: Path) -> tuple[MetaType, pd.DataFrame]:
        """Read data and metadata from the specified source path.

        This method reads the data and metadata from a given source path (such as a file),
        and returns the data in the form of a pandas DataFrame and the metadata as a dictionary.

        Note:
            Currently, the method returns dummy data and metadata for demonstration purposes.

        Args:
            srcpath (Path): The path to the source data file or directory.
                This argument is used to indicate where the data and metadata should be read from.

        Returns:
            self.data, self.meta

        Example:
            data, meta = reader.read(Path("data/sample.csv"))

        """
        self.data = pd.DataFrame([[1, 11], [2, 22], [3, 33]])
        self.meta = {"meta1": "value1", "meta2": "value2"}
        return self.data, self.meta
