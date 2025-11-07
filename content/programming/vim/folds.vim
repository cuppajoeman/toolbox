" Use marker-based folding
set foldmethod=marker
set foldmarker=startfold,endfold

" Function to create a fold with comment markers
function! CreateFoldMarkers()
  " Get the commentstring and extract the comment leader (e.g. //, #, --, etc.)
  let l:comment = matchstr(&commentstring, '^\zs.*\ze%s')
  if empty(l:comment)
    let l:comment = '// ' " fallback if commentstring is missing
  endif

  " Get the current line number (cursor position)
  let l:row = line('.')

  " Insert startfold and endfold markers below the current line
  call append(l:row - 1, l:comment . 'startfold')
  call append(l:row, l:comment . 'endfold')

  " Move cursor between them and go into insert mode at the end of the line
  call cursor(l:row + 1, 1)
  normal! A
endfunction

" Map <leader>cf to create the fold markers
nnoremap <silent> <leader>cf :call CreateFoldMarkers()<CR>
