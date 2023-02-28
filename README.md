# Cartoonify

![image](https://github.com/blucardin/cartoonify/blob/0eb2b040f14a9f3a0150a865b8e2566fbe06bc86/treesOutput40.png?raw=true)

#### Video Demo:  https://youtu.be/S3cUFmjqQ-U
#### Description: 
Cartoonify is a Python console application that can take an image or video file as input and produce a cartoonified version of it. The cartoonification process involves reducing the color depth of the image, detecting edges in the image, and overlaying the simplified colors and edges to create a cartoon effect.

The application is written in Python 3 and uses several external libraries such as OpenCV, scikit-image, progressbar, and moviepy. The code is divided into three main functions: reduce_image, draw_lines, and cartoonify, which are used to simplify the image, detect edges, and combine the simplified image and edges to create a cartoon effect, respectively.

The main function of the application is responsible for handling the input file, determining whether it is a photo or a video file, and processing each frame of the video or the entire photo file. The final output is saved as a new video or image file, depending on the input type.

The user can provide various flags to modify the output, such as changing the color depth, threshold for edge detection, and choosing between different edge detection algorithms. The application also includes a progress bar to indicate the progress of the cartoonification process for video files.

The usage of the application is to be entered through the command line in the following format:

python3 projectfinal.py (photo/video) (input file) (output file) (colordepth) (flags)

Where:

"photo/video" specifies whether the input is an image or a video

"input file" is the path to the input file

"output file" is the desired name and path of the output file

"colordepth" is the number of colors to reduce the image to

"flags" are optional arguments that can be passed to specify the edge detection and threshold values.

If "photo" is specified as the first argument, the application will convert the input image to a cartoon and save the result to the output file.

If "video" is specified as the first argument, the application will process each frame of the input video, convert it to a cartoon, and save it to a new video file. The audio from the original video is then added to the cartoonified video to create the final output.

Optional flags include "-c" to use the Canny edge detector, "-n" to turn off edge detection, and "-sX" to use the Sobel edge detector and set the edge threshold to X (where X is an integer value). If not specified, the default is the Sobel with threshold 50.


This project was created by Noah Virjee as the final project for the CS50p course. 

