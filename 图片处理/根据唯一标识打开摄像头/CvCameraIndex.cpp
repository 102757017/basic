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
