--[[
Give long inline code spans somewhere to break so they cannot overflow their
table column in the PDF.

Why this exists
---------------
pandoc renders a markdown pipe table whose delimiter row is uniform (`|---|`)
as equal-width `p{}` columns — five columns become 0.2\linewidth each, about
17 monospace characters at the body font size. Inline code is emitted as
`\texttt{...}`, and TeX has no legal breakpoint inside a token like
`credentialSubject.customerProfile.consumptionProfiles[].meterId`: it cannot
hyphenate across `.`, `[` or `]`, so the whole 63-character path is set as one
unbreakable box that runs straight over the neighbouring column. That is the
overlapping text seen in the Schedule I / normative-path tables of the
use-case overviews (and anywhere else a long JSON path lands in a narrow
cell).

What it does
------------
Splits a long `Code` inline into several `Code` inlines joined by explicit
LaTeX penalties. The typeset result is identical unless a break is actually
needed, because TeX prefers fewer lines (each costs \linepenalty):

  * everywhere — a free breakpoint after each run of path separators
    (`.` `/` `[` `]` `_` `-` `:` `@` `,` `;` `=` `#`), so a path wraps between
    its segments;
  * inside table cells only — a dear breakpoint at each camelCase hump and,
    failing that, an almost-forbidden one every MAX_RUN characters, for
    identifiers with no separator to break at (`installationAddress` alone is
    wider than a five-column cell). Restricted to tables because running prose
    has a full text width to play with, and a mid-identifier break there would
    be gratuitous.

Headings are left alone: their text also becomes a PDF bookmark string, where
raw LaTeX has no meaning.

LaTeX output only — a no-op for every other writer, so GitBook and the
docsify preview are unaffected.
]]

if FORMAT ~= 'latex' and FORMAT ~= 'beamer' then
  return {}
end

-- Spans at or below this length fit any column we use; leave them whole.
local MIN_LEN = 12
-- Longest run left without an emergency breakpoint inside a table. Twelve
-- monospace characters are ~72pt at the 10pt body size, comfortably inside
-- the ~91pt of a five-column cell.
local MAX_RUN = 12

local SEPARATOR = '[%.%[%]/_%-:@,;=#]'

local FREE_BREAK = pandoc.RawInline('latex', '\\allowbreak{}')
-- A camelCase hump is the least-bad place to split an identifier that has no
-- separator at all, so it is dearer than a separator break but cheaper than
-- the fixed-width one below.
local CAMEL_BREAK = pandoc.RawInline('latex', '\\penalty 4000\\relax{}')
-- Just under \nobreak (10000): TeX takes this only when every alternative is
-- an overfull line. \relax terminates the number scan so the following
-- \texttt is safe.
local COSTLY_BREAK = pandoc.RawInline('latex', '\\penalty 9000\\relax{}')

--- Split on separators, keeping each separator at the end of its chunk.
local function split_on_separators(text)
  local chunks, current = {}, ''
  for i = 1, #text do
    local char = text:sub(i, i)
    current = current .. char
    local next_char = text:sub(i + 1, i + 1)
    -- Break after a run of separators, not between them, so `[].` stays with
    -- the segment it terminates.
    if char:match(SEPARATOR) and next_char ~= '' and not next_char:match(SEPARATOR) then
      chunks[#chunks + 1] = current
      current = ''
    end
  end
  if current ~= '' then
    chunks[#chunks + 1] = current
  end
  return chunks
end

--- Split at camelCase humps: `consumptionProfiles` -> `consumption`, `Profiles`.
local function split_camel_case(text)
  local pieces, start = {}, 1
  for i = 1, #text - 1 do
    if text:sub(i, i):match('[%l%d]') and text:sub(i + 1, i + 1):match('%u') then
      pieces[#pieces + 1] = text:sub(start, i)
      start = i + 1
    end
  end
  pieces[#pieces + 1] = text:sub(start)
  return pieces
end

--- Append the fixed-width slices of `piece`, joined by last-resort breaks.
local function emit_slices(inlines, piece, attr)
  local offset = 1
  while offset <= #piece do
    if offset > 1 then
      inlines[#inlines + 1] = COSTLY_BREAK
    end
    inlines[#inlines + 1] = pandoc.Code(piece:sub(offset, offset + MAX_RUN - 1), attr)
    offset = offset + MAX_RUN
  end
end

--- Append `chunk` as Code inlines, subdividing long runs when `inside_table`.
local function emit_chunk(inlines, chunk, attr, inside_table)
  if not inside_table or #chunk <= MAX_RUN then
    inlines[#inlines + 1] = pandoc.Code(chunk, attr)
    return
  end
  for index, piece in ipairs(split_camel_case(chunk)) do
    if index > 1 then
      inlines[#inlines + 1] = CAMEL_BREAK
    end
    if #piece <= MAX_RUN then
      inlines[#inlines + 1] = pandoc.Code(piece, attr)
    else
      emit_slices(inlines, piece, attr)
    end
  end
end

-- Plain prose carries bare paths too ("...are at
-- schemas/MeterDataRequest/v0.6/examples/"). TeX treats one of those as a
-- single word with no hyphenation point, so it overhangs the right margin.
-- Slashes are a conventional place to break a path in running text, so this
-- applies in prose and tables alike.
local MIN_STR_LEN = 18

local function Str(el)
  -- A slash on its own is the glue in `consumers`/`resources`/`scope`/... —
  -- every span around it is short, so nothing here trips the length test
  -- below, yet the whole chain is one unbreakable run. Break after it.
  if el.text:match('^/+$') then
    return { el, FREE_BREAK }, false
  end
  if #el.text < MIN_STR_LEN or not el.text:find('/', 1, true) then
    return nil
  end
  local chunks = {}
  for chunk in el.text:gmatch('[^/]*/*') do
    if chunk ~= '' then
      chunks[#chunks + 1] = chunk
    end
  end
  if #chunks < 2 then
    return nil  -- a single trailing slash, nothing to break at
  end
  local inlines = {}
  for index, chunk in ipairs(chunks) do
    if index > 1 then
      inlines[#inlines + 1] = FREE_BREAK
    end
    inlines[#inlines + 1] = pandoc.Str(chunk)
  end
  -- `false`: the pieces are final, do not re-enter this filter on them.
  return inlines, false
end

local function code_splitter(inside_table)
  return function(el)
    if #el.text <= MIN_LEN then
      return nil
    end
    local chunks = split_on_separators(el.text)
    if #chunks == 1 and not inside_table then
      return nil  -- nothing to break on, and prose has room for it
    end
    local inlines = {}
    for index, chunk in ipairs(chunks) do
      if index > 1 then
        inlines[#inlines + 1] = FREE_BREAK
      end
      emit_chunk(inlines, chunk, el.attr, inside_table)
    end
    -- `false`: the pieces are final, do not re-enter this filter on them.
    return inlines, false
  end
end

-- Top-down so a block can refuse further traversal by returning `false`:
-- headings opt out entirely, and tables handle their own contents with the
-- in-table rules before the plain Code handler can reach them.
return {
  {
    traverse = 'topdown',
    Header = function(el) return el, false end,
    Table = function(el)
      return pandoc.walk_block(el, { Code = code_splitter(true), Str = Str }), false
    end,
    Code = code_splitter(false),
    Str = Str,
  },
}
