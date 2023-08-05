# Calcli
A command-line calculator made with python.

## Operators

'+' - add two numbers
'*' - multiply two numbers
'-' - subtract two numbers
'/' - divide two numbers
'^' - raise a number to power of other number
'|x|' - the absolute value of x
'x!' - factorial of x

### relational operators
'==' - returns 1 if two numbers are equals, else it returns 0
'>=' - returns 1 if a number is greater than or equals to other number, else it returns 0
'<=' - returns 1 if a number is less than or equals to other number, else it returns 0
'!=' - returns 1 if two numbers are different, else it returns 0
'<' - returns 1 if a number is less than other number, else it returns 0
'>' - returns 1 if a number is greater than other number, else it returns 0

## Negative values

Negative values must be between parentesis, in format (-x)


## functions

Some integrated functions (cannot be created more):
  1. sqrt(x) - returns the square root of x
  2. ctrt(x, y) - returns the y-root of x (x^(y^-1))
  3. perc(x) - returns the decimal shape of x percent
  4. perm(x) - returns the decimal shape of x permile
  5. receive() - returns the expression typed by user

examples:
  ```
$ ~ python3 parser.py
expression > sqrt(9)
3.0
expression > ctrt(27, 3)
3.0
expression > perc(93)
0.93
expression > perm(93)
0.093
expression > receive()
... 7 * 4
28
expression > .q
  ```


## extras

### variables and constants
`name = expr` for variables and `$name = expr` for constants

delete a variable typing `#{var name}`

### conditional lines
`(relational expression) -> onTrue [: onFalse|: (relational expression) -> elif ...]`
example:

```
$value = receive()
## if-then
(value == 6) -> 1

## if-then-else
(value == 6) -> 1 : 0

## if-then-elif-then...
(value == 6) -> 1 : (value == 8) -> 2 : 0

```

### loops
run a expression n times:
`[n] -> expr`

example:

```
[3] -> receive() + 1
... 4
5
5
5
```

### ranges
create a list with numbers:
`{start...end [-> steps]}`

example:
```
expression > a = {1...10}
expression > a
[1, 2, 3, 4, 5, 6, 7, 8, 9]
expression > a[0]
1
expression > a[-1]
9
expression > #a
expression > b = {1...100 -> 2}
expression > b[-1]
98

```
