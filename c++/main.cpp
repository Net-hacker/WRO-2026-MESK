#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    cv::VideoCapture cam(0);
    if (!cam.isOpened()) {
        std::cerr << "Camera could not be opened!" << std::endl;
        return -1;
    }
    cv::Mat frame;
    while (cam.isOpened()) {
        cam >> frame; 
        if (frame.empty()) {
            std::cerr << "Empty frame received!" << std::endl;
            break;
        }
        cv::imshow("WRO-CAM", frame);
        if (cv::waitKey(10) == 'q') {
            break;
        }
    }

    cam.release();
    cv::destroyAllWindows();
    return 0;
}
