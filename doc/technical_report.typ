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
#v(1cm)
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

~

#line(length: 100%, stroke: silver)

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

~

#line(length: 100%, stroke: silver)

= Implementation

In the first iteration of the AI Tutor was relatively stateless. It did not have a backend, and it did not have a database.

This was quite limiting in term of functionality, and therefore, this time around we had a complete redesign of the entire system.
Initially we just had a frontend with _too much_ functionality, and we hosted that on Google Cloud.

#figure(image("ai-tutor-2-diagram-light.png"), caption: "AI Tutor Infrastructure Diagram")

== Infrastructure

This time around we wanted to have something more robust with the ability to add one or two entire dimensions of features.
Given that we initially hosted on Google Cloud, and didn't really use any of the features of the Google Cloud except for the compute engine,
we decided to use something more cost effective and simple.

We settled on using a virtual private server from Hetzner.
This decision probably saved us \$40 to \$50 dollars a month, I would estimate that we saved an order of magnitude of money by switching to Hetzner.

Something that we didn't change from the first AI Tutor was that we used Docker and Docker compose.
Docker has made everything much easier to deploy as well as iterate quickly.
Using *Traefik* also made this process of development and deployment faster and less painful.

== Security

This bit of implementation was perhaps one of the most clever and interesting pieces of the project as a whole.
Coming back to the limitations that I mentioned previously, we did not have access to a developer API key.
We had expended a tremendous amount of effort to do this, but with no success.
There was a point where hope was starting to be lost, although, perhaps it was pure stubbornness or competition with the official UVU team, I *had* to find a solution.

I had already created a personal API key, and I toyed with the idea of having each user create an API key,
but knew that it would be too much an impediment to the user experience.

*So*, I decided to get creative. In the process of trying to make something incredibly secure, yet give us access to the data we needed, I realized that we could use the _JavaScript Console_ in the browser.
This shouldn't be a surprise to anyone in web development, but I was curious if I could make an API request from the console.
Assuming it wouldn't work I gave it a try. To my surprise I got back exactly what I had requested from the API.

At this moment, I was surprised that there was no protection against this kind of request, but I knew that most likely there were CORS (Cross-Origin Resource Sharing) limits / restrictions.
These are usually included by default on many web applications so that you have to explicitly allow a URL or service to access information.

So I got to thinking, is this something that we could make work? I realized that a browser extension, can indeed run arbitrary JavaScript to interact with a website as long as the user gives permission.
*As long as* the CORS policy allowed browser extensions, which I doubted heavily for security reasons, than this could totally work.

I whipped up a quick little browser extension and tested it out. Sure enough it worked like a charm.

- This was a *truly incredible moment*.

Given this discovery, I decided that we would use a browser extension to provide pseudo-access to the Canvas API.
For authentication, we just had the browser extension set a cookie on the site as a JSON web token.
This simplified and almost removed security as a concern because we could just use the current users existing login as our login.

Further still, our database, and sensitive data is not accessible from the outside web, so in order to get data, a request would need a valid JSON web token as well as an API key that I created.

I can confidently say that our site is incredibly secure.

== Frontend

Something important to our team is that we wanted to have a really solid user experience.
Given the constraint that we had a small team, with experience focused on data, this was an interesting challenge.

The first iteration of the project used a library for creating simple websites called #link("https://streamlit.io/")[#text(blue)[#underline[Streamlit]]].
This library made it incredibly easy to create and deploy very simple websites.

Another option that we considered is to use a different library, #link("https://svelte.dev/")[#text(blue)[#underline[Svelte]]], which was more in depth.

=== Chat Interface

In the end we settled on both, initially though we focused on Streamlit, and created a beta written in Svelte.

At first Streamlit was excellent, there was already a lot of easy ways to build AI chat applications, although after two or three months, it became apparent that Streamlit didn't have everything that we needed.
We managed to implement some rather hacky and interesting solution to this problem with Streamlit, but still we wanted a better solution.

We then decided to dive into the Svelte option. We didn't get quite to a position that we were satisfied with, but it was very cool nonetheless.
Svelte gave us the freedom we really wanted, but also required a lot more effort to design and implement everything we needed.

=== Browser Extension

The browser extension that I mentioned earlier is the key step of not only authentication but also the data pipeline for Canvas / course data.
For Google Chrome and Chromium based web browsers we also configured the extension to provide a side bar on *any site* to access the tutor.
This feature turned out to be truly a favorite among users which was cool, even though it was a small addition.
We simply just embedded the streamlit frontend as an Iframe within the side panel.

== Backend

I knew that at its heart, this project needed a brain, or central area to take care of the heavy lifting.

After some research #link("https://fastapi.tiangolo.com/")[#text(blue)[#underline[FastAPI]]] looked like an excellent option.
I just wanted something that we could use to offload the functionality, and create a barrier of sorts for security and clean design.
FastAPI worked excellent for this.

Essentially, FastAPI just lets you as a developer write functions with decorators, and the function becomes the API (http) endpoint.
There are great support, examples, and documentation.

=== AI

This is an *AI* Tutor after all, and we had some chaos this time around.
Primarily, I am talking about providers.
Originally we had a grant from #link("https://openai.com/")[#text(blue)[#underline[OpenAI]]] that we were using for credits to provide chat completions.

Although, one day recently after deployment, our credits were not working.
Within a couple hours, I had completely switched us over to using the #link("https://www.anthropic.com/")[#text(blue)[#underline[Anthropic]]] API.
Even though we didn't stay with Anthropic, I do think it is interesting to note that their AI behavior seemed to be more emotionally intelligent than OpenAI.

=== Tools

The real magic of the AI though, is the tool use / function calling.
This functionality is what really made this version of the AI special and unique.
This features essentially allows the AI to choose a _tool_, which is essentially just a defined JSON schema.
Then when generating a response, the tool call itself can be extracted and used in code.

The tools that we gave to our AI Tutor are:

- Grades
  - Show grades of assignments and courses overall.

- Course Questions
  - Access to information about upcoming assignments, recently submitted assignments, discussions, announcements, and more.

- Catalog
  - Access to the UVU course catalog with information about prerequisites, credit hours and more.

- Read Webpages
  - If the user pasted a URL or URLs, the AI could read those pages for the user.

- Execute Python Code
  - If calculation or precision was needed the AI could execute python code in a sandboxed environment.

These tools really made the AI feel and be truly useful to users.

=== Telemetry

As I have mentioned previously, we needed to collect some telemetry in order to answer some research questions.
As I had experience with #link("https://plausible.io/")[#text(blue)[#underline[Plausible Analytics]]],
I setup the self hosted version and collected data about how our users use the site.
One of the reasons I like Plausible is that it is privacy conscious.

#figure(image("plausible.png"), caption: "Plausible Analytics Dashboard")

== Database

The last portion of the implementation is the database.
After seeing the data that was coming back from the Canvas API, I just felt uncomfortable dealing with the inconsistencies of that data.
SQL didn't necessarily feel quite right.

So, we decided to go with #link("https://www.mongodb.com/")[#text(blue)[#underline[MongoDB]]], a document based database.
The real reasons why this decision was made are:

- We had a lot of JSON data, which fit well into Mongo.

- Saving chats would be incredibly easy.

- It would allow very quick prototyping and iteration.

This turned out tremendously well.

~

#line(length: 100%, stroke: silver)

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

~

#line(length: 100%, stroke: silver)

= Solutions

== Workarounds

- Browser Extension

== Clever Tricks

=== Authentication

- JWT / Cookie

~

#line(length: 100%, stroke: silver)

= Conclusion


== Findings

== Implications

// https://excalidraw.com/#json=JBsUsLgMPG4HTt90L85BY,f4kdzGTYkBLF-bAs9NdQxA
