-- Sustituye el codigo entre centinelas #--- ... #--- por un hueco para
-- completar en clase. Solo se carga bajo el perfil `notebooks`.
-- Adaptado de PhilChodrow/ml-notes-update (scripts/strip-hidden-code.lua).
return {
  {
    CodeBlock = function(el)
      el.text = string.gsub(el.text, "#%-%-%-.-#%-%-%-", "# TODO: completar en clase")
      return el
    end
  }
}
