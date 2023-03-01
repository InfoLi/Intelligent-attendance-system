// Tencent is pleased to support the open source community by making ncnn available.
//
// Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
//
// Licensed under the BSD 3-Clause License (the "License"); you may not use this file except
// in compliance with the License. You may obtain a copy of the License at
//
// https://opensource.org/licenses/BSD-3-Clause
//
// Unless required by applicable law or agreed to in writing, software distributed
// under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
// CONDITIONS OF ANY KIND, either express or implied. See the License for the
// specific language governing permissions and limitations under the License.

#include "net.h"
#include <iostream>
#include <algorithm>
#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <stdio.h>
#include <vector>

using namespace std;

namespace facenet128{

static int detect_squeezenet(const cv::Mat& bgr, std::vector<float>& result)
{


    ncnn::Net facenet;

    facenet.opt.use_vulkan_compute = true;

    // the ncnn model https://github.com/nihui/ncnn-assets/tree/master/models
    facenet.load_param("./model/mobilefacenet.param");
    facenet.load_model("./model/mobilefacenet.bin");


    ncnn::Mat in = ncnn::Mat::from_pixels_resize(bgr.data, ncnn::Mat::PIXEL_BGR2RGB, bgr.cols, bgr.rows,112,112);

    const float mean_vals[3] = {104.f, 117.f, 123.f};
    in.substract_mean_normalize(mean_vals, 0);

    ncnn::Extractor ex = facenet.create_extractor();
    ex.set_light_mode(true);

    ex.input("data", in);

    ncnn::Mat out;
    ex.extract("fc1", out);


    result.resize(out.w);
    for (int j = 0; j < out.w; j++)
    {
        result[j] = out[j];
    }

    return 0;
}


vector<float>  facenet(cv::Mat m)
{
    if (m.empty())
    {
        fprintf(stderr, "cv::imread failed\n");
        return vector<float>(-1);
    }


    std::vector<float> cls_scores;
    detect_squeezenet(m, cls_scores);


    return cls_scores;
}
}
