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
-- pandoc.path.normalize conserva los segmentos "..". Los enlaces usan esas
-- subidas de directorio, pero el manifiesto contiene rutas desde la raíz.
local function normaliza(ruta)
  ruta = pandoc.path.normalize(ruta):gsub("\\", "/")
  local partes = {}
  for parte in ruta:gmatch("[^/]+") do
    if parte == ".." and #partes > 0 and partes[#partes] ~= ".." then
      table.remove(partes)
    elseif parte ~= "." then
      table.insert(partes, parte)
    end
  end
  return (ruta:sub(1, 1) == "/" and "/" or "") .. table.concat(partes, "/")
end
-- Preview de un fichero suelto puede no definir QUARTO_PROJECT_DIR.
-- El filtro vive siempre en scripts/, junto a los manifiestos del proyecto.
local raiz = quarto.project.directory
  or pandoc.path.directory(quarto.utils.resolve_path("../contenido.txt"))
raiz = normaliza(raiz)

local function carga(nombre, incluir_inactivos)
  local f = io.open(pandoc.path.join({raiz, nombre}), "r")
  if f == nil then return end
  for linea in f:lines() do
    local l = linea:gsub("^%s+", ""):gsub("%s+$", "")
    if incluir_inactivos then l = l:gsub("^%-%s+", "") end
    if l ~= "" and not l:match("^#") and not l:match("^%-")
       and not l:match("^%[") and not l:match("^{") then
      publicados[normaliza(pandoc.path.join({raiz, l}))] = true
    end
  end
  f:close()
end

-- El perfil publico solo conoce contenido.txt. Revision permite ademas su lista
-- local; completo incluye todas las rutas. Ambos perfiles escriben fuera de docs/.
local perfiles = "," .. table.concat(quarto.project.profile or {}, ",") .. ","
local publica = perfiles:find(",publica,", 1, true) ~= nil
local completo = not publica and perfiles:find(",completo,", 1, true) ~= nil
carga("contenido.txt", completo)
if not publica and perfiles:find(",revision,", 1, true) then
  carga("revision.txt", false)
end

function Link(el)
  local destino = el.target:gsub("#.*$", "")
  if not destino:match("%.qmd$") then return el end
  if destino:match("^%a[%w+.-]*:") then return el end
  local absoluta
  if destino:match("^/") then
    absoluta = pandoc.path.join({raiz, destino:sub(2)})
  else
    absoluta = pandoc.path.join({pandoc.path.directory(quarto.doc.input_file), destino})
  end
  if publicados[normaliza(absoluta)] then return el end
  return pandoc.Span(el.content)
end
