import os
import re
from typing import TYPE_CHECKING, Any, Dict, List

from markupsafe import escape

if TYPE_CHECKING:
    from starlette_admin import BaseField


def prettify_class_name(name: str) -> str:
    return re.sub(r"(?<=.)([A-Z])", r" \1", name)


def slugify_class_name(name: str) -> str:
    return "".join(["-" + c.lower() if c.isupper() else c for c in name]).lstrip("-")


def is_empty_file(file: Any) -> bool:
    pos = file.tell()
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(pos)
    return size == 0


def get_file_icon(mime_type: str) -> str:
    mapping = {
        "image": "fa-file-image",
        "audio": "fa-file-audio",
        "video": "fa-file-video",
        "application/pdf": "fa-file-pdf",
        "application/msword": "fa-file-word",
        "application/vnd.ms-word": "fa-file-word",
        "application/vnd.oasis.opendocument.text": "fa-file-word",
        "application/vnd.openxmlformatsfficedocument.wordprocessingml": "fa-file-word",
        "application/vnd.ms-excel": "fa-file-excel",
        "application/vnd.openxmlformatsfficedocument.spreadsheetml": "fa-file-excel",
        "application/vnd.oasis.opendocument.spreadsheet": "fa-file-excel",
        "application/vnd.ms-powerpoint": "fa-file-powerpoint",
        "application/vnd.openxmlformatsfficedocument.presentationml": (
            "fa-file-powerpoint"
        ),
        "application/vnd.oasis.opendocument.presentation": "fa-file-powerpoint",
        "text/plain": "fa-file-text",
        "text/html": "fa-file-code",
        "text/csv": "fa-file-csv",
        "application/json": "fa-file-code",
        "application/gzip": "fa-file-archive",
        "application/zip": "fa-file-archive",
    }
    if mime_type:
        for key in mapping:
            if key in mime_type:
                return mapping[key]
    return "fa-file"


def html_params(kwargs: Dict[str, Any]) -> str:
    params = []
    for k, v in kwargs.items():
        if v is None:
            continue
        if v is True:
            params.append(k)
        elif v is False:
            pass
        else:
            params.append('{}="{}"'.format(str(k).replace("_", "-"), escape(v)))
    return " ".join(params)


def extract_fields(
    fields: List["BaseField"], action: str = "LIST"
) -> List["BaseField"]:
    arr = []
    for field in fields:
        if (
            (action == "LIST" and field.exclude_from_list)
            or (action == "DETAIL" and field.exclude_from_detail)
            or (action == "CREATE" and field.exclude_from_create)
            or (action == "EDIT" and field.exclude_from_edit)
        ):
            continue
        arr.append(field)
    return arr
