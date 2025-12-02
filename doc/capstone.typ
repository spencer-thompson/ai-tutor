#set page(margin: 1.5cm)
#set document(
  title: [AI Tutor],
  author: "Spencer Thompson",
)

#show link: set text(fill: blue)
#show link: underline

#set par(justify: true)
#set rect(stroke: silver, inset: 1em, outset: 1em)
#show heading.where(level: 4): set heading(numbering: none)
#set heading(numbering: "1.")
#show heading: h => [
  #set text(navy)
  #v(0.2cm)
  #smallcaps(h)
  #v(0.2cm)
]

#set text(16pt, font: "Berkeley Mono")


#v(4cm)
#align(center)[
  #text(navy, 64pt)[*AI Tutor*]

  #v(-1.1cm)

  #align(center)[
    #grid(
      columns: (0.5fr, 2fr, 0.3fr, 2fr, 0.5fr),
      [], line(length: 100%, stroke: navy), [#text(10pt, super(sym.circle.filled))], line(length: 100%, stroke: navy),
    )
  ]

  #v(-1.4cm)

  #text(navy, 64pt)[*Capstone*]

  // #line(length: 100%, stroke: 2pt + navy)

  ~
  #v(2cm)

  // #underline(offset: 0.3em)[CS 3310]


  ~

  *Spencer Thompson*

  #v(0.4cm)

  #datetime.today().display("[month repr:long] [day], [year]")
]

#v(2cm)

#show outline.entry.where(
  level: 1,
): set block(above: 1.1em)
#show outline.entry.where(
  level: 2,
): set block(above: 1.1em)

// #set text(10pt)
//
#pagebreak()
#outline(indent: 1.7em, title: [Table of Contents], depth: 3)

#set text(11pt)

#pagebreak()


= Intro

= Body

= Conclusion
