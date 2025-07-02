from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pandas as pd
from rdetoolkit.exceptions import StructuredError
from rdetoolkit import rdelogger


logger = rdelogger.get_logger("job.failed")


class ExcelDivider:
    """template class for dividing data.

    The class provides methods for handling Excel files, specifically:

    Attributes:
        file_path (str): Path to the Excel file to be processed.
        output_dir (str): Directory where the processed JSON files will be saved.
        debug (bool): A flag to enable or disable debug logging.

    Methods:
        __init__(self, file_path, output_dir, debug=False):
            Initializes the ExcelDivider with the provided file path,
            output directory, and debug flag.

    parse_date(self, date_str):
        Parses a date string and converts it to a Pandas datetime object,
        handling multiple date formats.

    divide(self):
        Processes the Excel file by reading the data,
        parsing date columns, and saving the data in JSON format.

    """

    def __init__(self, file_path: Path = Path("data/inputdata"), output_dir: Path = Path("data")):
        self.file_path = file_path
        self.output_dir = output_dir

    def divide(self) -> None:
        """Divide the data into 'constant' and 'variable' metadata.

        process the data based on configuration, attempt to parse dates,
        and then save the data as a JSON file.

        The method performs the following tasks:

        1. Reads the Excel file based on the provided configuration
        2. Attempts to parse and convert date columns
        3. Pairs columns marked as 'repeated-meta'
        4. Saves the processed data in a JSON format
        """
        first_file = self.get_files(Path(self.file_path))
        try:
            config_df = pd.read_excel(first_file, sheet_name="RDEconfig", header=0)
            df = config_df.query('category == "invoice"')
            output_csv_path = Path(self.output_dir, "tasksupport/invoicemeta.csv")
            df.to_csv(output_csv_path, index=False)

            sheet_name = config_df.query('key == "sheet_name"').iloc[0]["value"]
            usecols = config_df.query('key == "usecols"').iloc[0]["value"]
            skiprows = config_df.query('key == "skiprows"').iloc[0]["value"]
            df = pd.read_excel(
                first_file, sheet_name=sheet_name, usecols=range(usecols), skiprows=skiprows,
            )
            df = self.convert_dates(df)
            excelrow = skiprows + 2

            repeated_meta_columns = config_df.query('category == "repeated-meta"')['value'].tolist()
            for row in df.itertuples(index=False):
                constant = {}
                variable = []

                for i, column in enumerate(df.columns):
                    value = row[i]
                    base_col = column.split('.')[0]
                    if base_col not in repeated_meta_columns:
                        if pd.isna(value):
                            value = ""
                        constant[df.columns[i]] = {"value": value}

                if repeated_meta_columns:
                    variable_data: dict[str, list[Any]] = {}
                    for col in repeated_meta_columns:
                        variable_data[col] = []
                    for i, column in enumerate(df.columns):
                        base_col = column.split('.')[0]
                        if base_col in repeated_meta_columns:
                            variable_data[base_col].append(row[i])
                    paired_variables = []
                    for i in range(len(variable_data[repeated_meta_columns[0]])):
                        pair = {}
                        for col in repeated_meta_columns:
                            value = variable_data[col][i]
                            if pd.isna(value):
                                value = ""
                            pair[col] = {"value": value}
                        if pair:
                            paired_variables.append(pair)
                    variable = paired_variables

                meta = {"constant": constant, "variable": variable}
                self.save_json(meta, excelrow)
                excelrow += 1

        except Exception as e:
            error_message = f"failed to analyze. failure reason is: {e}"
            logger.error(f"ErrorCode=1\n{error_message}")
            raise StructuredError(error_message) from e

    def get_files(self, input_dir: Path) -> Path:
        """Read Excel file.

        This method searches for `.xlsx` files recursively within the provided directory.
        If no files are found, it raises a `StructuredError`.

        Args:
            input_dir (Path): The directory path where the method will search for `.xlsx` files.

        Returns:
            Path: The path of the first `.xlsx` file found within the directory.

        Raises:
            StructuredError: If no `.xlsx` files are found in the provided directory.

        """
        files = list(input_dir.glob("**/*.xlsx"))
        if not files:
            error_message = "No .xlsx files found in the 'data/inputdata' directory."
            logger.error(f"ErrorCode=1\n{error_message}")
            raise StructuredError(error_message)

        return files[0]

    def convert_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert columns in the DataFrame that can be parsed as dates to the 'YYYY-MM-DD' format.

        Converts columns of the DataFrame that can be parsed as dates to a specific format.

        Args:
            df (pd.DataFrame): The DataFrame to process.

        Returns:
            pd.DataFrame: The DataFrame with date columns converted to 'YYYY-MM-DD' format.

        """
        for column in df.columns:
            df[column] = df[column].apply(self.parse_date)
            if pd.api.types.is_datetime64_any_dtype(df[column]):
                df[column] = df[column].dt.strftime('%Y-%m-%d')
        return df

    def parse_date(self, date_str: str | pd.Timestamp) -> str | pd.Timestamp:
        """Parse a date string and convert it to a Pandas datetime object.

        It handles multiple date formats by iterating through a list of formats.

        Args:
            date_str (str): A string representing the date to be parsed.

        Returns:
            pandas.Timestamp or str: The parsed date as a Pandas datetime object.
            If parsing fails, the original string is returned.

        """
        if isinstance(date_str, str):
            formats = [
                "%Y-%m-%d", "%Y/%m/%d",
                "%m-%d-%Y", "%m/%d/%Y",
                "%d-%m-%Y", "%d/%m/%Y",
                "%d %B %Y", "%B %d, %Y",
                "%Y年%m月%d日", "%Y年%m月%d",
                "%Y.%m.%d",
            ]
            for fmt in formats:
                parsed_date = pd.to_datetime(date_str, format=fmt, errors='coerce')
                if pd.notna(parsed_date):
                    return parsed_date
        return date_str

    def save_json(self, meta: dict, excelrow: int) -> None:
        """Save the processed data in a JSON format.

        Args:
            meta (dict): The data to be saved in JSON format.
            excelrow (int): The row number used in the file name.

        Returns:
            None

        """
        title = f"rde_temp_{excelrow}"
        json_path = os.path.join(self.output_dir, "inputdata", f"{title}_meta.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
