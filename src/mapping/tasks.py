# get project structure
from django.conf import settings

# parallelzation
from celery import shared_task

import subprocess
import shutil
import os


# pylint: disable=no-member
def stitch_images_odm(output_path, input_pathes):
    # that images should be in [data_sets_path]/[project_name]/images
    data_sets_path = os.path.join(settings.MEDIA_ROOT, "odm_working_dir")

    if os.path.exists(os.path.join(data_sets_path, "default")):
        shutil.rmtree(os.path.join(data_sets_path, "default"))

    os.makedirs(data_sets_path, exist_ok=True)
    os.makedirs(os.path.join(data_sets_path, "default"), exist_ok=False)
    os.makedirs(os.path.join(data_sets_path, "default", "images"), exist_ok=False)

    for i, img_path in enumerate(input_pathes):
        shutil.copy(
            img_path,
            os.path.join(data_sets_path, "default", "images", f"{i}.png"),
        )

    subprocess.Popen(
        f'docker run -ti --rm -v "$(pwd)/{data_sets_path}":/datasets opendronemap/odm --project-path /datasets default --orthophoto-resolution 1 --orthophoto-png --skip-3dmodel --skip-report',
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
def stitch_images(output_path, input_pathes):
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
    )

    return success
