// #set page(margin: 2cm, height: auto, width: 26cm)
#set page(margin: 1cm)
#set text(24pt, font: "Berkeley Mono", weight: 700)
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

  = Week Fourteen Meeting Log

  #v(-0.3cm)
  // #text(12pt)[_Systems of Linear Differential Equations_]
  // #v(-0.6cm)
  #line(length: 50%, stroke: silver)
  #v(-0.6cm)
  #set text(24pt)

  AI Tutor

  #text(11pt, font: "Berkeley Mono")[
    Spencer Thompson | Landon Towers

    11/23/2025
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

- A lot of issues with our sprint documentation have been fixed, specifically:

  - Backlogs

  - Architecture Diagrams

  - Formatting

  - and more

== | What obstacles are you encountering?

- Landon created a pull request from the `main` branch to bring tests into the code,
  except the main branch has not had development for more than 6 months.
  I have asked him to check in with me when he is getting work done, and to rebase that pull
  request so that the tests are testing the code that is up to date.
  He has not communicated with me or committed this week.

== | What do you plan to accomplish by the next team meeting?

- Fix pull request

- Fixed analytics

- Added UX buttons to select which "role" of the tutor to use.

- Have automated tests running.

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
    Sprint: 4
    // ]
  ],
  [
    // #align(center)[
    Date: 11/23/2025
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
    100%
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
    0%
  ],
  [
    Landon Towers
  ],
  [
    0%
  ],
)

== | Notes

- We have no tests running still.
