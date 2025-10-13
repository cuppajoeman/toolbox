map <leader>w :w!<CR> "write to file quickly
map <leader>ve :e $MYVIMRC<CR>
map <leader>vs :source $MYVIMRC<CR>

function! SwitchExtension(newext)
  let l:filename = expand("%:r") . "." . a:newext
  execute "edit " . l:filename
endfunction

" TODO: I want this to be moved to cpp specific configuration file eventually
nnoremap <leader>hh :call SwitchExtension("hpp")<CR>
nnoremap <leader>cc :call SwitchExtension("cpp")<CR>
