$out_dir = 'build';
$aux_dir = 'build';
$pdf_mode = 1;
$bibtex_use = 2;
$max_repeat = 8;
$recorder = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';
$biber = 'biber --output-directory build %O %B';
@default_files = ('clio.tex');
