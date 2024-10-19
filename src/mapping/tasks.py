from celery import shared_task
import cv2
import stitching

# pylint: disable=no-member


def stitch_images_expanded(input_pathes):
    """
    Custom image stitching pipeline on top of "stitching" which
    is on top of "cv2".
    """

    print("start")
    print("files found")

    # read images and get a few different scales

    # CUSTOM: using final images here to decrease speed and increase confidence.
    FEATURE_SCALE = stitching.images.Images.Resolution.FINAL

    images = stitching.images.Images.of(input_pathes)
    low_imgs = list(images.resize(stitching.images.Images.Resolution.LOW))
    medium_imgs = list(images.resize(FEATURE_SCALE))
    final_imgs = list(images.resize(stitching.images.Images.Resolution.FINAL))
    print(f"{len(input_pathes)} loaded and scaled")

    # detect features that can be compared more easily

    finder = stitching.feature_detector.FeatureDetector()
    features = [finder.detect_features(img) for img in medium_imgs]

    print("feature found")

    # compare features of images to get a whether they shoudl be stitched together
    # the error is here. kind of. thing may not get matched properly
    matcher = stitching.feature_matcher.FeatureMatcher()
    matches = matcher.match_features(features)

    print("feature matched")

    # confidence_matrix = matcher.get_confidence_matrix(matches)
    # print(images.names)
    # print(confidence_matrix)

    # remove images that are not connected before moving on.
    # it is also here, kind of, when matches that are just a little to low get deleted
    # CUSTOM: This is one of only two values i changed
    subsetter = stitching.subsetter.Subsetter(confidence_threshold=0.6)

    # dot_notation = subsetter.get_matches_graph(images.names, matches)
    # print(dot_notation)

    indices = subsetter.get_indices_to_keep(features, matches)

    medium_imgs = subsetter.subset_list(medium_imgs, indices)
    low_imgs = subsetter.subset_list(low_imgs, indices)
    final_imgs = subsetter.subset_list(final_imgs, indices)
    features = subsetter.subset_list(features, indices)
    matches = subsetter.subset_matches(matches, indices)

    images.subset(indices)
    print(f"{len(input_pathes)-len(indices)} dissconnected images removed")

    # PRINT confidence level in a way similiar to the adjacency matrix.
    # print(images.names)
    # print(matcher.get_confidence_matrix(matches))

    # DRAW pair wise match between image pairs with detected shared area
    # all_relevant_matches = matcher.draw_matches_matrix(
    #     feature_base,
    #     features,
    #     matches,
    #     conf_thresh=0.8,
    #     inliers=False,
    #     matchColor=(0, 255, 0)
    # )

    # for idx1, idx2, img in all_relevant_matches:
    #     print(f"Matches Image {idx1+1} to Image {idx2+1}")
    #     plot_image(img, (20, 10))

    # this is the time consuming step.
    # Might be improved by calculating the homology matrices directly
    # if gps data is accurate and precise
    # DLASCL error will pop up if there are issues
    # can be resolves some what with with increased overlap and image count
    camera_estimator = stitching.camera_estimator.CameraEstimator()
    camera_adjuster = stitching.camera_adjuster.CameraAdjuster()
    wave_corrector = stitching.camera_wave_corrector.WaveCorrector()

    cameras = camera_estimator.estimate(features, matches)  # ERROR MAYBE HERE
    cameras = camera_adjuster.adjust(features, matches, cameras)  # ERROR HERE
    cameras = wave_corrector.correct(cameras)
    print("camera transformations found and adjusted")

    # good, doesn't fail and but result may be weird
    warper = stitching.warper.Warper(warper_type="stereographic")
    # good, fails some time
    # warper = Warper(warper_type="transverseMercator")
    # best result, almost always fails though...
    # warper = Warper(warper_type="plane")

    warper.set_scale(cameras)

    #
    low_sizes = images.get_scaled_img_sizes(stitching.images.Images.Resolution.LOW)
    camera_aspect = images.get_ratio(
        FEATURE_SCALE, stitching.images.Images.Resolution.LOW
    )  # since cameras were obtained on medium imgs

    warped_low_imgs = list(warper.warp_images(low_imgs, cameras, camera_aspect))
    warped_low_masks = list(
        warper.create_and_warp_masks(low_sizes, cameras, camera_aspect)
    )
    low_corners, low_sizes = warper.warp_rois(low_sizes, cameras, camera_aspect)

    final_sizes = images.get_scaled_img_sizes(stitching.images.Images.Resolution.FINAL)
    camera_aspect = images.get_ratio(
        FEATURE_SCALE, stitching.images.Images.Resolution.FINAL
    )

    warped_final_imgs = list(warper.warp_images(final_imgs, cameras, camera_aspect))
    warped_final_masks = list(
        warper.create_and_warp_masks(final_sizes, cameras, camera_aspect)
    )
    final_corners, final_sizes = warper.warp_rois(final_sizes, cameras, camera_aspect)
    print("camera warping applied")

    # CUSTOM because the goal isn't a rectangle
    cropper = stitching.cropper.Cropper(crop=False)

    mask = cropper.estimate_panorama_mask(
        warped_low_imgs, warped_low_masks, low_corners, low_sizes
    )
    low_corners = cropper.get_zero_center_corners(low_corners)

    cropper.prepare(warped_low_imgs, warped_low_masks, low_corners, low_sizes)

    cropped_low_masks = list(cropper.crop_images(warped_low_masks))
    cropped_low_imgs = list(cropper.crop_images(warped_low_imgs))
    low_corners, low_sizes = cropper.crop_rois(low_corners, low_sizes)

    # scale up since since lir was obtained with low res img
    lir_aspect = images.get_ratio(
        stitching.images.Images.Resolution.LOW, stitching.images.Images.Resolution.FINAL
    )
    cropped_final_masks = list(cropper.crop_images(warped_final_masks, lir_aspect))
    cropped_final_imgs = list(cropper.crop_images(warped_final_imgs, lir_aspect))
    final_corners, final_sizes = cropper.crop_rois(
        final_corners, final_sizes, lir_aspect
    )

    print("cropping completed")

    seam_finder = stitching.seam_finder.SeamFinder()

    seam_masks = seam_finder.find(cropped_low_imgs, low_corners, cropped_low_masks)
    seam_masks = [
        seam_finder.resize(seam_mask, mask)
        for seam_mask, mask in zip(seam_masks, cropped_final_masks)
    ]
    print("seam determined")

    compensator = stitching.exposure_error_compensator.ExposureErrorCompensator()

    compensator.feed(low_corners, cropped_low_imgs, cropped_low_masks)

    compensated_imgs = [
        compensator.apply(idx, corner, img, mask)
        for idx, (img, mask, corner) in enumerate(
            zip(cropped_final_imgs, cropped_final_masks, final_corners)
        )
    ]
    print("exposure compensation applied")

    blender = stitching.blender.Blender()
    blender.prepare(final_corners, final_sizes)
    for img, mask, corner in zip(compensated_imgs, seam_masks, final_corners):
        blender.feed(img, mask, corner)
    stitched, _ = blender.blend()
    print("image blended")

    # DRAW BLEND MASK
    # blended_seam_masks = seam_finder.blend_seam_masks(seam_masks, final_corners, final_sizes)
    # plot_image(seam_finder.draw_seam_lines(panorama, blended_seam_masks, linesize=3), (15, 10))

    return stitched


@shared_task
def stitch_images(output_path, input_paths):
    """
    Stitch images at input path and save it at the out put path

    Args:
        output_path: This is the address that the stitched image would be written to.
        input_paths: This is a second param.

    Returns:
        A boolean about whether image stitching worked without any Issue.
    """
    # default "cv2" version
    # stitcher = cv2.Stitcher.create(cv2.Stitcher_SCANS)
    # (status, stitched) = stitcher.stitch(input_paths)

    # if status == cv2.Stitcher_OK:
    #     cv2.imwrite(output_path, stitched)
    #     return True
    # else:
    #     return False

    # default "stitching" version
    # stitcher = stitching.stitcher(
    #     detector="orb",
    #     confidence_threshold=0.6,
    #     crop=False
    # )
    # try:
    #     stitched = stitcher.stitch(file_pathes)
    # except Exception as e:
    #     return False

    # cv2.imwrite(output_path, stitched)
    # return True

    # custom "stitching" version
    try:
        stitched = stitch_images_expanded(input_paths)
    except Exception as _:
        return False

    cv2.imwrite(output_path, stitched)
    return True
