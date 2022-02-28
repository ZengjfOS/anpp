# README

在多个Android项目自由跳转脚本，包含自动补全

## install

make install

## clean

make clean

## 使用方法

* `pp <tab><tab>`
  ```
  a800   l1400  m50    m8
  ```
  * list project
* `pp m50 <tab><tab>`
  ```
  android  bs1      bs2      dts      kernel   out
  ```
  * list component
* `m50 <tab><tab>`
  ```
  android  bs1      bs2      dts      kernel   out
  ```
  * list component

## 配置方法

* 修改androiddir.bash中如下数组
  * projects
    * 项目代码
  * products
    * 产品名称
  * kernels
    * 内核目录
  * dtss
    * 设备树目录
  * bootloaderStage1s
    * 第一阶段bootloader
  * bootloaderStage2s
    * 第二阶段bootloader
  * outs
    * out目录
  * components
    * 组件名称

