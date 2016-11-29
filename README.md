# mealplanner

A simple program that stores a library of recipes, lets you make a weekly meal
plan, and creates a shopping list based on your plan.

## Current functionality

Recipes and ingredients are stored in JSON files in the data directory. Each
recipe describes what ingredients it requires, and in what amount per
person. Each ingredient describes how long it typically lasts.

A meal plan for the week is input at the command line, one day at a time, and
the program will output a shopping list describing what to buy today. Warnings
will be issued for semantically invalid recipes (i.e. unknown ingredient), and
for ingredients which will go bad before being used.
