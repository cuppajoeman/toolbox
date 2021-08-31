map <leader>s :call UltiSnips#RefreshSnippets()<CR>
map <F3> :tabe ~/math-snippets/ <CR>
map <F4> :tabnew ~/programming-snippets/<CR>
map <F5> :tabnew ~/tool-box/<CR>

" ultisnips
let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<tab>"
let g:UltiSnipsJumpBackwardTrigger="<s-tab>"
" If you want :UltiSnipsEdit to split your window.
"let g:UltiSnipsEditSplit="vertical"
let g:UltiSnipsSnippetDirectories=["math-snippets", "programming-snippets"]
