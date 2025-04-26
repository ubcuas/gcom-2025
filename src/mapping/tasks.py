# get project structure
from django.conf import settings

# parallelzation
from celery import shared_task

import subprocess
import shutil
import os
import math


# pylint: disable=no-member
def stitch_images_odm(
    output_path: str, input_pathes: list[str], geo_data: list = None
) -> bool:
    """_summary_

    Args:
        output_path (str): The path that the output will be saved to
        input_pathes (str): List of pathes each of which is an image.
        geo_data (list, optional): The list of logs following the discord example data format. Defaults to None.

    Returns:
        bool: whether the task executed successfully, currently always True,
    """

    input_pathes.sort()

    # that images should be in [data_sets_path]/[project_name]/images
    data_sets_path = os.path.join(settings.MEDIA_ROOT, "odm_working_dir")

    if os.path.exists(os.path.join(data_sets_path, "default")):
        shutil.rmtree(os.path.join(data_sets_path, "default"))

    os.makedirs(data_sets_path, exist_ok=True)
    os.makedirs(os.path.join(data_sets_path, "default"), exist_ok=False)
    os.makedirs(os.path.join(data_sets_path, "default", "images"), exist_ok=False)

    for img_path in input_pathes:
        img_name = os.path.split(img_path)[1]
        shutil.copy(
            img_path,
            os.path.join(data_sets_path, "default", "images", img_name),
        )

    if geo_data is not None:
        geo_data.sort(key=lambda x: x["data"]["Img"])

        lat_center = 0
        lat_center_count = 0
        lng_center = 0
        lng_center_count = 0
        for g in geo_data:
            if g["data"]["lat"] != 0:
                lat_center += g["data"]["lat"]
                lat_center_count += 1
            if g["data"]["lng"] != 0:
                lng_center += g["data"]["lng"]
                lng_center_count += 1

        ns_hemisphere = "N" if lat_center > 0 else "S"
        geo_projection = f"WGS84 UTM {math.floor(lng_center/6)+31}{ns_hemisphere}\n"

        # geo_data_path = os.path.join(data_sets_path, "default", "images", "geo.txt")
        geo_data_path = os.path.join(data_sets_path, "default", "geo.txt")

        with open(geo_data_path, "w+", encoding="utf-8") as fi:
            fi.write(geo_projection)
            for g in geo_data:
                image_original_path = input_pathes[geo_data["data"]["Img"] - 1]
                img_name = os.path.split(image_original_path)[1]
                img_lat = geo_data["data"]["Lat"]
                img_lng = geo_data["data"]["Lng"]
                img_alt = geo_data["data"]["Alt"]
                fi.write(f"{img_name} {img_lat} {img_lng} {img_alt}\n")

    subprocess.Popen(
        f'docker run --rm -v "$(pwd)/{data_sets_path}":/datasets opendronemap/odm --project-path /datasets default --orthophoto-resolution 1 --orthophoto-png --skip-3dmodel --skip-report',
        shell=True,
        stdout=subprocess.DEVNULL,
    ).wait()

    generated_png_path = os.path.join(
        data_sets_path, "default", "odm_orthophoto", "odm_orthophoto.png"
    )

    shutil.copy(
        generated_png_path,
        output_path,
    )
    return True


@shared_task
def stitch_images(output_path, input_pathes, geo_data=None):
    """
    Stitch images at input path and save it at the out put path

    Args:
        output_path: This is the address that the stitched image would be written to.
        input_pathes: these are where the images would be read from.

    Returns:
        A boolean about whether image stitching worked without any Issue.
    """

    success = stitch_images_odm(
        output_path,
        input_pathes,
        geo_data,
    )

    return success
