" Function to handle auto-completion in insert mode
function! Auto_complete_string()
    " Check if the popup menu (completion suggestions) is currently visible
    if pumvisible()
        " If the popup menu is visible, use Ctrl-n to select the next item in the list
        return "\<C-n>"
    else
        " If the popup menu is not visible, initiate auto-completion with
        " Ctrl-x Ctrl-o and evaluate the result of Auto_complete_opened()
        " Insert the result of the expression into the command line
        return "\<C-x>\<C-o>\<C-r>=Auto_complete_opened()\<CR>"
    end
endfunction

" Function to determine if the completion popup menu is opened
function! Auto_complete_opened()
    " Check if the popup menu (completion suggestions) is currently visible
    if pumvisible()
        " If the popup menu is visible, return the Down arrow key sequence
        " This moves the selection down in the completion menu
        return "\<Down>"
    end
    " If the popup menu is not visible, return an empty string
    return ""
endfunction

" Not sure what this does, hopefully someone can figure it out
inoremap <expr> <Nul> Auto_complete_string()

" Map the <C-Space> key in insert mode to use the Auto_complete_string function
" This allows the <C-Space> key to handle completion based on the visibility of the popup menu
inoremap <expr> <C-Space> Auto_complete_string()
