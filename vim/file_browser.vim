nmap <C-n> :call VToggleNetrw()<CR>
let g:netrw_winsize=20 " set the size of it to take up 20% of the windows width
let g:netrw_banner = 0 " hide the text at the top
let g:netrw_liststyle = 3 " tree style listings

function! VToggleNetrw()
        let n = bufnr("$") " The result is a Number, which is the highest buffer number
        let netrw_already_open = 0
        while (n >= 1) 
            if (getbufvar(n, "&filetype") == "netrw") " check to see if the buffer's filetype is netrw
                silent exe "bwipeout " . n
                let netrw_already_open = 1
            endif
            let n -= 1
        endwhile
    if !netrw_already_open " if not already open
        silent Lexplore "then launch it
    endif
endfunction
