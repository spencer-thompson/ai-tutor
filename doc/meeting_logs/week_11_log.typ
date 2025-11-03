// #set page(margin: 2cm, height: auto, width: 26cm)
#set page(margin: 1cm)
#set text(26pt, font: "Berkeley Mono", weight: 700)
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

  = Week Eleven Meeting Log

  #v(-0.3cm)
  // #text(12pt)[_Systems of Linear Differential Equations_]
  // #v(-0.6cm)
  #line(length: 50%, stroke: silver)
  #v(-0.6cm)
  #set text(24pt)

  AI Tutor

  #text(11pt, font: "Berkeley Mono")[
    Spencer Thompson | Landon Towers

    11/2/2025
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

- We got the staging environment working!
  In addition, we added a bunch of new domains to test various different builds of the tutor on.

- We successfully deployed a new version of the AI Tutor with a variety of fixes as well as
  migrating to the new GPT-5 model.

- The new deployed Tutor also more accurately follows the behavior that the Tech Management Department wants it to.

== | What obstacles are you encountering?

- Communication is difficult, particularly when discussing more technical aspects of the codebase.

- There are several different departments all connected to this project, all with different feedback, requirements, and wants.
  Providing the features, paperwork, and deliverables for all parties involved is incredibly difficult.

== | What do you plan to accomplish by the next team meeting?

- Have official tests written and running.

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
    Date: 11/2/2025
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

- It may be beneficial for our team to have a meeting to more specifically discuss
  how the project responsibilities will be split between team members.
