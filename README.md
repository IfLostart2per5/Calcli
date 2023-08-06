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
'==' - returns 1 if two numbers are equals, else it returns 0.  
'>=' - returns 1 if a number is greater than or equals to other number, else it returns 0.  
'<=' - returns 1 if a number is less than or equals to other number, else it returns 0.  
'!=' - returns 1 if two numbers are different, else it returns 0.  
'<' - returns 1 if a number is less than other number, else it returns 0.  
'>' - returns 1 if a number is greater than other number, else it returns 0.  

## Negative values

Negative values must be puted between parentesis, in format (-x)


## functions

Some integrated functions (cannot be created more):
  1. sqrt(x) - returns the square root of x  
  2. ctrt(x, y) - returns the y-root of x (x^(y^-1))  
  3. perc(x) - returns the decimal shape of x percent  
  4. perm(x) - returns the decimal shape of x permile  
  5. receive() - returns the expression typed by user  

example:
```
/>> sqrt(9)
3.0
/>> ctrt(27, 3)
3.0
/>> perc(93)
0.93
/>> perm(93)
0.093
/>> receive()
... 7 * 4
28
/>> .q
  ```


## extras

### variables and constants
`name = expr` for variables and `$name = expr` for constants.  
  

delete a variable typing `#{var name}`  

create a posterior-assignment variable typing `post {var name}`  

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


### ranges and lists

create a range with numbers:  
`{start...end [-> steps]}`  

create a list with numbers:  
`{n1, n2, n3, ..., n_n}`  

ranges example:  
```
/>> a = {1...10}
/>> a
[1, 2, 3, 4, 5, 6, 7, 8, 9]
/>> a[0]
1
/>> a[-1]
9
/>> b = {1...100 -> 2}
/>> b[-1]
98
```

list example:  
```
/>> list = {1, 4, 3, 6}
/>> list[0]
1
/>> list[1]
4
/>> .q
```

### lazy ranges and lists
create a lazy range/list adding a '@' at the final of the list/range.
  
Note:  
Its running generator expressions at the backend  

```
/>> a = {1...10@}
/>> ## access each element with arrow index ([->]) syntax
/>> a[->]
1
/>> a[->]
2
/>> #a
/>> b = {1...10 -> 2@}
/>> b
[1, 3, 5, 7, 9]@lazy_mode
/>> b[->]
1
/>> b[->]
3
/>> b[->]
5
/>> #b
/>> c = {2, 5, 3, 9@}
/>> c[->]
2
/>> c[->]
5
/>> c[->]
3
/>> c[->]
9
/>> c[->]
Erro: a expressão geradora acabou
/>> c
Valor c não foi declarado
/>> .q
```

note too that when occurs the end of the lazy list, it is deleted.

