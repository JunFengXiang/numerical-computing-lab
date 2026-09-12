function Math(el)
  local _, comma_count=el.text:gsub(",","")
  if el.mathtype == "InlineMath" and (#el.text > 90 or comma_count >= 5) and not el.text:find("begin",1,true) then
    el.text=el.text:gsub("([^\\]),", "%1,\\allowbreak ")
  end
  return el
end

function Para(el)
  if pandoc.utils.stringify(el):gsub("%s","") == "表8.1" then
    return {pandoc.RawBlock("latex", "\\Needspace{19\\baselineskip}"),el}
  end
  return el
end

function Image(el)
  if el.src:match("publisher%-mark%-original") then
    el.attributes.width="25%"
  elseif el.src:match("pdf%-322%-cover%-logo") then
    el.attributes.width="20%"
  elseif el.src:match("figure%-13%.2") or el.src:match("fig%-13%-2") then
    el.attributes.width="42%"
  else
    el.attributes.width="85%"
  end
  return el
end

function Table(el)
  local s=pandoc.utils.stringify(el)
  local roomy=s:find("625",1,true) and s:find("364",1,true) and s:find("425",1,true)
  local wide=s:find("widehat L_n",1,true) and s:find("332",1,true) and #el.colspecs==4
  local sor=s:find("松弛因子",1,true) and s:find("109",1,true) and #el.colspecs==2
  if wide then
    local specs=el.colspecs
    local widths={0.07,0.43,0.07,0.43}
    for i=1,4 do specs[i][2]=widths[i] end
    el.colspecs=specs
  end
  if roomy then
    return {
      pandoc.RawBlock("latex", "\\begingroup\n\\renewcommand{\\arraystretch}{2.2}"),
      el,
      pandoc.RawBlock("latex", "\\endgroup")
    }
  end
  return el
end
