#include <iostream>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>

int main()
{
    cv::Mat img_1(300, 400, CV_16UC3);
    cv::imshow("img_1", img_1);
    cv::waitKey(0);
    cv::destroyWindow("img_1");


    cv::Mat img_2(300, 400, CV_8UC3, cv::Vec3b(255, 255, 255));
    img_2.rowRange(100, 200) = cv::Vec3b(255, 0, 0);
    cv::imshow("img_2", img_2);
    cv::waitKey(0);
    cv::destroyWindow("img_2");

    cv::Mat img_3(300, 300, CV_8U, 128);
    cv::imshow("img_3", img_3);
    cv::waitKey(0);
    cv::destroyWindow("img_3");

    cv::Mat img_4(300, 400, CV_8UC3, cv::Vec3b(0, 255, 255));
    cv::imshow("img_4", img_4);
    cv::waitKey(0);
    cv::destroyWindow("img_4");

    cv::Mat img_5;
    img_4.copyTo(img_5);
    cv::imshow("img_5", img_5);
    cv::waitKey(0);
    cv::destroyWindow("img_5");
    return 0;
}
