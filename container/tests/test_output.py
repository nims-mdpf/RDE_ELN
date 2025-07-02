import os
import shutil
from typing import Union, List
import pytest

# setup_inputdata_folder関数（そのまま）
def setup_inputdata_folder(inputdata_name: Union[str, List[str]]):
    """テスト用でdataフォルダ群の作成とrawファイルの準備
    Args:
        inputdata_name (Union[str, List[str]]): rawファイル名
    """
    destination_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    print(destination_path)
    os.makedirs(destination_path, exist_ok=True)
    os.makedirs(os.path.join(destination_path, "inputdata"), exist_ok=True)
    os.makedirs(os.path.join(destination_path, "invoice"), exist_ok=True)
    inputdata_original_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputdata"
    )
    print(inputdata_original_path)
    if isinstance(inputdata_name, List):
        for item in inputdata_name:
            print(item)
            shutil.copy(
                os.path.join(inputdata_original_path, item),
                os.path.join(destination_path, "inputdata"),
            )
    else:
        shutil.copy(
            os.path.join(inputdata_original_path, inputdata_name),
            os.path.join(destination_path, "inputdata"),
        )
    shutil.copy(
        os.path.join(inputdata_original_path, "invoice.json"),
        os.path.join(destination_path, "invoice"),
    )

    os.makedirs(os.path.join(destination_path, "tasksupport"), exist_ok=True)
    tasksupport_original_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "template", "tasksupport"
    )
    shutil.copy(
        os.path.join(tasksupport_original_path, "invoice.schema.json"),
        os.path.join(destination_path, "tasksupport"),
    )
    shutil.copy(
        os.path.join(tasksupport_original_path, "metadata-def.json"),
        os.path.join(destination_path, "tasksupport"),
    )
    shutil.copy(
        os.path.join(tasksupport_original_path, "rdeconfig.yaml"),
        os.path.join(destination_path, "tasksupport"),
    )

class TestOutputCase1:
    """case1
    単一ファイルのテスト:
        "ELNtest_variable_sample.xlsx"
    """

    inputdata: Union[str, List[str]] = "ELNtest_variable_sample.xlsx"

    # setup_mainフィクスチャを引数として指定
    def test_setup(self):
        # setup_inputdata_folderで必要なフォルダとファイルを準備
        setup_inputdata_folder(self.inputdata)

    def test_nonshared_raw_file(self, setup_main, data_path):
        assert os.path.exists(os.path.join(data_path, "nonshared_raw", "ELNtest_variable_sample.xlsx"))

    def test_meta_files(self, data_path):
        assert os.path.exists(os.path.join(data_path, "meta", "metadata.json"))
        assert os.path.exists(os.path.join(data_path, "divided", "0001", "meta", "metadata.json"))
        assert os.path.exists(os.path.join(data_path, "divided", "0002", "meta", "metadata.json"))
