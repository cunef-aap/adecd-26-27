-- Desactiva los enlaces a paginas que todavia no se publican.
--
-- El sitio publico solo lleva el material con version definitiva, y un enlace de una pagina
-- publicada a un .qmd que no lo esta tiene dos consecuencias malas: el alumno se encuentra
-- un 404, y sobre todo Quarto trata ese .qmd como un recurso y COPIA EL FUENTE al directorio
-- de salida. Es decir, publicaria el capitulo inedito, o un solucionario, en su version .qmd.
--
-- Este filtro convierte esos enlaces en texto llano, de modo que ni se rompen ni arrastran el
-- fuente. Cuando el capitulo se publique, el enlace vuelve solo: la lista la lee de
-- contenido.txt, que es la unica fuente de verdad.

local publicados = {}

local function carga()
  local f = io.open(quarto.project.directory .. "/contenido.txt", "r")
  if f == nil then return end
  for linea in f:lines() do
    local l = linea:gsub("^%s+", ""):gsub("%s+$", "")
    if l ~= "" and not l:match("^#") and not l:match("^%-")
       and not l:match("^%[") and not l:match("^{") then
      publicados[l] = true
    end
  end
  f:close()
end

carga()

function Link(el)
  local destino = el.target:gsub("#.*$", "")
  if not destino:match("%.qmd$") then return el end
  -- las rutas del proyecto son de un nivel (curso/x.qmd), asi que basta quitar los ../
  local relativa = destino:gsub("^%.%./", ""):gsub("^%./", "")
  if publicados[relativa] then return el end
  return pandoc.Span(el.content)
end
