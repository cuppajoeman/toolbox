function! OpenRangerTerminal()
  " Open a new terminal window and run ranger
  :term ranger

  " Get the buffer number of the newly created terminal
  let l:buf = bufnr('%')

  " Set the buffer name to "ranger"
  call setbufvar(l:buf, '&buftype', 'terminal')
  call setbufvar(l:buf, '&filetype', 'ranger')
endfunction

" Map <leader>ran to open ranger in a terminal
nnoremap <leader>ran :call OpenRangerTerminal()<CR>

" start a terminal with a custom buffer name so it can be found easily
command! -nargs=1 NamedTerminal execute 'terminal bash \#' . expand('<args>')
nnoremap <leader>nt :NamedTerminal 


" Function to open a terminal in the current file's directory
function! OpenTerminalInCurrentDir()
  " Get the directory of the current file
  let l:dir = expand('%:p:h')
  " Change the working directory to the current file's directory
  execute 'cd ' . l:dir
  " Open a terminal window in the current window
  execute 'terminal'
endfunction

" Command to open a terminal in the current file's directory
command! TermInDir call OpenTerminalInCurrentDir()

" Key mapping to open a terminal in the current file's directory
nnoremap <leader>td :TermInDir<CR>

" Key mappings for terminal mode
" Get out of Terminal-Mode
tnoremap <leader>t<Esc> <C-\><C-n>
