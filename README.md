todo
====

A very primitive Flask web app written for myself in order to keep
track of the different projects I'm working on.

Problems with the implementation include:

- Possible race conditions with the MongoDB access.
- There's very limited checking of form input.
- Using the names of the todo items as their ids.  This limits the
  possible choices of names in order to not mess up jQuery and
  database operations.

Since I am the only user I don't mind the above problems.

The site is deployed at Heroku:
[https://michaels-todo.herokuapp.com/](https://michaels-todo.herokuapp.com/).
