;;以下代码非常的关键，主要解决中文英文真正等宽的问题，即：
;;Hello World|
;;你好，世界.|
;;宽度应该是完全一致的。如果上面两行的竖线没有对齐，说明：
;;你的终端或者vi编辑器或者emacs编辑器是不合格的
;;
;;设置后就不会出现表格等对不齐的问题
;;遗憾是中文字会稍微大一些。

;;字号仍然是从.Xresources里面读取
;;Emacs.Font: Monaco-10.5
;;(custom-set-faces '(default ((t (:family "Monaco")))))
;;UTF8环境下起作用的是这一条
;;(set-fontset-font "fontset-default" 'han "Microsoft YaHei 12" )
;;这些是以防万一的
;;(set-fontset-font "fontset-default" 'chinese-gbk "Microsoft YaHei 12" )
;;(set-fontset-font "fontset-default" 'unicode "Microsoft YaHei 12" )

;;设置电池显示格式
(setq battery-mode-line-format "[Bat %p%%]")

(custom-set-variables
 '(display-battery-mode t)
 '(display-time-mode t)
 '(global-font-lock-mode t)
 '(column-number-mode t)
 ;;'(scroll-bar-mode (quote right))
 '(scroll-bar-mode nil)
 '(show-paren-mode t)
 '(tool-bar-mode nil)
)

;;设置为浮点数就是比例，设置为整形就是行数
;;这里设置为1行，对ido模式可能不适用，但减少了
;;大部分情况下的跳跃问题，比如leim模式下汉字字高引起的跳跃
;;(setq max-mini-window-height 1)
;;(global-hl-line-mode t)
(setq use-file-dialog nil)
;;禁用启动信息,前两条在dotemacs中可以用，但在default.el和site-start.el中都不能用。
;;所以，三条都写上了
(setq inhibit-startup-message t)
(setq inhibit-startup-screen t)
(setq initial-scratch-message nil)
;;(setq initial-buffer-choice 'none)

;;关闭出错时的提示声
(setq visible-bell nil)

;;不产生~备份文件
;;(setq make-backup-files nil)
;;(setq-default make-backup-files nil) 

;;Put back files to /tmp/emacs-<uid> dir.
;;http://www.emacswiki.org/emacs/AutoSave
(defconst emacs-tmp-dir (format "%s/%s-%s/" temporary-file-directory "emacs" (user-uid)))


(defun make-emacs-tmp-dir (fn)
  (if (not (file-exists-p fn))
    (make-directory fn)))
(make-emacs-tmp-dir emacs-tmp-dir)

(setq backup-directory-alist
    `((".*" . ,emacs-tmp-dir)))
(setq auto-save-file-name-transforms
    `((".*" ,emacs-tmp-dir t)))
(setq auto-save-list-file-prefix
    emacs-tmp-dir)


(defun save-all ()
    (interactive)
    (save-some-buffers t))
(add-hook 'focus-out-hook 'save-all)


;;光标靠近鼠标的时候，让鼠标自动让开，别挡住视线
(mouse-avoidance-mode 'animate)

;;下面的这个设置可以让光标指到某个括号的时候显示与它匹配的括号
(show-paren-mode t)
(setq show-paren-style 'parentheses)

;;设置缺省模式是text，而不是基本模式
(setq default-major-mode 'text-mode)
(add-hook 'text-mode-hook 'turn-on-auto-fill)

;;防止页面滚动时跳动
(setq scroll-margin 3
      scroll-conservatively 10000)

;;打开行号支持
(setq linum-format "%3d")
(global-linum-mode t)

;;定义全局键，选中区域后，自动按照某特殊字符对齐代码
(global-set-key (kbd "C-x a r") 'align-regexp)

;;Emacs Helper functions
(global-set-key [(meta up)] 'move-text-up)
(global-set-key [(meta down)] 'move-text-down)
(global-set-key [(control o)] 'eh-open-next-line)
(global-set-key [f1] 'de-ansi-term)
(global-set-key [f11] 'text-scale-increase)
(global-set-key [f12] 'text-scale-decrease)

;;对需要调用browser的mode，用uniopen打开
(setq browse-url-browser-function 'browse-url-generic
      browse-url-generic-program "uniopen")
                                                       
;;建立一个新行并自动缩进
;;快捷键ctrl+o
(defun eh-open-next-line (arg)
  "Move to the next line (like vi) and then opens a line."
  (interactive "p")
  (cond
    ((eq (point) (line-end-position))
    ;;如果是在行尾，只是增加一个新行。
    (open-line arg)
    (next-line 1)
    (indent-according-to-mode)
    )
    ((not (eq (point) (line-end-position)))
    ;;如果是在行中，将本行后面的内容断行到下两行，然后缩进，
    ;;然后回退一行到空行，然后缩进
    ;;尤其是自动补齐{}的时候，可以自动建一个新的空行。
    (newline)
    (open-line arg)
    (next-line 1)
    (indent-according-to-mode)
    (previous-line)
    (indent-according-to-mode))
  ))



;;下面一组函数是跳转、跳回相关的
;;存储当前位置到register
(defun eh-point-to-register()
  "Store cursorposition _fast_ in a register. 
   Use eh-jump-to-register to jump back to the stored 
   position."
  (interactive)
  (setq zmacs-region-stays t)
  (point-to-register 8))

;;跳转到刚才存储的位置
(defun eh-jump-to-register()
  "Switches between current cursorposition and position
   that was stored with ska-point-to-register."
  (interactive)
  (setq zmacs-region-stays t)
  (let ((tmp (point-marker)))
        (jump-to-register 8)
        (set-register 8 tmp)))


;;这组函数可以上下移动代码行或者选中的代码块
  
(defun move-text-internal (arg)
  (cond
   ((and mark-active transient-mark-mode)
    (if (> (point) (mark))
        (exchange-point-and-mark))
    (let ((column (current-column))
          (text (delete-and-extract-region (point) (mark))))
      (forward-line arg)
      (move-to-column column t)
      (set-mark (point))
      (insert text)
      (exchange-point-and-mark)
      (setq deactivate-mark nil)))
   (t
    (let ((column (current-column)))
      (beginning-of-line)
      (when (or (> arg 0) (not (bobp)))
        (forward-line)
        (when (or (< arg 0) (not (eobp)))
          (transpose-lines arg))
        (forward-line -1))
      (move-to-column column t)))))

(defun move-text-down (arg)
  "Move region (transient-mark-mode active) or current line
  arg lines down."
  (interactive "*p")
  (move-text-internal arg))

(defun move-text-up (arg)
  "Move region (transient-mark-mode active) or current line
  arg lines up."
  (interactive "*p")
  (move-text-internal (- arg)))

;;ansi-term的定义，调用ansi-term，快捷键定义为F1

(defun de-ansi-term ()
  "Start an bash ansi term that will be closed when it finishes"
  (interactive)
  (let ((buf (de-next-term-buffer))
	(in-term-p (eq major-mode 'term-mode))
	wind)
    (if in-term-p
	;; in a terminal, create a new one
	(de-new-ansi-term)
      ;; not in a terminal, do any terminals exist?
      (if buf
	  (progn
	    ;; if it's visible, switch to it
	    (if (setq wind (de-next-term-window))
		(select-window wind)
	      ;; maybe i hid the terminal - do the splitting thing again
	      (if (> (length (window-list)) 1)
		  (progn
		    (other-window 1)
		    (switch-to-buffer buf))
		(pop-to-buffer buf))))
	;; no terminals
	(de-new-ansi-term)))))

(defun de-new-ansi-term (&optional supress-pop)
  (ansi-term "/bin/bash")
  ;; standard setup stuff
  (define-key term-raw-map (kbd "C-o") 'other-window)
  (define-key term-raw-map (kbd "M-`") 'erc-track-switch-buffer)
  (set-process-sentinel (get-buffer-process
			 (current-buffer)) 'de-ansi-term-sentinel)
  ;; split the new terminal with the calling window
  (unless supress-pop
    (let ((b (current-buffer)))
      (switch-to-buffer (other-buffer))
      (pop-to-buffer b))))

(defun de-ansi-term-sentinel (process change)
  "Close the terminal window when the process finishes"
  (when (or (string-match "finished" change)
            (string-match "exited" change))
    (kill-buffer (current-buffer))
    (if (> (length (window-list)) 1)
        (delete-window))))

(defun de-next-term-buffer ()
  "Return the next terminal buffer, or nil"
  (let (buf)
    (mapc (lambda (b)
	    (unless buf
	      (with-current-buffer b
		(when (eq major-mode 'term-mode)
		  (setq buf b)))))
	  (buffer-list))
    buf))

(defun de-next-term-window ()
  (let (wind (buf (de-next-term-buffer)))
    (when buf
      (walk-windows
       (lambda (w)
	 (unless wind
	   (when (equal (window-buffer w) buf)
	     (setq wind w))))))
    wind))

;;引入redo模式，emacs的undo tree不是正常人可以理解的。
;;(require 'redo+)
;;(global-set-key (kbd "C-x r") 'redo)

;;打开文件时如果目录还不存在，就创建它，注意make-directory的第二个参数t可以递归创建目录。
;;这个对某些mode的影响较大，如果目录不存在mode可能会初始化失败
(defadvice find-file (before make-directory-maybe (filename &optional wildcards) activate)
  "Create parent directory if not exists while visiting file."
  (unless (file-exists-p filename)
    (let ((dir (file-name-directory filename)))
      (unless (file-exists-p dir)
      (when (yes-or-no-p (format "Create directory?: %s " dir)) 
        (make-directory dir t))
        ))))

;;没有region时拷贝一行
(defadvice kill-ring-save (before slickcopy activate compile)
    "When called interactively with no active region, copy a single line instead."
    (interactive
     (if mark-active (list (region-beginning) (region-end))
       (list (line-beginning-position)
             (line-beginning-position 2)))))

(defadvice kill-region (before slickcut activate compile)
    "When called interactively with no active region, kill a single line instead."
    (interactive
     (if mark-active (list (region-beginning) (region-end))
       (list (line-beginning-position)
             (line-beginning-position 2)))))


;;F10切换是否全屏
(defun toggle-fullscreen (&optional f)
   (interactive)
   (let ((current-value (frame-parameter nil 'fullscreen)))
      (set-frame-parameter nil 'fullscreen
                            (if (equal 'fullboth current-value)
                                (if (boundp 'old-fullscreen) old-fullscreen nil)
                                (progn (setq old-fullscreen current-value)
                                       'fullboth)))))

(global-set-key [f10] 'toggle-fullscreen)

