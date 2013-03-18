;; set username
(setq user-full-name "Gauthier FRIDIERE")

;(add-to-list 'load-path "~/.emacs.d/packages/")
;    (require 'yasnippet) ;; not yasnippet-bundle
(add-to-list 'load-path
              "~/.emacs.d/plugins/yasnippet")
(require 'yasnippet)
(yas-global-mode 1)
(add-to-list 'load-path "~/.emacs.d")    ; This may not be appeared
; if you have already added.
(require 'auto-complete-config)
(add-to-list 'ac-dictionary-directories "~/.emacs.d/ac-dict")
(ac-config-default)
;; raccourci pour question emacs
(defalias 'yes-or-no-p 'y-or-n-p)

;; mon fichier de conf std
(load "/home/oicho/.emacs.d/Oicho_style.el")

(setq c-default-style "oicho")
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; vectra
(defun vectra-man-on-word ()
  "Appelle le man sur le mot pointé par le curseur"
  (interactive)
  (manual-entry (current-word)))


;;;;;;;;;;;;;;;;;;;
;; Activer la coloration syntaxique
(global-font-lock-mode t)
;; gdb
(setq-default gdb-many-windows t)
(setq-default tab-width 2)

(setq tab-width 2
      c-default-style "k&r"
      c-block-comment-prefix ""
      c-basic-offset 2)
(setq-default indent-tabs-mode nil)

;; indent all
(defun indent-whole ()
  (interactive)
  (mark-whole-buffer)
  (indent-region (region-beginning) (region-end))
  )
(global-set-key (kbd "C-c t") 'indent-whole)

;; montre les espaces fin de lignes
(setq-default show-trailing-whitespace t)
(defun delete-trailing-whitespace-exit ()
  (if (string= ".article" (buffer-name))
      ()
    (if (string= ".followup" (buffer-name))
	()
      (delete-trailing-whitespace))))

(add-hook 'write-file-hooks 'delete-trailing-whitespace-exit)
;; Afficher ligne col dans emacs
(column-number-mode t)
(line-number-mode t)
;; ... est sur le bord
(require 'linum)
;; Reduit la fontion sur elle meme
(add-hook 'c-mode-common-hook 'hs-minor-mode)
(add-hook 'lisp-mode-hook 'hs-minor-mode)
(add-hook 'emacs-lisp-mode-hook 'hs-minor-mode)
(add-hook 'python-mode-hook 'hs-minor-mode)
(global-set-key [f1] 'hs-hide-block)
;; Et la 'de'reduit
(global-set-key [f2] 'hs-show-block)
;; Page garde
(defun insert-header-guard ()
  (interactive)
  (if (string-match "\\.h\\(h\\|xx\\)?$" (buffer-name))
      (let ((header-guard
             (upcase (replace-regexp-in-string "[-.]" "_"
					              (buffer-name)))))
        (save-excursion
          (goto-char (point-min))
          (insert "#ifndef " header-guard "_\n")
          (insert "# define " header-guard "_\n\n")
          (goto-char (point-max))
          (insert "\n#endif /* !" header-guard "_ */")))
    (message "Invalid C/C++ header file.")))
;; cinfg mini buffer
(global-set-key [M-left] 'windmove-left)
(global-set-key [M-right] 'windmove-right)
(global-set-key [M-up] 'windmove-up)
(global-set-key [M-down] 'windmove-down)
(global-set-key [M-S-left] 'shrink-window-horizontally)
(global-set-key [M-S-right] 'enlarge-window-horizontally)
(global-set-key [M-S-down] 'enlarge-window)
(global-set-key [M-S-up] 'shrink-window)
;; Afficher la 'parenthèse correspondante'
(require 'paren)
(show-paren-mode)
;; montre les lignes trop longues
(setq fill-column 79)

;; Pas de fichier temp
(setq make-backup-files nil)

(setq-default auto-fill-function 'do-auto-fill)
(defun eightycols nil
  (defface line-overflow
    '((t (:background "red" :foreground "white")))
    "Face to use for `hl-line-face'.")
  (highlight-regexp "^.\\{80,\\}$" 'line-overflow))

(add-hook 'find-file-hook 'eightycols)
(display-time)
(setq display-time-24hr-format 1)


(global-set-key (kbd "<f7>") 'compile)
(global-set-key (kbd "<f4>") 'comment-or-uncomment-region)
;; activer l affichage ligne dans marge gauche
(global-set-key [f6] 'linum-mode)
(global-set-key [f3]  'goto-line)
;; ctrl + f1 montr le man du mot courant
(global-set-key [f5]  'vectra-man-on-word)
(setq ;; scrolling
  scroll-margin 0                        ;; do smooth scrolling, ...
  scroll-conservatively 100000           ;; ... the defaults ...
  scroll-up-aggressively 0               ;; ... are very ...
  scroll-down-aggressively 0             ;; ... annoying
  scroll-preserve-screen-position t)     ;; preserve screen pos with
;; C-v/M-v

;; Pas de ligne en plus a la fin d emacs
(setq next-line-add-newlines nil)
