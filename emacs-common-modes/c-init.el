;;If files contains below words, treat it as objc files.
(setq magic-mode-alist
  (append (list
       '("\\(.\\|\n\\)*\n#import" . objc-mode)
       '("#import" . objc-mode)
       '("\\(.\\|\n\\)*\n@class" . objc-mode)
       '("@class" . objc-mode)
       '("\\(.\\|\n\\)*\n@implementation" . objc-mode)
       '("@implementation" . objc-mode)
       '("\\(.\\|\n\\)*\n@interface" . objc-mode)
       '("@interface" . objc-mode)
       '("\\(.\\|\n\\)*\n@protocol" . objc-mode)
       '("@protocol" . objc-mode))
      magic-mode-alist))

(setq local-eassist-header-switches
            '(("h" . ("cpp" "cxx" "c++" "CC" "cc" "C" "c" "mm" "m"))
            ("hh" . ("cc" "CC" "cpp" "cxx" "c++" "C"))
            ("hpp" . ("cpp" "cxx" "c++" "cc" "CC" "C"))
            ("hxx" . ("cxx" "cpp" "c++" "cc" "CC" "C"))
            ("h++" . ("c++" "cpp" "cxx" "cc" "CC" "C"))
            ("H" . ("C" "CC" "cc" "cpp" "cxx" "c++" "mm" "m"))
            ("HH" . ("CC" "cc" "C" "cpp" "cxx" "c++"))
            ("cpp" . ("hpp" "hxx" "h++" "HH" "hh" "H" "h"))
            ("cxx" . ("hxx" "hpp" "h++" "HH" "hh" "H" "h"))
            ("c++" . ("h++" "hpp" "hxx" "HH" "hh" "H" "h"))
            ("CC" . ("HH" "hh" "hpp" "hxx" "h++" "H" "h"))
            ("cc" . ("hh" "HH" "hpp" "hxx" "h++" "H" "h"))
            ("C" . ("hpp" "hxx" "h++" "HH" "hh" "H" "h"))
            ("c" . ("h"))
            ("m" . ("h"))
            ("mm" . ("h"))))

(defun local-eassist-string-without-last (string n)
  "This function truncates from the STRING last N characters."
  (substring string 0 (max 0(- (length string) n))))


(defun local-eassist-switch-h-cpp ()
  "Switch header and body file according to `eassist-header-switches' var.
The current buffer's file name extention is searched in
`eassist-header-switches' variable to find out extention for file's counterpart,
for example *.hpp <--> *.cpp."
  (interactive)
  (let* ((ext (file-name-extension (buffer-file-name)))
         (base-name (local-eassist-string-without-last (buffer-name) (length ext)))
         (base-path (local-eassist-string-without-last (buffer-file-name) (length ext)))
         (count-ext (cdr (find-if (lambda (i) (string= (car i) ext)) local-eassist-header-switches))))
    (cond
     (count-ext
      (unless
          (or
           (loop for b in (mapcar (lambda (i) (concat base-name i)) count-ext)
         when (bufferp (get-buffer b)) return
         (if (get-buffer-window b)
             (switch-to-buffer-other-window b)
           (if (get-buffer-window b t)
               (switch-to-buffer-other-frame b)
             (switch-to-buffer b))))
           (loop for c in (mapcar (lambda (count-ext) (concat base-path count-ext)) count-ext)
                 when (file-exists-p c) return (find-file c)))
        (message "There is no corresponding pair (header or body) file.")))
     (t
      (message "It is not a header or body file! See eassist-header-switches variable.")))))

(defun my-c-mode-common-hook ()

  ;;Vi方式的%跳转到匹配括号C-M-n/p f/b也是可以的
  (local-set-key (kbd "C-%") 'goto-match-paren)
  (defun goto-match-paren (arg)
    "Go to the matching  if on (){}[], similar to vi style of % "
    (interactive "p")
    ;; first, check for "outside of bracket" positions expected by forward-sexp, etc.
    (cond ((looking-at "[\[\(\{]") (forward-sexp))
          ((looking-back "[\]\)\}]" 1) (backward-sexp))
          ;; now, try to succeed from inside of a bracket
          ((looking-at "[\]\)\}]") (forward-char) (backward-sexp))
          ((looking-back "[\[\(\{]" 1) (backward-char) (forward-sexp))
          (t nil)))
  ;;设置自己的注释风格，如果使用/* */方式，最好打开上面注释掉的函数
  (setq comment-style 'extra-line)

  ;;更好的识别c/c++后缀，方便eassist-switch-h-cpp不出错
  (setq eassist-header-switches
            '(("h" . ("cpp" "cxx" "c++" "CC" "cc" "C" "c" "mm" "m"))
            ("hh" . ("cc" "CC" "cpp" "cxx" "c++" "C"))
            ("hpp" . ("cpp" "cxx" "c++" "cc" "CC" "C"))
            ("hxx" . ("cxx" "cpp" "c++" "cc" "CC" "C"))
            ("h++" . ("c++" "cpp" "cxx" "cc" "CC" "C"))
            ("H" . ("C" "CC" "cc" "cpp" "cxx" "c++" "mm" "m"))
            ("HH" . ("CC" "cc" "C" "cpp" "cxx" "c++"))
            ("cpp" . ("hpp" "hxx" "h++" "HH" "hh" "H" "h"))
            ("cxx" . ("hxx" "hpp" "h++" "HH" "hh" "H" "h"))
            ("c++" . ("h++" "hpp" "hxx" "HH" "hh" "H" "h"))
            ("CC" . ("HH" "hh" "hpp" "hxx" "h++" "H" "h"))
            ("cc" . ("hh" "HH" "hpp" "hxx" "h++" "H" "h"))
            ("C" . ("hpp" "hxx" "h++" "HH" "hh" "H" "h"))
            ("c" . ("h"))
            ("m" . ("h"))
            ("mm" . ("h"))))

  (require 'newcomment)
  (local-set-key "\C-ch" 'local-eassist-switch-h-cpp)
  (local-set-key "\C-cj" 'save-mark)
  (local-set-key "\C-cb" 'goto-mark)
  ;;按F6弹出devhelp mini assistant窗口
  (local-set-key [f6] 'devhelp-assistant-word-at-point)


  ;;这个函数主要是为了跳到开头添加头文件 
  ;;其实并没有完全达到目的，最好是跳到include块的结尾
  (defun save-mark()
    (interactive)
    (eh-point-to-register))
  (defun goto-mark()
    (interactive)
    (eh-jump-to-register))

  ;;添加C++ Header的标识头，这样emacs可以方便的识别文件为C++ Header
  ;;否则，语法的高亮和部分缩进规则用的是C-mode，对于class以及public等关键字的处理是不对的。
  (defun cpp-header ()
    (interactive "*")
    (c++-mode)
    (goto-line 0)
    (insert "/* -*-C++-*- */\n")
  )
  (defun objc-header ()
    (interactive "*")
    (objc-mode)
    (goto-line 0)
    (insert "/* -*-objc-*- */\n")
  )

)

(add-hook 'c-mode-common-hook 'my-c-mode-common-hook)
(add-hook 'objc-mode-common-hook 'my-c-mode-common-hook)


