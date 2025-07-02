import json
import os
import shutil
from typing import Union, List


def setup_inputdata_folder(inputdata_name: Union[str, List[str]]):
    """テスト用でdataフォルダ群の作成とrawファイルの準備
    Args:
        inputdata_name (Union[str, List[str]]): rawファイル名
    """
    destination_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(destination_path, exist_ok=True)
    os.makedirs(os.path.join(destination_path, "inputdata"), exist_ok=True)
    os.makedirs(os.path.join(destination_path, "invoice"), exist_ok=True)
    inputdata_original_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputdata"
    )
    print(inputdata_original_path)
    if isinstance(inputdata_name, List):
        for item in inputdata_name:
            shutil.copy(
                os.path.join(inputdata_original_path, "ELNtest_variable_sample.xlsx"),
                os.path.join(destination_path, "inputdata"),
            )
    else:
        shutil.copy(
            os.path.join(inputdata_original_path, "ELNtest_variable_sample.xlsx"),
            os.path.join(destination_path, "inputdata"),
        )
    print(inputdata_original_path)
    shutil.copy(
        os.path.join(inputdata_original_path, "invoice.json"),
        os.path.join(destination_path, "invoice"),
    )

    # tasksupport
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


class TestMeta:
    """case1
    メタデータテスト: ELNtest_variable_sample.xlsx
    """

    inputdata: Union[str, List[str]] = "ELNtest_variable_sample.xlsx"

    def test_setup(self):
        setup_inputdata_folder(self.inputdata)

    def test_metadata_constant(self, setup_main, setup_metadatadef_json):
        metadata = "metadata.json"
        result_metadata_filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "meta", metadata
        )

        with open(result_metadata_filepath, mode="r", encoding="utf-8") as f:
            contents = json.load(f)

        for k in contents["constant"].keys():
            constant_meta_key = setup_metadatadef_json.get(k)
            assert constant_meta_key is None or constant_meta_key, f"Key '{k}' is missing in metadata definition"

    def test_metadata_variable(self, setup_metadatadef_json):
        metadata = "metadata.json"
        result_metadata_filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "meta", metadata
        )

        with open(result_metadata_filepath, mode="r", encoding="utf-8") as f:
            contents = json.load(f)

        result_variable_keys = [k for item in contents["variable"] for k in item.keys()]
        for k in result_variable_keys:
            # metadata.json: variable
            variable_meta_key = setup_metadatadef_json.get(k)
            except_variable_flag = setup_metadatadef_json.get(k, {}).get("variable")

            assert (variable_meta_key is None or variable_meta_key) and (except_variable_flag is not None), \
                f"Key '{k}' is missing in variable metadata or variable flag is None"
