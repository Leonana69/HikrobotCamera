import cv2, numpy as np
from ctypes import *
import sys

from .MvImport.MvCameraControl_class import *

class HikCamera:
    def __init__(self) -> None:
        # Create a camera object
        deviceList = MV_CC_DEVICE_INFO_LIST()
        tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
        if ret != 0:
            print("enum devices fail! ret[0x%x]" % ret)
            sys.exit()

        if deviceList.nDeviceNum == 0:
            print("find no device!")
            sys.exit()

        stDeviceInfo = cast(deviceList.pDeviceInfo[0], POINTER(MV_CC_DEVICE_INFO)).contents
        self.cam = MvCamera()
        ret = self.cam.MV_CC_CreateHandle(stDeviceInfo)
        if ret != 0:
            print("create handle fail! ret[0x%x]" % ret)
            sys.exit()

        ret = self.cam.MV_CC_OpenDevice(0)
        if ret != 0:
            print("open device fail! ret[0x%x]" % ret)
            sys.exit()

    def start_stream(self):
        # Continuously read images
        ret = self.cam.MV_CC_StartGrabbing()
        if ret != 0:
            print("start grabbing fail! ret[0x%x]" % ret)
            sys.exit()
        self.stParam = MVCC_INTVALUE()
        memset(byref(self.stParam), 0, sizeof(MVCC_INTVALUE))
        ret = self.cam.MV_CC_GetIntValue("PayloadSize", self.stParam)
        if ret != 0:
            print("get payload size fail! ret[0x%x]" % ret)
            sys.exit()

        self.pData = (c_ubyte * self.stParam.nCurValue)()
        self.stImageInfo = MV_FRAME_OUT_INFO_EX()
        memset(byref(self.stImageInfo), 0, sizeof(self.stImageInfo))

    def stop_stream(self):
        # Stop reading images
        ret = self.cam.MV_CC_StopGrabbing()
        if ret != 0:
            print("stop grabbing fail! ret[0x%x]" % ret)
            sys.exit()

    def get_frame_reader(self):
        ret = self.cam.MV_CC_GetOneFrameTimeout(self.pData, self.stParam.nCurValue, self.stImageInfo, 1000)
        if ret == 0:
            print("get one frame: Width[%d], Height[%d], nFrameNum[%d] nCurValue[%d]" % (
                self.stImageInfo.nWidth, self.stImageInfo.nHeight, self.stImageInfo.nFrameNum, self.stParam.nCurValue))

            # Convert the image data to a numpy array
            pData = np.array(self.pData)
            pData = pData.reshape(self.stImageInfo.nHeight, self.stImageInfo.nWidth, 3)
            return pData