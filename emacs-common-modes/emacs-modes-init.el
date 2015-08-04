;; csharp-init.el
(autoload 'csharp-mode "csharp-mode" "Major mode for editing C# code." t)
(setq auto-mode-alist
(append '(("\\.cs$" . csharp-mode)) auto-mode-alist))

;; igrep-init.el
(autoload 'igrep "igrep"
  "*Run `grep` PROGRAM to match REGEX in FILES..." t)
(autoload 'igrep-find "igrep"
  "*Run `grep` via `find`..." t)
(autoload 'igrep-visited-files "igrep"
  "*Run `grep` ... on all visited files." t)
(autoload 'dired-do-igrep "igrep"
  "*Run `grep` on the marked (or next prefix ARG) files." t)
(autoload 'dired-do-igrep-find "igrep"
  "*Run `grep` via `find` on the marked (or next prefix ARG) directories." t)
(autoload 'Buffer-menu-igrep "igrep"
  "*Run `grep` on the files visited in buffers marked with '>'." t)
(autoload 'igrep-insinuate "igrep"
  "Define `grep' aliases for the corresponding `igrep' commands." t)

;; Use php-mode for .php,.php3,.php4 and .phtml files
(autoload 'php-mode "php-mode" "Major mode for editing PHP code." t)

(add-to-list 'auto-mode-alist
	     '("\\.php[34]\\'\\|\\.php\\'\\|\\.phtml\\'" . php-mode))

;; rpm-spec-mode for spec files

(autoload 'rpm-spec-mode "rpm-spec-mode" "RPM spec mode." t)
(add-to-list 'auto-mode-alist '("\\.spec$" . rpm-spec-mode))


;;根据emacs启动时的时间决定用什么主题。
;;晚上用深色主题
;;白天用默认主题
(defvar night-hour 18 
  "When to start with dark theme.")

(defvar day-hour 8 
  "When to start with light theme.")

;;use default themes provided by emacs-24
;;(defun night-theme()
;;    (interactive)
;;    (require 'my-color-theme)
;;    (enable-theme 'desert) ;;desert or turquoise or forest
;;)
(defun color-theme-timer ()
  "Sets color theme according to current time. Customize `night-hour' and `day-hour'."
  (interactive)
  (let ((hour (nth 2 (decode-time)))
        (minute (nth 1 (decode-time))))
    (if (or (>= hour night-hour) (< hour day-hour) )
      (load-theme 'tango-dark)
      (load-theme 'tango-dark))))
;;      (message "Day, default theme"))))

(color-theme-timer)

;;(require 'fill-column-indicator)
;;(define-globalized-minor-mode global-fci-mode fci-mode (lambda () (fci-mode 1)))
;;(setq-default fill-column 80)
;;(global-fci-mode 1)

;;(require 'column-marker)
;;(define-globalized-minor-mode global-cm-mode column-marker-1 (lambda () (column-marker-1 80)))
;;(global-cm-mode 1)
