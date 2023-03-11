;; - If you see this:
;; cpbotha@meepzen3:/tmp$ convert -trim -antialias orgtexFrCVbZ.pdf -quality 100 bleh.png
;; convert-im6.q16: attempt to perform an operation not allowed by the security policy `PDF' @ error/constitute.c/IsCoderAuthorized/408.
;; OR: "org-compile-file: File "/tmp/orgtexjdH822.png" wasn’t produced.  Please adjust ‘imagemagick’ part of ‘org-preview-latex-process-alist’."
;; delete the 6 "disable ghostscript format types" lines in /etc/ImageMagick-6/policy.xml
;; https://stackoverflow.com/questions/52998331/imagemagick-security-policy-pdf-blocking-conversion

;; we add melpa so we can install ox-hugo
(setq package-archives
      '(
        ("elpa" . "https://elpa.gnu.org/packages/")
        ("nongnu" . "https://elpa.nongnu.org/nongnu/")
        ("melpa" . "https://melpa.org/packages/")
        ;; fallback for when the official ones act up
        ;;("melpa" . "https://raw.githubusercontent.com/d12frosted/elpa-mirror/master/melpa/")
        ;;("gnu"   . "https://raw.githubusercontent.com/d12frosted/elpa-mirror/master/gnu/")
        )
      )


(package-initialize)

;; Bootstrap `use-package'
;; http://www.lunaryorn.com/2015/01/06/my-emacs-configuration-with-use-package.html
;; use-package autoloads will make sure it get pulled in at the right time
;; read "package autoloads":  http://www.lunaryorn.com/2014/07/02/autoloads-in-emacs-lisp.html
(unless (package-installed-p 'use-package)
  (package-refresh-contents)
  (package-install 'use-package))

(use-package ox-hugo
  :ensure t
  :config
  (setq org-export-with-broken-links 'mark)
  (setq org-hugo-external-file-extensions-allowed-for-copying
        '("jpg" "jpeg" "js" "json" "tiff" "png" "svg" "gif" "mp4" "pdf" "odt" "doc" "ppt" "xls" "docx" "pptx" "xlsx"))

  (plist-put  (cdr (assoc 'imagemagick org-preview-latex-process-alist)) :latex-compiler '("pdflatex -shell-escape -interaction nonstopmode -output-directory %o %f") )


  )

