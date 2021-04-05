# RSA

We use markdown within these pages.

## A subsection

Lala some text

### An even sub-er section

this is all placeholder text.

## Tables

We can make tables

| One | Two | Three |
| ---- | ----- | ------ |
| 1 | 2 | 3 |

## Math

We can do latex math. We can do things inline $\sqrt{n}$ or in blocks

$
\begin{align}
    f(x) =& 2(x-2) \\
        =& 2x-4 
\end{align}
$

## Other Stuff

We can cite sources {cite}`fivesort`, make things *italic* or **bold**. We can referecen websites [A website](https://legacy.jupyterbook.org/guide/publish/github-pages.html) that tells you how to make this book the webpage in github.

You can also put in color coded source code either `sys.exit(0)` inline or as a block

```Python
def modpower(x,y,N):
    if y==0:
        return 1
    elif y%2==0:
        temp = modpower(x,y//2,N)
        temp = (temp*temp)%N
        return temp
    else:
        temp = modpower(x,y-1,N)
        temp = (temp*x)%N
        return temp
```


```Python
import base64
def convertToASCII(num,maxLen):
    res=""
    base=256
    while num > 0:
        rem = num % base
        rem = chr(rem)
        res+=rem
        num=num//base
    if len(res) < maxLen:
        res+=chr(0)
    return res
ENCODED=[1234,5436,3234,6534,5675,3456]
N=7000
maxSize=len(convertToASCII(N,0))
myFinalText=""
for num in ENCODED:
    myFinalText += convertToASCII(num,maxSize)
message_bytes = myFinalText.encode()
base64_bytes = base64.b64encode(message_bytes)
print(base64_bytes)
```
