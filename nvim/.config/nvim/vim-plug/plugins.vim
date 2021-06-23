" Auto install plug if it doesn't exist
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

"Load plugins here (pathogen or vundle)
call plug#begin(stdpath('data') . '/plugged')
  " have my own custom snippets
  Plug 'SirVer/ultisnips'
  " Plug 'christoomey/vim-tmux-navigator'
  " Work with latex
  Plug 'lervag/vimtex'
  " Show regex result as I create it
  Plug 'markonm/traces.vim'
  " Surround things
  Plug 'tpope/vim-surround'
  " Simple text editing
  Plug 'junegunn/goyo.vim'
  " Plug 'flipcoder/vim-textbeat'
  " Language server protocol configurations
  Plug 'neovim/nvim-lspconfig'
  " auto completion
  Plug 'hrsh7th/nvim-compe'
call plug#end()

" Refactor link to plugin after pasting link
map <leader>pr 0vf/;;cPlug 'A'
