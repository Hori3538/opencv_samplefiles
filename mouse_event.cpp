// #include <opencv2\opencv.hpp>
// #include <opencv_lib.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>

#include <iostream>

cv::Rect rectangle_value;


void mouse_callback(int event, int x, int y, int flags, void *userdata)
{
    bool *isClick = static_cast<bool *>(userdata);
    if (event == cv::EVENT_LBUTTONDOWN) {
        *isClick = true;
        std::cout << "Draw rectangle\n"
            << " start position (x, y) : " << x << ", " << y << std::endl;
        rectangle_value = cv::Rect(x, y, 0, 0);
    }
    if (event == cv::EVENT_LBUTTONUP) {
        *isClick = false;
        std::cout << " end   position (x, y) : " << x << ", " << y << std::endl;
        rectangle_value.width = x - rectangle_value.x;
        rectangle_value.height = y - rectangle_value.y;
    }
    if (event == cv::EVENT_MOUSEMOVE) {
        if (*isClick) {
            rectangle_value.width = x - rectangle_value.x;
            rectangle_value.height = y - rectangle_value.y;
        }
    }
}

int main()
{
    // cv::Mat img = cv::imread("./cpp_img.png");
    cv::Mat img = cv::imread("../data/fruits.png");
    cv::Mat draw_img = img.clone();
    std::string window_name = "example";
    bool isClick = false;
    int key;

    cv::imshow(window_name, img);
    cv::setMouseCallback(window_name, mouse_callback, &isClick);
    while(1){
        key = 0;

        // 左ボタンが押されたら描画開始
        if (isClick == true) {
            // rectangle(draw_img, rectangle_value, Scalar(255, 0, 0), 3, CV_AA);
            // cv::rectangle(draw_img, rectangle_value, cv::Scalar(255, 0, 0), 3);
            // cv::rectangle();
        }

        cv::imshow(window_name, draw_img);
        draw_img = img.clone();

        // qキーが押されたら終了
        key = cv::waitKey(1);
        if (key == 'q')
            break;
    }

    return 0;
}
