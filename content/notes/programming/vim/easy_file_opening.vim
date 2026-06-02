" open files relative to the directory the current file lives in, 'c' refers
" to current dir
map <leader>ce :e <C-R>=fnamemodify(expand("%:p:h"), ":~:.") . "/" <CR>
map <leader>ct :tabe <C-R>=fnamemodify(expand("%:p:h"), ":~:.") . "/" <CR>
map <leader>cs :split <C-R>=fnamemodify(expand("%:p:h"), ":~:.") . "/" <CR>
map <leader>cv :vsplit <C-R>=fnamemodify(expand("%:p:h"), ":~:.") . "/" <CR>
