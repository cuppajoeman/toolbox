" syntax on

" enable filetype plugins and indentation
filetype plugin indent on

set list
set listchars=tab:»\ ,extends:›,precedes:‹,nbsp:·,trail:·
" tab:»\     - Display tabs as '»' followed by a space
" extends:›  - Show '›' in the last column when a line extends beyond the right of the screen (when 'wrap' is off)
" precedes:‹ - Show '‹' in the first column when a line extends beyond the left of the screen (when 'wrap' is off)
" nbsp:·     - Display non-breakable space characters as '·' (Unicode U+00A0).
"              These are invisible characters that look like regular spaces but
"              can cause subtle bugs in code, config files, and string comparisons.
"              Commonly introduced by copying text from web pages or Word documents,
"              or by accidentally pressing Option+Space on macOS.
" trail:·    - Display trailing whitespace (spaces/tabs at the end of a line) as '·'


" removing all of this
" c - autowrap, r - autoinsert, o - comment leader
autocmd FileType * setlocal formatoptions-=cro

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

set scrolloff=999
