"                                  _
"  _______  ______  ____  ____ _  (_)___  ___  ____ ___  ____ _____
" / ___/ / / / __ \/ __ \/ __ `/ / / __ \/ _ \/ __ `__ \/ __ `/ __ \
"/ /__/ /_/ / /_/ / /_/ / /_/ / / / /_/ /  __/ / / / / / /_/ / / / /
"\___/\__,_/ .___/ .___/\__,_/_/ /\____/\___/_/ /_/ /_/\__,_/_/ /_/
"         /_/   /_/         /___/

" Automatic vim-plug installation
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif


" Plugins
call plug#begin('~/.vim/plugged')
Plug 'junegunn/goyo.vim'
Plug 'SirVer/ultisnips'
Plug 'haya14busa/incsearch.vim'
Plug 'lervag/vimtex'
call plug#end()


".▄▄ · ▄▄▄ .▄▄▄▄▄▄▄▄▄▄▪   ▐ ▄  ▄▄ • .▄▄ ·
"▐█ ▀. ▀▄.▀·•██  •██  ██ •█▌▐█▐█ ▀ ▪▐█ ▀.
"▄▀▀▀█▄▐▀▀▪▄ ▐█.▪ ▐█.▪▐█·▐█▐▐▌▄█ ▀█▄▄▀▀▀█▄
"▐█▄▪▐█▐█▄▄▌ ▐█▌· ▐█▌·▐█▌██▐█▌▐█▄▪▐█▐█▄▪▐█
" ▀▀▀▀  ▀▀▀  ▀▀▀  ▀▀▀ ▀▀▀▀▀ █▪·▀▀▀▀  ▀▀▀▀

" Leader
	let mapleader =" "

" Enable autocompletion:
	set wildmode=longest,list,full

" Disables automatic commenting on newline:
	autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o

" Open this file easily
    map <leader>ve :vs ~/.vimrc<CR>
    map <leader>vr :source ~/.vimrc<CR>

" Code
	syntax on
	" Verilog
	autocmd BufNewFile,BufRead *.v,*.vs set syntax=verilog

" Persistent Undo
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

" Splits open at the bottom and right
    set splitbelow
    set splitright

" Shortcutting split navigation, saving a keypress:
    map <C-h> <C-w>h
    map <C-j> <C-w>j
    map <C-k> <C-w>k
    map <C-l> <C-w>l

" Search settings
    set incsearch
    set nowrapscan

" Indentataion
    set autoindent
    " size of a hard tabstop
    set tabstop=4

    " size of an "indent"
    set shiftwidth=4

" colorscheme 
	" colorscheme wal
	set background=dark

" Vimcompletesme selection
	inoremap <expr> <CR> pumvisible() ? "\<C-y>" : "\<C-g>u\<CR>"

" Copy file to clipboard
	let @c = 'gg"+yG'

" Simple copy pasting
	nnoremap <C-y> "+y
	vnoremap <C-y> "+y
	nnoremap <C-p> "+gP
	vnoremap <C-p> "+gP

" Keep cursor in center of page
	augroup VCenterCursor
	  au!
	  au BufEnter,WinEnter,WinNew,VimResized *,*.*
			\ let &scrolloff=winheight(win_getid())/2
	augroup END

" Open help in a new tab
	cabbrev help tab help

"  ___               ___   ___         ___  
" |   | |     |   | |       |   |\  | |     
" |-+-  |     |   | | +-    +   | + |  -+-  
" |     |     |   | |   |   |   |  \|     | 
"        ---   ---   ---   ---         ---  

" Goyo for more readable text
    map <leader>g :Goyo \| set linebreak<CR>
    set nocompatible
    set number
    set relativenumber
                                          
"" Vimtex
	let g:vimtex_view_method='zathura'
	let g:tex_flavor = 'latex'
	au BufReadPost *.tex set syntax=tex
	map <leader>ims /\$.\{-}\$<CR>

"" Ultisnips

	map <F2> :sp ~/.vim/LocalSnippets/words.snippets<CR>
	map <F3> :sp ~/.vim/LocalSnippets/tex.snippets<CR>
	map <F4> :sp ~/.vim/LocalSnippets/math.snippets<CR>

" Trigger configuration. Do not use <tab> if you use https://github.com/Valloric/YouCompleteMe.
	let g:UltiSnipsExpandTrigger="<tab>"
	let g:UltiSnipsJumpForwardTrigger="<tab>"
	let g:UltiSnipsJumpBackwardTrigger="<s-tab>"
	let g:UltiSnipsSnippetDirectories=[$HOME.'/.vim/LocalSnippets']
	filetype plugin indent on

" Inc search
	map /  <Plug>(incsearch-forward)
	map ?  <Plug>(incsearch-backward)
	set hlsearch
	let g:incsearch#auto_nohlsearch = 1
	map n  <Plug>(incsearch-nohl-n)
	map N  <Plug>(incsearch-nohl-N)
	map *  <Plug>(incsearch-nohl-*)
	map #  <Plug>(incsearch-nohl-#)
	map g* <Plug>(incsearch-nohl-g*)
	map g# <Plug>(incsearch-nohl-g#)map g/ <Plug>(incsearch-stay)

