nmap <C-n> :call VToggleNetrw()<CR>
let g:netrw_winsize=20 " set the size of it to take up 20% of the windows width

function! VToggleNetrw()
        let number_open_buffers = bufnr("$") " The result is a Number, which is the highest buffer number
        let netrw_already_open = 0
        while (number_open_buffers >= 1) 
            if (getbufvar(i, "&filetype") == "netrw") " check to see if the buffer's filetype is netrw
                silent exe "bwipeout " . i
                let netrw_already_open = 1
            endif
            let number_open_buffers -= 1
        endwhile
    if !netrw_already_open " if not already open
        silent Vexplore "then launch it
    endif
endfunction
