# ----------------- xxx -----------------
# Object detector by [nulldev]
# ----------------- xxx -----------------

# Imports
import cv2
import ntpath
import os
import time
from os import path

# Const vars
MATCH_METHODS = {
    "ccoeff": cv2.TM_CCOEFF,
    "ccoeff_normed": cv2.TM_CCOEFF_NORMED,
    "ccorr": cv2.TM_CCORR,
    "ccorr_normed": cv2.TM_CCORR_NORMED,
    "sqdiff": cv2.TM_SQDIFF,
    "sqdiff_normed": cv2.TM_SQDIFF_NORMED,
}


def custom_cv_from_match(
    img_map_path, img_target_path, method, results_folder, rect_rgb, rect_thickness
):

    start_time = time.time()

    # Check result folder structure
    if results_folder[-1] != "/" or results_folder[-1] != "\\":
        results_folder += "/"

    results_folder = path.normcase(results_folder)

    # Check if strings paths is other than empty or white spaces
    if not img_map_path or not img_target_path or not results_folder:
        return

    if img_map_path.isspace() or img_target_path.isspace() or results_folder.isspace():
        return

    # Check if values is other than null
    if (
        img_map_path is None
        or img_target_path is None
        or method is None
        or results_folder is None
    ):
        return

    # Check selected method
    selected_method = eval(method) if type(method) == str else method

    # Get images from resources folder
    internal_map = cv2.imread(img_map_path, cv2.IMREAD_GRAYSCALE)
    internal_target = cv2.imread(img_target_path, cv2.IMREAD_GRAYSCALE)

    if internal_map is None or internal_target is None:
        return

    # Get target W and H of target
    target_width, target_height = internal_target.shape[::-1]

    # Use OpenCV match template with selected method
    match_result = cv2.matchTemplate(internal_map, internal_target, selected_method)

    # Get min and max values with their positions
    result_min, result_max, result_min_pos, result_max_pos = cv2.minMaxLoc(match_result)

    # Calculate positions of rect
    if selected_method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = result_min_pos
    else:
        top_left = result_max_pos

    bottom_right = (top_left[0] + target_width, top_left[1] + target_height)

    restore_map = cv2.imread(img_map_path, cv2.IMREAD_COLOR)

    # Draw a rect
    cv2.rectangle(restore_map, top_left, bottom_right, rect_rgb, rect_thickness)

    # Check if results path exist
    if not os.path.exists(results_folder):
        os.mkdir(results_folder)

    # Save result path
    save_path = "{results_path}out_{img_out_name}".format(
        img_out_name=ntpath.basename(img_map_path), results_path=results_folder
    )

    total_execution_time = time.time() - start_time

    try:
        cv2.imwrite(
            save_path,
            restore_map,
        )
    except:
        raise Exception("Save result image error")
    else:
        return (save_path, round(total_execution_time, 2))
