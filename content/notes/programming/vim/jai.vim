" Jai programming tools.

let s:server_job = 0
let s:server_channel = 0
let s:server_root = ''
let s:server_exe = ''
let s:project_root = ''

function! s:NormalizePath(path) abort
  return substitute(fnamemodify(a:path, ':p'), '\\', '/', 'g')
endfunction

function! s:JaiProjectRoot() abort
  let l:starts = [expand('%:p:h'), getcwd()]
  for l:start in l:starts
    if empty(l:start)
      continue
    endif

    let l:programming_dir = finddir('src/tbx/programming', l:start . ';')
    if !empty(l:programming_dir)
      let l:programming_dir = s:NormalizePath(l:programming_dir)
      let s:project_root = s:NormalizePath(fnamemodify(l:programming_dir . '/../../..', ':p'))
      return s:project_root
    endif
  endfor

  if !empty(s:server_root)
    return s:server_root
  endif

  if !empty(s:project_root)
    return s:project_root
  endif

  return ''
endfunction

function! s:JaiProgrammingExe(root) abort
  if empty(a:root)
    return ''
  endif

  let l:candidates = [
        \ a:root . '/src/tbx/programming/programming.exe',
        \ ]

  for l:candidate in l:candidates
    if executable(l:candidate)
      return l:candidate
    endif
  endfor

  return ''
endfunction

function! s:JaiLocation() abort
  return s:NormalizePath(expand('%:p')) . '@' . line('.') . ':' . col('.')
endfunction

function! s:JaiServerRunning() abort
  return s:server_job isnot 0 && job_status(s:server_job) ==# 'run'
endfunction

function! s:JaiStopServer() abort
  if s:JaiServerRunning()
    try
      call ch_sendraw(s:server_channel, "quit\n")
      call ch_read(s:server_channel, {'timeout': 500})
    catch
    endtry
    try
      call job_stop(s:server_job)
    catch
    endtry
  endif

  let s:server_job = 0
  let s:server_channel = 0
  let s:server_root = ''
  let s:server_exe = ''
endfunction

function! s:JaiMaybeStartServer() abort
  if !has('job') || !has('channel')
    return 0
  endif

  let l:root = s:JaiProjectRoot()
  if empty(l:root)
    return 0
  endif

  let l:exe = s:JaiProgrammingExe(l:root)
  if empty(l:exe)
    return 0
  endif

  if s:JaiServerRunning() && s:server_root ==# l:root && s:server_exe ==# l:exe
    return 1
  endif

  call s:JaiStopServer()

  let l:job = job_start([l:exe, 'server', '-dir', l:root], {
        \ 'in_io': 'pipe',
        \ 'out_io': 'pipe',
        \ 'err_io': 'pipe',
        \ 'cwd': l:root,
        \ })
  if l:job is 0 || l:job is -1
    return 0
  endif

  let l:channel = job_getchannel(l:job)
  call ch_setoptions(l:channel, {'mode': 'nl', 'timeout': 5000})

  let l:ready = ch_read(l:channel)
  if l:ready !~# '^ready,'
    try
      call job_stop(l:job)
    catch
    endtry
    return 0
  endif

  let s:server_job = l:job
  let s:server_channel = l:channel
  let s:server_root = l:root
  let s:server_exe = l:exe
  return 1
endfunction

function! s:JaiServerRequest(command) abort
  if !s:JaiMaybeStartServer()
    return ''
  endif

  try
    call ch_sendraw(s:server_channel, a:command . "\n")
    let l:response = ch_read(s:server_channel, {'timeout': 5000})
    if l:response =~# '^error,request_file_not_found'
      call s:JaiStopServer()
      if s:JaiMaybeStartServer()
        call ch_sendraw(s:server_channel, a:command . "\n")
        let l:response = ch_read(s:server_channel, {'timeout': 5000})
      endif
    endif
    return l:response
  catch
    call s:JaiStopServer()
    return ''
  endtry
endfunction

function! s:JaiOneShot(command, ...) abort
  let l:root = s:JaiProjectRoot()
  let l:exe = s:JaiProgrammingExe(l:root)
  if empty(l:exe)
    echoerr 'Could not find src/tbx/programming/programming.exe for this Jai project.'
    return ''
  endif

  let l:cmd = shellescape(l:exe) . ' ' . a:command . ' ' . shellescape(s:JaiLocation())
  for l:arg in a:000
    let l:cmd .= ' ' . shellescape(l:arg)
  endfor
  let l:cmd .= ' -dir ' . shellescape(l:root)

  return trim(system(l:cmd))
endfunction

function! s:JaiParseDefinition(response) abort
  let l:response = trim(a:response)
  if l:response =~# '^ok,definition,'
    let l:target = substitute(l:response, '^ok,definition,', '', '')
    let l:target = substitute(l:target, ',ms=.*$', '', '')
  else
    let l:lines = split(l:response, "\n")
    let l:target = trim(l:lines[-1])
  endif

  return matchlist(l:target, '^\(.*\)@\([0-9]\+\):\([0-9]\+\)$')
endfunction

function! s:JaiResponseValue(response, key) abort
  let l:match = matchlist(a:response, a:key . '=\([0-9]\+\)')
  if empty(l:match)
    return 0
  endif
  return str2nr(l:match[1])
endfunction

function! JaiGoToDefinition() abort
  let l:response = s:JaiServerRequest('definition ' . s:JaiLocation())
  if empty(l:response)
    let l:response = s:JaiOneShot('-find_def')
  endif

  if l:response =~# '^ok,no_definition,'
    echo l:response
    return
  endif

  if empty(l:response) || l:response =~# '^error,'
    echoerr empty(l:response) ? 'Jai definition lookup failed.' : l:response
    return
  endif

  let l:match = s:JaiParseDefinition(l:response)
  if empty(l:match)
    echoerr 'Unexpected Jai programming output: ' . l:response
    return
  endif

  execute 'edit +' . l:match[2] . ' ' . fnameescape(l:match[1])
  call cursor(str2nr(l:match[2]), str2nr(l:match[3]))
  normal! zv
endfunction

function! JaiRenameSymbol() abort
  let l:old_name = expand('<cword>')
  let l:new_name = input('Rename ' . l:old_name . ' to: ', l:old_name)
  if empty(l:new_name) || l:new_name ==# l:old_name
    return
  endif

  let l:location = s:JaiLocation()
  let l:preview = s:JaiServerRequest('rename_preview ' . l:location . ' ' . l:new_name)
  let l:allow_modules = 0

  if !empty(l:preview) && l:preview =~# '^ok,rename_preview,'
    let l:module_edits = s:JaiResponseValue(l:preview, 'module_edits')
    if l:module_edits > 0
      let l:choice = confirm('Rename touches ' . l:module_edits . ' occurrence(s) in Jai modules. Apply anyway?', "&No\n&Yes", 1)
      if l:choice != 2
        echo l:preview
        return
      endif
      let l:allow_modules = 1
    endif
  endif

  let l:root = s:JaiProjectRoot()
  let l:exe = s:JaiProgrammingExe(l:root)
  if empty(l:exe)
    echoerr 'Could not find src/tbx/programming/programming.exe for this Jai project.'
    return
  endif

  let l:cmd = shellescape(l:exe) . ' -rename ' . shellescape(l:location) . ' ' . shellescape(l:new_name) . ' -dir ' . shellescape(l:root) . ' -y'
  if l:allow_modules
    let l:cmd .= ' -allow_jai_modules_rename'
  endif

  let l:output = trim(system(l:cmd))
  if v:shell_error != 0
    echoerr l:output
    return
  endif

  checktime
  echo l:output
endfunction

augroup jai_programming_tools
  autocmd!
  autocmd VimLeavePre * call s:JaiStopServer()
augroup END

command! JaiRestartServer call s:JaiStopServer() | call s:JaiMaybeStartServer()
command! JaiServerStatus echo 'root=' . s:server_root . ' exe=' . s:server_exe . ' running=' . s:JaiServerRunning()

nnoremap <leader>gd :call JaiGoToDefinition()<CR>
nnoremap <leader>rn :call JaiRenameSymbol()<CR>


