########################################################################
#
# Copyright (c) 2020, STEREOLABS.
#
# All rights reserved.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
########################################################################

"""

README

Note: This file has been modified to record SVO at 1080p

# Stereolabs ZED - SVO Recording utilities

This sample shows how to record video in Stereolabs SVO format.
SVO video files can be played with the ZED API and used with its different modules.

## Getting started

- First, download the latest version of the ZED SDK on [stereolabs.com](https://www.stereolabs.com).
- For more information, read the ZED [API documentation](https://www.stereolabs.com/developers/documentation/API/).

## Run the sample

The default recording compression is H264 which provides fast encoding and efficently compressed SVO file. It can be changed to H265 or LOSSLESS (image based PNG compression) depending on the hardware capabilities. [See API Documentation for more information](https://www.stereolabs.com/docs/api/python/classpyzed_1_1sl_1_1SVO__COMPRESSION__MODE.html)

```
python svo_recording.py svo_file.svo
```

Use Ctrl-C to stop the recording.

"""

import sys
import pyzed.sl as sl
from signal import signal, SIGINT

cam = sl.Camera()     # Create a ZED camera object


"""
A simple sigint handler to stop recording when the user hits Ctrl-C
"""
def handler(signal_received, frame):
    cam.disable_recording()
    cam.close()
    sys.exit(0)

"""
Setup the signal handler
"""
signal(SIGINT, handler)

def main():
    if not sys.argv or len(sys.argv) != 2:
        print("Only the path of the output SVO file should be passed as argument.")
        exit(1)
    """
        init is a variable of type sl.InitParameters. It defines the initialization parameters of the ZED camera.
    """
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Z_UP  # Use ROS-style coordinate system
    init.depth_mode = sl.DEPTH_MODE.NONE

    status = cam.open(init)
    """
        The camera has now been opened and initialized with 'init' . The above function returns 'ERROR_CODE.SUCCESS' if it
        is sucessfully opened 
    """
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    path_output = sys.argv[1]   #simply the path of the output SVO file

    recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.H264)
    """
        RecordingParameters is a class that has the options used to record. 
        Further Description: https://www.stereolabs.com/docs/api/python/classpyzed_1_1sl_1_1RecordingParameters.html#details
    """
    err = cam.enable_recording(recording_param)
    """
        Creates an SVO file to be filled ... uses the parameters we defined in recording_param
        The function returns an error code that can be checked using the ERROR_CODE class(?)
        Further Description : https://www.stereolabs.com/docs/api/python/classpyzed_1_1sl_1_1Camera.html#a4e17c372d93750b60f3a45a49d7127d2
    """
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    runtime = sl.RuntimeParameters()
    """
        Class containing parameters that defines the behavior of sl.Camera.grab()
        Further Description: https://www.stereolabs.com/docs/api/python/classpyzed_1_1sl_1_1RuntimeParameters.html

    """
    print("SVO is Recording, use Ctrl-C to stop.")
    frames_recorded = 0

    """
        The following loop is used to record the SVO file.
        The loop will run until the user presses Ctrl-C
        sl.Camera.grab()
        This method will grab the latest images from the camera, rectify them,
        and compute the measurements based on the RuntimeParameters provided (depth, point cloud, tracking, etc.)
        Further Description :https://www.stereolabs.com/docs/api/python/classpyzed_1_1sl_1_1RuntimeParameters.html#a54b1041e82c3484cd584cacf1f3becf4

    """
    while True:
        if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS :
            frames_recorded += 1
            print("Frame count: " + str(frames_recorded), end="\r")

if __name__ == "__main__":
    main()
