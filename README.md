# SOEN487 Web Services and Applications
## Assignment 1
### Winter 2019
### Prof: Denis Rinfret

## Developing and testing a service to access and modify a database

Starting from the start-up code provided, you have to use SQLAlchemy
to design and create a database, create views to access and modify
the data in your database, and create unit and functional tests to
test your service.

This assignment has to be done __individually__.

### Step 1: Design your database

Your database should contain at least 3 base tables, and they should be
connected through some relationships. You have to use SQLAlchemy to
create the models and to create the necessary relationships by using
foreign keys and back references (or other similar SQLAlchemy constructs).

_You can choose any meaningful topic you want for your DB_.
It is OK to use something related to your project, but this assignment
must be done individually, not as a group.

You must produce a model dependency diagram in PNG format to document
your DB. It should include the fields of each model.
_Note_: that's very easy to do with PyCharm.

You must use SQLite for your DB for this assignment.

### Step 2: Create the views

__Note: if you follow the TDD methodology, you should do step 3 before
this step.__

Create the views in a similar style to the views created for `Person`.
You might not need to have a `Person` model in your DB, therefore
don't leave it there if you don't need it.

You will probably end up with too many views, so splitting up your
views into many files and grouping these files in a subfolder is
probably a good idea. You could also use _Flask Blueprints_ for this.

You should have views for each model, to get all instances of the model
or a specific one by id or by any appropriate search condition. You
should also have views using `POST`, `PUT` and/or `DELETE` methods to update
the database. If appropriate, you could also have views that will add
instances of 2 related models at the same time to avoid dependency
problems.

### Step 3: Test your views

Write functional tests not only for each view, but also for each possible
case of each view. Test your views with good and bad data. You must
validate the data and handle exceptions correctly. You might also need
to write unit tests for your helper functions if necessary.

## Deliverables and grading

- A private Git repository located on BitBucket or GitHub, shared with
denis.rinfret@concordia.ca . Make sure to share it with the correct
email address to avoid sharing it with another account with a similar
name.
- Grading overview:
    - Database, including models and diagram: 20%
    - Views: 40%
    - Tests: 20%
    - Peer review of 2 other assignments: 20%
- __Note__: Participation in the peer review process is mandatory to
receive grades for the assignments. More details about the peer review
will be provided later.
- __Due Wednesday February 13, 2019 before midnight.__