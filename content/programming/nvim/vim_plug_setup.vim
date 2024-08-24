let data_dir = has('nvim') ? stdpath('data') . '/site' : '~/.vim'
if empty(glob(data_dir . '/autoload/plug.vim'))
  silent execute '!curl -fLo '.data_dir.'/autoload/plug.vim --create-dirs  https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

call plug#begin()
" moving in directories
Plug 'justinmk/vim-dirvish'
" fuzzy finding
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
" language servers
Plug 'prabirshrestha/vim-lsp'
Plug 'mattn/vim-lsp-settings'
" auto completion
Plug 'prabirshrestha/asyncomplete.vim'
Plug 'prabirshrestha/asyncomplete-lsp.vim'
" c++ 
Plug 'bfrg/vim-cpp-modern'
Plug 'tpope/vim-commentary'
Plug 'vim-scripts/DoxygenToolkit.vim'
"Function / class comment :
"  In vim, place the cursor on the line of the function header (or returned
"  value of the function) or the class.  Then execute the command :Dox.  This
"  will generate the skeleton and leave the cursor after the @brief tag.


" python 

Plug 'averms/black-nvim', {'do': ':UpdateRemotePlugins'}

" html
Plug 'mattn/emmet-vim'
" colorscheme
Plug 'cocopon/iceberg.vim'
" focus 
Plug 'junegunn/goyo.vim'
call plug#end()

" dirvish use :cd % to change root

" colorscheme setup
set termguicolors
colorscheme iceberg

" autocompleteion setup
inoremap <expr> <Tab>   pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
inoremap <expr> <cr>    pumvisible() ? asyncomplete#close_popup() : "\<cr>"

" emmet setup
let g:user_emmet_install_global = 0
autocmd FileType html,css EmmetInstall

" doxygen toolkit setup
let g:DoxygenToolkit_authorName="cuppajoeman"


" vim.fzf bindings
nmap <leader>fz :Files<CR>
nmap <leader>bz :Buffers<CR>

" configure clang format
function! Formatonsave()
  let l:formatdiff = 1
  if has('python')
    pyf ~/projects/llvm-project/clang/tools/clang-format/clang-format.py
  elseif has('python3')
    py3f ~/projects/llvm-project/clang/tools/clang-format/clang-format.py
  endif
endfunction
autocmd BufWritePre *.h,*.cc,*.cpp call Formatonsave()

" for vim-lsp
function! s:on_lsp_buffer_enabled() abort
    setlocal omnifunc=lsp#complete
    setlocal signcolumn=yes
    if exists('+tagfunc') | setlocal tagfunc=lsp#tagfunc | endif
    nmap <buffer> gd <plug>(lsp-definition)
    nmap <buffer> gs <plug>(lsp-document-symbol-search)
    nmap <buffer> gS <plug>(lsp-workspace-symbol-search)
    nmap <buffer> gr <plug>(lsp-references)
    nmap <buffer> gi <plug>(lsp-implementation)
    nmap <buffer> gt <plug>(lsp-type-definition)
    nmap <buffer> ga <plug>(lsp-code-action)
    nmap <buffer> <leader>rn <plug>(lsp-rename)
    nmap <buffer> [g <plug>(lsp-previous-diagnostic)
    nmap <buffer> ]g <plug>(lsp-next-diagnostic)
    nmap <buffer> K <plug>(lsp-hover)
    nmap <buffer> <expr> <leader><c-u> lsp#scroll(-4)
    nmap <buffer> <expr> <leader><c-d> lsp#scroll(+4)

    let g:lsp_format_sync_timeout = 1000
    autocmd! BufWritePre *.rs,*.go call execute('LspDocumentFormatSync')
    
    " refer to doc to add more commands
endfunction

augroup lsp_install
    au!
    " call s:on_lsp_buffer_enabled only for languages that has the server registered.
    autocmd User lsp_buffer_enabled call s:on_lsp_buffer_enabled()
augroup END
