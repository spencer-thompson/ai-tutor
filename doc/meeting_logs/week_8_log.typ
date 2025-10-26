// #set page(margin: 2cm, height: auto, width: 26cm)
#set page(margin: 1cm)
#set text(28pt, font: "Berkeley Mono", weight: 700)
#set math.mat(align: right, gap: 10pt)
#set enum(indent: 1em)
#set list(indent: 1.5em)
#set heading(hanging-indent: 1.8cm)
#set enum(numbering: "(a)")
#show heading: h => [
  #set text(navy)
  #v(0.3cm)
  #h
  #v(0.3cm)
]

#align(center)[
  #v(2cm)

  = Week Eight Meeting Log

  #v(-0.3cm)
  // #text(12pt)[_Systems of Linear Differential Equations_]
  // #v(-0.6cm)
  #line(length: 50%, stroke: silver)
  #v(-0.6cm)
  #set text(24pt)

  AI Tutor

  #text(11pt, font: "Berkeley Mono")[
    Spencer Thompson | Landon Towers

    10/12/2025
  ]
]

#let rev_color = blue

#set text(10pt, font: "Berkeley Mono", weight: 400)
#let rev(x) = text(fill: rev_color, $#x$)
#let answer(x) = rect[
  $
    #x
  $
]


#v(2cm)


== | What have you done since last team meeting?

- We got a new virtual machine for staging the environment.

- We also managed to plan out some next steps regarding features such as:

  - Migrating to GPT-5

  - Fixing some issues with database initialization

  - Moving to a combination of Sqlite and MongoDB

== | What obstacles are you encountering?

- We are having issues running the local development environment on Landon's computer.
  This could be an issue with the existing code, so I will look into it.

== | What do you plan to accomplish by the next team meeting?

- Hopefully get the local development environment working on everyone's computers.

~

== | Contributions

#table(
  columns: (1fr,) * 4,
  // row-gutter: 1em,
  stroke: none,
  align: horizon,
  [
    // #align(center)[
    Team: 7
    // ]
  ],
  [
    // #align(center)[
    Sprint: 1
    // ]
  ],
  [
    // #align(center)[
    Date: 10/12/2025
    // ]
  ],
  [
    // #align(center)[
    Team Score: 100%
    // ]
  ],
  table.hline(start: 0, end: 4),
  [
    *Name:*
  ],
  [
    *Contribution (%):*
  ],
  [
    *Signature:*
  ],
  [
    *Individual Score:*
  ],
  table.hline(start: 0, end: 4),
  [
    Spencer Thompson
  ],
  [
    50%
  ],
  [
    Spencer Thompson
  ],
  [
    100%
  ],
  [
    Landon Towers
  ],
  [
    50%
  ],
  [
    Landon Towers
  ],
  [
    100%
  ],
)

== | Notes

- N/A
