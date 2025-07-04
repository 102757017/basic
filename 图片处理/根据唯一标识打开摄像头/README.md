描述：根据摄像头硬件标识（如vid_1234&pid_4321）获取`OpenCV`打开照相机中所需参数index下标，适用于Windows平台，cv.VideoCapture(int index, CAP_DSHOW)。

关键词：Python；OpenCV；VideoCapture；camera_id；index；下标；索引



为什么需要这样一个函数？

如果电脑中只有 1 个照相机设备，那么我们使用 OpenCV 打开时，传递的下标参数使用默认的 0 即可；

但是但电脑中有多个照相机设备时，我们需要打开特定照相机时，我们就不知道哪个设备对应那个下标了，而且当设备的插口发生变化时其下标也会变化。

通过查看 OpenCV 源码可得知（可参考[cap_dshow.cpp](https://github.com/opencv/opencv/blob/4.6.0/modules/videoio/src/cap_dshow.cpp)videoInput::getDevice函数），在打开照相机时，是通过枚举系统照相机设备找到对应下标的照相机，那么我们只需要通过同样的方式枚举，通过照相机特定标识判断是否匹配，返回对应下标即可。



具体源码及已编译动态链接库：[Myles Yang/CvCameraIndex (gitee.com)](https://gitee.com/snwjas/cv-camera-index)



如何在Python中使用：

```python
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
    camera_index = get_camera_index('vid_1234&pid_4321')
    print(camera_index)
```



C++实现（CvCameraIndex.cpp）：

```c++
#include <string>
#include <algorithm>
#include <DShow.h>
#pragma comment(lib, "Strmiids.lib")

#define DllExport					_declspec(dllexport)
#define MAX_DEVICE_PATH_LENGTH		255


extern "C" DllExport int getCameraIndex(const char* hwid);


/**
 * Get the index of the camera opened by the opencv function VideoCapture(int index, CAP_DSHOW)
 * Only available on windows platforms.
 * For the method, refer to opencv ver.4.6 source code cap_dshow.cpp function videoInput::getDevice.
 *
 * @param hwid: Camera hardware ID (Case insensitive): e.g."vid_1234&pid_4321"
 * @return int: Index of the camera, return -1 in case of acquisition failure
 *
 * @author Myles Yang
 */
DllExport int getCameraIndex(const char* hwid)
{
	bool done = false;
	int deviceCounter = 0;
	int cameraIndex = -1;

	// Initialize COM
	HRESULT hr = NULL;
	hr = CoInitialize(NULL);
	// always true when python is called
	//if (FAILED(hr))
	//{
	//	return cameraID;
	//}

	// Create the System Device Enumerator.
	ICreateDevEnum* pSysDevEnum = NULL;
	hr = CoCreateInstance(CLSID_SystemDeviceEnum, NULL, CLSCTX_INPROC_SERVER, IID_ICreateDevEnum, reinterpret_cast<void**>(&pSysDevEnum));
	if (FAILED(hr))
	{
		CoUninitialize();
		return cameraIndex;
	}
	// Obtain a class enumerator for the video input category.
	IEnumMoniker* pEnumCat = NULL;
	hr = pSysDevEnum->CreateClassEnumerator(CLSID_VideoInputDeviceCategory, &pEnumCat, 0);
	if (hr == S_OK)
	{
		// Enumerate the monikers.
		IMoniker* pMoniker = NULL;
		ULONG cFetched;
		while ((!done) && (pEnumCat->Next(1, &pMoniker, &cFetched) == S_OK))
		{
			// Bind the first moniker to an object
			IPropertyBag* pPropBag;
			hr = pMoniker->BindToStorage(0, 0, IID_IPropertyBag, (void**)&pPropBag);
			if (SUCCEEDED(hr))
			{
				// To retrieve the filter's DevicePath, do the following:
				VARIANT varName;
				varName.vt = VT_BSTR;
				VariantInit(&varName);

				hr = pPropBag->Read(L"DevicePath", &varName, 0);
				if (SUCCEEDED(hr))
				{
					// convert DevicePath to char*
					char devicePath[MAX_DEVICE_PATH_LENGTH] = { 0 };
					int count = 0;
					while (varName.bstrVal[count] != 0x00)
					{
						devicePath[count] = varName.bstrVal[count];
						count++;
					}
					std::string devicePathString = devicePath; // lower string

					// to lower
					std::string hwidString = hwid;
					std::transform(hwidString.begin(), hwidString.end(), hwidString.begin(), ::tolower);

					// match
					int matched = devicePathString.find(hwidString);
					if (matched >= 0)
					{
						cameraIndex = deviceCounter;
						done = true;
					}
				}

				deviceCounter++;

				VariantClear(&varName);
				pPropBag->Release();
				pPropBag = NULL;
			}
			pMoniker->Release();
			pMoniker = NULL;
		}
		pEnumCat->Release();
		pEnumCat = NULL;
	}
	pSysDevEnum->Release();
	pSysDevEnum = NULL;
	CoUninitialize();

	return cameraIndex;
}
```


