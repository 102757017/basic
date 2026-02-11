# camindexcheck_pyside6_fixed.py
import sys
import ctypes
import re
import os
# CHANGE 1: Import from PySide6 instead of PyQt5
from PySide6.QtWidgets import QApplication, QMessageBox
# CHANGE 2: Import QMediaDevices instead of QCameraInfo for Qt6 API
from PySide6.QtMultimedia import QMediaDevices

# --- OpenCV Camera Index Ctypes Wrapper ---
DLL_PATH = 'lib/CvCameraIndex_x64.dll'

def get_opencv_camera_index_from_dll(hwid):
    """ 
    使用提供的 DLL 获取 cv.VideoCapture(camera_index, cv2.CAP_DSHOW) 的参数 camera_index。
    :param hwid: 硬件标识，不区分大小写，如 'VID_1BCF&PID_2B9B&MI_00#6&1D6F8A2E&0&0000'
    :return: OpenCV 的索引下标，返回 -1 时获取失败。
    """
    try:
        _CvCameraIndex = ctypes.cdll.LoadLibrary(DLL_PATH)
        _CvCameraIndex.getCameraIndex.argtypes = [ctypes.c_char_p]
        _CvCameraIndex.getCameraIndex.restype = ctypes.c_int
        
        b_hwid = bytes(hwid, encoding='utf-8')
        return _CvCameraIndex.getCameraIndex(b_hwid)
    except FileNotFoundError:
        print(f"错误: 动态链接库 '{DLL_PATH}' 未找到。请确保文件路径正确。")
        return -2
    except Exception as e:
        print(f"错误: 调用DLL时发生未知错误: {e}")
        return -1

# --- HWID Parsing Functions ---

def parse_hwid_from_qt_device_name(device_name):
    """
    (FIXED - This function remains the same as the corrected PyQt5 version)
    Parses the full hardware ID, including the unique instance path, from the Qt device name string.
    """
    # This regex finds 'vid_' and captures everything up until the '{' character,
    # which typically marks the beginning of the device interface class GUID.
    match = re.search(r'(vid_[^\{]+)', device_name, re.IGNORECASE)
    if match:
        hwid = match.group(1).strip()
        return hwid
    return None

def normalize_hwid(hwid):
    """
    标准化HWID格式，确保大小写一致
    """
    parts = hwid.split('#')
    if len(parts) > 0:
        parts[0] = parts[0].upper()
    # Re-join the full path
    return '#'.join(parts)

# --- Main Comparison Logic ---

def compare_camera_indices():
    print("=" * 80)
    print("开始对比 Qt 和 OpenCV 的摄像头索引与HWID对应关系...")
    print("=" * 80)

    # CHANGE 3: Use QMediaDevices.videoInputs() for PySide6/Qt6 API
    all_camera_devices = QMediaDevices.videoInputs()

    if not all_camera_devices:
        print("系统中没有检测到任何可用摄像头。")
        QMessageBox.warning(None, "无摄像头", "系统中没有检测到任何可用摄像头。")
        return

    # CHANGE 4: Update print statement for the new API
    print(f"\n[Qt] 通过 QMediaDevices.videoInputs() 发现 {len(all_camera_devices)} 个摄像头:\n")
    
    qt_camera_map = {}
    hwid_qt_map = {}
    
    # CHANGE 5: Iterate through QCameraDevice objects
    for i, device in enumerate(all_camera_devices):
        # CHANGE 6: Get device ID using device.id().data().decode()
        device_name = device.id().data().decode()
        # The fix in parse_hwid_from_qt_device_name is critical and remains in effect
        hwid = parse_hwid_from_qt_device_name(device_name)
        
        if not hwid:
            print(f"  - Qt Index: {i}")
            print(f"    设备ID: {device_name}") # Changed "设备名" to "设备ID" for clarity with Qt6 API
            print(f"    警告: 无法从此设备ID中解析出标准 HWID。")
            continue
            
        normalized_hwid = normalize_hwid(hwid)
        qt_camera_map[i] = normalized_hwid
        hwid_qt_map[normalized_hwid] = i
        
        print(f"  - Qt Index: {i}")
        print(f"    设备ID: {device_name}")
        print(f"    解析出的 HWID: {hwid}")
        print(f"    标准化 HWID: {normalized_hwid}")
        
    print("\n" + "-" * 80 + "\n")

    if not os.path.exists(DLL_PATH):
        print(f"错误: 无法继续对比，因为 '{DLL_PATH}' 不存在。")
        QMessageBox.critical(None, "DLL未找到", f"无法找到DLL文件: {DLL_PATH}")
        return

    print("[OpenCV] 通过 DLL 查询每个HWID对应的OpenCV索引:\n")
    
    opencv_camera_map = {}
    hwid_opencv_map = {}
    
    all_match = True
    match_details = []
    
    for qt_index, hwid in qt_camera_map.items():
        # This part was fixed previously and remains the same:
        # We use the FULL, normalized HWID for the query to distinguish between identical cameras.
        hwid_for_search = hwid

        print(f"  查询 HWID: '{hwid_for_search}' (使用完整路径进行搜索)...")
        
        opencv_index = get_opencv_camera_index_from_dll(hwid_for_search)
        
        if opencv_index >= 0:
            opencv_camera_map[opencv_index] = hwid
            hwid_opencv_map[hwid] = opencv_index
            
            is_match = (qt_index == opencv_index)
            match_details.append({
                'hwid': hwid,
                'qt_index': qt_index,
                'opencv_index': opencv_index,
                'match': is_match
            })
            
            if not is_match:
                all_match = False
            
            print(f"    > Qt Index: {qt_index}")
            print(f"    > OpenCV Index: {opencv_index}")
            status = '✅ 一致' if is_match else '❌ 不一致'
            print(f"    [结论]: {status}")
        else:
            match_details.append({
                'hwid': hwid,
                'qt_index': qt_index,
                'opencv_index': '查询失败',
                'match': False
            })
            all_match = False
            print(f"    > OpenCV Index: 查询失败 (DLL 返回 {opencv_index})")
            print("    [结论]: ❌ 查询失败")
        
        print("-" * 40)

    # ... (The rest of the result printing code is fine and does not need changes) ...
    print("\n" + "=" * 80)
    print("[详细对比结果]")
    print("=" * 80)
    
    print("\nQt 摄像头列表:")
    print(f"{'Index':<7}| {'HWID'}")
    print("-" * 80)
    for index, hwid in sorted(qt_camera_map.items()):
        print(f"{index:<7}| {hwid}")
    
    print("\nOpenCV 摄像头列表:")
    print(f"{'Index':<7}| {'HWID'}")
    print("-" * 80)
    temp_hwid_check = {}
    for index, hwid in sorted(opencv_camera_map.items()):
        warning = ""
        if hwid in temp_hwid_check:
            warning = f"  <-- 警告: 此HWID已映射到索引 {temp_hwid_check[hwid]}"
        print(f"{index:<7}| {hwid}{warning}")
        temp_hwid_check[hwid] = index

    print("\n索引对应关系对比:")
    print(f"{'HWID':<50} | {'Qt Index':<10} | {'OpenCV Index':<12} | {'状态'}")
    print("-" * 90)
    for detail in match_details:
        status = "✅ 一致" if detail['match'] else "❌ 不一致"
        hwid_display = (detail['hwid'][:47] + '...') if len(detail['hwid']) > 50 else detail['hwid']
        print(f"{hwid_display:<50} | {detail['qt_index']:<10} | {str(detail['opencv_index']):<12} | {status}")

    print("\n" + "=" * 80)
    if all_match and qt_camera_map:
        print("🎉 总结: 所有检测到的摄像头在 Qt 和 OpenCV 中的索引完全一致！")
        QMessageBox.information(None, "对比结果", "所有摄像头索引完全一致！")
    else:
        print("⚠️ 总结: 发现索引不一致或查询失败的情况。")
        mismatch_count = len([d for d in match_details if not d['match']])
        QMessageBox.warning(None, "对比结果", 
                          f"发现 {mismatch_count} 个摄像头索引不一致或查询失败。\n请查看控制台输出获取详细信息。")
    print("=" * 80)

if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    compare_camera_indices()
