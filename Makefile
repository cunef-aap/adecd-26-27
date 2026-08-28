# Aprendizaje Automatico: Prediccion (G244) — CUNEF
# Uso habitual:  make check && make sitio && make notebooks

.PHONY: check marcas sitio notebooks preview publicar datos limpiar \
        pdfs pdfs-soluciones soluciones-estado

check:                       ## centinelas emparejados + reglas mecánicas de estilo
	python scripts/check-centinelas.py
	python scripts/check-estilo.py

marcas:                      ## marcas de revisión .nuevo sin aceptar
	python scripts/aceptar-marcas.py --listar

sitio: check                 ## renderiza el sitio a docs/
	quarto render --profile publica

notebooks: check             ## cuadernos con huecos -> docs/live-notebooks/
	python scripts/crear-ipynb.py
	mkdir -p docs/datos
	cp datos/prostate.data datos/airbnb_madrid.csv docs/datos/

preview:                     ## servidor local con recarga
	quarto preview --profile publica

pdfs: sitio                  ## PDF de capitulos, hojas y apendices -> pdf/
	python scripts/crear-pdfs.py

pdfs-soluciones:             ## PDF de los solucionarios, sin dejarlos publicados
	python scripts/soluciones.py --mostrar
	quarto render --profile publica
	python scripts/crear-pdfs.py --solo hoja
	python scripts/soluciones.py --ocultar
	quarto render --profile publica
	@echo
	@echo "Los solucionarios estan en pdf/problemas/ y vuelven a estar ocultos"
	@echo "en el sitio. Comprueba con: make soluciones-estado"

soluciones-estado:           ## dice si los solucionarios se publicarian o no
	python scripts/soluciones.py --estado

datos:                       ## espeja y submuestrea los datasets
	python scripts/descargar-datos.py

publicar: sitio notebooks marcas
	python scripts/soluciones.py --estado
	git add -A
	git commit -m "Actualiza el sitio"
	git push origin main

limpiar:
	rm -rf docs .quarto _freeze
