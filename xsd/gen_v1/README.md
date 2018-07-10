The format for input.txt:

first line is the name of the xsd file, follow the name in EXCEL (ignore punctuation leave captilization as is, ie Text: Title + Subtitle =>  TextTitleSubtitle)

Starting from the second line, one element per line

EXCEL element format: name, description, type, multivar, mandatory, tab (separated by tab (\t))

description and everything after mandatory is ignored.

Run program in terminal:
    python xsd-generator.py input.txt

Output is stored in the same directory in the form of NAME.xsd



Keywords
Link: blank has to be Yes or No
Hotel: checkin and checkout two separate fields
Metric has to be keyword
