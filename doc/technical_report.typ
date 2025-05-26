#set page(margin: 1.2cm)
#set text(28pt, font: "Berkeley Mono", weight: 700)
#set enum(indent: 1em)
#set list(indent: 1em)
#set math.mat(align: center, delim: "[", gap: 0.75em)
#set math.vec(align: right)
#set math.cases(gap: 0.5em)
#set table(align: left)
#set par(justify: true)
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

This project, the AI Tutor, is a project that has now been under development for quite some time.
We have seen some exciting success regarding utilizing artificial intelligence in real world application.

This report outlines Why, How, and What this project is all about, with a focus on the technical design, implementation and solution.

== Background

As previously mentioned, the AI Tutor project started back in early 2024.
In discussions with the excellent faculty in Tech Management Department at Utah Valley University,
we hypothesized that using the new and exciting technology of large language models,
we could provide excellent, _personalized_ tutoring to students 24/7.

So we set out to develop a simple application to accomplish this goal.
The original AI Tutor was indeed a success.
Quickly the project gained attention among multiple departments and more than a handful of students.
Although, given the rather breakneck pace of development, there was a rather rapid accumulation of technical debt.
Some of the core features that we wanted had become quite difficult.

After the original scope of the project had been completed, we still had a desire to have a system that was better suited for both students and professors.
As the lead developer, I had the feeling that a fresh start might be better than attempting to pay down a significant amount of technical debt.
Therefore, this report is particularly focused on:

- The evolution of the project as a whole.

- The features that gives the AI Tutor an advantage over *every other alternative*.

- The design and implementation of the tutor, as well as the challenges faced along the way.

=== Context

A rather interesting piece of context to keep in mind while reading this report is that: during the duration of this project, every single piece of technology has changed *drastically*.
Oftentimes the APIs or services that we were utilizing evolved or changed overnight.
This could possibly be attributed to the incredible amount of development and hype around the use of generative AI.

The point being, many other competitors both at our own university and others, were quickly building and iterating on similar ideas.
Our team built and deployed *two* complete iterations, while other teams have yet to deploy their projects.

=== Purpose

From the beginning our project was focused on providing a rather niche ideal.
We all had this idea of a tutor or assistant that had intimate knowledge of a student's courses.

== Goals

Primarily we wanted:

- 24/7 access to students to assist with coursework.

- Personalized responses to student questions that were unique to _each_ student.

- Answer questions about the syllabus, upcoming assignments, grades and more.

The hope and idea being that, this could be an incredibly valuable resource for students, faculty and the university as a whole.

== Limitations

During the duration of this project, there were really two main issues.

1. Incredibly Busy Semester.

2. Canvas API Key Permissions.

The first problem is simply that the developer team and I had incredibly difficult and loaded semesters.
In addition, we had several other job opportunities open up.
Given that graduation is just over the horizon, it is absolutely true that this somewhat hindered our development.

Regardless though, this first problem pales in comparison to the other.
Our university had a competing team that was also working on an AI assistant.
We diligently attempted to work with this other team, over the course of a year,
but they were obstinate, they insisted that they wanted to hire outside talent.

Part of this problem was that they were unwilling to give us an API Key.
This could also have been university permissions issue.

*Not having* a proper API Key was a truly difficult challenge.
Especially given that our team had already deployed to active courses, while they had not.

= Design

The overall design of the project can be a bit confusing at first. Really there are *five* major distinct pieces.

- *Browser Extension*
  - For user authentication and communication with the Canvas API.

- *Frontend*
  - The chat interface for using the AI Tutor.

- *Backend*
  - Where all the data processing and external API calls happen.

- *Analytics*
  - The service that monitors and displays the user Telemetry data.

- *Database*
  - Where we store everything we need.

== Data

The order in which each piece will be explained is the rough order that they function.
As a whole, the system is essentially two data pipelines with a unified user interface.
Essentially these two pipelines are:

- Analytics
  - Telemetry and usage data gathered from students.

- Canvas
  - Student data regarding assignments, courses, submissions, etc.

=== Pipeline

While the analytics data is interesting and deserves its own time in the spotlight, it is not the focus of the project.

The Canvas data is really where things get interesting.

- I knew that we needed to grab data from the Canvas LMS, which is #link("https://github.com/instructure/canvas-lms")[#text(blue)[#underline[Open Source]]].
  After thoroughly reading the documentation and looking into the source code, I knew I was on the right track.

- We also needed to process that data and cross reference it with our own users.

- Lastly, we needed a way to securely store and retrieve our mix of user data and course data.

$
  "Canvas" quad arrow quad "Our Code" quad arrow quad "Storage"
$

=== Analytics

From the beginning, we also knew that we wanted to get some data to attempt to answer the question:

#align(center)[
  *Does AI Tutoring help students?*
]

~

In addition to the data pipeline, we also needed a smaller pipeline to get user telemetry data to dive into answering this question.

== AI Behavior

From the first iteration of the AI Tutor, we knew that the behavior of the AI Tutor itself was particularly important.
It was difficult just to get the tutor not to send super long messages, let alone get it to answer questions with a high accuracy.
We needed something extra to get the results that we wanted and needed.

= Implementation

// TODO:
- Lessons Learned from first iteration

#figure(image("ai-tutor-2-diagram-light.png"), caption: "AI Tutor Infrastructure Diagram")

== Infrastructure

- Hetzner VPS
// TODO:
- Cost reduction
- Docker & Compose

== Security

- JWT
- Keys
- SSH
- 2FA?

== Frontend

// TODO:
- User Interface
- Prioritize good User Experience

=== Browser Extension

- Side panel
// TODO:
- Cookies

=== Chat Interface

- Streamlit
// TODO:

== Backend

- FastAPI
// TODO:

=== AI

- OpenAI API
// TODO:

=== Tools

- Catalog
// TODO:
- Upcoming Assignments
- Grades

=== Telemetry

// TODO:
- Plausible Analytics

== Database

- MongoDB
// TODO:
- Document Based

= Challenges

// TODO:
== Permissions

- UVU
// TODO:
- Competing Team

== API Inconsistency

// TODO:
=== Canvas LMS
// TODO:

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
