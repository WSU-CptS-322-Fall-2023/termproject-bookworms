# Software Requirements Specification

## Your Project Title
--------
Prepared by:

* `Clara Greer`,`<organization>`
* `Tyler Lighthall`,`<organization>`
* `Cristobal Escobar`,`<organization>`

---

**Course** : CptS 322 - Software Engineering Principles I

**Instructor**: Sakire Arslan Ay

---

## Table of Contents
- [Software Requirements Specification](#software-requirements-specification)
  - [Your Project Title](#your-project-title)
  - [Table of Contents](#table-of-contents)
  - [Document Revision History](#document-revision-history)
- [1. Introduction](#1-introduction)
  - [1.1 Document Purpose](#11-document-purpose)
  - [1.2 Product Scope](#12-product-scope)
  - [1.3 Document Overview](#13-document-overview)
- [2. Requirements Specification](#2-requirements-specification)
  - [2.1 Customer, Users, and Stakeholders](#21-customer-users-and-stakeholders)
  - [2.2 Use Cases](#22-use-cases)
  - [2.3 Non-Functional Requirements](#23-non-functional-requirements)
- [3. User Interface](#3-user-interface)
- [4. Product Backlog](#4-product-backlog)
- [4. References](#4-references)
- [Appendix: Grading Rubric](#appendix-grading-rubric)

<a name="revision-history"> </a>

## Document Revision History

| Name | Date | Changes | Version |
| ------ | ------ | --------- | --------- |
|Revision 1 |2023-10-05 |Initial draft | 1.0        |
|      |      |         |         |
|      |      |         |         |

----
# 1. Introduction

This document will outline all of the requirements for the Book App.

## 1.1 Document Purpose

Describe the purpose of the Software Requirement Specification (SRS) document and its intended audience.
The purpose of this Software Requirement Specification document is to clearly outline the 

## 1.2 Product Scope

Identify the product whose software requirements are specified in this document. Explain what the product that is covered by this SRS will do. Provide a short description of the software being specified and its purpose, including relevant benefits, objectives, and goals.

## 1.3 Document Overview

Describe what the rest of the document contains and how it is organized.

----
# 2. Requirements Specification

This section specifies the software product's requirements. Specify all of the software requirements to a level of detail sufficient to enable designers to design a software system to satisfy those requirements, and to enable testers to test that the software system satisfies those requirements.

The book app must have:

* Login/logout 
  * Two types of accounts can log in (admin or user).
  * If a user doesn't have an account they can get directed to an create account.
* Register account
  * Create either a user or admin account.
  * Must input an original username and email to register account.
* Book Reviews
  * Create a review
    * A user can create a review an already established book, or add a new book to the book app library.
    * A review must have a book to be a review of and a rating from five stars.
      * A review can also include a small paragraph or tags but are not required. 
    * Must be a logged in user to create a review.
  * Review interactions
    * Only logged in users can interact with other posted reviews, but anyone can still look at the reviews. (i.e. A user doesn't need to be logged in to read reviews)
    * Interacting includes: commenting and liking. 
    * Users can delete their own posts at any time, admins can delete anyone's post at anytime. 
  * Search/filter
    * Reviews can be searched for by existing books in the library, by key words, or tags.
    * The reviews can also be filtered by time/date, alphabetically, book, star-rating, tags.


## 2.1 Customer, Users, and Stakeholders

A brief description of the customer, stakeholders, and users of your software.

The customer, stakeholders, and users are anyone who has an interest in reading; from the avid bookworm to someone who wants to get into reading.

----
## 2.2 Use Cases

This section will include the specification for your project in the form of use cases. The section should start with a short description of the actors involved (e.g., regular user, administrator, etc.) and then follow with a list of the use cases.

For each use case you should have the following:

* Name,
* Actors,
* Triggers (what initiates the use case),
* Preconditions (in what system state is this use case applicable),
* Actions (what actions will the code take to implement the use case),
* Alternative paths
* Postconditions (what is the system state after the use case is done),
* Acceptance tests (list one or more acceptance tests with concrete values for the parameters, and concrete assertions that you will make to verify the postconditions).

Each use case should also have a field called "Iteration" where you specify in which iteration you plan to implement this feature.

You may use the following table template for your use cases. Copy-paste this table for each use case you will include in your document.

~~~ Actors ~~~
Logged-in user      - A user logged in with a regular user account.
Not-logged-in user  - A user not logged in. 
Admin               - A user logged into an admin account

| Use case # 1      |   |
| ------------------ |--|
| Name              | "enter your reponse here"  |
| Users             | "enter your reponse here"  |
| Rationale         | "enter your reponse here"  |
| Triggers          | "enter your reponse here"  |
| Preconditions     | "enter your reponse here"  |
| Actions           | "enter your reponse here"  |
| Alternative paths | "enter your reponse here"  |
| Postconditions    | "enter your reponse here"  |
| Acceptance tests  | "enter your reponse here"  |
| Iteration         | "enter your reponse here"  |

| Use case # 1      |   |
| ------------------ |--|
| Name              | "enter your reponse here"  |
| Users             | "enter your reponse here"  |
| Rationale         | "enter your reponse here"  |
| Triggers          | "enter your reponse here"  |
| Preconditions     | "enter your reponse here"  |
| Actions           | "enter your reponse here"  |
| Alternative paths | "enter your reponse here"  |
| Postconditions    | "enter your reponse here"  |
| Acceptance tests  | "enter your reponse here"  |
| Iteration         | "enter your reponse here"  |

----
## 2.3 Non-Functional Requirements

List the non-functional requirements in this section.

You may use the following template for non-functional requirements.

1. [Enter a Concise Requirement Name]:  [provide a concise description, in clear and easily understandable language to specify the requirement]

----
# 3. User Interface

Here you should include the sketches or mockups for the main parts of the interface.

----
# 4. Product Backlog

Here you should include a link to your GitHub repo issues page, i.e., your product backlog. Make sure to create an issue for each use case. You should also create issues for the initial development tasks that you plan to work on during iteration1. 

----
# 4. References

Cite your references here.

For the papers you cite give the authors, the title of the article, the journal name, journal volume number, date of publication and inclusive page numbers. Giving only the URL for the journal is not appropriate.

For the websites, give the title, author (if applicable) and the website URL.

----
----
# Appendix: Grading Rubric
(Please remove this part in your final submission)

These is the grading rubric that we will use to evaluate your document. 

| Max Points  | **Content** |
| ----------- | ------- |
| 10          | Do the requirements clearly state the customers’ needs? |
| 5           | Do the requirements avoid specifying a design (note: customer-specified design elements are allowed; non-functional requirements may specify some major design requirements)? |
| | |  
|    | **Completeness** |
| 25 | Are use cases written in sufficient detail to allow for design and planning? |
| 4 | Do use cases have acceptance tests? | 
| 25 | Is your use case model complete? Are all major use cases included in the document? |
| 10 |  Are the User Interface Requirements given with some detail? Are there some sketches, mockups?  |
| | |  
|   | **Clarity** |
| 5 | Is the document carefully written, without typos and grammatical errors? |
| 4 | Is each part of the document in agreement with all other parts? |
|   | Are all items clear and not ambiguous? (Minor document readability issues should be handled off-line, not in the review, e.g. spelling, grammar, and organization). |
|   |   |
|    | **GitHub Issues** |
| 12 | Has the team setup their GitHub Issues page? Have they  generated the list of user stories, use-cases, created milestones, assigned use-cases (issues) to milestones?   Example GitHub repo (check the issues): https://github.com/WSU-CptS322-Fall2022/TermProjectSampleRepo/issues  |

