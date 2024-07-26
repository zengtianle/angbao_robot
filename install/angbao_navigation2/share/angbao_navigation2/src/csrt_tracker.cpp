
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <dirent.h>

#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include "geometry_msgs/Twist.h"

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/tracking/tracking.hpp>
#include <opencv2/core/ocl.hpp>

static const std::string RGB_WINDOW = "RGB Image window";

#define Max_linear_speed 0.5
#define Min_linear_speed 0.3
#define Min_distance 1.5
#define Max_distance 5.0
#define Max_rotation_speed 0.75

float linear_speed = 0;
float rotation_speed = 0;

float k_linear_speed = (Max_linear_speed - Min_linear_speed) / (Max_distance - Min_distance);
float h_linear_speed = Min_linear_speed - k_linear_speed * Min_distance;

float k_rotation_speed = 0.004;
float h_rotation_speed_left = 1.2;
float h_rotation_speed_right = 1.36;
 
int ERROR_OFFSET_X_left1 = 100;
int ERROR_OFFSET_X_left2 = 300;
int ERROR_OFFSET_X_right1 = 340;
int ERROR_OFFSET_X_right2 = 540;


cv::Mat rgbimage;
cv::Mat depthimage;
cv::Rect2d selectRect;
cv::Point origin;
cv::Rect2d result;

bool select_flag = false;
bool bRenewROI = false;  // the flag to enable the implementation of KCF algorithm for the new chosen ROI
bool bBeginKCF = false;
bool enable_get_depth = false;

bool HOG = true;
bool FIXEDWINDOW = false;
bool MULTISCALE = true;
bool SILENT = true;
bool LAB = false;

// Create CSRTracker object
cv::Ptr<cv::TrackerCSRT> tracker = cv::TrackerCSRT::create();

float dist_val[5] ;

void onMouse(int event, int x, int y, int, void*)
{
    if (select_flag)
    {
        selectRect.x = MIN(origin.x, x);        
        selectRect.y = MIN(origin.y, y);
        selectRect.width = abs(x - origin.x);   
        selectRect.height = abs(y - origin.y);
        selectRect &= cv::Rect2d(0, 0, rgbimage.cols, rgbimage.rows);
    }
    if (event == cv::EVENT_LBUTTONDOWN)
    {
        bBeginKCF = false;  
        select_flag = true; 
        origin = cv::Point(x, y);       
        selectRect = cv::Rect2d(x, y, 0, 0);  
    }
    else if (event == cv::EVENT_LBUTTONUP)
    {
        select_flag = false;
        bRenewROI = true;
    }
}

class ImageConverter
{
  	ros::NodeHandle nh_;
  	image_transport::ImageTransport it_;
  	image_transport::Subscriber image_sub_;
  	image_transport::Subscriber depth_sub_;
	
	ros::Subscriber camera_info_;
	sensor_msgs::CameraInfo	camera_info;

	cv::Mat	colorImage;
	cv::Mat	depthImage	= cv::Mat::zeros( 480, 640, CV_16UC1 );

public:
	ros::Publisher pub;

	ImageConverter() : it_(nh_)
  	{
    	// Subscrive to input video feed and publish output video feed
    	image_sub_ = it_.subscribe("/camera/color/image_raw", 1, 
      	  &ImageConverter::imageCb, this);
    	depth_sub_ = it_.subscribe("/camera/aligned_depth_to_color/image_raw", 1, 
      	  &ImageConverter::depthCb, this);
    	camera_info_ = nh_.subscribe("/camera/aligned_depth_to_color/camera_info", 1,
          &ImageConverter::cameraInfoCb, this);
    	
		pub = nh_.advertise<geometry_msgs::Twist>("tarcker/cmd_vel", 1000); // track/cmd_vel

		cv::namedWindow(RGB_WINDOW);
    	//cv::namedWindow(DEPTH_WINDOW);
 	}

	~ImageConverter()
  	{
    	cv::destroyWindow(RGB_WINDOW);
    	//cv::destroyWindow(DEPTH_WINDOW);
  	}

	void imageCb(const sensor_msgs::ImageConstPtr& msg)
  	{
    	cv_bridge::CvImagePtr cv_ptr;
    	try
    	{
      		cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
    	}
    	catch (cv_bridge::Exception& e)
    	{
      		ROS_ERROR("cv_bridge exception: %s", e.what());
      		return;
    	}

    	cv_ptr->image.copyTo(rgbimage);
		// rgbimage = cv_ptr->image;

    	cv::setMouseCallback(RGB_WINDOW, onMouse, 0);

 		if(bRenewROI)
    	{
        	tracker->init(rgbimage, selectRect);
        	bBeginKCF = true;
       	 	bRenewROI = false;
        	enable_get_depth = false;
    	}

    	if(bBeginKCF)
    	{
        	bool res = tracker->update(rgbimage, selectRect);
			if (res)
			{
				result = selectRect;
				cv::rectangle(rgbimage, result, cv::Scalar( 0, 255, 255 ), 1, 8 );
				enable_get_depth = true;
			}
        	// cv::rectangle(rgbimage, result, cv::Scalar( 0, 255, 255 ), 1, 8 );
        	// enable_get_depth = true;
    	}
    	else
        	cv::rectangle(rgbimage, selectRect, cv::Scalar(255, 0, 0), 2, 8, 0);

    	cv::imshow(RGB_WINDOW, rgbimage);
    	cv::waitKey(1);
  	}
	
	void cameraInfoCb(const sensor_msgs::CameraInfo &msg)
	{
		camera_info = msg;
	}
  
	void depthCb(const sensor_msgs::ImageConstPtr& msg)
  	{
  		cv_bridge::CvImagePtr cv_ptr;
  		try
  		{
  			cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_16UC1);
			cv_ptr->image.copyTo(depthimage);
  		}
  		catch (cv_bridge::Exception& e)
  		{
			ROS_ERROR( "cv_bridge exception: %s", e.what() );
			return;
  		}

    	if(enable_get_depth)
    	{
      		dist_val[0] = 0.001 * depthimage.at<u_int16_t>(result.y+result.height/3 , result.x+result.width/3) ;
      		dist_val[1] = 0.001 * depthimage.at<u_int16_t>(result.y+result.height/3 , result.x+2*result.width/3) ;
      		dist_val[2] = 0.001 * depthimage.at<u_int16_t>(result.y+2*result.height/3 , result.x+result.width/3) ;
      		dist_val[3] = 0.001 * depthimage.at<u_int16_t>(result.y+2*result.height/3 , result.x+2*result.width/3) ;
      		dist_val[4] = 0.001 * depthimage.at<u_int16_t>(result.y+result.height/2 , result.x+result.width/2) ;

      		float distance = 0;
      		int num_depth_points = 5;
      		for(int i = 0; i < 5; i++)
      		
			{
        		if(dist_val[i] > 0.4 && dist_val[i] < 10.0)
          			distance += dist_val[i];
        		else
          			num_depth_points--;
      		}
      		
			distance /= num_depth_points;

			//calculate linear speed
      		if(distance > Min_distance)
        		linear_speed = distance * k_linear_speed + h_linear_speed;
      		else
        		linear_speed = 0;

      		if(linear_speed > Max_linear_speed)
       			linear_speed = Max_linear_speed;

      		//calculate rotation speed
      		int center_x = result.x + result.width/2;
      		if(center_x < ERROR_OFFSET_X_left1) 
        		rotation_speed =  Max_rotation_speed;
      		else if(center_x > ERROR_OFFSET_X_left1 && center_x < ERROR_OFFSET_X_left2)
        		rotation_speed = -k_rotation_speed * center_x + h_rotation_speed_left;
      		else if(center_x > ERROR_OFFSET_X_right1 && center_x < ERROR_OFFSET_X_right2)
       			rotation_speed = -k_rotation_speed * center_x + h_rotation_speed_right;
      		else if(center_x > ERROR_OFFSET_X_right2)
        		rotation_speed = -Max_rotation_speed;
      		else 
        		rotation_speed = 0;

      		// std::cout <<  dist_val[0]  << " / " <<  dist_val[1] << " / " << dist_val[2] << " / " << dist_val[3] <<  " / " << dist_val[4] << std::endl;
      		std::cout <<  "distance = " << distance << std::endl;
		}

  	}
};

int main(int argc, char** argv)
{
	ros::init(argc, argv, "csrt_track");
	ImageConverter ic;
  
	while(ros::ok())
	{
		ros::spinOnce();

    	geometry_msgs::Twist twist;
    	twist.linear.x = linear_speed; 
    	twist.linear.y = 0; 
    	twist.linear.z = 0;
    	twist.angular.x = 0; 
    	twist.angular.y = 0; 
    	twist.angular.z = rotation_speed;
    	ic.pub.publish(twist);

		if (cv::waitKey(33) == 'q')
      		break;
	}

	return 0;
}
