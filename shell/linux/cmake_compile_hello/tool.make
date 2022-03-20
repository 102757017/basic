# 设置交叉编译的目标操作系统,可选：Windows,Linux
SET(CMAKE_SYSTEM_NAME Windows)
# 这个是可选项，但是在移动开发中很重要，代表目标系统的硬件或者CPU型号，例如ARM，X86 etc
SET(CMAKE_SYSTEM_PROCESSOR x86)


# 设置工具链目录
#SET(TOOL_CHAIN_DIR /opt/FriendlyARM/toolschain/4.5.1)
#SET(TOOL_CHAIN_INCLUDE 
#    ${TOOL_CHAIN_DIR}/arm-none-linux-gnueabi/sys-root/usr/include
#    ${TOOL_CHAIN_DIR}/arm-none-linux-gnueabi/include
#    )
#SET(TOOL_CHAIN_LIB 
#    ${TOOL_CHAIN_DIR}/arm-none-linux-gnueabi/sys-root/usr/lib
#    ${TOOL_CHAIN_DIR}/arm-none-linux-gnueabi/lib
#    )


# 指定c/c++编译器
# mingw-w64有两个gcc,用i686-w64-mingw32-gcc编译出来的程序就是32位的,而x86_64-w64-mingw32-gcc编译出来的就是64位的
SET(CMAKE_C_COMPILER  x86_64-w64-mingw32-gcc)
SET(CMAKE_CXX_COMPILER x86_64-w64-mingw32-g++)

# 编译64位的程序
SET(CMAKE_CXX_FLAGS"${CMAKE_CXX_FLAGS} -m64")
SET(CMAKE_C_FLAGS"${CMAKE_C_FLAGS} -m64")


# 不一定需要设置,指定编译目标操作系统版本时的搜索根路径,编译器到指定的根目录下寻找对应的系统库
# mingw-w64有两个根路径，32位的根目录：/usr/i686-w64-mingw32，64位的根目录：/usr/x86_64-w64-mingw32
SET(CMAKE_FIND_ROOT_PATH  "/usr/x86_64-w64-mingw32" )

#对FIND_PROGRAM()起作用,有三种取值，NEVER,ONLY,BOTH,第一个表示不在你CMAKE_FIND_ROOT_PATH下进行查找，第二个表示只在这个路径下查找，第三个表示先查找这个路径，再查找全局路径，对于这个变量来说，一般都是调用宿主机的程序，所以一般都设置成NEVER
SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
#只在指定目录下查找库文件
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
#只在指定目录下查找头文件
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
#只在指定目录下查找依赖包
SET(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
