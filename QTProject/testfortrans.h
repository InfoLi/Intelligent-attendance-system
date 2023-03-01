#ifndef TESTFORTRANS
#define TESTFORTRANS
#include <opencv2/opencv.hpp>

cv::Mat reImg;

namespace test{
    void testReadImage(){//测试用：用于读取用于传输图片的文件
        try{
            reImg = cv::imread("./1.jpg");
        }catch(cv::Exception e){
            std::cout << e.what() << std::endl;
        };
    };
}




#endif // TESTFORTRANS

