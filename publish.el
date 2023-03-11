;; cpbotha: if org-hugo--search-and-get-anchor (called by org-hugo-link) yields error,
;; export stops, so here we advise it to just report and return the "normal" anochor-not-found ""
;; (my database is old, sometimes there are links to files outside of ith that don't exist anymore)
(defun oh--saga (orig-org-hugo--search-and-get-anchor &rest args)
  (condition-case err
      (apply orig-org-hugo--search-and-get-anchor args)
    (error (progn
             (message "=====> org-link-search IGNORED ERROR: %s" err)
             ""))))

;; if you DO WANT ox-hugo to error out on each missing link so you can fix it, just comment out the line below
(advice-add #'org-hugo--search-and-get-anchor :around #'oh--saga)

(recentf-mode -1)

;; this is the main publish org -> md function
;; it improves over jethrokuan's original in the following ways:
;; - supports nested org-files (it will maintain the directory structure on the hugo side)
;; - overrides any HUGO directives you might already have in your org mode files
(defun cpb/publish (org-dir in_file hugo-base-dir out_file)
  (with-current-buffer (find-file-noselect in_file)
    ;; unfortunately, these are overridden by e.g. #+HUGO_BASE_DIR in the file if they are present
    (let* ((org-hugo-base-dir hugo-base-dir)
           ;; directory-files-recursively is 10x faster than find-lisp-find-files
           (org-id-extra-files (directory-files-recursively org-dir "\.org$"))
           (org-hugo-content (file-name-concat org-hugo-base-dir "content"))
           ;; the section is the directory relative to "content" containing the output md
           (org-hugo-section (file-name-directory (file-relative-name out_file org-hugo-content)))
           (cpb-oh-pub-dir (file-name-concat org-hugo-content org-hugo-section)))

      ;; org-hugo--get-pub-dir is called by org-hugo-export-to-md right after reading all hugo vars
      ;; we override it in order to
      ;; temporarily override org-hugo--get-pub-dir else #+HUGO_* file properties override ours!
      ;; we restore _our_ base/section into info, and we also return the full pub-dir to where we want it
      (cl-letf (((symbol-function 'org-hugo--get-pub-dir) #'(lambda (info)
                                                              (plist-put info :hugo-base-dir org-hugo-base-dir)
                                                              (plist-put info :hugo-section org-hugo-section)
                                                              (plist-put info :hugo-bundle nil)
                                                              cpb-oh-pub-dir)))

        (org-hugo-export-to-md)
      ))))
