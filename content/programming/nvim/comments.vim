nnoremap <C-_> :s/^\(.*\)/\/\/ \1/<CR>:noh<CR>
" no auto commenting
autocmd FileType * set formatoptions-=cro
