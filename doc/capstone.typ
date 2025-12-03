#set page(margin: 1.5cm)
#set document(
  title: [AI Tutor],
  author: "Spencer Thompson",
)

#show link: set text(fill: blue)
#show link: underline

#set par(justify: true)
#set rect(stroke: silver, inset: 1em, outset: 1em)
#show heading.where(level: 2): set heading(numbering: none)
// #let unary(.., last) = ""
#set heading(numbering: "I |")
#show heading: h => [
  #set text(navy)
  #v(0.2cm)
  #smallcaps(h)
  #v(0.2cm)
]

#set text(16pt, font: "Berkeley Mono")


#v(4cm)
#align(center)[
  #text(navy, 64pt, tracking: 0.02em)[*AI Tutor*]

  #v(-1.1cm)

  #align(center)[
    #grid(
      columns: (0.5fr, 2fr, 0.3fr, 2fr, 0.5fr),
      [], line(length: 100%, stroke: navy), [#text(10pt, super(sym.circle.filled))], line(length: 100%, stroke: navy),
    )
  ]

  #v(-1.4cm)

  #text(navy, 64pt, tracking: 0em)[*Overview*]

  // #line(length: 100%, stroke: 2pt + navy)

  ~
  #v(2cm)

  // #underline(offset: 0.3em)[CS 3310]


  ~

  #text(tracking: 0.04em)[*Spencer Thompson*]

  #v(0.4cm)

  #datetime.today().display("[month repr:long] [day], [year]")
]

#v(2cm)

#show outline.entry.where(
  level: 1,
): set block(above: 2.2em, below: 1.2em)
#show outline.entry.where(
  level: 2,
): set block(above: 1.0em)

// #set text(10pt)
//
#pagebreak()
#outline(indent: 1.5em, title: [Table of Contents], depth: 3)

#set text(11pt)

#pagebreak()


= The Beginning

The AI Tutor project started out of conversations shared from a mutual interest
in realistic capabilities of an exciting new technology.

With #link("https://www.uvu.edu/directory/employee/?id=eXpuVHFkeWcrVkF0N2pvTjdpNmg2dz09")[Dr. Ahmed Alsharif] and
#link("https://www.uvu.edu/directory/employee/?id=ZnBHYXBLNUN3cUgvV2ZNQjFVTEUzdz09")[Dr. Armen Ilikchyan]

== An Idea

The idea was using this new and exciting technology to build an AI assistant for students at UVU.

== AI AI AI

The project was started right around the beginning of 2024, and at the time
AI was buzzing.

- AI Hype

- Interesting tech

== Natural Evolution

- The team

- the scope

- the features

= The Journey

- Exciting work

- Users Users Users

== Roadblocks

- Auth / Permission

== Scrappy Solutions

- JWTs / Extension

== Iterating with Intensity

- Lots of failures

- Wasted code

- Bad ideas

- Quick deployments

= Suffering from Success


== Oh hi canvas

- Users

- Scope creep

- Bugs on Bugs

== Burn it to the Ground

- Quick adoption

== Oh, that's a lot of users

- Dopamine

= The Existential Crisis

- Unsettling feelings

== It's Concious?

- Recursive AI, with code execution

- Scary Capabillities

- Thinking


== Unforeseen Consequences

- If you write code you own it

== Don't you know AI will replace you?

- oof

= The End

- A long journey

- Learned a lot

== Success?

- yea

- lots of users 😎

== Lessons Learned

- Production code is different

- Schemas are really important, and no matter how hard you try they are never enough

- Documentation is really important

== An Exciting Future

- yea idk
