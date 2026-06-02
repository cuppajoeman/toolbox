" Define a Vim function to toggle Goyo
function! ToggleGoyo()
    if exists("g:is_goyo_active") && g:is_goyo_active
        " Run :Goyo!
        exec 'Goyo!'
        let g:is_goyo_active = 0
    else
        " Run :Goyo 120
        exec 'Goyo 120'
        let g:is_goyo_active = 1
    endif
endfunction

" Map the function to a keybinding, e.g., <leader>g
nnoremap <leader>g :call ToggleGoyo()<CR>
