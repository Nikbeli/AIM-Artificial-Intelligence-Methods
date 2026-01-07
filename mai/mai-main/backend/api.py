from apiflask import FileSchema, Schema, fields
from flask import send_file

from backend import api_bp, dataset_path
from backend.service import Service


class FileUpload(Schema):
    file = fields.File(required=True)


class ColumnInfoDto(Schema):
    datatype = fields.String()
    items = fields.List(fields.String())


class TableColumnDto(Schema):
    name = fields.String()
    datatype = fields.String()
    items = fields.List(fields.String())


service = Service(dataset_path)


@api_bp.post("/dataset")
@api_bp.input(FileUpload, location="files")
def upload_dataset(files_data):
    uploaded_file = files_data["file"]
    return service.upload_dataset(uploaded_file)


@api_bp.get("/dataset")
def get_all_datasets():
    return service.get_all_datasets()


@api_bp.get("/dataset/<string:name>")
@api_bp.output(TableColumnDto(many=True))
def get_dataset_info(name: str):
    return service.get_dataset_info(name)


@api_bp.get("/dataset/<string:name>/<string:column>")
@api_bp.output(ColumnInfoDto)
def get_column_info(name: str, column: str):
    return service.get_column_info(name, column)


@api_bp.get("/dataset/draw/hist/<string:name>/<string:column>")
@api_bp.output(
    FileSchema(type="string", format="binary"), content_type="image/png", example=""
)
def get_dataset_hist(name: str, column: str):
    data = service.get_hist(name, column)
    data.seek(0)
    return send_file(data, download_name=f"{name}.hist.png", mimetype="image/png")
