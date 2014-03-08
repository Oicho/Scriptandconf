" editzone.vim
" Parameters related to the edition zone

  set number

set laststatus=2
set statusline=%f\ %l\|%c\ %m%=%p%%\ (%Y%R)

set wildmenu
set hid
set noerrorbells
set novisualbell

"set cursorline"

if version >= 703
  set colorcolumn=+1
endif

" disclaimer: not everyone will love that. With a good colorscheme, it is
" really helpful.
set encoding=utf-8
set list
set listchars=tab:.\ ,eol:¬
function! NumberToggle()
if(&relativenumber == 1)
  set number
else
  set relativenumber
endif
endfunc

                  nnoremap <C-n> :call NumberToggle()<cr>
