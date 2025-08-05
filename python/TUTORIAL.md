# The Lambda REPL

Welcome to the lambda REPL.

You can enter a lambda term at the prompt to see its result under
normal order beta reduction; use backslash (\\) for the lambda symbol.

Some examples:

```
\x.x

\x.\y.x

(\x.\y.x \x.x)
```

This works for all lambda terms, though the result is interesting
normally only for application terms. Upon evaluation, fresh names are
generated for *local* values, since the original ones are discarded
due to the use of DeBruijn indices to avoid name-clashes.

As a side note, the Python
[wonderwords](https://wonderwords.readthedocs.io/en/latest/index.html)
package is used when pretty-printing an evaluated AST for generating
random dictionary words that substitute for the original names. Hence

`\x.x`

might get printed back to the user as

`\voting.voting`

## Syntax

The REPL supports evaluating classic lambda calculus expressions, with
some divergence from convention, inspired mostly from Greg
Michaelson's excellent book, *An Introduction to Functional
Programming Through Lambda Calculus* (Dover, 2011).

### Application
In this implementation, parentheses are always required for
application, which naturally requires at least two arguments. However,
more than two arguments are allowed; such an expression is desugared
into a left-fold of successive binary applications. Example:

`\x.\y.\z.(x y z)`

gets desgurared into

`\x.\y.\z.((x y) z)`

and is evaluated from there.

In my opinion, this results in more visually intuitive code. For
example, the traditional way to write the first expression above would
be as

`\x.\y.\z.x y z`

which to a naive reader presents itself as an expression involving
three separate terms, when in fact it's a single term.

### Assignment Statements
Assignment statements can also be used to create persistent
definitions. The list of names between the assignee and the `:=` are
considered as function *parameters*:

`def identity x := x`

Abstractions are still allowed to appear on the right side, and so the
following are equivalent:

```
def apply fn arg := (fn arg)
def apply fn := \arg.(fn arg)
def apply := \fn.\arg.(fn arg)
```

Generally speaking, this implementation works precisely as would be
implied by the preceding illustration: moving parameters to the right,
thus constructing an equivalent lambda abstraction.

For the time being, assignment is only allowed at the top-level.

#### How it's done

