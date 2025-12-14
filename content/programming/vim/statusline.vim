set laststatus=2

" Empty it out
set statusline=

" Filename
set statusline+=%t\ \|\  

" Modified flag
set statusline+=%m\ \|\  

" Filetype
set statusline+=%y\ \|\  

" Search direction (FWD/BWD)
set statusline+=%{v:searchforward\ ?\ 'FWD'\ :\ 'BWD'}\ \|\  

" Right-align the rest
set statusline+=%=\ \|\  

" Time
set statusline+=%{strftime('%H:%M:%S')}\ \|\  

" Line, column, and percent through file
set statusline+=\[%l:%c\ %p%%\]
