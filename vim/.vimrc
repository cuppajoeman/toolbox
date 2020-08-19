"\___/\__,_/ .___/ .___/\__,_/_/ /\____/\___/_/ /_/ /_/\__,_/_/ /_/
"         /_/   /_/         /___/

" Automatic vim-plug installation
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

"python import sys; sys.path.append("/usr/lib/python3.8/site-packages")

" Plugins
call plug#begin('~/.vim/plugged')
Plug 'junegunn/goyo.vim'
Plug 'SirVer/ultisnips'
Plug 'dag/vim-fish'
Plug 'markonm/traces.vim'
Plug 'lervag/vimtex'
Plug 'morhetz/gruvbox'
Plug 'tpope/vim-surround'
"Plug 'FredKSchott/CoVim'
call plug#end()


" Leader
	let mapleader =" "

" Enable autocompletion:
	set wildmode=longest,list,full

" Disables automatic commenting on newline:
	" autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o

" Open this file easily
    map <leader>ve :tabnew ~/.vimrc<CR>
    map <leader>vr :source ~/.vimrc<CR>

" Code
	syntax on

" Buffers
  nnoremap <leader>b :ls<cr>:b<space>

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

" Have a vartical ruler
    set colorcolumn=80

" Indentataion
    filetype plugin indent on
    " On pressing tab, insert 2 spaces
    set expandtab
    " show existing tab with 2 spaces width
    set tabstop=2
    set softtabstop=2
    " when indenting with '>', use 2 spaces width
    set shiftwidth=2

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
        set clipboard=unnamedplus
        nnoremap <C-y> "+y
        vnoremap <C-y> "+y
        nnoremap <C-p> "+gp
        vnoremap <C-p> "+gp

" Keep cursor in center of page
	augroup VCenterCursor
	  au!
	  au BufEnter,WinEnter,WinNew,VimResized *,*.*
			\ let &scrolloff=winheight(win_getid())/2
	augroup END

" COMMANDS

" compile markdown into pdf
  command Mdc :!pandoc % -o temp.pdf

" Connected visual split
  command Connvs :vsp|exe "norm! \<c-f>"|setl scrollbind|wincmd p|setl scrollbind
  command Date :put=strftime('%F')

" Open help in a new tab
	cabbrev help tab help
" Vertically split a buffer
  cabbrev vb vert sb
" folding
  set foldmethod=syntax

" statusline
	let laststatus=2

" searching with casing
  set ignorecase
  set smartcase

" Don't break your fingers on regex
  cmap <c-o> .\{-}

" clear highlighting
	command C let @/=""

" View man pages in vim
    runtime! ftplugin/man.vim
    let g:ft_man_open_mode = 'tab'

                                                               
"  _|      _|                                                    
"  _|_|  _|_|    _|_|_|    _|_|_|  _|  _|_|    _|_|      _|_|_|  
"  _|  _|  _|  _|    _|  _|        _|_|      _|    _|  _|_|      
"  _|      _|  _|    _|  _|        _|        _|    _|      _|_|  
"  _|      _|    _|_|_|    _|_|_|  _|          _|_|    _|_|_|    
                                                               
" To use this the markdown file on the left and the corresponding tex file on
" the right, use @n on the right side and @s on the left

let @i = 'F$l"lyt=f=l"ryt$'
let @d = '"lyt=f=l"ry$'


"  ___               ___   ___         ___  
" |   | |     |   | |       |   |\  | |     
" |-+-  |     |   | | +-    +   | + |  -+-  
" |     |     |   | |   |   |   |  \|     | 
"        ---   ---   ---   ---         ---  

" Goyo for more readable text
    " map <leader>g :Goyo 75% \| set linebreak<CR>
    map <leader>g :Goyo \| set linebreak<CR>
    let g:goyo_linenr=1
    let g:goyo_height=100
    set nocompatible
    set number
    set relativenumber
                                          
"" Vimtex
	let g:vimtex_view_method='zathura'
	let g:tex_flavor = 'latex'
  set conceallevel=1
  let g:tex_conceal='abdmg'
	au BufReadPost *.tex set syntax=tex
	map <leader>ims ?\$.\{-}\$<CR>
	map <leader>dms ?\\\[\_.\{-}\\\]<CR>

"" Ultisnips
	map <F2> :tabnew ~/.vim/LocalSnippets/<CR>

" Trigger configuration. Do not use <tab> if you use https://github.com/Valloric/YouCompleteMe.
	let g:UltiSnipsExpandTrigger="<tab>"
	let g:UltiSnipsJumpForwardTrigger="<tab>"
	let g:UltiSnipsJumpBackwardTrigger="<s-tab>"
	let g:UltiSnipsSnippetDirectories=['LocalSnippets']
	filetype plugin indent on

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

" Question: Getting tired of switching tabs all the time

" DISCUSSION:
" cuppajoeman | Right now I'm using gt and gT to go through tabs, sometimes I have a lot of tabs open so it's painful to manually  
"             | remember the number of each tab, what solutions do you guys have for going to tabs quickly? I've used fuzzy        
"             | finding before in vscode but not sure if that would be necessary here                                              
" cuppajoeman | (I also know how to jump directly to a tab)                                                                        
"      nedbat | cuppajoeman: one option would be to not use tabs, and just use buffers                                             
"      nedbat | cuppajoeman: IDEs like VSCode use a tab per file, but in vim, tabs are more like workspaces.                       
" cuppajoeman | Ahh, that's interesting, thanks for the comment! And just to be sure a buffer is just like where a representation  
"             | of the file resides in memory right?                                                                               
"      nedbat | cuppajoeman: it's a file in memory, yes                                                                            
" cuppajoeman | So opening a couple files in buffers means that they're in memory but they're not necessarily all being displayed  

" https://stackoverflow.com/questions/102384/using-vims-tabs-like-buffers/103590#103590
" 

" PROBELM: was tired of having to give full path
" SOLUTION: Each window can have their own current directory different from the global one
" To change the cwd to the one where the file is located do:
    " :lcd %:p:h
"In these commands, % gives the name of the current file, %:p gives its full path, and %:p:h gives its directory (the "head" of the full path). "
