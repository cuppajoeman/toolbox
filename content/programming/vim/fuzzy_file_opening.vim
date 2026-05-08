function! FuzzyFindFile()
  " Directories to ignore
  let l:ignore_dirs = ['.git', 'build']

  " File patterns to ignore (swap files, etc.)
  let l:ignore_files = ['*.swp', '*.swo', '*.swn', '*~', '*.o', '*.obj']

  " Build the prune expression for directories
  let l:prune_expr = join(map(copy(l:ignore_dirs), "'-name ' . v:val . ' -prune'"), " -o ")

  " Build the ignore expression for files
  let l:ignore_expr = join(map(copy(l:ignore_files), "'! -name ' . shellescape(v:val)"), " ")

  " Full find command
  let l:cmd = 'find . \( ' . l:prune_expr . ' \) -o -type f ' . l:ignore_expr . ' -print'

  " Run the command
  let l:files = split(system(l:cmd), "\n")
  
  " Strip leading ./
  let l:files = map(l:files, 'substitute(v:val, "^\\./", "", "")')

  let l:query = input("Search for file: ")
  if empty(l:query)
    return
  endif

  " Filter matches (case-insensitive)
  let l:matches = filter(l:files, 'v:val =~? l:query')

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
    if l:choice =~ '^\d\+$' && str2nr(l:choice) < len(l:matches)
      execute 'edit' fnameescape(l:matches[str2nr(l:choice)])
    else
      echo "\nInvalid selection."
    endif
  else
    echo "No matching files."
  endif
endfunction

nnoremap <leader>sf :call FuzzyFindFile()<CR>
