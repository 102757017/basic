echo 关联jupyter
pip install nbopen
python -m nbopen.install_win

echo 自动发现目录下的虚拟环境，虚拟环境中必须包含ipykernel
pip install nb_venv_kernels