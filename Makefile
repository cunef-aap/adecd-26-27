# Aprendizaje Automatico: Prediccion (G244) — CUNEF
# Uso habitual:  make check && make sitio && make notebooks

.PHONY: check marcas sitio notebooks preview publicar datos limpiar pdfs publicado

check:                       ## centinelas emparejados + reglas mecánicas de estilo
	python scripts/check-centinelas.py
	python scripts/check-estilo.py

marcas:                      ## marcas de revisión .nuevo sin aceptar
	python scripts/aceptar-marcas.py --listar

sitio: check                 ## renderiza a docs/ SOLO lo publicado en contenido.txt
	python scripts/publicado.py --sitio
	quarto render --profile publica

notebooks: check             ## cuadernos con huecos -> docs/live-notebooks/
	python scripts/crear-ipynb.py
	mkdir -p docs/datos
	cp datos/prostate.data datos/airbnb_madrid.csv docs/datos/

preview:                     ## servidor local con recarga
	quarto preview --profile publica

# Los PDF salen del libro COMPLETO, no del sitio: se suben al Campus Virtual a medida
# que cada capitulo tiene version definitiva, antes de publicarse en la web. Van a
# _completo/ para no ensuciar docs/, que es lo que se publica.
pdfs: check                  ## PDF de todo el libro, incluidos solucionarios -> pdf/
	python scripts/publicado.py --completo
	quarto render --profile publica --output-dir _completo
	python scripts/publicado.py --sitio
	python scripts/crear-pdfs.py --desde _completo

publicado:                   ## dice que documentos se publican en la web
	python scripts/publicado.py --estado

datos:                       ## espeja y submuestrea los datasets
	python scripts/descargar-datos.py

publicar: sitio notebooks marcas   ## fuente al repo privado y sitio al publico
	python scripts/publicado.py --estado
	git add -A
	git commit -m "Actualiza el sitio"
	git push origin main
	python scripts/publicar-sitio.py

limpiar:
	rm -rf docs _completo .quarto _freeze
