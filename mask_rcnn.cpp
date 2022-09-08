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
    std::cout << "cv version: " << CV_VERSION << std::endl;
    std::string file = "../data/cars.mp4";
    if (argc > 1){
        file = argv[1];
    }

    cv::VideoCapture video;
    video.open(file);

    if(video.isOpened() == false){
        return 0;
    }

    std::string proto = "../model/Mask_r-cnn/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt";
    std::string weight = "../model/Mask_r-cnn/frozen_inference_graph.pb";
    // std::string proto = "../model/ssd_mobilenet_v2_coco_2018_03_29.pbtxt";
    // std::string weight = "../model/frozen_inference_graph.pb";

    cv::dnn::Net net = cv::dnn::readNet(proto, weight);
    net.setPreferableBackend(cv::dnn::DNN_BACKEND_CUDA);
    net.setPreferableTarget(cv::dnn::DNN_TARGET_CUDA);
    std::string label_file = "../model/object_detection_classes_coco.txt";
    std::vector<std::string> class_names = read_file(label_file);

    std::vector<cv::Scalar> colors;
    // Load the colors
    std::string colorsFile = "../model/Mask_r-cnn/colors.txt";
    std::ifstream colorFptr(colorsFile.c_str());
    std::string line;
    while (getline(colorFptr, line)) {
        char* pEnd;
        double r, g, b;
        r = strtod (line.c_str(), &pEnd);
        g = strtod (pEnd, NULL);
        b = strtod (pEnd, NULL);
        cv::Scalar color = cv::Scalar(r, g, b, 255.0);
        colors.push_back(cv::Scalar(r, g, b, 255.0));
    }
    
    cv::Mat image;
    while(1){
        video >> image;
        if(image.empty()) break;

        cv::Mat blob = cv::dnn::blobFromImage(image, 1, cv::Size(image.cols, image.rows), cv::Scalar());
        // cv::Mat blob = cv::dnn::blobFromImage(image, 1, cv::Size(300, 300));
        net.setInput(blob);
        std::vector<std::string> outNames(2);
        outNames[0] = "detection_out_final";
        outNames[1] = "detection_masks";
        std::vector<cv::Mat> pred;
        net.forward(pred, outNames);
        // std::vector<cv::Mat> pred = net.forward();
        // cv::Mat pred_mat(pred.size[2], pred.size[3], CV_32F, pred.ptr<float>());
        cv::Mat pred_detections = pred[0];
        cv::Mat pred_masks = pred[1];
        // Output size of masks is NxCxHxW where
        // N - number of detected boxes
        // C - number of classes (excluding background)
        // HxW - segmentation shape
        int num_detections = pred_detections.size[2];
        int num_classes = pred_masks.size[1];

        pred_detections = pred_detections.reshape(1, pred_detections.total() / 7);

        float conf_threshold = 0.4;
        float mask_threshold = 0.3;
        for(int i=0; i<num_detections; i++){
            float conf = pred_detections.at<float>(i, 2);

            if(conf > conf_threshold){
                int x0 = int(pred_detections.at<float>(i, 3) * image.cols);
                int y0 = int(pred_detections.at<float>(i, 4) * image.rows);
                int x1 = int(pred_detections.at<float>(i, 5) * image.cols);
                int y1 = int(pred_detections.at<float>(i, 6) * image.rows);

                x0 = std::max(0, std::min(x0, image.cols - 1));
                y0 = std::max(0, std::min(y0, image.rows - 1));
                x1 = std::max(0, std::min(x1, image.cols - 1));
                y1 = std::max(0, std::min(y1, image.rows - 1));

                cv::Rect rect(x0, y0, x1-x0+1, y1-y0+1);
                cv::rectangle(image, rect, cv::Scalar(255, 255, 255), 2);

                int id = int(pred_detections.at<float>(i, 1));
                cv::Mat object_mask(pred_masks.size[2], pred_masks.size[3], CV_32F, pred_masks.ptr<float>(i, id));

                std::string label = class_names[id] + ":" + std::to_string(conf);

                int baseline = 0;
                cv::Size  label_size = cv::getTextSize(label,
                        cv::FONT_HERSHEY_SIMPLEX,0.5, 1, &baseline);
                cv::putText(image, label, cv::Point(x0, y0),
                        cv::FONT_HERSHEY_SIMPLEX, 1, cv::Scalar(0, 0, 0), 2);

                cv::Scalar color = colors[id % colors.size()];

                cv::resize(object_mask, object_mask, cv::Size(rect.width, rect.height));
                cv::Mat mask = (object_mask > mask_threshold);
                cv::Mat colored_roi = (0.3 * color + 0.7 * image(rect));
                colored_roi.convertTo(colored_roi, CV_8UC3);

                std::vector<cv::Mat> contours;
                cv::Mat hierarchy;
                mask.convertTo(mask, CV_8U);
                cv::findContours(mask, contours, hierarchy, cv::RETR_CCOMP, cv::CHAIN_APPROX_SIMPLE);
                cv::drawContours(colored_roi, contours, -1, color, 5, cv::LINE_8, hierarchy, 100);
                colored_roi.copyTo(image(rect), mask);


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
