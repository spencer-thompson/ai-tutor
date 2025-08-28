// Prepare and submit a Completion Timeline for your project or thesis, with week by week tasks.
//
// Key suggestion: Be disciplined about setting aside dedicated time to work on this project for about 7-10 hours per week.
//
// Consider a traditional calendar, a flowchart, a color-coded task list, a diagram, or any organizing method that suits you. This may be an update to the outline or timeline you previously created.


#set page(width: 35cm, height: 18cm, margin: 1cm)

#set text(font: "Berkeley Mono", 16pt)
#align(center)[
  #text(navy)[
    = AI TUTOR | Completion Timeline
    Spencer Thompson | Capstone Project
  ]
]

#set text(font: "Berkeley Mono", 12pt)

#v(0.5cm)
#let design = oklch(60%, 0.5, 240deg, 20%)
#let plan = oklch(60%, 0.5, 90deg, 20%)
#let code = oklch(60%, 0.5, 180deg, 20%)
#let docs = oklch(60%, 0.5, 0deg, 20%)
#let refactor = oklch(60%, 0.5, 320deg, 20%)

#align(center)[

  #grid(
    columns: 5,
    row-gutter: 2em,
    column-gutter: 2em,
    [
      #rect(inset: 1em, fill: plan)[
        == PLAN
      ]
    ],
    [
      #rect(inset: 1em, fill: design)[
        == DESIGN
      ]
    ],
    [
      #rect(inset: 1em, fill: code)[
        == CODE
      ]
    ],
    [
      #rect(inset: 1em, fill: refactor)[
        == REFACTOR
      ]
    ],

    [
      #rect(inset: 1em, fill: docs)[
        == DOCS
      ]
    ],
  )
]

#set text(font: "Berkeley Mono", 8pt)

#v(0.5cm)
#line(stroke: silver, length: 100%)
#v(0.5cm)

#grid(
  columns: (1fr,) * 7,
  row-gutter: 2em,
  column-gutter: 2em,
  [
    #rect(inset: 1em, fill: plan, height: 30%, width: 100%)[
      == Week 1
      SEP 1 - SEP 7
      #line(stroke: navy, length: 100%)
      - Plan new features, bug fixes and sprints.

      - Outline team member responsibilities.
    ]
  ],
  [
    #rect(inset: 1em, fill: design, height: 30%, width: 100%)[
      == Week 2
      SEP 8 - SEP 14
      #line(stroke: navy, length: 100%)
      - Design new features and major refactoring.

      - Design how modules and separate code will communicate.

      - Design APIs
    ]
  ],
  [
    #rect(inset: 1em, fill: code, height: 30%, width: 100%)[
      == Week 3
      SEP 15 - SEP 21
      #line(stroke: navy, length: 100%)
      - Rapidly add new features.

      - Accumulate technical debt.

      - Deploy
    ]
  ],
  [
    #rect(inset: 1em, fill: code, height: 30%, width: 100%)[
      == Week 4
      SEP 22 - SEP 28
      #line(stroke: navy, length: 100%)
      - Finish prototype for features.

      - Identify problem areas and technical debt.

      - Deploy
    ]
  ],
  [
    #rect(inset: 1em, fill: code, height: 30%, width: 100%)[
      == Week 5
      SEP 29 - OCT 5
      #line(stroke: navy, length: 100%)
      - Add tests, polish features and fix bugs.

      - Deploy
    ]
  ],
  [
    #rect(inset: 1em, fill: refactor, height: 30%, width: 100%)[
      == Week 6
      OCT 6 - OCT 12
      #line(stroke: navy, length: 100%)
      - Pay back technical debt.

      - Remove as much code as possible until the tutor breaks then fix it.
    ]
  ],
  [
    #rect(inset: 1em, fill: docs, height: 30%, width: 100%)[
      == Week 7
      OCT 13 - OCT 19
      #line(stroke: navy, length: 100%)
      - Write documentation, primarily code documentation of existing and new code.

      - Code comments and READMEs
    ]
  ],

  [
    #rect(inset: 1em, fill: plan, height: 30%, width: 100%)[
      == Week 8
      OCT 20 - OCT 26
      #line(stroke: navy, length: 100%)
      - Plan any changes to features, and overdue fixes.

      - Plan how to pay back more tricky aspects of technical debt.
    ]
  ],
  [
    #rect(inset: 1em, fill: code, height: 30%, width: 100%)[
      == Week 9
      OCT 27 - NOV 2
      #line(stroke: navy, length: 100%)
      - Start or change new features.

      - Accumulate technical debt.

      - Deploy
    ]
  ],
  [
    #rect(inset: 1em, fill: code, height: 30%, width: 100%)[
      == Week 10
      NOV 3 - NOV 9
      #line(stroke: navy, length: 100%)
      - Finish out all features in project scope.

      - Identify technical debt.

      - Deploy
    ]
  ],
  [
    #rect(inset: 1em, fill: refactor, height: 30%, width: 100%)[
      == Week 11
      NOV 10 - NOV 16
      #line(stroke: navy, length: 100%)
      - Major code removal and addition of code comments.

      - Once again delete as much code as possible until the tutor breaks and fix again.
    ]
  ],
  [
    #rect(inset: 1em, fill: code, height: 30%, width: 100%)[
      == Week 12
      NOV 17 - NOV 23
      #line(stroke: navy, length: 100%)
      - Polish out features.

      - Fix bugs.

      - Tweak and enhance tutor behavior.

      - Finish features.
    ]
  ],
  [
    #rect(inset: 1em, fill: refactor, height: 30%, width: 100%)[
      == Week 13
      NOV 24 - NOV 30
      #line(stroke: navy, length: 100%)
      - Major code cleanup.

      - Make sure every file is documented with comments and doc-strings.

      - Aim for maintainability.
    ]
  ],
  [
    #rect(inset: 1em, fill: docs, height: 30%, width: 100%)[
      == Week 14
      DEC 1 - DEC 7
      #line(stroke: navy, length: 100%)
      - Technical Report.

      - Project Report.

      - Analytics Report.

      - Project Finished.
    ]
  ],
)
