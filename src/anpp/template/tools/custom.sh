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

    # echo "argc: $#"
    # echo "argv: $@"

    if [ $1 == "source" ]; then
        echo "source ~/.anpp/.androiddir.sh"
        source ~/.anpp/.androiddir.sh

        return 0
    elif [ $# -eq 1 ] && [ $1 == "vim" ]; then
        touch ~/.vimrc

        vim_anpp_config_start=`grep "ANPP CONFIG START" ~/.vimrc`
        vim_anpp_config_end=`grep "ANPP CONFIG END" ~/.vimrc`
        if [ -z "${vim_anpp_config_start}" ] && [ -z "${vim_anpp_config_end}" ]; then
            cat <<EOF >> ~/.vimrc
" ANPP CONFIG START
filetype on
filetype plugin on
filetype indent on
syntax enable
set hlsearch
hi Search cterm=NONE ctermfg=white ctermbg=black
set tabstop=4
set shiftwidth=4
" ANPP CONFIG END
EOF
        else
            # 1. Using sed to delete all lines between two matching patterns
            #   https://stackoverflow.com/questions/6287755/using-sed-to-delete-all-lines-between-two-matching-patterns
            # sed -i '/" ANPP CONFIG START/,/" ANPP CONFIG END/{{d;};}' ~/.vimrc
            echo "anpp vim configured"
        fi
        return 0

    elif [ $# -eq 1 ] && [ $1 == "tmux" ]; then
        touch ~/.tmux.conf

        tmux_anpp_config_start=`grep "ANPP CONFIG START" ~/.tmux.conf`
        tmux_anpp_config_end=`grep "ANPP CONFIG END" ~/.tmux.conf`
        if [ -z "${tmux_anpp_config_start}" ] && [ -z "${tmux_anpp_config_end}" ]; then
            cat <<EOF >> ~/.tmux.conf
# ANPP CONFIG START
set -g default-terminal "screen-256color"
set -g history-limit 10000

# Use Alt-arrow keys to switch panes
unbind-key j
bind-key j select-pane -D
unbind-key k
bind-key k select-pane -U
unbind-key h
bind-key h select-pane -L
unbind-key l
bind-key l select-pane -R

unbind '"'
bind - splitw -v -c '#{pane_current_path}'
unbind %
bind | splitw -h -c '#{pane_current_path}'
# ANPP CONFIG END
EOF
        else
            # 1. Using sed to delete all lines between two matching patterns
            #   https://stackoverflow.com/questions/6287755/using-sed-to-delete-all-lines-between-two-matching-patterns
            # sed -i '/# ANPP CONFIG START/,/# ANPP CONFIG END/{{d;};}' ~/.tmux.conf
            echo "anpp tmux configured"
        fi
        return 0
    else
        return 1
    fi
}
