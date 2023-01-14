import requests
import sys
import os
import shutil
import tarfile

r = requests.get("https://files.pythonhosted.org/packages/13/2e/bc4c0026659cea46aca867f4d71e8bab5a6430b4c005c51e174da5e6e4a2/pyinstaller-5.7.0.tar.gz")
with open("pyinstaller.tgz","wb+") as f:
    f.write(r.content)

with tarfile.open("pyinstaller.tgz") as f:
    f.extractall("pyinstaller")
    os.system(f'python pyinstaller/pyinstaller-5.7.0/PyInstaller --onefile main.py')
shutil.rmtree("pyinstaller")
shutil.rmtree("build")
shutil.move("dist/main","jns")
print("Successfully built and bootstrapped JNS!")
print("Adding JNS to PATH...")
os.system(f"setx PATH %PATH%;{os.path.dirname(os.path.abspath(__file__))}")
with open(os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "jns.cmd"), "w+") as f:
    f.write(f"setx PATH %PATH%;{os.path.dirname(os.path.abspath(__file__))}")
