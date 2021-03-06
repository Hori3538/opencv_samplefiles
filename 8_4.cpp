#include <iostream>
#include <fstream>
#include <sstream>
#include <opencv2/opencv.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/dnn/dnn.hpp>

std::vector<std::string> read_file(std::string filename, char delimiter='\n')
{
    std::vector<std::string> result;
    std::ifstream fin(filename);
    if (!fin){
        std::cout << "ファイルを開けませんでした。" << std::endl;
        exit(1);
    }
    std::string line;
    while (getline(fin, line)) {
        std::istringstream stream(line);
        std::string field;
        while (getline(stream, field, delimiter)) {
            result.push_back(field);
        }
    }
    fin.close();
    return result;
}
int main(int argc, char** argv)
{
    std::string file = "../data/cars.mp4";
    if (argc > 1){
        file = argv[1];
    }

    cv::VideoCapture video;
    video.open(file);

    if(video.isOpened() == false){
        return 0;
    }

    std::string proto = "../model/ssd_mobilenet_v2_coco_2018_03_29.pbtxt";
    std::string weight = "../model/frozen_inference_graph.pb";

    cv::dnn::Net net = cv::dnn::readNet(proto, weight);
    std::string label_file = "../model/object_detection_classes_coco.txt";
    std::vector<std::string> class_names = read_file(label_file);
    
    cv::Mat image;
    while(1){
        video >> image;
        if(image.empty()) break;

        cv::Mat blob = cv::dnn::blobFromImage(image, 1, cv::Size(300, 300));
        net.setInput(blob);
        cv::Mat pred = net.forward();
        cv::Mat pred_mat(pred.size[2], pred.size[3], CV_32F, pred.ptr<float>());

        float conf_threshold = 0.2;
        for(int i=0; i<pred_mat.rows; i++){
            float conf = pred_mat.at<float>(i, 2);

            if(conf > conf_threshold){
                int x0 = int(pred_mat.at<float>(i, 3) * image.cols);
                int y0 = int(pred_mat.at<float>(i, 4) * image.rows);
                int x1 = int(pred_mat.at<float>(i, 5) * image.cols);
                int y1 = int(pred_mat.at<float>(i, 6) * image.rows);

                cv::Rect object(x0, y0, x1-x0, y1-y0);
                cv::rectangle(image, object, cv::Scalar(255, 255, 255), 2);
                int id = int(pred_mat.at<float>(i, 1));
                std::string label = class_names[id-1] + ":" + std::to_string(conf);

                int baseline = 0;
                cv::Size  label_size = cv::getTextSize(label,
                        cv::FONT_HERSHEY_SIMPLEX,0.5, 1, &baseline);
                cv::putText(image, label, cv::Point(x0, y0),
                        cv::FONT_HERSHEY_SIMPLEX, 1, cv::Scalar(0, 0, 0), 2);

            }
        }

        cv::imshow("window", image);
        int key = cv::waitKey(5);
        if(key == 27) break;
        else if(key ==32) cv::waitKey();
    }
    cv::destroyAllWindows();

    return 0;
}
