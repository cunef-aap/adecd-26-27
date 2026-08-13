-- Colapsa por defecto los callouts de solucion en HTML.
function Callout(el)
  if quarto.doc.isFormat("html") then
    if el.type == "sol" then
      if not el.collapse then el.collapse = true end
    end
    return el
  end
end
