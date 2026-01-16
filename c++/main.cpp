#include <opencv2/opencv.hpp>
#include <iostream>
/*
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
} */


//#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
//#include <iostream>

int main() {
    cv::VideoCapture cam(0); 
    if (!cam.isOpened()) return -1;

    cv::dnn::Net net = cv::dnn::readNet("yolov8.onnx"); // Modell laden

    cv::Mat frame;
    while (true) {
        cam >> frame;
        if (frame.empty()) break;

        // 1. Frame vorbereiten
        cv::Mat blob = cv::dnn::blobFromImage(frame, 1/255.0, cv::Size(640,640), cv::Scalar(), true, false);

        // 2. Netzeingabe setzen und Vorhersage
        net.setInput(blob);
        std::vector<cv::Mat> outputs;
        net.forward(outputs);

        // 3. Bounding Boxes + Labels zeichnen
        // -> hier müsste man Output analysieren (modellabhängig)

        cv::imshow("AI Detection", frame);
        if (cv::waitKey(1) == 'q') break;
    }
    cam.release();
    cv::destroyAllWindows();
}
