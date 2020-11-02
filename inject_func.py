import os
import sys
import re

# pattern 1
# one or more alphanumeric character [a-zA-Z0-9_]+ then come (
# [a-zA-Z0-9_]+\(


'''
algorithm for dealing with next line

depends on if (){ are found

case 1
    only ( is found
    look for ) on the next line

case 2
    () both are found
    if next character is {, then this will confirm that it is a function
    if next character is throws, then look for { 
case 3
    (){ are all found
    function found


case 4
    () are found but { not found, but instead ; is found.
    this line is not a function definition
    start new function search on the next line




'''


args = sys.argv

rootDir = args[1]

cur_filename = ""
cur_full_filename = ""
file_read = ""

file_line = ""

for dirs, subdirs, files in os.walk(rootDir):
    print(dirs)
    print(subdirs)

    for file in files:
        if ".java" in file:
            print("this file is java " + file )
            print("path to the java file is " + dirs + "/" + file )

            cur_filename = file
            cur_full_filename = dirs + "/" + file


            file_read = open(cur_full_filename)
            file_line = file_read.readline()


            case1 = False
            case2 = False
            case3 = False
            case4 = False

            case2_indentation = False
            case2_func_closing_curly_brace = False
            openning_curly_brace = 0
            closing_curly_brace = 0
            remaining_curly_brace_pair = 0
            openning_parentheses = 0
            closing_parentheses = 0

            function_name = ""

            new_file_lines = []

            while file_line:



                # check if we are continuing search for function definition from previous line
                if case4:
                    # search for new function definition is true
                    print("case4 true. begin search for new function definition" )
                    case4 = False


                elif case3 and not case4:
                    # we need to add print statement then look for }
                    print("case3 " )



                elif case2 and not case3 and not case4:
                    # we need to look for {
                    print("case2 " )


                    if case2_func_closing_curly_brace:
            
                        print(" inner block ")

                        if "{" in file_line:
                            openning_curly_brace += 1

                        if "}" in file_line:
                            closing_curly_brace += 1

                        remaining_curly_brace_pair = openning_curly_brace - closing_curly_brace
        

                        if remaining_curly_brace_pair != 0:
                            # function closing curly brace not found yet
                            # add this line to new file and read next line
                            new_file_lines.append(file_line)
                            file_line = file_read.readline()

                            continue

                        elif remaining_curly_brace_pair == 0:
                            # function closing curly brace found
                            case2_func_closing_curly_brace = False
                            case2 = False
                            #add this line to new file and read next line
                            new_file_lines.append(file_line)
                            file_line = file_read.readline()

                            openning_curly_brace = closing_curly_brace = 0


                            continue
                

                    if case2_indentation:
                        # this is the line right after {

                        # now this line might consist of whitespace with new line character. or just new line only.
                        if file_line.isspace():
                            # this line consists of whitespace only. still looking for any character after { so case2_indentation should be true
                            # add this line to new file and read next line
                            new_file_lines.append(file_line)
                            file_line = file_read.readline()
                
                            continue

                        # character right after { is found
                        leadingspaces = len(file_line) - len(file_line.lstrip(' ') )
                        function_tracing_str = "System.out.println(\"FUNCTION_TRACING:\"".rjust( len("System.out.println(\"FUNCTION_TRACING\":") + leadingspaces )
            
                        print(" printing FUNCTION_TRACING ")

                        # make sure this does not contain either super or this statement because super or this method needs to be the first statement to be executed in the function
                        if not "super" in file_line and not "this(" in file_line.replace(" ", ""):

                            print("this statement does not contain super or this statement " + file_line )


                            if "{" in file_line:
                                openning_curly_brace += 1

                            if "}" in file_line:
                                closing_curly_brace += 1


                            new_file_lines.append( function_tracing_str + " + " + "\"" +  cur_full_filename + ":" + function_name +  "\");\n" )

                            # now that functoin debug statement added, now we need to look for }
                            # add current line to new file. read next line
                            case2_func_closing_curly_brace = True
                            new_file_lines.append(file_line)
                            file_line = file_read.readline()

                        # either super or this statement is present on the line
                        elif "super" in file_line or  "this(" in file_line.replace(" ", "") :

                            return_present = False

                            print(" this statement contains super or this statement " + file_line )

                            # super or this is present. now, we need to check if this or super statement ends on this line or continuing to next line
                            if not  file_line.rstrip().endswith(";") :
                                
                                # we also need to check if it contains return
                                if "return" in file_line:
                                    return_present = True

                                print(" this super or this statement does not contain ; to end this statement " + file_line )
                                # this or super statement continues on the next line as well
                                semicolon = False

                                # loop until semicolon is found
                                while not semicolon:
                                    # add this line to new file because this super statement does not end on this line
                                    new_file_lines.append(file_line)
                                    file_line = file_read.readline()

                                    if ";" in file_line:
 
                                        print(" this super or this statement contains ; " + file_line )

                                        # super or this statement ends on this line
                                        # add this line to the new file and read next line
                                        new_file_lines.append(file_line)
                                        file_line = file_read.readline()


                                        # check for return statement
                                        if "return" in file_line:
                                            return_present = True

                                        # make sure that this statement does not contain "this" statement or super statement.
                                        # if this contains either one, then loop again until this statement ends
                                        if not ( "super" in file_line or  "this(" in file_line.replace(" ", "") ):
                                            semicolon = True


                                            case2_func_closing_curly_brace = True


                            elif file_line.rstrip().endswith(";"):
                                # this super stament ends on this line

                                # check for return statement
                                if "return" in file_line:
                                    return_present = True

                                case2_func_closing_curly_brace = True
                                new_file_lines.append(file_line)
                                file_line = file_read.readline()

                            # make sure also that this is not return statement, because if it is we can not add anything after return statement
                            if not return_present:
                                # super and this statement ended. now add function debug print statement                            
                                new_file_lines.append( function_tracing_str + " + " + "\"" +  cur_full_filename + ":" + function_name +  "\");\n" )


                        case2_indentation = False

                        continue

                    else:

                        # check if first character is {
                        # to do so, first, we need to remove white space from the head of the line
                        match = re.match( "{", file_line.lstrip() )

                        # check if character after () is {
                        if match:
                            print(" case2. function definition found " )

                            openning_curly_brace += 1


                            # now we need to know if { is by itself on the line or it contains any characters together on the line.
                            if len( file_line.strip() ) == 1:
                                print(" { is by itself on this line " )

                                # adding debug print statement but we don't know what indentation this function uses. so we need to see next line to find
                                # out how many spaces to put before print statement so that print statement will aline with other statements in the function
                                case2_indentation = True

                                new_file_lines.append(file_line)
                                file_line = file_read.readline()

                                continue
                       
                        # is this throws statement? if so, read next line
                        elif "throw" in file_line:
                            new_file_lines.append(file_line)
                            file_line = file_read.readline()

                            continue

                        # is this black line?
                        elif not file_line.isspace() and not "throw" in file_line:
                            # first character after () was not {, so this is not function definition
                            # but this might be the start of function definition so don't read next line

                            case2 = False

                        elif file_line.isspace():
                            # this is blank line
                            # add this line and read next line
                            new_file_lines.append(file_line)
                            file_line = file_read.readline()


                elif case1 and  not case2 and not case3 and not case4 :
                    # we need to look for ) 
                    print("case1 ")

                    if "(" in file_line:
                        openning_parentheses += 1

                    if ")" in file_line:
                        closing_parentheses += 1

                    remaining_parentheses_pair = openning_parentheses - closing_parentheses

                    if remaining_parentheses_pair != 0:
                        # outermost parentheses pair not found yet
                        # add this line to new file. read next line
                        new_file_lines.append(file_line)
                        file_line = file_read.readline()

                        continue

                    elif remaining_parentheses_pair == 0 and not "{" in file_line:
                        # outermost parentheses pair is found. make sure that this line does not contain "{"
                        # add this line to new file. read next line
                        new_file_lines.append(file_line)
                        file_line = file_read.readline()

                        # case2 is the one that handles after parentheses are found
                        case2 = True
                        case1 = False

                        continue

                    elif remaining_parentheses_pair == 0 and "{" in file_line:
                        # pass this line to the case2
                        case2 = True
                        case1 = False

                        continue


                # do not enter interface function
                if "interface" in file_line and "{" in file_line:
                    # equivelent to entering function definition
                    case2 = True
                    case2_func_closing_curly_brace = True
                    openning_curly_brace = True
                        
                    new_file_lines.append(file_line)
                    file_line = file_read.readline()

                    continue


                elif "interface" in file_line and not "{" in file_line:
                    # equivelent to finding () and now need to find {
                    case2 = True
                    
                    new_file_lines.append(file_line)
                    file_line = file_read.readline()

                    while not "{" in file_line:
                        # keep reading next line until { appears
                        new_file_lines.append(file_line)
                        file_line = file_read.readline()

                    case2_func_closing_curly_brace = True
                    openning_curly_brace = True


                # begin search for new function definition
                pattern1 = "[a-zA-Z0-9_]+\("


                match = re.search( pattern1 , file_line )


                # make sure that this does not contain class defnition
                if( match and ( "class" not in file_line ) ):

                    print("this contains ( and does not contain class" + file_line);

                    function_name = re.search( "[a-zA-Z0-9_]+", match.group() ).group()
        
                    case1 = True

                    openning_parentheses += 1

                    # ( is found. now look for )
                    if ")" in file_line:

                        closing_parentheses += 1
                        
                        case1 = False
                        case2 = True

                        print(" () are found. " + file_line )

                        # ( and ) are found. now look for {. if found this will confirm that this is a function
                        if "{" in file_line:
                            case1 = case2 = False
                            case3 = True
                    
                            openning_curly_brace += 1

                            print(" (){ are found. " + file_line )

                        elif ";" in file_line:
                            # because { is not present but ; is present instead. this means that this is not function definition but this is function calling
                            print(" ; is found. not function definition " + file_line )

                            case1 = case2 = case3 = False
                            case4 = True

                        else:
                            case3 = False

                    else:
                        case2 = False

                else:
                    case1 = False

                new_file_lines.append(file_line)

                file_line = file_read.readline()

            
            file_read.close()
            file_read = open(cur_full_filename, mode='w')
            file_read.writelines(new_file_lines)
            file_read.close()




