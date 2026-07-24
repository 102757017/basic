import win32com.client
import pythoncom
import sys

def check_directshow():
    print("===== DirectShow 组件检查 =====")
    
    try:
        # 尝试创建系统设备枚举器
        print("尝试创建 SystemDeviceEnumerator...")
        clsid = "{62BE5D10-60EB-11d0-BD3B-00A0C911CE86}"
        try:
            obj = win32com.client.Dispatch(clsid)
            print("✅ SystemDeviceEnumerator 创建成功!")
        except Exception as e:
            print(f"❌ 创建失败: {e}")
            print("可能原因: 组件未注册或媒体功能包未安装")
        
        # 尝试查询视频输入设备
        print("\n尝试枚举视频设备...")
        try:
            pythoncom.CoInitialize()
            dev_enum = win32com.client.Dispatch(clsid)
            enum_moniker = dev_enum.CreateClassEnumerator(
                "{860BB310-5D01-11d0-BD3B-00A0C911CE86}", 0)
            
            if enum_moniker:
                count = 0
                while enum_moniker.Next():
                    count += 1
                print(f"✅ 找到 {count} 个视频设备")
            else:
                print("❌ 未找到视频设备枚举器")
        except Exception as e:
            print(f"❌ 枚举失败: {e}")
    
    finally:
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    check_directshow()
    input("\n按 Enter 键退出...")
