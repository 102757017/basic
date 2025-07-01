import cv2
import subprocess
import platform
import re
import json
import pprint

def get_camera_indices(device_addresses):
    """
    查找一个或多个USB摄像头在OpenCV中的索引。
    此版本主要支持 Windows 操作系统。

    Args:
        device_addresses (str or list): 单个设备地址字符串，或包含多个设备地址字符串的列表。
                                        设备地址可以是 Instance ID 或 Hardware ID 的一部分。

    Returns:
        dict: 一个字典，键是原始的设备地址字符串，值是对应的OpenCV索引号。
              如果未找到，则值为 -1。
    """
    if not isinstance(device_addresses, list):
        device_addresses = [device_addresses]

    # 初始化结果字典，所有请求地址默认未找到
    found_camera_indices = {addr: -1 for addr in device_addresses}
    
    system = platform.system()
    system_cameras_info = [] # 存储系统检测到的所有摄像头信息

    if system == "Windows":
        try:
            # 使用PowerShell获取更详细的设备信息
            command = [
                "powershell", "-Command",
                "Get-PnpDevice -Class Camera | "
                "Select-Object FriendlyName,InstanceId,HardwareID | "
                "ConvertTo-Json -Depth 10"
            ]
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore')
            devices = json.loads(result)
            
            print("\n===== Windows系统摄像头列表（用于匹配）=====")
            for i, device in enumerate(devices):
                friendly_name = device.get("FriendlyName", "N/A")
                instance_id = device.get("InstanceId", "N/A").strip() # 移除潜在空白
                hardware_ids = [hid.strip() for hid in device.get("HardwareID", [])] # 移除潜在空白

                # 打印设备信息用于调试
                print(f"设备 {i} (OpenCV 索引):")
                print(f"  名称: {friendly_name}")
                print(f"  InstanceID: '{instance_id}'")
                print(f"  HardwareID: {hardware_ids}")
                print("-" * 40)
                
                # 收集所有可能的设备地址（包括InstanceID和HardwareID）
                all_addresses = [instance_id] + hardware_ids
                system_cameras_info.append({
                    "friendly_name": friendly_name,
                    "opencv_index": i,
                    "all_addresses": [addr.upper() for addr in all_addresses if addr] # 统一转大写方便匹配
                })
            
        except Exception as e:
            print(f"错误：获取Windows摄像头信息失败。请确保PowerShell可用且有权限。")
            print(f"详细错误: {e}")
            return found_camera_indices # 返回全部未找到

    else:
        print(f"当前操作系统 ({system}) 的摄像头识别逻辑未实现或不支持。")
        return found_camera_indices

    # --- 开始匹配阶段 ---
    for target_addr_original in device_addresses:
        target_addr_norm = target_addr_original.upper().strip()
        
        # 如果这个地址已经被找到了，跳过
        if found_camera_indices[target_addr_original] != -1:
            continue

        for sys_cam in system_cameras_info:
            for sys_addr in sys_cam["all_addresses"]:
                # 使用 'in' 进行子串匹配，因为用户可能只提供部分HardwareID
                # 如果需要精确匹配，请将 'in' 改为 '=='
                if target_addr_norm in sys_addr: # 允许部分匹配
                    # 匹配成功，现在验证该索引是否真的能被OpenCV打开
                    current_opencv_index = sys_cam["opencv_index"]
                    cap = cv2.VideoCapture(current_opencv_index)
                    if cap.isOpened():
                        found_camera_indices[target_addr_original] = current_opencv_index
                        cap.release()
                        # 一个请求地址找到了，就跳出当前系统摄像头的所有地址循环
                        # 并进入下一个请求地址的匹配
                        break 
                    else:
                        print(f"警告：请求地址 '{target_addr_original}' 匹配到摄像头 '{sys_cam['friendly_name']}' (索引 {current_opencv_index})，但OpenCV无法打开。")
                        cap.release()
            
            # 如果当前 target_addr_original 已经找到了，就跳出对 system_cameras_info 的循环
            if found_camera_indices[target_addr_original] != -1:
                break

    # 打印最终结果
    print("\n===== 最终匹配结果 =====")
    for addr, index in found_camera_indices.items():
        if index != -1:
            print(f"请求地址: '{addr}' --> 摄像头索引: {index}")
        else:
            print(f"请求地址: '{addr}' --> 未找到匹配的摄像头")

    return found_camera_indices

# 使用示例
if __name__ == "__main__":
    # 定义要查找的多个摄像头地址
    target_device_addresses = [
        r"USB\VID_0C45&PID_636B&MI_00\7&315A9F63&0&0000", # 示例 InstanceID
        r"USB\VID_046D&PID_0825",                          # 示例 HardwareID (Logitech C270)
        r"VID_XXXX&PID_YYYY",                             # 另一个示例 HardwareID
        r"My_Custom_Webcam",                              # 示例 FriendlyName (如果系统信息中包含)
        r"USB\VID_046D&PID_081B",                           # 另一个示例 HardwareID (Logitech C920)
    ]

    # 调用函数查找多个摄像头
    found_indices = get_camera_indices(target_device_addresses)
    pprint.pprint(found_indices)
    
