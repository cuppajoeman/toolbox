" Put plugins and dictionaries in this dir (also on Windows)
let vim_dir = '$HOME/.vim'

let vim_dir_not_on_runtime_path = stridx(&runtimepath, expand(vim_dir)) == -1

if vim_dir_not_on_runtime_path
  let &runtimepath.=','.vim_dir
endif

" Keep undo history across sessions by storing it in a file
if has('persistent_undo')
    let my_undo_dir = expand(vim_dir . '/undo_dir')
    " Create dirs
    call system('mkdir ' . vim_dir)
    call system('mkdir ' . my_undo_dir)
    let &undodir = my_undo_dir
    set undofile
endif
