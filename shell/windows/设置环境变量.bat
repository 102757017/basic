echo 1. ������ʱ��������(����ģʽ)
set BAT_HOME=c:\bat

echo 2. ������ʱ��������(׷��ģʽ)
set BAT_HOME=c:\bat
set BAT_HOME=%BAT_HOME%;c:\bat

echo 3. �������û�������(����ģʽ)
setx /M "BAT_HOME" "c:\bat"

echo 4. �������û�������(׷��ģʽ)�������´򿪵��ն�����Ч,��ǰ�ն˲���������Ч
echo �� win10 �����Ҽ�ѡ�����Ա������С�
echo /M ��ѡ��ϵͳ����˼���� win10 �����ǻ��ϸ�����ϵͳ�����������û����������ģ�Ĭ�ϵ����û��������������ԣ����Ҫ�޸�ϵͳ������������ô����Ҫ�������ָ��.
echo PATH ��·������˼����˼����Ҫ���õĲ�����PATH.
setx /M Path "%Path%;D:\ProgramData\Anaconda3;D:\ProgramData\Anaconda3\Scripts;D:\ProgramData\Anaconda3\Library\bin"

cmd /k echo.