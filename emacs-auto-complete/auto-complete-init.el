;;clang auto complete settings
(require 'auto-complete-config)
(require 'auto-complete-clang-async)

;;BEGIN auto-complete配置，主要是为了把系统的include目录全部加给clang
(defun my-ac-config ()
;;  (define-key ac-mode-map  [(control return)] 'auto-complete)
;;  (setq iphoneos-includes
;;    (substring
;;      (shell-command-to-string "find /usr/share/iPhoneOS5.0.sdk/usr/include/ -type d -printf \" -I%p \"")
;;     0 -1))
;;
;;  (setq ac-clang-cflags (split-string (concat iphoneos-includes " -I/usr/share/iPhoneOS5.0.sdk/usr/include")))
;;
  (setq ac-sources '(ac-source-clang-async))
  (ac-clang-launch-completion-process)
  (auto-complete-mode t)
)
;;END 

(add-hook 'c-mode-common-hook 'my-ac-config)
(add-hook 'objc-mode-common-hook 'my-ac-config)
