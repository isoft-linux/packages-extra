(require 'racer)
(require 'company)

(add-hook 'rust-mode-hook #'racer-mode)
(add-hook 'racer-mode-hook #'eldoc-mode)

(add-hook 'racer-mode-hook #'company-mode)
(global-set-key (kbd "TAB") #'company-indent-or-complete-common) ;
(setq company-tooltip-align-annotations t)

;(add-hook 'rust-mode-hook 
;  '(lambda () 
;     (racer-activate)
;     (local-set-key (kbd "M-.") #'racer-find-definition)
;     (local-set-key (kbd "TAB") #'racer-complete-or-indent)))
