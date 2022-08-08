# README

在多个Android项目自由跳转脚本，包含自动补全，可以直接修改template或者修改json配置进行安装，支持自定义命令

# 目录

* [一、配置方法](#一配置方法)
  * [1.1 修改androiddir.bash.template](#11-修改androiddirbashtemplate)
  * [1.2 修改config.json](#12-修改configjson)
* [二、install](#二install)
  * [2.1 直接安装androiddir.bash.template修改](#21-直接安装androiddirbashtemplate修改)
  * [2.2 安装config.json修改](#22-安装configjson修改)
* [三、clean](#三clean)
* [四、使用方法](#四使用方法)
  * [4.1 自动补全使用](#41-自动补全使用)
  * [4.2 项目源代码跳转](#42-项目源代码跳转)
  * [4.3 其他跳转命令](#43-其他跳转命令)
* [五、自定义命令](#五自定义命令)
* [六、自定义别名](#六自定义别名)

# 一、配置方法

## 1.1 修改androiddir.bash.template

修改文件数组：[androiddir.bash.template](androiddir.bash.template)

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

## 1.2 修改config.json

修改json数据：[config.json](config.json)

* defaultPath：所有项目的根目录
* project_keys：用于定义project支持哪些属性，定义了但是在project中没有赋值的会使用`.`（路径）替代
  * project: 项目文件夹名
  * product：项目对应的产品名
  * kernel：内核相对路径，相对于projects
  * dts：dts相对路径，相对kernels
  * bootloaderStage1s：第一阶段bootloader
  * bootloaderStage2s：第二阶段bootloader
  * out：out目录，不含product名
  * efuse：签名工具目录
* components：用于合成路径，以及shell命令的alias
  * cmd：shell命令alias
  * combine：使用project_keys中的属性，完成cmd命令的路径组合

# 二、install

## 2.1 直接安装androiddir.bash.template修改

* `make template`
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
* `source ~/.bashrc`

## 2.2 安装config.json修改

* 以下三条命令执行的内容是一致的
  * `make`
  * `make json`
  * `make install`
* make log
  ```
  python3 ./generator.py ~/.androiddir.sh
  defaultPath: ~/zengjf/
  projects: ['M0-project', 'A00-project', 'M8-project', 'L00-project']
  products: ['M0', 'k61v1_64_bsp', 'k62v1_64', 's138']
  kernels: ['kernel-4.9', 'kernel-4.9', 'kernel-4.19', 'android/kernel/msm-4.14']
  bootloaderStage1s: ['vendor/mediatek/proprietary/bootable/bootloader/preloader', 'vendor/mediatek/proprietary/bootable/bootloader/preloader', 'vendor/mediatek/proprietary/bootable/bootloader/preloader', 'android/fibo/bp_code/boot_images']
  bootloaderStage2s: ['vendor/mediatek/proprietary/bootable/bootloader/lk', 'vendor/mediatek/proprietary/bootable/bootloader/lk', 'vendor/mediatek/proprietary/bootable/bootloader/lk', 'android/bootable/bootloader/edk2']
  outs: ['out/target/product', 'out/target/product', 'out/target/product', 'android/out/target/product']
  efuses: ['vendor/mediatek/proprietary/scripts/sign-image_v2', 'vendor/mediatek/proprietary/scripts/sign-image_v2', 'vendor/mediatek/proprietary/scripts/sign-image_v2', 'sc13x_download_images_v2/qcm6125-la-2-0/common/sectools']
  check if source .androiddir.sh path in /home/pi/.bashrc:
  .androiddir.sh path not source in /home/pi/.bashrc
  tail ~/.bashrc last 2 line for terminal check
  ~/.bashrc content
  ...
  # add anpp(https://github.com/ZengjfOS/anpp) function to bash env
  source ~/.androiddir.sh
  ```
* `source ~/.bashrc`

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


# 五、自定义命令

* 以上的命令都是相对通用的命令，如果需要自定义其他的命令，在[custom.sh](custom.sh)中进行处理
* `project_product_custom()`会被传入完整的项目参数，以供所有的数据处理，参数顺序参考[config.json](config.json)中的`project_keys`数组顺序
* 自定义命令依赖project名字调用，例如：`m0 test`命令，调用M0-project的test自定义功能。本质是调用[custom.sh](custom.sh)中`project_product_custom()`，需要自行完成针对参数判断处理
* 支持anppc（android project product custom）直接调用project_product_custom()函数处理

# 六、自定义别名

[config.json](config.json)中的`alias`字段用于自定义shell alias
