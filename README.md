# Minij

## Table of contents

* [About](#about)
* [Grammar Explanation](#grammar-explanation)
* [Getting Started](#getting-started)
* [Usage](#usage)
    * [Examples](#examples)
* [Attribution](#attribution)

## About

A toy implementation of a compiler written in python. The compiler supports a language with a syntax
similar to Java.

## Grammar Explanation

The syntax of the language is very similar to the syntax of Java, which is why the tokens are
practically the same. There are some considerations that you should keep in mind, such as:

* The language is **case sensitive**, such that `if` is a reserved word but `IF` is an identifier.
* All the comments must have an end.

### Reserved words

These are a collection of keywords that are predefined identifiers that have special meaning to the
compiler. They cannot be used in your program.

* void
* int
* double
* boolean
* string
* class
* const
* interface
* null
* this
* extends
* implements
* for
* while
* if
* else
* return
* break
* New
* System
* out
* println

### Identifiers

An identifier is a sequence of letters, digits and dollar sign. It can start with anyone except a
number.

```java
// bad
float 1number = 3.4;

// good
int number1 = 1;
int anotherNumber1 = 1;
```

### Comments

The language supports single and multi line comments. This could be useful to explain parts of the
code and make it more readable.

* For single line comments use `//`.
* For multi line comments use `/*` to start and `*/` to end.

### Constants

* The boolean constants are `true` or `false`.

* A integer constant can be expressed in base 10 or base 16.
    * In base 10 it must be only a sequence of digits from 0 to 9.
    * In base 16 it must start with `0x` or `0X` and be followed by any hexadecimal value.

```java
// bad
int bad = 98.1;
int another = .12;

// good
int base10 = 8;
int anotherBase10 = 012;
int base16 = 0X0;
int anotherBase16 = 0x12aE;
```

* A double constant it must be a sequence of digits followed by a point and:
    * A sequence of numbers or nothing.
    * An exponential notation with the sign of the exponent.

```java
// bad
double bad = 32.1.2;
double another = .12;
double badExponential = .2e-3;

// good
double number = 8.;
double anotherNumber = 3.82;
double exponential = 12.E3;
int anotherExponential = 3.2e-2;
```

* The string constant is a sequence of characters surround by `""`, this cannot contain:
    * A double quote.
    * A new line.
    * Null character.

## Getting Started

These instructions will get you a copy of the project up and running on your machine.

### 1. Install dependencies

* [Git](https://git-scm.com/downloads)
* [Python >=3.4](https://www.python.org/downloads/)
* [GNU Make](https://www.gnu.org/software/make/)

### 2. Get the code

sh
git clone https://github.com/betoSolares/minij.git


### 3.Compile

sh
cd minij
pip install -r requirements/build.txt
make build


These should create a directory called `build` with an executable file inside called `minij`.

## Usage

### Examples

## Attribution

You are free to copy, modify and distribute the project with attribution under the terms of the MIT
License. See the [LICENSE](https://github.com/betoSolares/minij/blob/master/LICENSE) file for more
information.

