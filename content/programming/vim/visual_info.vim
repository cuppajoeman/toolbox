syntax on

" enable filetype plugins and indentation
filetype plugin indent on

color habamax
set number
set relativenumber
set showcmd
set showmatch

" highlight current line
set cursorline
hi CursorLine cterm=NONE ctermbg=236 ctermfg=NONE guibg=#3c3836

" highlight current column
set cursorcolumn
" Optional: customize color
hi CursorColumn cterm=NONE ctermbg=236 ctermfg=NONE guibg=#3c3836

" faster redrawing
set ttyfast

" show line/column number in status bar
set ruler
