" Turn on syntax highlighting
syntax on

" Don't indent when pasting
set copyindent
set pastetoggle=<F2>

" Please...
set belloff=all

" Set colorscheme
set termguicolors
" colorscheme blue-moon

" Keep cursor in center of page
	augroup VCenterCursor
	  au!
	  au BufEnter,WinEnter,WinNew,VimResized *,*.*
			\ let &scrolloff=winheight(win_getid())/2
	augroup END

" Return to last edit position when opening files (You want this!)
autocmd BufReadPost *
     \ if line("'\"") > 0 && line("'\"") <= line("$") |
     \   exe "normal! g`\"" |
     \ endif

" Folding
set foldmethod=indent   
set foldnestmax=10
set nofoldenable
set foldlevel=2


" For plugins to load correctly
filetype plugin indent on

" Security
set modelines=0

" Show relative line numbers
set relativenumber

" Show file stats
set ruler

" Blink cursor on error instead of beeping (grr)
set visualbell

" Draw a underline current location 
set cursorline
set cursorcolumn

highlight CursorColumn guibg=#292d3e

" Encoding
set encoding=utf-8

" === WHITESPACE === 
" set wrap
" set textwidth=79
" set formatoptions=tcqrn1
filetype plugin indent on
" On pressing tab, insert 2 spaces
" set expandtab
" " show existing tab with 2 spaces width
" set tabstop=2
" set softtabstop=2
" " when indenting with '>', use 2 spaces width
" set shiftwidth=2

" Cursor motion
set scrolloff=3
set backspace=indent,eol,start
set matchpairs+=<:> " use % to jump between pairs

" === PERSISTENT UNDO ===
set noswapfile

" Let's save undo info!
if !isdirectory($HOME."/.config/nvim")
  call mkdir($HOME."/.config/nvim", "", 0770)
endif

" All permissions only for me (privacy)
if !isdirectory($HOME."/.config/nvim/undo-dir")
  call mkdir($HOME."/.config/nvim/undo-dir", "", 0700)
endif

" === PERSISTENT UNDO ===
set noswapfile

" Let's save undo info!
if !isdirectory($HOME."/.config/nvim")
  call mkdir($HOME."/.config/nvim", "", 0770)
endif

" All permissions only for me (privacy)
if !isdirectory($HOME."/.config/nvim/undo-dir")
  call mkdir($HOME."/.config/nvim/undo-dir", "", 0700)
endif

set undodir=~/.config/nvim/undo-dir
set undofile

" Splits open at the bottom and right
set splitbelow
set splitright

" Enable very magic by default
nnoremap / /\v
vnoremap / /\v
cnoremap %s/ %smagic/
cnoremap \>s/ \>smagic/
nnoremap :g/ :g/\v
nnoremap :g// :g//

set hlsearch
set incsearch
set ignorecase
set smartcase
set showmatch
