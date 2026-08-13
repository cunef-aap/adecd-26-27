-- Elimina unicamente las lineas centinela `#---` del sitio publicado;
-- el codigo se muestra completo.
-- Adaptado de PhilChodrow/ml-notes-update (scripts/strip-hidden-delims.lua),
-- con el patron ANCLADO: el original borraba cualquier linea que contuviese
-- tres guiones en cualquier posicion, lo que se comeria en silencio
-- comentarios decorativos como `# --- Calculo del R2 ---`.
return {
  {
    CodeBlock = function(el)
      local lines = pandoc.List()
      for line in (el.text .. "\n"):gmatch("([^\n]*)\n") do
        if not string.match(line, "^%s*#%-%-%-%s*$") then
          lines:insert(line)
        end
      end
      el.text = table.concat(lines, "\n")
      return el
    end
  }
}
