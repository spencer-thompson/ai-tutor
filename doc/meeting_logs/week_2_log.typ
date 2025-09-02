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

  = Week Two Meeting Log

  #v(-0.3cm)
  // #text(12pt)[_Systems of Linear Differential Equations_]
  // #v(-0.6cm)
  #line(length: 50%, stroke: silver)
  #v(-0.6cm)
  #set text(24pt)

  AI Tutor

  #text(11pt, font: "Berkeley Mono")[
    Spencer Thompson | Landon Towers | Keomony Mary

    8/31/2025
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


#v(3cm)


== | What have you done since last team meeting?

- We met with the tech management department at UVU to get the project up and running for them.
  The tech management department has the AI Tutor deployed in their classes.

- We made a plan for the next 14 weeks regarding what work needs to be done.

- We started diving into the code and seeing how it works and what issues need to be addressed first.

  - For example, `gpt-5` is causing some issues that we need to fix

== | What obstacles are you encountering?

- Documentation: There is not enough documentation for the existing code, and some common understanding
  of how everything works is in order.

- Reproducibility: Currently, getting a local development environment up and running is tricky.
  Landon has been working on that, as well as familiarizing himself with the code.

- Communication: Working with a new team is always hard, and we are figuring out how to best do this effectively.

== | What do you plan to accomplish by the next team meeting?

- Fix the immediately important bugs so that production is working as intended.

- Have a development environment working and well documented.

- We all should have a better understanding of the workings of the existing code.

== | Notes

- We are all excited and ready to work hard to make this project excellent.
