#include <iostream>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>

int main()
{
    cv::Mat img = cv::imread("../data/fruits.png");

    if(img.empty()){
        std::cout << "Can not read image" << std::endl;
        return 0;
    }
    cv::imshow("win_img", img);
    cv::waitKey(0);
    cv::destroyWindow("win_img");

    return 0;
}
