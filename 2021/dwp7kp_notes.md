# Notes:
.vue files update live without need for refresh.

# Questions:
- What are credentials to REST query backend?

# Issues:
## Small Tasks
- Professor has a grade?
	- Professor view
	- Select course
	- Grade is displayed at top, but what does it mean? Currently displaying 'Grade: 50' but my one student has a 52.5%. 1 of 2 nodes is yellow for student. This number doesn't seem to change when adding more students and changing grades.

- Grade calculation is whack
	- Student
	- Course -> node
	- Node has 2 assignmetns (each of weight=10). Having a grade of 70 in 1 and no grade in the other produces a node value of 70.

- Student grade doesn't change when competency -> mastery
	- Student view
	- Course
	- See title. When adding a student to a course their initial grade is 50 when joining a class with 2 incomplete nodes.

- Search feature
	- Enrolling students in class
		- Professor
		- Class -> roster
		- Add way to search for when there are hundreds of students. We should also test what this looks like with 100s of students
	- View grades
		- Professor
		- Class -> node -> view grades
		- add lookup
		
- Add error message
	- Edit grades
		- Professor
		- Class -> node -> edit grades
		- Giving a number higher than 100 removes a studen's grade all together. It should prevent the update and display an error message

## Large Tasks
- Grade scope integration

- Enforce authentication for all pages

## Quality of Life
- Edit graph returns to wrong page
	- Professor view
	- Select course -> edit graph -> save
	- Should return back to course page. Currently returns to full professor view.
	
- Professor viewing graph shows as incomplete
	- Professor view
	- Select course
	- All nodes show as red. This isn't very useful. Maybe display stats like submission %, mastery %, and average grade?

- Weight of assignment is not displayed to student
	- Student view
	- Select course -> click nodes
	- only grade is showed, not weight of assignment
	
- When google token expires, cite continues to do things
	- Professor view (at least)
	- Select course -> node
	- Certain boxes weren't showing up, but previously rendered content was still there. There was no indication my token had expired. Refreshing page removed most content. Going back to home page and loging in fixed it. Add something to tell the user their token expired.

- Editing grades does not prompt all students
	- Professor view
	- Course -> node -> edit grades -> student box
	- Clicking in assignment auto promps all assignments. Students does not. Typing one letter and back spacing does show all options

- Night mode option would be nice

- Prevent auto account login. Force you to select which email you want.
