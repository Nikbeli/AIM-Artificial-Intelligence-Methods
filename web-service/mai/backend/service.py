import io
import os
import pathlib
from typing import BinaryIO, Dict, List

import pandas as pd
from matplotlib.figure import Figure
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


class Service:
    def __init__(self, dataset_path: str | None) -> None:
        if dataset_path is None:
            raise Exception("Dataset path is not defined")
        self.__path: str = dataset_path

    def __get_dataset(self, filename: str) -> pd.DataFrame:
        full_file_name = os.path.join(self.__path, secure_filename(filename))
        return pd.read_csv(full_file_name)

    def upload_dataset(self, file: FileStorage) -> str:
        if file.filename is None:
            raise Exception("Dataset upload error")
        file_name: str = file.filename
        full_file_name = os.path.join(self.__path, secure_filename(file_name))
        file.save(full_file_name)
        return file_name

    def get_all_datasets(self) -> List[str]:
        return [file.name for file in pathlib.Path(self.__path).glob("*.csv")]

    def get_dataset_info(self, filename) -> List[Dict]:
        dataset = self.__get_dataset(filename)
        dataset_info = []
        for column in dataset.columns:
            items = dataset[column].astype(str)
            column_info = {
                "name": column,
                "datatype": dataset.dtypes[column],
                "items": items,
            }
            dataset_info.append(column_info)
        return dataset_info

    def get_column_info(self, filename, column) -> Dict:
        dataset = self.__get_dataset(filename)
        datatype = dataset.dtypes[column]
        items = sorted(dataset[column].astype(str).unique())
        return {"datatype": datatype, "items": items}

    def get_hist(self, filename, column) -> BinaryIO:
        dataset = self.__get_dataset(filename)
        bytes = io.BytesIO()
        plot: Figure | None = dataset.plot.hist(column=[column], bins=80).get_figure()
        if plot is None:
            raise Exception("Can't create hist plot")
        plot.savefig(bytes, dpi=300, format="png")
        return bytes
