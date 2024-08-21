" Function to create a new scratch buffer
function! ScratchBuffer()
  " Create a new buffer
  enew
  " Set the buffer type to 'nofile'
  setlocal buftype=nofile
  " Hide the buffer when it's abandoned
  setlocal bufhidden=hide
  " Optionally, set a name for easy identification
  let b:scratch_name = "Scratch"
  " Set filetype to 'text' or any other type if needed
  setlocal filetype=text
  " Optionally, move the cursor to the beginning
  normal! gg
endfunction

" Command to create a new scratch buffer
command! Scratch call ScratchBuffer()

" Function to delete the current scratch buffer
function! DeleteScratch()
  " Ensure you're in a scratch buffer
  if &buftype ==# 'nofile'
    " Delete the buffer
    bd!
  else
    echo "Not a scratch buffer"
  endif
endfunction

" Command to delete the current scratch buffer
command! DeleteScratchBuffer call DeleteScratch()

" Function to list all scratch buffers
function! ListScratch()
  " Iterate over all buffers
  for buf in range(1, bufnr('$'))
    " Check if buffer is a scratch buffer
    if getbufvar(buf, '&buftype') == 'nofile'
      " Print the buffer number and name
      echo "Buffer " . buf . ": " . bufname(buf)
    endif
  endfor
endfunction

" Command to list all scratch buffers
command! ListScratchBuffers call ListScratch()

" Key mappings for managing scratch buffers
nnoremap <leader>ss :Scratch<CR>  " Create a new scratch buffer
nnoremap <leader>sd :DeleteScratchBuffer<CR>  " Delete the current scratch buffer
nnoremap <leader>sl :ListScratchBuffers<CR>  " List all scratch buffers
