" open files relative to the directory the current file lives in, 'c' refers
" to current dir
map <leader>ce :e <C-R>=expand("%:p:h") . "/" <CR>
map <leader>ct :tabe <C-R>=expand("%:p:h") . "/" <CR>
map <leader>cs :split <C-R>=expand("%:p:h") . "/" <CR>
map <leader>cv :vsplit <C-R>=expand("%:p:h") . "/" <CR>
