#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

int main()
{
    cv::Mat src = cv::imread("../data/fruits.png");

    cv::Mat dst;
    cv::Canny(src, dst, 50, 150);

    cv::imshow("win_src", src);
    cv::imshow("win_dst", dst);

    cv::imwrite("../data/image_dst.jpg", dst);
    cv::waitKey(0);
    cv::destroyAllWindows();

    return 0;
}
