" Jai programming tools.

function! s:JaiProgrammingExe()
  let l:root = getcwd()
  let l:candidates = [
        \ l:root . '/src/tbx/programming/programming.exe',
        \ l:root . '/bin/programming.exe',
        \ ]

  for l:candidate in l:candidates
    if executable(l:candidate)
      return l:candidate
    endif
  endfor

  return ''
endfunction

function! s:JaiLocation()
  return expand('%:p') . '@' . line('.') . ':' . col('.')
endfunction

function! JaiGoToDefinition()
  let l:exe = s:JaiProgrammingExe()
  if empty(l:exe)
    echoerr 'Could not find programming.exe at src/tbx/programming/programming.exe or bin/programming.exe.'
    return
  endif

  let l:cmd = shellescape(l:exe) . ' -find_def ' . shellescape(s:JaiLocation()) . ' -dir ' . shellescape(getcwd())
  let l:output = trim(system(l:cmd))

  if v:shell_error != 0 || empty(l:output)
    echoerr l:output
    return
  endif

  let l:lines = split(l:output, "\n")
  let l:target = trim(l:lines[-1])
  let l:match = matchlist(l:target, '^\(.*\)@\([0-9]\+\):\([0-9]\+\)$')
  if empty(l:match)
    echoerr 'Unexpected programming.exe output: ' . l:output
    return
  endif

  execute 'edit +' . l:match[2] . ' ' . fnameescape(l:match[1])
  call cursor(str2nr(l:match[2]), str2nr(l:match[3]))
  normal! zv
endfunction
function! JaiRenameSymbol()
  let l:exe = s:JaiProgrammingExe()
  if empty(l:exe)
    echoerr 'Could not find programming.exe at src/tbx/programming/programming.exe or bin/programming.exe.'
    return
  endif

  let l:old_name = expand('<cword>')
  let l:new_name = input('Rename ' . l:old_name . ' to: ', l:old_name)
  if empty(l:new_name) || l:new_name ==# l:old_name
    return
  endif

  let l:cmd = shellescape(l:exe) . ' -rename ' . shellescape(s:JaiLocation()) . ' ' . shellescape(l:new_name) . ' -dir ' . shellescape(getcwd()) . ' -y'
  let l:output = trim(system(l:cmd))

  if v:shell_error != 0
    echoerr l:output
    return
  endif

  checktime
  echo l:output
endfunction

nnoremap <leader>gd :call JaiGoToDefinition()<CR>
nnoremap <leader>rn :call JaiRenameSymbol()<CR>
