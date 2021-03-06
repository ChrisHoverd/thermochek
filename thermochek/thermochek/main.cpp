#include <opencv2/core.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/objdetect.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/video.hpp>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <vector>
#include <chrono>
//#include <wiringPi.h>


using namespace std;
using namespace cv;

//declare global variables
CascadeClassifier face_cascade;
Mat frame;
Mat gray;
//for rPi: string cascade_path = "haarcascade_frontalface_default.xml";
string cascade_path = "C:\\opencv\\build\\etc\\haarcascades\\haarcascade_frontalface_default.xml";
double g_scale = 1.0;
//int green_LED = 1;
//int red_LED = 0;

//Timer class used to control calculation intervals for the face cascades
class Timer
{
public:
    Timer() : beg_(clock_::now()) {}
    void reset() { beg_ = clock_::now(); }
    double elapsed() const {
        return std::chrono::duration_cast<second_>
            (clock_::now() - beg_).count();
    }

private:
    typedef std::chrono::high_resolution_clock clock_;
    typedef std::chrono::duration<double, std::ratio<1> > second_;
    std::chrono::time_point<clock_> beg_;
};



static void detectAndDraw(Mat& img, CascadeClassifier& cascade, double scale, Timer& tmr) {
    vector<Rect> faces;
    cvtColor(img, gray, COLOR_BGR2GRAY);
    resize(gray, gray, { (int)((double)gray.size().width / scale), (int)((double)gray.size().height / scale) });

    if (tmr.elapsed() > 5)
    {
        cascade.detectMultiScale(gray, faces, 1.1, 3, 0, Size(30, 30));
        std::cout << "Looking for faces..." << std::endl;

        for (const auto& r : faces) {
            rectangle(gray, { r.x , r.y }, { r.x + r.width, r.y + r.height }, Scalar(255, 0, 0), 2);
        }

        if (faces.size() >= 1) {
            std::cout << faces.size() << " Face(s) Found!" << std::endl;
            //digitalWrite(green_LED, HIGH);
            //digitalWrite(red_LED, LOW);
        }
        else {
            std::cout << "No Face(s) Found!" << std::endl;
            //digitalWrite(red_LED, HIGH);
            //digitalWrite(green_LED, LOW);
        }
        tmr.reset();
    }
}

int main()

{
    //wiringPiSetup();
    //pinMode(green_LED, OUTPUT);
    //pinMode(red_LED, OUTPUT);
    Timer tmr;
    VideoCapture camera(0);
    if (!camera.isOpened()) {
        std::cerr << "ERROR: Could not open camera" << std::endl;
    }

    while (true) {
        camera.read(frame);
        if (!face_cascade.load(cascade_path)) {
            std::cerr << "ERROR: Could not load classifier..." << std::endl;
        }

        detectAndDraw(frame, face_cascade, g_scale, tmr);
        imshow("Webcam", gray);
        if (waitKey(10) >= 0) {
            //Turn LEDs off
            //digitalWrite(red_LED, LOW);
            //digitalWrite(green_LED, LOW);
            break;
        }
    }

    return 0;
}
