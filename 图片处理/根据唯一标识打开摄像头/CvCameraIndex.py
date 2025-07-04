import ctypes

# 加载对应位数动态链接库
_CvCameraIndex = ctypes.cdll.LoadLibrary('lib/CvCameraIndex_x64.dll')
_CvCameraIndex.getCameraIndex.argtypes = [ctypes.c_char_p]
_CvCameraIndex.getCameraIndex.restype = ctypes.c_int


def get_camera_index(hwid: str) -> int:
    """ 获取cv.VideoCapture(camera_index, cv2.CAP_DSHOW)参数camera_index
    :param hwid: 硬件标识，不区分大小写，如vid_1234&pid_4321
    :return: 索引下标，返回 -1 时获取失败
    """
    b_hwid = bytes(hwid, encoding='utf-8')
    return _CvCameraIndex.getCameraIndex(b_hwid)


if __name__ == '__main__':
    camera_index = get_camera_index('VID_1BCF&PID_2B9B')
    print(camera_index)
