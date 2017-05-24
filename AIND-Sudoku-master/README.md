# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
How do we use constraint propagation to solve the naked twins problem?  
Constraint propagation is a method for reducing the search space by applying constraints and reducing the number of possibilities.
The basic idea of constraint propagation is to detect and remove variables that are no longer required to be included, by repeated analysis and evaluation of the constraints.

In the Naked Twins problem, we evaluate each unit repeatedly to remove numbers from possible values. Unit in this case can be either a row, a column or a grid.Within the unit we look for cells with only two possibilties and check if there are duplicates to it.We can detect digits in the duplicates which cannot be used among other cells in the unit.Like in the example below, '23' which is a duplicate in column 3 and other items in column 3 cannot have 2 or 3 and thus need to be removed.
<img src='naked-twins.png'>

This kind of constraint propogation in Naked Twins is a perfect way to eliminate possibilities and reduce search space.


# Question 2 (Diagonal Sudoku)
How do we use constraint propagation to solve the diagonal sudoku problem?  
Diagonal sudoku is like a regular sudoku where the numbers 1-9 has to appaear only once along the 2 diagonals.In our solution we add the diagonal units to the peer group and overall units and thereby the strategy we use for "Eliminate" and "Only_Choice" works fine here also.

We device the eliminiate strategy by focusing on the constraint that if a box has a value assigned, then none of the peers of this box can have this value. In this case, peer of a box can be its rows,columns, 3 x 3 grid or other diagonal items.Eliminate strategy can be effectively used for reducing the number of items. 

When there is only one choice for a digit in a box, then that digit must be assigned to that box.This strategy is called "only_choice", which can be applied to all units for eliminating items.

