map <leader>g :Goyo <CR>

" Quitting whether Goyo is active or not
ca wq :w<cr>:call Quit()<cr>
ca q :call Quit()<cr>
function! Quit()
    if winnr('$') > 3
        Goyo
    endif
    quit
endfunction
