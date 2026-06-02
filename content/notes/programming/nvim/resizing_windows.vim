function! ResizeWinHeightByPercentage(percentage)
  let target = &lines * a:percentage / 100
  execute "resize " . target
endfunction

function! ResizeWinWidthByPercentage(percentage)
  let target = &columns * a:percentage / 100
  execute "vertical resize " . target
endfunction

" Vertical resizing (columns)
nnoremap <leader>x1 :call ResizeWinWidthByPercentage(12.5)<CR>
nnoremap <leader>x2 :call ResizeWinWidthByPercentage(25)<CR>
nnoremap <leader>x3 :call ResizeWinWidthByPercentage(37.5)<CR>
nnoremap <leader>x4 :call ResizeWinWidthByPercentage(50)<CR>
nnoremap <leader>x5 :call ResizeWinWidthByPercentage(62.5)<CR>
nnoremap <leader>x7 :call ResizeWinWidthByPercentage(87.5)<CR>
nnoremap <leader>x8 :call ResizeWinWidthByPercentage(100)<CR>

" Horizontal resizing (rows)
nnoremap <leader>y1 :call ResizeWinHeightByPercentage(12.5)<CR>
nnoremap <leader>y2 :call ResizeWinHeightByPercentage(25)<CR>
nnoremap <leader>y3 :call ResizeWinHeightByPercentage(37.5)<CR>
nnoremap <leader>y4 :call ResizeWinHeightByPercentage(50)<CR>
nnoremap <leader>y5 :call ResizeWinHeightByPercentage(62.5)<CR>
nnoremap <leader>y7 :call ResizeWinHeightByPercentage(87.5)<CR>
nnoremap <leader>y8 :call ResizeWinHeightByPercentage(100)<CR>
