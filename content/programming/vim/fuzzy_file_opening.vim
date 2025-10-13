function! FuzzyFindFile()
  " Directories to ignore
  let l:ignore_dirs = ['.git', 'build']

  " Build the prune expression dynamically
  let l:prune_expr = join(map(l:ignore_dirs, "'-name ' . v:val . ' -prune'"), " -o ")

  " Full find command
  let l:cmd = 'find . \( ' . l:prune_expr . ' \) -o -type f -print'

  " Run the command
  let l:files = split(system(l:cmd), "\n")

  let l:query = input("Search for file: ")

  " Filter matches
  let l:matches = filter(l:files, 'v:val =~ l:query')

  " If only one match, open it
  if len(l:matches) == 1
    execute 'edit' fnameescape(l:matches[0])
    return
  endif

  " Let user select one from matches
  if len(l:matches) > 1
    echo "Matching files:"
    for i in range(len(l:matches))
      echo i . ": " . l:matches[i]
    endfor
    let l:choice = input("Select file number: ")
    if l:choice =~ '^\d\+$' && l:choice < len(l:matches)
      execute 'edit' fnameescape(l:matches[l:choice])
    endif
  else
    echo "No matching files."
  endif
endfunction

nnoremap <leader>f :call FuzzyFindFile()<CR>
