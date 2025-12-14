" Function to open a terminal in the current window
function! OpenTerminalInCurrentWindow()
  " Open a terminal window in the current window
  execute 'terminal ++curwin'
endfunction

" Function to open a terminal in the current file's directory
function! OpenTerminalInCurrentDir()
  " Get the directory of the current file
  let l:dir = expand('%:p:h')
  " Change the working directory to the current file's directory
  execute 'cd ' . l:dir
  " Open a terminal window in the current window
  call OpenTerminalInCurrentWindow()
endfunction

" Function to run ranger in the current window
function! RunRangerInCurrentWindow()
  " Run ranger in the current window
  execute 'terminal ++curwin ranger'
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

" Be able to hide the terminal
noremap <leader>tq <C-w>:hide<CR>

" Open a terminal in the current window
noremap <leader>ter :call OpenTerminalInCurrentWindow()<CR>

" exit terminal mode without breaking your pinky
tnoremap <Esc><Esc> <C-\><C-n>
