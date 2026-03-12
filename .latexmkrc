# Force latexmk to use XeLaTeX (required by fontspec)
# Use synctex, nonstopmode and show file-line errors
$pdflatex = 'xelatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S';
$bibtex = 'bibtex %O %S';
$makeindex = 'makeindex %O %S';
$dvipdf = '';
$pdf_mode = 1;

# Keep aux files in project directory
$aux_dir = '.';

# Clean additional generated files when running latexmk -c
push @generated_exts, 'synctex.gz';