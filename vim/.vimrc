" Don't try to be vi compatible
set nocompatible

" leader key
let mapleader = " "

" Helps force plugins to load correctly when it is turned back on below
filetype off

" Auto install plug if it doesn't exist
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

"Load plugins here (pathogen or vundle)
call plug#begin('~/.vim/plugged')
Plug 'christoomey/vim-tmux-navigator'
Plug 'lervag/vimtex'
Plug 'SirVer/ultisnips'
Plug 'markonm/traces.vim'
Plug 'tpope/vim-surround'
call plug#end()

" === VIMRC ===
" Open this file easily
map <leader>ve :tabnew ~/.vimrc<CR>
map <leader>vr :source ~/.vimrc<CR>

" Refactor link to plugin after pasting link
map <leader>pr 0vf/;;cPlug 'A'

" === BUFFERS ===

" Quick Buffer list
nnoremap <leader>b :ls<cr>:b<space>


" === GENERAL SETTINGS ===

" Turn on syntax highlighting
syntax on

" Set colorscheme
colorscheme torte

" For plugins to load correctly
filetype plugin indent on

" Replace the word under cursor
nnoremap <Leader>r :%s/\<<C-r><C-w>\>/

" Security
set modelines=0

" Show relative line numbers
set relativenumber

" Show file stats
set ruler

"jump to the last position when reopening a file
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif


" Show bufferlist and prepare input
  nnoremap <leader>b :ls<cr>:b<space>

" Blink cursor on error instead of beeping (grr)
set visualbell

" Fast O
set noesckeys

" Draw a underline current location 
  set cursorline

" Encoding
set encoding=utf-8

" === WHITESPACE === 
" set wrap
" set textwidth=79
" set formatoptions=tcqrn1
filetype plugin indent on
" On pressing tab, insert 2 spaces
set expandtab
" show existing tab with 2 spaces width
set tabstop=2
set softtabstop=2
" when indenting with '>', use 2 spaces width
set shiftwidth=2

" Cursor motion
set scrolloff=3
set backspace=indent,eol,start
set matchpairs+=<:> " use % to jump between pairs
runtime! macros/matchit.vim

" === PERSISTENT UNDO ===
set noswapfile

" Let's save undo info!
if !isdirectory($HOME."/.vim")
  call mkdir($HOME."/.vim", "", 0770)
endif

" All permissions only for me (privacy)
if !isdirectory($HOME."/.vim/undo-dir")
  call mkdir($HOME."/.vim/undo-dir", "", 0700)
endif

set undodir=~/.vim/undo-dir
set undofile

" === MOVEMENT ===
"
" Move up/down editor lines
nnoremap j gj
nnoremap k gk

" Splits open at the bottom and right
set splitbelow
set splitright

" Shortcutting split navigation, saving a keypress:
map <C-h> <C-w>h
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-l> <C-w>l

" Move lines around using the Alt modifier
"The command :m .+1 (which can be abbreviated to :m+) moves the current line to after line number .+1 (current line number + 1). That is, the current line is moved down one line.

"The command :m .-2 (which can be abbreviated to :m-2) moves the current line to after line number .-2 (current line number − 2). That is, the current line is moved up one line.

"After visually selecting some lines, entering :m '>+1 moves the selected lines to after line number '>+1 (one line after the last selected line; '> is a mark assigned by Vim to identify the selection end). That is, the block of selected lines is moved down one line.

The == re-indents the line to suit its new position. For the visual-mode mappings, gv reselects the last visual block and = re-indents that block. 
nnoremap <A-j> :m .+1<CR>==
nnoremap <A-k> :m .-2<CR>==
inoremap <A-j> <Esc>:m .+1<CR>==gi
inoremap <A-k> <Esc>:m .-2<CR>==gi
vnoremap <A-j> :m '>+1<CR>gv=gv
vnoremap <A-k> :m '<-2<CR>gv=gv

" === ABBR. ===
" Don't break your fingers on regex

" Non greedy version of .*
  cmap <c-o> .\{-}
" Operate on visual selection
  cmap <c-v> \%V

" Allow hidden buffers
set hidden

" Rendering
set ttyfast

" Status bar
set laststatus=2

" Last line
set showmode
set showcmd

" Searching
nnoremap / /\v
vnoremap / /\v
set hlsearch
set incsearch
set ignorecase
set smartcase
set showmatch
map <leader><space> :let @/=''<cr> " clear search

" Remap help key.
map <F1> :tab help<CR>

" Open help in a new tab
cabbrev h tab help

" Formatting
map <leader>q gqip

" Visualize tabs and newlines
set listchars=tab:▸\ ,eol:¬
" Uncomment this to enable by default:
" set list " To enable by default
" Or use your leader key + l to toggle on/off
map <leader>l :set list!<CR> " Toggle tabs and EOL

" === CUSTOM TEXT OBJECTS ===

" In Line: entire line sans white-space
xnoremap <silent> il :<c-u>normal! g_v^<cr>
onoremap <silent> il :<c-u>normal! g_v^<cr>

" === CUSTOM BEHAVIOR ===


" Keep cursor in center of page
	augroup VCenterCursor
	  au!
	  au BufEnter,WinEnter,WinNew,VimResized *,*.*
			\ let &scrolloff=winheight(win_getid())/2
	augroup END

" Connected visual split
  command Connvs :vsp|exe "norm! \<c-f>"|setl scrollbind|wincmd p|setl scrollbind

" Insert date
  command Date :put=strftime('%F')

" PLUGINS
" ultisnips
let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<tab>"
let g:UltiSnipsJumpBackwardTrigger="<s-tab>"
" If you want :UltiSnipsEdit to split your window.
let g:UltiSnipsEditSplit="vertical"
let g:UltiSnipsSnippetDirectories=["math-snippets", "programming-snippets"]

map <F2> :tabnew ~/math-snippets/math.snippets<CR>
map <F3> :tabnew ~/math-snippets/<CR>
map <F4> :tabnew ~/programming-snippets/<CR>
map <F5> :tabnew ~/tool-box/<CR>
map <leader>s :call UltiSnips#RefreshSnippets()<CR>

"map <leader>f :vnew \| 0read ! ~/math-snippets/snippet_finder.sh 
map <leader>f :tabnew ~/<CR>

map <leader>h :tab help 

" === MEDIAWIKI ===

" media wiki convert
  map <leader>ltm :!pandoc % -t mediawiki -o output.txt<CR>

