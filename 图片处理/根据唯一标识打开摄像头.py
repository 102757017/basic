import cv2
from pygrabber.dshow_graph import DsGraph # 修正这里！

def list_camera_properties():
    """
    列出所有DirectShow摄像头及其属性，包括名称、索引和设备路径。
    """
    devices = DsGraph().get_input_devices() # 使用修正后的 DsGraph
    camera_map = {} # 存储 {device_path: index}
    print("Enumerating cameras...")
    for idx, dev in enumerate(devices):
        # 尝试用当前索引打开摄像头，以确保它是一个可用的视频设备
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW) 
        if not cap.isOpened():
            print(f"  Camera {idx}: '{dev['name']}' (Path: {dev['device_path']}) - NOT OPENED by OpenCV, skipping.")
            cap.release()
            continue
        cap.release() # 立即释放，我们只是检查可用性
        
        info = {
            "index": idx,
            "name": dev['name'],
            "device_path": dev['device_path']
        }
        camera_map[dev['device_path']] = idx # 存储设备路径到索引的映射
        print(f"  Camera {idx}: '{dev['name']}'")
        print(f"    Device Path: {dev['device_path']}")
        
    return camera_map

def get_camera_index_by_device_path(target_device_path):
    """
    根据摄像头的完整设备实例路径查找其当前的OpenCV索引。
    Args:
        target_device_path (str): 目标摄像头的完整设备实例路径，
                                  例如 'USB\\VID_046D&PID_082D\\MSFT\\ABC1234567890'
    Returns:
        int or None: 匹配到的摄像头的OpenCV索引，如果未找到则返回 None。
    """
    devices = DsGraph().get_input_devices() # 使用修正后的 DsGraph
    
    for idx, dev in enumerate(devices):
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap.release()
            continue
        cap.release() # 释放资源
        
        if dev['device_path'] == target_device_path:
            print(f"Found camera with path '{target_device_path}' at OpenCV index {idx}")
            return idx
            
    print(f"Camera with device path '{target_device_path}' not found or not available.")
    return None

if __name__ == "__main__":
    print("--- Listing All Camera Properties ---")
    camera_path_to_index_map = list_camera_properties()
    print("--- End Listing ---\n")

    print("Mapping from Device Path to OpenCV Index:")
    for path, index in camera_path_to_index_map.items():
        print(f"  '{path}' -> {index}")

    specific_camera_path = r"USB\VID_046D&PID_082D\MSFT\ABC1234567890" 

    camera_index = get_camera_index_by_device_path(specific_camera_path)

    if camera_index is not None:
        cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW) 
        if not cap.isOpened():
            print(f"Error: Could not open camera at index {camera_index} for path '{specific_camera_path}'")
        else:
            print(f"Successfully opened camera at index {camera_index} using path '{specific_camera_path}'")
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow(f"Camera: {specific_camera_path}", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
    else:
        print("Could not find the specified camera based on its device path.")
