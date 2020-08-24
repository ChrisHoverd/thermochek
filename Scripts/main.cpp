#include <opencv2/opencv.hpp>
#include <vector>

using namespace std;
using namespace cv;
double g_scale = 2.0;

//declare global variables
CascadeClassifier face_cascade;
Mat frame;
Mat gray;
string cascade_path = "C:\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_default.xml";

static void detectAndDraw(Mat& img, CascadeClassifier& cascade, double scale) {
    vector<Rect> faces;
    cvtColor(img, gray, COLOR_BGR2GRAY);
    resize(gray, gray, { (int)((double)gray.size().width / scale), (int)((double)gray.size().height / scale) });
    cascade.detectMultiScale(gray, faces, 1.1, 3, 0, Size(30, 30));
    for (const auto& r : faces) {
        rectangle(gray, { r.x , r.y }, { r.x + r.width, r.y + r.height }, Scalar(255, 0, 0), 2);
    }

}

int main()

{
    VideoCapture camera(0);
    if (!camera.isOpened()) {
        std::cerr << "ERROR: Could not open camera" << std::endl;
    }

    while (true) {
        camera.read(frame);
        if (!face_cascade.load(cascade_path)) {
            std::cerr << "ERROR: Can not load classifier..." << std::endl;
        }

        detectAndDraw(frame, face_cascade, g_scale);
        imshow("Webcam", gray);
        if (waitKey(10) >= 0) {
            break;
        }
    }

    return 0;
}