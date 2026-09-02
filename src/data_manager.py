import os
import re
from datetime import datetime

import openpyxl


# ============================================================
# DATA FOLDER
# ============================================================

DATA_FOLDER = "data"


def get_next_run_number(driver_number):

    os.makedirs(
        DATA_FOLDER,
        exist_ok=True
    )

    pattern = re.compile(
        rf"^D{driver_number}_run(\d+)"
    )

    highest = 0

    for name in os.listdir(DATA_FOLDER):

        match = pattern.match(name)

        if match:

            run_num = int(match.group(1))

            if run_num > highest:
                highest = run_num

    return highest + 1


def create_workbook(run_number, driver_number=1):

    os.makedirs(
        DATA_FOLDER,
        exist_ok=True
    )


    filename = (
        f"D{driver_number}_run{run_number:02d}.xlsx"
    )


    path = os.path.join(
        DATA_FOLDER,
        filename
    )


    # If the same driver/run combination already exists,
    # create another unique file instead of overwriting it.

    if os.path.exists(path):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"D{driver_number}_run{run_number:02d}_"
            f"{timestamp}.xlsx"
        )

        path = os.path.join(
            DATA_FOLDER,
            filename
        )


    wb = openpyxl.Workbook()

    ws = wb.active

    ws.title = "N-Back Data"


    # --------------------------------------------------------
    # ONLY REQUIRED DATA COLUMNS
    # --------------------------------------------------------

    ws.append([
        "Trial",
        "Number",
        "Response",
        "Time"
    ])


    # Formatting

    ws.freeze_panes = "A2"

    ws.column_dimensions["A"].width = 12

    ws.column_dimensions["B"].width = 12

    ws.column_dimensions["C"].width = 15

    ws.column_dimensions["D"].width = 18


    save_workbook(
        wb,
        path
    )


    return wb, ws, path


# ============================================================
# APPEND TRIAL
# ============================================================

def append_trial(
    ws,
    trial,
    number,
    response,
    reaction_time_ms
):

    ws.append([
        trial,
        number,
        response,
        reaction_time_ms
    ])


# ============================================================
# SAVE
# ============================================================

def save_workbook(
    wb,
    path
):

    wb.save(path)
    
