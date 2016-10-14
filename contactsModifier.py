"""
This beautiful piece of code helped me modify all my contacts by appending the
mexican international prefix "+521" to all of them.
When I first created my contacts list I was living at mexico, and there was 
no need to add the mexican international prefix to the contacts.
Then I moved out from Mexico, and when getting an international number, whatsapp was
not identifying my contacts because they were lacking the international prefix.
So instead of going one by one adding the prefix, this little piece of code made
that happen for me.
"""

PREFIX = '+521';

# Helper functions:

def openFile():	
	"""
	Asks the user for the file name and tries to open it.
	Once opened returns that file.

	.File name must be provided with the .vcf ending.

	.The .vcf file must be stored on the same folder as this script,
	 else it will never find it.

	.If the file name is incorrect, or the .vcf file is not in the
	same folder as the script, it will keep asking the folder name.

	"""
	while(True):
		file_name = input("Enter vcf filename: ");
		if file_name.endswith('.vcf'):
				try:
					file = open(file_name);
					return file;
				except IOError: 
					print("\tError: File does not appear to exist.");
		else: print("Enter the file name followed by .vcf");

def getNumber(line):
	"""Returns the Phone Number of a Contact.
	Arguments: line.
    Assumes that the given line is one that contains a phone number"""
	if line.find("pref:") != -1: return line[line.find("pref:") + 5:]
	if line.find("VOICE:") != -1: return line[line.find("VOICE:") + 6:]
	else: return ""

def modifyNumber(number):
	"""
	I have a number, and I want to put +521 in front of it when the number starts with 55.
	(Numbers that start with 55 are mexican cellphones). Other numbers are maybe home numbers, 
	or from other country, and I don't want to modify those.
	Also, I want to get rid of the parenthesis and spaces so there are no overwritting problems.

	Ex:

	(55) 3052 6879 ---> +5215530526879.
	5290 1099 -----> 5290 1099 # Leaves it that way because its a home number.
	"""
	if(number.startswith('(')): number = eliminateParenthesis(number);
	if(number.startswith("55")): # Numbers that start with 55 are mexican cellphones.
		number = eliminateSpaces(number);
		number = PREFIX + number; # Append prefix
	return number;

def eliminateSpaces(number):
	new = number.replace(u'\xa0', u''); # In my contacts list there are some contacts that contain whitespaces as non-ASCII, i.e. \xa0
	new = new.replace(' ', '');
	return new;

def eliminateParenthesis(number):
	new = number.replace('(', '');
	new = new.replace(')', '');
	return new;

# Main Program:
contacts_file = openFile();
newContent = [];
for line in contacts_file:
	if line.startswith("TEL"): # Lines that start with "TEL" are the ones that contain phone numbers.
		number = getNumber(line);
		new_number = modifyNumber(number);
		new_line = line.replace(number, new_number);
		newContent.append(new_line); # Add the line with the modified number to the new content.
	else:
		newContent.append(line); # Nothing to overwrite in this line, just add it to the new content as it is.

# Write the new contacts list.
# It is just the old one with the numbers modified.

outputFile = open('newContacts.vcf','w')
outputFile.writelines(newContent)
outputFile.close();

print ("Yei!! Done. Check that your contacts were updated correctly.")


