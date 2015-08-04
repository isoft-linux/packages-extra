;;(add-to-list 'load-path "~/.emacs.d/site-lisp/eim")
(require 'eim)
;;(autoload 'eim-use-package "eim" "Another emacs input method")
;; Tooltip 暂时还不好用
(setq eim-use-tooltip nil)

;;如果需要五笔，打开以下设置
;;(register-input-method
;; "eim-wb" "euc-cn" 'eim-use-package
;; "五笔" "汉字五笔输入法" "wb.txt")
(register-input-method
 "eim-py" "euc-cn" 'eim-use-package
 "拼音" "汉字拼音输入法" "py.txt")

;;使用英文标点
(setq eim-punc-translate-p nil) 
(setq default-input-method "eim-py")
