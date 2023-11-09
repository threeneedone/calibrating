# -*- coding: utf-8 -*-

import os
from glob import glob
import calibrating  
from calibrating import imread, shows
from calibrating.stereo_matching import FeatureMatchingAsStereoMatching

print('__file__',os.path.join(
        os.getcwd()  ,"data"
    ))
checkboard_img_dir = os.path.abspath(
    os.path.join(
        os.getcwd() ,
        "data"
    )
)

assert os.path.isdir(
    checkboard_img_dir
), 'Not found "data"'

board = calibrating.Chessboard(checkboard=(11, 8), size_mm=20)

caml = calibrating.Cam(glob(f"{checkboard_img_dir}/*/L.bmp"), board)
print('caml:', caml)
camr = calibrating.Cam(glob(f"{checkboard_img_dir}/*/R.bmp"), board)
print('camr:', camr)


shows([cam.vis_image_points_cover() for cam in (caml, camr)])

stereo = calibrating.Stereo(caml, camr)
print('stere0:', stereo)

caml.vis_stereo(camr, stereo)

max_depth = 3
stereo_matching = calibrating.SemiGlobalBlockMatching()

stereo.set_stereo_matching(stereo_matching, max_depth=max_depth)

key = caml.valid_keys_intersection(camr)[0]
imgl = imread(caml[key]["path"])
imgr = imread(camr[key]["path"])

stereo_result = stereo.get_depth(imgl, imgr)
depth_stereo = stereo_result["unrectify_depth"]


rectify_depth = stereo_result['rectify_depth']
rectify_depth_vis = calibrating.vis_depth(rectify_depth, fix_range=(0.6, max_depth), slicen=1)

depth_stereo_vis = calibrating.vis_depth(depth_stereo, fix_range=(0.6, max_depth), slicen=1)
undistort_img1 = stereo_result["undistort_img1"]
rectify_img1 = stereo_result["rectify_img1"]
rectify_img2 = stereo_result["rectify_img2"]

shows([depth_stereo_vis])
# , rectify_depth_vis , undistort_img1, rectify_img1, rectify_img2, stereo_matching_lofter

# calibrating.vis_align(stereo_result["undistort_img1"], stereo_result["unrectify_depth"])

