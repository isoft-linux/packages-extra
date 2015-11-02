(require 'racer)
(add-hook 'rust-mode-hook 
  '(lambda () 
     (racer-activate)
     (local-set-key (kbd "M-.") #'racer-find-definition)
     (local-set-key (kbd "TAB") #'racer-complete-or-indent)))
