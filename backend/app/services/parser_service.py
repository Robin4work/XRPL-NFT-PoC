# import os


# def parse_raman(file_path: str):

#     return {
#         "puf_hash": None,
#         "stone_id": None,
#         "certificate_number": None,
#         "laboratory": None,
#         "species": None,
#         "carat_weight": None,
#         "color": None,
#         "clarity": None,
#         "treatment": None,
#         "origin": None,
#         "natural_origin": None,
#         "raman_laser_nm": None,
#         "raman_snr": None,
#         "scan_date": None,
#         "emission_date": None,
#         "source_file": os.path.basename(file_path)
#     }


# def parse_ftir(file_path: str):

#     return {
#         "source_file": os.path.basename(file_path)
#     }


# def parse_uv(file_path: str):

#     return {
#         "source_file": os.path.basename(file_path)
#     }


import os

import pandas as pd


def _read_spectrum_row_count(file_path: str) -> int:
    """
    Counts the numeric data rows in an instrument export, skipping any
    '#'-prefixed comment/header lines. Used only as a light sanity check
    (e.g. to confirm the file actually parsed), not for the fingerprint
    itself -- that's still generate_csv_hash()'s job.
    """
    df = pd.read_csv(
        file_path,
        sep=None,
        engine="python",
        comment="#",
        header=None,
    )
    return len(df)


def _parse_hash_header(file_path: str) -> dict:
    """
    Some instrument exports (e.g. the MAGI GemmoSphere UV file) prefix the
    numeric data with a block of '# Key=Value' comment lines describing the
    scan and, sometimes, the stone itself (operator-entered fields like
    Material/Color/Weight). This reads that block into a plain dict.
    Returns {} if the file has no such header (e.g. FTIR .CSV, which is
    pure numeric data with no header at all).
    """
    header = {}
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("#"):
                break
            line = line.lstrip("#").strip()
            if "=" in line:
                key, _, value = line.partition("=")
                header[key.strip()] = value.strip()
    return header


def parse_raman(file_path: str):
    # The Raman .txt export (extracted from the instrument's .wdf/.zip
    # bundle) only carries a "#Wave  #Intensity" column-label comment --
    # no operator-entered stone metadata lives in this file. The fingerprint
    # itself is computed separately by hash_service.generate_csv_hash().
    row_count = _read_spectrum_row_count(file_path)

    return {
        "puf_hash": None,
        "stone_id": None,
        "certificate_number": None,
        "laboratory": None,
        "species": None,
        "carat_weight": None,
        "color": None,
        "clarity": None,
        "treatment": None,
        "origin": None,
        "natural_origin": None,
        "raman_laser_nm": None,
        "raman_snr": None,
        "scan_date": None,
        "emission_date": None,
        "source_file": os.path.basename(file_path),
        "raman_point_count": row_count,
    }


def parse_ftir(file_path: str):
    # FTIR .CSV export is pure numeric data (wavenumber, absorbance) with
    # no header or comment lines -- nothing else to extract here.
    row_count = _read_spectrum_row_count(file_path)

    return {
        "source_file": os.path.basename(file_path),
        "ftir_point_count": row_count,
    }


def parse_uv(file_path: str):
    # The UV export's comment header sometimes carries operator-entered
    # stone fields (Material, Color, Weight, Tag) alongside instrument
    # settings (HardwareVersion, ExposureTime, etc). Map the ones that
    # correspond to certificate fields; keep the rest as raw device info
    # so nothing is silently discarded.
    header = _parse_hash_header(file_path)
    row_count = _read_spectrum_row_count(file_path)

    def non_empty(value):
        return value if value else None

    return {
        "source_file": os.path.basename(file_path),
        "uv_point_count": row_count,
        "species": non_empty(header.get("Material")),
        "color": non_empty(header.get("Color")),
        "scan_date": non_empty(header.get("TimeStamp")),
        "uv_device_metadata": header,
    }