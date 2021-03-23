#!/bin/bash

# 默认Workspace目录，所有的project存放的目录
export defaultPath=~/zengjf/
projects=(
    M50-project
    A800-project
    MTK6762D-project
)
products=(
    M50
    k61v1_64_bsp_pax
    k62v1_64_pax
)
kernels=(
    kernel-4.9
    kernel-4.9
    kernel-4.19
)

function project_product() {
    project=
    product=
    kernel=
    currentpath=`pwd`

    # 支持直接命令行输入命令进行跳转
    if [ $# -lt 1 ]; then
        for i in "${!projects[@]}"
        do
            echo $i: ${projects[i]} -- ${products[i]} -- ${kernels[i]}
        done
        echo
        cd $defaultPath
    elif [ $1 == "workspace" ]; then
        cd $defaultPath
    else

        # 直接跳转到项目目录
        for i in "${!projects[@]}"
        do
            project_lowercase=${projects[i]%%-*}
            project_lowercase=${project_lowercase,,}
            if [ ${1,,} == "${project_lowercase}" ]; then
                project=${projects[i]}
                product=${products[i]}

                cd ${defaultPath}/${projects[i]}

                pwd
                return
            fi
        done

        # 依赖当前所处的项目目录进行跳转
        for i in "${!projects[@]}"
        do
            if [[ ${currentpath} =~ "${projects[i]}" ]]; then
                project=${projects[i]}
                product=${products[i]}
                kernel=${kernels[i]}

                if [ $1 == "android" ]; then
                    cd ${defaultPath}/${project}
                elif [ $1 == "kernel" ]; then
                    cd ${defaultPath}/${project}/${kernel}
                elif [ $1 == "dts" ]; then
                    cd ${defaultPath}/${project}/${kernel}/arch/arm64/boot/dts/mediatek/
                elif [ $1 == "lk" ]; then
                    cd ${defaultPath}/${project}/vendor/mediatek/proprietary/bootable/bootloader/lk
                elif [ $1 == "pl" ]; then
                    cd ${defaultPath}/${project}/vendor/mediatek/proprietary/bootable/bootloader/preloader

                elif [ $1 == "out" ]; then
                    cd ${defaultPath}/${project}/out/target/product/${product}
                fi

                break
            fi
        done

        if [ "${project}" == "" ]; then
            echo "please jump to your android project at first"
            cd ${defaultPath}
        fi
    fi

    pwd
}

alias android="project_product android"
alias dts="project_product dts"
alias kernel="project_product kernel"
alias out="project_product out"
alias device="project_product device"
alias lk="project_product lk"
alias pl="project_product pl"
alias workspace="project_product workspace"
alias a800="project_product a800"
alias m50="project_product m50"
alias m8="project_product mtk6762d"
alias pd="project_product"
alias log="cd ~/log"

