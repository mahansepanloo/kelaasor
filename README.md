Certainly! Below is a structured outline for your README that includes the functionality you've described for the accounts, classes, exercises, and forum components of your application. You can customize or expand upon it as needed.

---

# Project README

## Table of Contents
1. [Accounts](#accounts)
   - [Register](#register)
   - [Login](#login)
   - [Change Password](#change-password)
   - [Edit User](#edit-user)
   - [User Info](#user-info)
   - [SMS Sending System](#sms-sending-system)
   
2. [Classes](#classes)
   - [Create Class](#create-class)
   - [Add Public Class](#add-public-class)
   - [Add User to Private Class](#add-user-to-private-class)
   - [Add Private Password](#add-private-password)
   - [Add Private Email Class](#add-private-email-class)
   - [Edit Class](#edit-class)
   - [Sub Create Class](#sub-create-class)

3. [Exercises](#exercises)
   - [Create Exercise View](#create-exercise-view)
   - [Sub Criteria Create](#sub-criteria-create)
   - [Edit Exercise View](#edit-exercise-view)
   - [Create Group Manual](#create-group-manual)
   - [Create Group Auto](#create-group-auto)
   - [Submit Answer](#submit-answer)
   - [Answer Create Judge](#answer-create-judge)
   - [All Answers](#all-answers)
   - [Score Text Answer](#score-text-answer)
   - [Ranking View](#ranking-view)
   - [Register User Scores](#register-user-scores)
   - [Alert System](#alert-system)
   - [Change Group Members' Scores](#change-group-members-scores)
   - [Download Question Files](#download-question-files)

4. [Forum](#forum)
   - [Question List Create View](#question-list-create-view)
   - [Answer Question Create View](#answer-question-create-view)

---

## Accounts

### Register
- Users can register through the system, which sends an OTP via SMS for verification.

### Login
- Authentication is based on JWT tokens.

### Change Password
- Users can change their password using an OTP.

### Edit User
- Users can edit and view their information except for the password and logout status.

### User Info
- Displays user activity, including class lists, register statuses, and grades.

### SMS Sending System
- SMS messages are sent through `utils` in the app.

---

## Classes

### Create Class
- Displays the classes of a teacher.
- Allows the creation of new classes.

### Add Public Class
- Enables users to join public classes.

### Add User to Private Class
- Adds a user to private classes, sending email invitations or passwords via Celery (email settings in the app).

### Add Private Password
- Users can join private classes using the sent password.

### Add Private Email Class
- Users can join private classes using the sent invitation link.

### Edit Class
- Displays class information.
- Allows editing of class details.
- Enables removal of students from classes.

### Sub Create Class
- Displays grades.
- Allows creation and deletion of grade entries.

---

## Exercises

### Create Exercise View
- Displays class questions.
- Allows adding questions to the class.
- Supports adding questions to the inbox and pulling from inbox to questions.

### Sub Criteria Create
- Creates and edits scoring criteria for questions.

### Edit Exercise View
- Allows editing of existing questions.

### Create Group Manual
- Facilitates manual creation of groups.

### Create Group Auto
- Facilitates automatic group creation.

### Submit Answer
- Allows submission of answers, which can be graded by the instructor or TA.

### Answer Create Judge
- Records answers, with automated grading.

### All Answers
- Displays all responses related to questions.

### Score Text Answer
- Involves grading by the instructor or TA.
- Displays the answer.
- Allows editing of the given score.

### Ranking View
- Displays the ranking of students within the class.

### Register User Scores
- Records detailed scores for students.

### Alert System
- Implements alerts for students regarding question changes or updates based on SIGNALS.

### Change Group Members' Scores
- Enables modification of scores for group members.

### Download Question Files
- Allows downloading of question files.

---

## Forum

### Question List Create View
- Facilitates the submission of questions.

### Answer Question Create View
- Enables responses to questions.

---

Feel free to modify any section or add additional details as necessary!
