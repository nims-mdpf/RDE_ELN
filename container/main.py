import rdetoolkit

from pathlib import Path
from eln.divide_excel import ExcelDivider
from modules import datasets_process


divider = ExcelDivider(file_path=Path("data/inputdata"), output_dir=Path("data"))

divider.divide()
rdetoolkit.workflows.run(custom_dataset_function=datasets_process.dataset)
