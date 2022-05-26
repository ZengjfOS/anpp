# 1. argv: refer to config.json "project_keys" array order except ${1}
#     ${1}: cmd
#     ${2}: defaultPath
#     ${3}: project
#     ${4}: product
#     ${5}: kernel
#     ${6}: dts
#     ${7}: bootloaderStage1
#     ${8}: bootloaderStage2
#     ${9}: out
#     ${10}: efuse
# 2. return:
#     0: function run success
function project_product_custom() {

    echo $@

    if [ $1 == "test" ]; then
        return 0
    else
        return 1
    fi
}
