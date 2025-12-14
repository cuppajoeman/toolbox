function! FuzzyFindBuffer()
  " Get all listed buffers
  let l:buffers = filter(range(1, bufnr('$')), 'buflisted(v:val)')
  let l:names = map(l:buffers, 'bufname(v:val) == "" ? "[No Name]" : bufname(v:val)')

  if empty(l:names)
    echo "No open buffers."
    return
  endif

  " Ask user for query
  let l:query = input("Search for buffer: ")

  " Filter matches
  let l:matches = filter(copy(l:names), 'v:val =~ l:query')

  if len(l:matches) == 1
    " Jump directly if only one match
    let l:idx = index(l:names, l:matches[0])
    execute 'buffer ' . l:buffers[l:idx]
    return
  elseif len(l:matches) > 1
    " Show numbered list for selection
    echo "Matching buffers:"
    for i in range(len(l:matches))
      echo i . ": " . l:matches[i]
    endfor
    let l:choice = input("Select buffer number: ")
    if l:choice =~ '^\d\+$' && l:choice < len(l:matches)
      let l:idx = index(l:names, l:matches[l:choice])
      execute 'buffer ' . l:buffers[l:idx]
    endif
  else
    echo "No matching buffers."
  endif
endfunction

nnoremap <leader><leader> :call FuzzyFindBuffer()<CR>

 

" by default vim doesn't let you switch buffers when there are unsaved
" changes, which is a problem because sometimes we're half way through a
" change and want to go to a new file for a second to cross reference
" something but vim won't let us do that so we turn on hidden
set hidden
