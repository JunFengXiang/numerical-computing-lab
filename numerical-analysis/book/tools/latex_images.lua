-- Keep source figures in reading order and retain their original printed labels.
function Image(el)
  local widths = {
    ["figure-2.1.png"] = "54%",
    ["figure-2.2.png"] = "54%",
    ["figure-2.3.png"] = "80%",
    ["figure-2.4.png"] = "95%"
  }
  local name = el.src:match("[^/]+$")
  el.attributes.width = widths[name] or "90%"
  return el
end
