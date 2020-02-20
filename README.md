# Brief Introduction of iComOS

iComOS is an operating system for internet of things (IoT), which can be running on communication chips, especially for NB-IoT communication chips such as Hi2115 and MT2625. The benefit is that iComOS can shrink an IoT node by cutting off the microcontroller (MCU), thus reducing the cost, size, and power consumption. Furthermore, using iComOS, developers can focus on the development of IoT applications and pay less attention to hardware adaptation.

The iComOS SDK for Hi2115 (iComOS_Hi21xx_SDK_V1.2.zip) and MT2625 (iComOS_MT26xx_SDK_V1.1.zip) can be downloaded in this page. These SDKs are free. If any user has interest in iComOS, please download and develop based on it. Feedbacks and comments are welcome. We are look forward to more business cooperations!


# Fast Develop Guide for iComOS SDK
(iComOS_Hi21xx_SDK_V1.2 as an example)

1.	Preparation

1.1 Operating System

Each of the following operating systems is acceptable:
-	Windows 7 32bit or 64bit
-	Windows 10 32bit or 64bit

1.2 Compiler Tools
-	GCC
-	SCons
-	DOS

1.3 Coding language
-	C

1.4 Hardware
-	Communication Chip with Hi2115 such as Quectel BC28
-	Other accessories, such as USB line.

1.5 Software
-	Tools Package (Tools.zip)
-	iComOS SDK (iComOS_Hi21xx_SDK_V1.2.zip)

Directory	Description of iComOS SDK:
-	build_scons: Target directory, You can find the .bin file after compiling.
-	docments:	Documents
-	scons_targets:	Script files
-	src/config:	Project config directory
-	src/custom:	System config directory. You can change the application by modify the files in src/custom/private.
-	src/example:	Example files. Each file could be used to generate an executable bin file.
-	src/libs:	Libaray diretory
-	src/user:	Project root directory. User could create own project under this directory 
-	tools:	Directory for script tools

2.	Develop Tools Installation

2.1 GCC

Find gcc-arm-none-eabi-4_9-2015q2-20150609-win32.exe in the Tools package. Execute it as admin user to install GCC.

Note:
Please check the option “Add path to environment variable” after installation. If you forgot it, please add the installation path (default is “C:\Program Files (x86)\GNU Tools ARM Embedded\4.9 2015q2\bin”) to the system parameters.

2.2 SCons

Before installation, please make sure you have installed Python 2.7. Other version may leads to some compile errors. 
-	Python 2.7, you can find python-2.7.10.msi in the Tools package to install Python 2.7.
-	Pywin32, you can find pywin32-220.win32-py2.7.exe in the Tools package to install pywin32.
-	SCons, you can find scons-2.4.0-setup.exe in the Tools package to install SCons

2.3 UpdatePackage

UpdatePackage tool is used to update the fwpkg firmware.
You can find UpdatePackage-3.22.0.14.msi in the Tools package to install UpdatePackage tool. 

2.4 UEUpdater
-	For Windows 7 (skip it if you use Windows 10)
Please install Microsoft .NET Framework (4.7.2 or higher version) first. 
You can find microsoft .NET framework 4.7.2.exe in the Tools package to install it.
-	UEUpdater
UEUpdater tool could download the fwpkg file into the modules (e.g., BC28).
You can find UEUpdaterUI-3.22.0.14.msi in the Tools package to install UEUpdater.

2.5 UEMonitor

UEMonitor is used to obtain the log information from the modules (e.g., BC28).
You can find UEMonitor-3.22.0.14.msi in the Tools package to install UEMonitor.

3.	Application Development

3.1 How to start
-	You can directly create a new .c file in /src/user/private as a new application.
-	We provide some examples in /src/example/private. You can copy one example to /src/usr/private and then modify it as you like.
-	You can find an example.c in FirstExample package, which is a test example using GPIO to control the LED twinkling every 500ms.

3.2 Modify script

When you try to use your own application (copy an example or create by yourself), please disable the example application by annotating “_QUECTEL_OPEN_EXAMPLE_” in \src\SConscript.

if "_QUECTEL_OPEN_CPU_" in env['CPPDEFINES']: 

env.Append( CPPDEFINES=["_QUECTEL_IOT_OPEN_"]) #Enable iot function 

#env.Append( CPPDEFINES=["_QUECTEL_ONET_OPEN_"]) #Disable onenet function

#env.Append( CPPDEFINES=["_QUECTEL_OPEN_EXAMPLE_"]) #Disable example

4.	Compile and Merge

4.1 Define library file

SDK has provided 2 different library files which related to Huawei OceanConnect Platform and OneNET Platform respectively. You can modify the script file to decide which Platform you are going to use. 

In \src\SConscript :

if "_QUECTEL_OPEN_CPU_" in env['CPPDEFINES']: 

env.Append( CPPDEFINES=["_QUECTEL_IOT_OPEN_"]) #Enable iot function 

#env.Append( CPPDEFINES=["_QUECTEL_ONET_OPEN_"]) #Disable onenet function

4.2 Define module

Please indicate the module. You can define it in the scons.bat under root directory. For example,
-	opencpu_bc35g relates to BC35-G and BC95 R2.0
-	opencpu_bc28 relates to BC28

In \scons.bat :

C:\Python27\Scripts\scons.bat -c target=opencpu_bc28 

C:\Python27\Scripts\scons.bat target=opencpu_bc28

4.3 Compile

Open the cmd under root directory and execute following commands:
-	scons.bat -c
-	scons.bat

If everything is OK, you can find the bin file after compiling.
-	BC28：\build_scons\BC28 
-	BC35-G/BC95 R2.0： \build_scons\BC35G 

4.4 Merge fwpkg Firmware

Next, we should merge the bin file with fwpkg firmware.

(1)	Create a new directory named “fwpkg” under root directory, put the standard firmware into “fwpkg” (use BC28 as example, find BC28JAR01A10.fwpkg in FirstExample package).

(2)	Open the cmd under root directory and execute following command:

"C:\Program Files (x86)\Neul\UpdatePackage\UpdatePackage.exe" updateApplication --in .\fwpkg\BC28JAR01A10.fwpkg –folder .\build_scons\BC28 --out BC28JAR01A10_OCN

(3)	After that, download the generated fwpkg firmware into module.
