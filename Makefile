pdf: cv.tex
	pdflatex cv.tex

cv.tex: cv.json
	python3 cv_builder.py

clean:
	rm -f cv.{pdf,tex,aux,log}
