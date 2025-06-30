import cv2
import subprocess
import platform
import re
import json

def get_camera_index(device_address):
    system = platform.system()
    camera_list = []

    if system == "Windows":
        try:
            # 增强版命令：获取更详细的设备信息（包括硬件ID）
            # 确保PowerShell命令返回的数据在InstanceId和HardwareID中没有额外的空格
            command = [
                "powershell", "-Command",
                "Get-PnpDevice -Class Camera | "
                "Select-Object FriendlyName,InstanceId,HardwareID | "
                "ConvertTo-Json -Depth 10"
            ]
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore')
            devices = json.loads(result)
            
            print("\n===== Windows摄像头设备列表 =====")
            for i, device in enumerate(devices):
                friendly_name = device.get("FriendlyName", "N/A")
                instance_id = device.get("InstanceId", "N/A")
                hardware_ids = device.get("HardwareID", ["N/A"])
                
                # 打印设备信息用于调试
                print(f"设备 {i}:")
                print(f"  名称: {friendly_name}")
                print(f"  InstanceID: {instance_id}")
                print(f"  HardwareID: {hardware_ids}")
                print("-" * 40)
                
                # 收集所有可能的设备地址（包括InstanceID和HardwareID）
                # 移除InstanceID和HardwareID字符串中的潜在空白字符
                all_addresses = [instance_id.strip()] + [hid.strip() for hid in hardware_ids]
                camera_list.append((friendly_name, all_addresses, i))
            
        except Exception as e:
            print(f"获取Windows摄像头信息失败: {e}")
            print(f"原始错误信息: {e}")
            return -1

    # Linux和macOS的代码与之前一致，此处省略...
    # 如需完整代码，请告知，可补充完整

    # 查找匹配的设备地址（Windows专用逻辑）
    if system == "Windows":
        # 统一转大写匹配，并确保目标地址本身也去除空白
        target_address = device_address.upper().strip() 
        for name, addresses, index in camera_list:
            for addr in addresses:
                # 使用 == 进行精确匹配，因为InstanceID通常是唯一的
                # 或者如果你只想匹配子串，可以继续使用 in
                if target_address == addr.upper(): # 更改为精确匹配
                    # 验证摄像头索引，明确使用CAP_DSHOW
                    cap = cv2.VideoCapture(index)
                    if cap.isOpened():
                        print(f"DEBUG: 匹配成功，找到设备 '{name}' 在索引 {index}")
                        cap.release()
                        return index
                    else:
                        print(f"警告：索引 {index} ({name}) 可匹配但无法通过OpenCV打开。")
                        cap.release() # 确保释放资源
        print(f"未找到与 '{device_address}' (处理后: '{target_address}') 匹配的设备地址。")
    return -1

# 使用示例
if __name__ == "__main__":
    device_address = r"USB\VID_0C45&PID_636B&MI_00\7&315A9F63&0&0000"  

    index = get_camera_index(device_address)
    if index != -1:
        print(f"成功找到摄像头，编号为: {index}")
    else:
        print("未找到匹配的摄像头")

