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
Plug 'junegunn/vim-peekaboo'
Plug 'jiangmiao/auto-pairs'
Plug 'tpope/vim-fugitive'
Plug 'takac/vim-hardtime'
Plug 'morhetz/gruvbox'
Plug 'vim-airline/vim-airline'
Plug 'SirVer/ultisnips'
Plug 'plasticboy/vim-markdown'
Plug 'tpope/vim-surround'
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

" Goyo for more readable text
    map <leader>g :Goyo \| set linebreak<CR>
    set nocompatible
    set number
    set relativenumber

" Code
	syntax on
	" Verilog
	autocmd BufNewFile,BufRead *.v,*.vs set syntax=verilog

" Hardmode
	let g:hardtime_default_on = 1

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
	colorscheme gruvbox

" See through bg
	hi Normal guibg=NONE ctermbg=NONE

" Bar
	let g:airline_section_b = '%{strftime("%H:%M")}'

" Vimcompletesme selection
	inoremap <expr> <CR> pumvisible() ? "\<C-y>" : "\<C-g>u\<CR>"

" openframeworks compile
	" autocmd  BufRead,BufNewFile  *.cpp let &makeprg = 'if [ -f Makefile ]; then make Release && make RunRelease; else make Release -C .. && make RunRelease -C ..; fi'
" middle of line command
	" map <leader>m :call cursor(0, virtcol('$')/2)<CR>
	map <leader>m :make<CR>
	map <leader>c :! caou %<CR>
	map <leader>r :! rm -v !(*.md)<CR>

	map <leader>M :make \| copen <CR>

" Open bottom terminal
	map <leader>bt :new +resize10 term://bash<CR>

" Help in new tab
	com! -nargs=1 Th :tab h <args> 

" Copy file to clipboard
	let @c = 'gg"*yG'

" Simple copy pasting
	nnoremap <C-y> "+y
	vnoremap <C-y> "+y
	nnoremap <C-p> "+gP
	vnoremap <C-p> "+gP

"  ___               ___   ___         ___  
" |   | |     |   | |       |   |\  | |     
" |-+-  |     |   | | +-    +   | + |  -+-  
" |     |     |   | |   |   |   |  \|     | 
"        ---   ---   ---   ---         ---  
                                          
autocmd FileType vim let b:vcm_tab_complete = 'vim'

"" Vimtex
	let g:vimtex_view_method='zathura'
	let g:tex_flavor = 'latex'
	au BufReadPost *.tex set syntax=tex

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
