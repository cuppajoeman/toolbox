set termwinsize=10x0  

" open a terminal at the current file location
map <F6> :let $VIM_DIR=expand('%:p:h')<CR>:terminal<CR>cd $VIM_DIR<CR>clear<CR>
