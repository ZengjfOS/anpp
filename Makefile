bashrc_dir := ~/.bashrc
anpp_dir := ~/.anpp
androiddir_file := .androiddir.sh
androiddir_bashrc_lines := 2
androiddir_bashrc := $(shell grep \$(anpp_dir)/$(androiddir_file) $(bashrc_dir))

all: install

check_bashrc:
	@echo check if source $(androiddir_file) path in $(bashrc_dir):
ifeq ($(androiddir_bashrc), )
	@echo $(androiddir_file) path not source in $(bashrc_dir)
	@echo "# add anpp(https://github.com/ZengjfOS/anpp) function to bash env" >> $(bashrc_dir)
	@echo "source $(anpp_dir)/$(androiddir_file)" >> $(bashrc_dir)
	@echo "tail $(bashrc_dir) last $(androiddir_bashrc_lines) line for terminal check"
	@echo "$(bashrc_dir) content"
	@echo "..."
	@tail -n $(androiddir_bashrc_lines) $(bashrc_dir)
	@sync
else
	@echo $(androiddir_file) path already exists in $(bashrc_dir): $(androiddir_bashrc)
endif

template: check_bashrc
	mkdir -p $(anpp_dir)
	cp androiddir.bash.template $(anpp_dir)/$(androiddir_file)

generator:
	mkdir -p $(anpp_dir)
	python3 ./generator.py $(anpp_dir)/$(androiddir_file)

	# for tools
	cp -r tools/* $(anpp_dir)/

install: generator check_bashrc
json: generator check_bashrc

clean:
	rm -rf $(anpp_dir)
	sed -i "/$(androiddir_file)/d" $(bashrc_dir)
	sed -i "/ZengjfOS\/anpp/d" $(bashrc_dir)

