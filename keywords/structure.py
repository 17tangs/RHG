#each keyword is made up of the value, description, and key fields. Each field is a list, inside the list is all the different components in the form of strings that will make up this field. For example, if we want the key field of country keyword to be hotel code - country code then it would be ["hotelCode", "countryCode", "-"]. The last element of this list is the character in between these components. This is ignored if there is only one character

#Each component is formatted in this way: a|b|c. a is the name of the component, b are the flags for each word, and c is the separation characters.
#the flags are below:
#s: standard (first letter is capitalized and the rest is lowercase)
#u: all uppercase
#l: all lowercase
#c: remove all special characters
#d: default, use format from excel input
#for example "countryName|u| " would mean all caps with white space between words.
#"city|cl|-" would mean each word in city is lowercase and alphanumeric separated by a dash.


brandStructure = [[["brands|u|"],["brands|u|"], ["brands|u|"]]]

countryStructure=[[["countryNames|s|"], ["countryNames|s|"], ["countryCodes|u|"]]]

stateStructure = [[["countryNames|s|"], ["countryNames|s|"], ["countryCodes|u|"]],
                  [["stateNames|s|","countryNames|s|", ", "], ["stateNames|s|"], ["stateCodes|u|", "countryCodes|u|","-"]]]

cityStructure =  [[["countryNames|s|"], ["countryNames|s|"], ["countryNames|l|-"]],
                  [["stateNames|s|","countryNames|s|", ", "], ["stateNames|s|"], ["stateNames|l|-", "countryCodes|l|-", "-"]],
                  [["cities|s|","stateNames|s|","countryNames|s|", ", "], ["cities|s|"], ["cities|l|-", "stateCodes|l|-", "countryCodes|l|-", "-"]]]

hotelStructure = [[["countryNames|s|"], ["countryNames|s|"], ["||"]],
                  [["stateNames|s|","countryNames|s|", ", "], ["stateNames|s|"], ["||"]],
                  [["cities|s|","stateNames|s|","countryNames|s|", ", "], ["cities|s|"], ["||"]],
                  [["hotelNames|s|"], ["hotelNames|s|"], ["hotelCodes|u|"]]]

roomStructure =  [[["countryNames|s|"], ["countryNames|s|"], ["||"]],
                  [["stateNames|s|","countryNames|s|", ", "], ["stateNames|s|"], ["||"]],
                  [["cities|s|","stateNames|s|","countryNames|s|", ", "], ["cities|s|"], ["||"]],
                  [["hotelNames|s|"], ["hotelNames|s|"], ["hotelCodes|u|"]],
                  [["grt|s|"], ["grt|s|"], ["hotelCodes|u|", "grtCode|u|", "-"]],
                  [["prt|s|"], ["prt|s|"], ["hotelCodes|u|", "prtCode|u|", "-"]]]



