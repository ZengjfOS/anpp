# README

在多个Android项目自由跳转脚本，包含自动补全

# 一、配置方法

修改文件数组：androiddir.bash.template

* defaultPath：所有项目的根目录
* projects: 项目文件夹名
* products：项目对应的产品名
* kernels：内核相对路径，相对于projects
* dtss：dts相对路径，相对kernels
* bootloaderStage1s：第一阶段bootloader
* bootloaderStage2s：第二阶段bootloader
* outs：out目录，不含product名
* efuses：签名工具目录
* components：跳转命令别命（alias）

# 二、install

`make install`

```
cp androiddir.bash.template ~/.androiddir.sh
check if source .androiddir.sh path in /home/pi/.bashrc:
.androiddir.sh path not source in /home/pi/.bashrc
tail ~/.bashrc last 2 line for terminal check
~/.bashrc content
...
# add anpp(https://github.com/ZengjfOS/anpp) function to bash env
source ~/.androiddir.sh
```

# 三、clean

`make clean`

```
rm ~/.androiddir.sh
sed -i "/.androiddir.sh/d" ~/.bashrc
sed -i "/ZengjfOS\/anpp/d" ~/.bashrc
```

# 四、使用方法

## 4.1 自动补全使用

* `anpp <tab><tab>`
  ```
  a00   l00  m0    m8
  ```
  * list project
* `anpp m0 <tab><tab>`
  ```
  android  bs1      bs2      dts      kernel   out
  ```
  * list component
* `m0 <tab><tab>`
  ```
  android  bs1      bs2      dts      kernel   out
  ```
  * list component

## 4.2 项目源代码跳转

* projects中的名字去除`-project`后缀，小写名字可以直接跳转到对应的目录
* 譬如M0-project，去除名字为M0，小写为m0，所以直接在终端输入m0，可以直接调转到其源代码根目录

## 4.3 其他跳转命令

NO. | 命令名 | 说明
:--:|:------:|:-----
1 | android  | 跳转到当前project的根目录
2 | bs1      | 跳转到当前project的bootloader第一阶段目录
3 | bs2      | 跳转到当前project的bootloader第二阶段目录
4 | dts      | 跳转到当前project的设备树目录
5 | kernel   | 跳转到当前project的内核目录
6 | out      | 跳转到当前project的out目录
7 | efuse    | 跳转到当前project的签名工具目录

