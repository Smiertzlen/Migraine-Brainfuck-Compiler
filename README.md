## Migraine-Brainfuck-Compiler
A compiler from a selfmade programming syntax (migraine) to brainfuck.

This is the current devopment status:

# Currently implemented:
- variables
- variable modification
- arithmetic calculations
- several operators

# Operators:
- &#43; (addition)
- &#45; (subtraction)
- &#42; (multiplikation)
- ! (not)
- && (logical and)
- || (logical or)
- -& (logical nand)
- -| (logical nor)
- ^^ (logical xor)
- -^ (logical xnor)
- == (equals)
- -= (not equals)
- <= (lower or equals)
- &#62;= (greater or equals)
- < (lower)
- &#62; (greater)
- &#35; (Comment - one line)
- (...) (paranthesis)

Paranthesis are correctly evaluated

# Output:
The `print` command is ready to use. It can either output a string, or a variable value. Combination of the two and a new line operator are not implemented yet.

# Missing operators:
- / (division)
- % (modulo)

# Currently known issues:
1. In the test_1.mico, two for loops are used. Yet the console output is not correct.
2. All operators have not yet been thoroughly tested. Bugs may occur

The compiler uses a specific syntax called migraine.
It requires for all variables to be initialized at the top of the current depth level. Currently, only `byte` is supported.
Support for double, float and int will come as soon as I can figure out some of the operations.

Problematic loops from test_1.mico:
```Python
for(q=1:1:3){
    for(p=1:1:2){
        byte k
        k=q+p
        print(k)
    }
}
```

# Example
Example code: (test_1.mico)

```Python
byte a
byte b
byte c
byte d
a=0
b=20
d=!(a+b)
c=10
print(c)

if(d){
    print(d)
}else{
    print(c)
}

while(5<=c){
    print(c)
    c=c-1
}

do{
    print(c)
}while(5<=c)

do{
    byte e
    e=4+b
    print(e)
}while(5<=c)

for(t=1:1:3){
    print(t)
}

for(q=1:1:3){
    for(p=1:1:2){
        byte k
        k=q+p
        print(k)
    }
}
```

## Next Steps
Currently, the compiler is not thoroughly tested. First task will be to fix this and test the hell out of this program. All bugs must be purged!
Next of, the string and variable concatenation is not implemented. (Well...not even String String concatenation is implemented..)
Also new variable types beside byte would be nice. This may need a hole rewrite of the compiler, as adding new types of variables mean new operators, which now are not very easy to implement.
Besides all of this, a function handling would be nice. This would mean, that functions will be translated to brainfuck code and inserted at the specific position.
Identification and implementation will probably also need a rewrite of code.

Also a more simplistic version of Migraine, SimpleMigraine, will be implemented. It takes a lot of pressure of your shoulders, if you can actually write more simplistic code like
```Python
a = 4
b = 3
c = 0
while(a <= b){
    c += a + b
    print(2*c)
    a -= 1
}
```

So another task will be a translator from SimpleMigraine to Migraine and from there to Brainfuck Code.

So next up will probably be a lot of fixes and a whole new compiler with improved features and a simi (Simple Migraine) to mico (Migraine Code) translator.

Bear with me, as I am fairly new to Python and this is my first big project.

## Future....
In the future, I plan to use this compiler to implement a more universally usable compiler. Also Whitespace and other esoteric programming languages interest me, so be prepared for more fun with uncommon languages.
But besides that, who knows what else is to come.


