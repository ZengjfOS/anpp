#!/bin/python3

import json
import sys

if len(sys.argv) != 2:
	out_file_path = "androiddir.bash"
else:
	out_file_path = sys.argv[1]

# get config
config_file = open('config.json')
config = json.load(config_file)
config_file.close()

## get data
defaultPath = config["defaultPath"]
projects=[]
products=[]
kernels=[]
dtss=[]
bootloaderStage1s=[]
bootloaderStage2s=[]
outs=[]
efuses=[]
for project in config["projects"]:
	projects.append(project["project"])
	products.append(project["product"])
	kernels.append(project["kernel"])
	dtss.append(project["dts"])
	bootloaderStage1s.append(project["bootloaderStage1s"])
	bootloaderStage2s.append(project["bootloaderStage2s"])
	outs.append(project["out"])
	efuses.append(project["efuse"])

## show data
print("defaultPath: " + defaultPath)
print("projects: " + str(projects))
print("products: " + str(products))
print("kernels: " + str(kernels))
print("bootloaderStage1s: " + str(bootloaderStage1s))
print("bootloaderStage2s: " + str(bootloaderStage2s))
print("outs: " + str(outs))
print("efuses: " + str(efuses))

## generator file
anpp_config_start = "##### ANPP CONFIG START #####"
anpp_config_end = "##### ANPP CONFIG END #####"
anpp_template_skip_line = False
with open(out_file_path, 'w', encoding = 'utf-8') as f_out:
	with open("androiddir.bash.template", 'r', encoding = 'utf-8') as f_in:
		for line in f_in:
			if line.strip() == anpp_config_start:
				anpp_template_skip_line = True
				f_out.write(line)

				f_out.write("# default Workspace dir, all projects are here\n")
				f_out.write("export defaultPath=" + defaultPath + "\n")
				f_out.write("\n")

				f_out.write("# android project\n")
				f_out.write("projects=(\n")
				for project in projects:
					f_out.write("    " + project + "\n")
				f_out.write(")\n")
				f_out.write("\n")

				f_out.write("# android product\n")
				f_out.write("products=(\n")
				for product in products:
					f_out.write("    " + product + "\n")
				f_out.write(")\n")
				f_out.write("\n")

				f_out.write("# android product kernel dir name, relative to project dir\n")
				f_out.write("kernels=(\n")
				for kernel in kernels:
					f_out.write("    " + kernel + "\n")
				f_out.write(")\n")
				f_out.write("\n")

				f_out.write("# android product kernel dts dir name\n")
				f_out.write("dtss=(\n")
				for dts in dtss:
					f_out.write("    " + dts + "\n")
				f_out.write(")\n")
				f_out.write("\n")

				f_out.write("# android product bootloader stage 1th dir name, relative to project dir\n")
				f_out.write("#   1. mtk: preloader\n")
				f_out.write("#   2. qcom: xbl\n")
				f_out.write("bootloaderStage1s=(\n")
				for bs1 in bootloaderStage1s:
					f_out.write("    " + bs1 + "\n")
				f_out.write(")\n")
				f_out.write("\n")

				f_out.write("# android product bootloader stage 2th dir name, relative to project dir\n")
				f_out.write("#   1. mtk: lk\n")
				f_out.write("#   2. qcom: edk2\n")
				f_out.write("bootloaderStage2s=(\n")
				for bs2 in bootloaderStage2s:
					f_out.write("    " + bs2 + "\n")
				f_out.write(")\n")
				f_out.write("\n")

				f_out.write("# android product out dir, relative to project dir\n")
				f_out.write("outs=(\n")
				for out in outs:
					f_out.write("    " + out + "\n")
				f_out.write(")\n")
				f_out.write("\n")

				f_out.write("# efuse sign dir, relative to project dir\n")
				f_out.write("efuses=(\n")
				for efuse in efuses:
					f_out.write("    " + efuse + "\n")
				f_out.write(")\n")
				f_out.write("\n")

			elif line.strip() == anpp_config_end:
				anpp_template_skip_line = False

			if not anpp_template_skip_line:
				f_out.write(line)
