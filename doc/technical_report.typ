#set page(margin: 1.2cm)
#set text(28pt, font: "Berkeley Mono", weight: 700)
// #show math.equation: set text(font: )
#set enum(indent: 1em)
#set list(indent: 1em)
#set math.mat(align: center, delim: "[", gap: 0.75em)
#set math.vec(align: right)
#set math.cases(gap: 0.5em)
#set heading(hanging-indent: 0.78cm)
#set table(align: left)
#show heading: h => [
  #set text(navy)
  #v(0.3cm)
  #h
  #v(0.3cm)
]


#let answer(x) = align(center)[
  #rect[
    $
      #x
    $
  ]
]

#let rev(x) = text(fill: blue, $#x$)
#let bigspace = $quad quad quad quad$

#v(3cm)
#align(center)[

  = AI Tutor

  #v(-0.6cm)
  #line(length: 50%, stroke: silver)

  #v(-0.8cm)
  #text(14pt, weight: 400)[_Technical Report_]
  // #v(-0.6cm)
  //

  #set text(16pt)
  Spencer Thompson

  // #text(11pt, font: "Berkeley Mono")[
  //   MATH 3640 | Due 4/22/2025
  // ]
]

// #set text(11pt, font: "Latin Modern Mono Caps")
#set text(12pt, font: "Berkeley Mono", weight: 400)

// https://excalidraw.com/#json=JBsUsLgMPG4HTt90L85BY,f4kdzGTYkBLF-bAs9NdQxA
