" Function to open a terminal in the current window
function! OpenTerminal()
  " Open a terminal window in the current window
  execute 'terminal'
endfunction

" Function to open a terminal in the current file's directory
function! OpenTerminalInCurrentDir()
  " Get the directory of the current file
  let l:dir = expand('%:p:h')
  " Change the working directory to the current file's directory
  execute 'cd ' . l:dir
  " Open a terminal window in the current window
  call OpenTerminal()
endfunction

" Function to run ranger in the current window
function! RunRangerInCurrentWindow()
  " Run ranger in the current window
  execute 'terminal ranger'
endfunction

" Command to open a terminal in the current file's directory
command! TermInDir call OpenTerminalInCurrentDir()

" Command to run ranger in the current window
command! TDR call RunRangerInCurrentWindow()

" Key mappings
" Key mapping to open a terminal in the current file's directory
nnoremap <leader>td :TermInDir<CR>

" Key mapping to run ranger in the current window
nnoremap <leader>tr :TDR<CR>

" Key mappings for terminal mode
" Get out of Terminal-Mode
tnoremap <leader>t<Esc> <C-\><C-n>
