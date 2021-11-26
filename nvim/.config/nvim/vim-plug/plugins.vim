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
  Plug 'motemen/vim-help-random'
  " Plug 'flipcoder/vim-textbeat'
  "Plug 'takac/vim-hardtime'
  " Language server protocol configurations
  "Plug 'neovim/nvim-lspconfig'
  " auto completion
  "Plug 'hrsh7th/nvim-compe'
  "Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}  " We recommend updating the parsers on update
  "nice on the eyes
  Plug 'kyazdani42/blue-moon'
  Plug 'danro/rename.vim'
  " because pyright doesn't do formatting
  "Plug 'mhartington/formatter.nvim'
call plug#end()

" Refactor link to plugin after pasting link
map <leader>fl 0vf/;;cPlug 'A'
