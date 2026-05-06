(defun org-grades-to-csv (output-file)
  "Extract grades from org-mode buffer and write to OUTPUT-FILE as CSV.
Does not modify the buffer."
  (interactive "FOutput CSV file: ")
  (let* ((data '())
         (columns '())
         (current-name nil)
         (current-section nil)
         (current-entry nil))

    ;; Parse buffer
    (save-excursion
      (goto-char (point-min))
      (while (not (eobp))
        (let ((line (buffer-substring-no-properties
                     (line-beginning-position)
                     (line-end-position))))
          (cond
           ;; Level 1: student name (e.g., "* DONE Bertolotto")
           ((string-match "^\\* \\(?:DONE\\|TODO\\|\\) *\\(.+\\)" line)
            ;; Save previous entry if any
            (when current-entry
              (push (nreverse current-entry) data))
            (setq current-name (string-trim (match-string 1 line)))
            (setq current-entry (list (cons "Name" current-name)))
            (setq current-section nil))

           ;; Level 2: assignment section (e.g., "** Simple model of the Sun")
           ((string-match "^\\*\\* \\(.+\\)" line)
            (setq current-section (string-trim (match-string 1 line))))

           ;; Level 3: grade category (e.g., "*** Physical correctness 4")
           ((string-match "^\\*\\*\\* \\(.+?\\)\\s-*\\([0-9.]+\\|N/A\\)?$" line)
            (let* ((category (string-trim (match-string 1 line)))
                   (raw-value (match-string 2 line))
                   (value (cond
                           ((null raw-value) "")
                           ((string-match-p "N/A" raw-value) "N/A")
                           (t (string-trim raw-value))))
                   (col-name (concat current-section " - " category)))
              ;; Track unique columns
              (unless (member col-name columns)
                (setq columns (append columns (list col-name))))
              ;; Add to current entry
              (when current-entry
                (push (cons col-name value) current-entry)))))
          (forward-line 1)))

      ;; Don't forget the last entry
      (when current-entry
        (push (nreverse current-entry) data)))

    (setq data (nreverse data))

    ;; Write CSV
    (with-temp-file output-file
      (let ((all-cols (cons "Name" columns)))
        ;; Header row
        (insert (mapconcat #'identity
                           (mapcar (lambda (c)
                                     (concat "\"" (replace-regexp-in-string "\"" "\"\"" c) "\""))
                                   all-cols)
                           ","))
        (insert "\n")
        ;; Data rows
        (dolist (row data)
          (insert (mapconcat #'identity
                             (mapcar (lambda (col)
                                       (let ((val (or (cdr (assoc col row)) "")))
                                         (concat "\"" (replace-regexp-in-string "\"" "\"\"" val) "\"")))
                                     all-cols)
                             ","))
          (insert "\n"))))

    (message "CSV written to %s" output-file)))
