# Injuect_into_func
inject debug print statement into every java functions! ( some functions are not supported )

# instructions
execute inject_func.py with java top directory commandline parameter

for example

in linux

python3 inject_func.py (top directory of java project )

it will look for all java files under the specified top directory

# cautions
some functions that span multiple line are not supported yet

function pattern 3, which is 

functionName() {

is not supported yet

Because I used maven source code as a test material, pattern 3 barely appeared in maven source code. 
Fuctions in maven source code has the frequent style of

functionName() 

{

  statement;
  
  some statement;
  
  :
  
  :

}

