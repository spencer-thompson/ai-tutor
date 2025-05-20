#set page(margin: 1.2cm)
#set text(28pt, font: "Berkeley Mono", weight: 700)
// #show math.equation: set text(font: )
#set enum(indent: 1em)
#set list(indent: 1em)
#set math.mat(align: center, delim: "[", gap: 0.75em)
#set math.vec(align: right)
#set math.cases(gap: 0.5em)
#set table(align: left)
#show heading: h => [
  #set text(navy, weight: 700)
  #v(0.3cm)
  #h
  #v(0.1cm)
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

#v(1cm)
#align(center)[

  #text(navy, 40pt, weight: 700)[AI Tutor]

  #v(-1.2cm)
  #line(length: 50%, stroke: silver)

  #v(-0.8cm)
  #text(14pt, weight: 400)[_Technical Report_]
  // #v(-0.6cm)

  #set text(16pt)
  Spencer Thompson

]

#show outline.entry.where(level: 1): set block(above: 1.2em)
#set heading(hanging-indent: 0.78cm, numbering: "1.")
#set text(11pt, font: "Berkeley Mono", weight: 400)
#v(0.4cm)
#outline(title: smallcaps("Table of Contents"))


= Introduction

== Background

- Version 2
- Complete rewrite

=== Context

- AI Hype

=== Purpose

- Custom personalized tutoring
- 24/7 access

== Scope

=== Goals

=== Limitations

- Other opportunities
- A very difficult semester

= Design

- Browser Extension

== Data

=== Analytics

=== Pipeline

=== Storage


== Security

- JWT
- Keys
- SSH
- 2FA?

== AI Behavior

- Class specific behavior / answers

= Implementation

- Lessons Learned from first iteration

== Infrastructure

- Hetzner VPS
- Cost reduction
- Docker & Compose

== Frontend

- User Interface
- Prioritize good User Experience

=== Browser Extension

- Side panel
- Cookies

=== Chat Interface

- Streamlit

== Backend

- FastAPI

=== AI

- OpenAI API

=== Tools

- Catalog
- Upcoming Assignments
- Grades

=== Telemetry

- Plausible Analytics

== Database

- MongoDB
- Document Based

= Challenges

== Permissions

- UVU
- Competing Team

== API Inconsistency

=== Canvas LMS

- Name vs Course Code

=== Plausible Analytics

- Weirdest API I have ever seen
- Cartesian products galore

== Messy Data

- Canvas
- My own Design

=== Live Service

- Developing / Adding features for an application in use is difficult

= Solutions

== Workarounds

- Browser Extension

== Clever Tricks

=== Authentication

- JWT / Cookie

= Conclusion

== Findings

== Implications

// https://excalidraw.com/#json=JBsUsLgMPG4HTt90L85BY,f4kdzGTYkBLF-bAs9NdQxA
