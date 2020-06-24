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
Plug 'morhetz/gruvbox'
Plug 'tpope/vim-surround'
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
    map <leader>ve :tabnew ~/.vimrc<CR>
    map <leader>vr :source ~/.vimrc<CR>

" Code
	syntax on

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
    " set tabstop=4
	" For david
	set tabstop=8 softtabstop=0 expandtab shiftwidth=4 smarttab



    " size of an "indent"
    set shiftwidth=4

" colorscheme 
	set background=dark
	colorscheme gruvbox
	" vim hardcodes background color erase even if the terminfo file does
	" not contain bce (not to mention that libvte based terminals
	" incorrectly contain bce in their terminfo files). This causes
	" incorrect background rendering when using a color theme with a
	" background color.
	let &t_ut=''


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

" statusline
	let laststatus=2

" clear highlighting
	command C let @/=""

" View man pages in vim
    runtime! ftplugin/man.vim
    let g:ft_man_open_mode = 'tab'


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
	map <leader>dms /\\\[\_.\{-}\\\]<CR>

"" Ultisnips
	map <F2> :tabnew ~/.vim/LocalSnippets/words.snippets<CR>
	map <F3> :tabnew ~/.vim/LocalSnippets/tex.snippets<CR>
	map <F4> :tabnew ~/.vim/LocalSnippets/math.snippets<CR>

" Trigger configuration. Do not use <tab> if you use https://github.com/Valloric/YouCompleteMe.
	let g:UltiSnipsExpandTrigger="<tab>"
	let g:UltiSnipsJumpForwardTrigger="<tab>"
	let g:UltiSnipsJumpBackwardTrigger="<s-tab>"
	let g:UltiSnipsSnippetDirectories=['LocalSnippets']
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

" '||'  '|'                  .'|.          '||     '||''''|                   .          
"  ||    |   ....    ....  .||.   ... ...   ||      ||  .    ....     ....  .||.   ....  
"  ||    |  ||. '  .|...||  ||     ||  ||   ||      ||''|   '' .||  .|   ''  ||   ||. '  
"  ||    |  . '|.. ||       ||     ||  ||   ||      ||      .|' ||  ||       ||   . '|.. 
"   '|..'   |'..|'  '|...' .||.    '|..'|. .||.    .||.     '|..'|'  '|...'  '|.' |'..|' 
                                                                                       
" REGEX
" QUESTION: How do I do the .* in regex to match newlines too?
" ANSWER: 
" \_. matches any character including end-of-line. However, as :h \_. warns, using it with * will match all text to the end of the buffer.
" \{-} is similar to *, matching 0 or more instances of the proceeding atom. But it matches as few as possible instead of as many as possible. This makes \{-} safe if your example pattern appears more than once. For example:
" 
" author = {{foo
"            bar}},
" 
" editor = {{buz
"            baz}},
" 
" Using %s/{{\(\_.*\)}}/{\1}/g changes the starting double brace for author, but the closing double brace for editor. Since * matches as many atoms as possible, the pattern matches until the last double brace it finds. This results in the following:
" 
" author = {foo
"            bar}},
" 
" editor = {{buz
"            baz},
" 
" However, using %s/{{\(\_.\{-}\)}}/{\1}/g gives the desired result for both author and editor as it stops searching at the first double brace it finds:
" 
" author = {foo
"            bar},
" 
" editor = {buz
"            baz},

                                                                                       


