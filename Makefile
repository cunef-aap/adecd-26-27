# Aprendizaje Automatico: Prediccion (G244) — CUNEF
# Uso habitual:  make check && make sitio && make notebooks

.PHONY: check sitio notebooks preview publicar datos limpiar

check:                       ## centinelas #--- emparejados en todos los .qmd
	python scripts/check-centinelas.py

sitio: check                 ## renderiza el sitio a docs/
	quarto render --profile publica

notebooks: check             ## cuadernos con huecos -> docs/live-notebooks/
	python scripts/crear-ipynb.py

preview:                     ## servidor local con recarga
	quarto preview --profile publica

datos:                       ## espeja y submuestrea los datasets
	python scripts/descargar-datos.py

publicar: sitio notebooks
	git add docs capitulos curso problemas evaluacion assets scripts datos _quarto*.yml
	git commit -m "Actualiza el sitio"
	git push origin main

limpiar:
	rm -rf docs .quarto _freeze
