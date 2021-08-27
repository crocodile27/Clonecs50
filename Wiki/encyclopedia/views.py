from django.shortcuts import render
#importing a specific function called "render" "from shortcuts module which renders a page
from markdown2 import Markdown
#importing a specific function called "Markdown" from markdown2 which converts markdown to html
markdowner = Markdown ()
from . import util
""". is basically meaning from the same file directory import this module"""
import markdown
"""I have this installed through pip, markdown basically converts markdown into html, you can install through pip install markdown"""
import random
"""this random module will help us randomly choose between the entries."""


def index(request):
	"""This is the home page and it basically renders the index page and
	 gives the page the list of entries that are created by util.list_entries. 
	 Things that exist in utils is something used in many places or doesn't fit
	somewhere else."""
	return render(request,"encyclopedia/index.html",{
		"entries": util.list_entries()
		})

def convert_to_HTML(title):
	"""This function turns input into markdown language and is later used by the search function.
	You might be wondering if this is a common function why can't I just get it from util. 
	Well, it already uses get_entry from util so it doesn't work.

	1. Here we use a shortcut md = markdown.Markdown()
	2. Entry is fetched by util.get entry. Here we see again that util fetches information.
	3. html = markdown.Markdown.convert(entry) if entry is not equal to None.
	return html.
	
 	so it will look like this:
	md = markdown.Markdown()
	entry = util.get_entry(title)
	html = md.convert(entry) if entry else None 
	"""

	#but you can also write it like this where you get the entry from util and 
	#then directly convert it to HTML if the entry exists, else return None
	entry = util.get_entry(title)
	html = markdown.markdown(entry) if entry else None

	return html

def entry(request,title):
	"""This function is used to generate the entry but since each entry differs, 
	the request will take in title as an argument,"""
	#gets the page from util
	entryPage = util.get_entry(title)
	#checks if entrypage exists or not
	if entryPage is None:
		#if it doesn't exist we return a page that includes the title and 
		#states that the page doesn't exist while giving the people an option to choose to create a new page.
		return render(request, "encyclopedia/nonExistingEntry.html",{
			"entryTitle": title 
			})
	#if the page does exist however, we will then render the page and convert the entry into html.
	else: 
		return render(request, "encyclopedia/entry.html", {
			#Here you can either choose to directly get the entry and convert it to html as below
			#"entry": markdowner.convert(entryPage)
			#Or you can use the function previously created that fetches the page based on its title and converts it into html.
			"entry": convert_to_HTML(title),
			"entryTitle": title
			}) 

def search(request):
	"""This function is placed in the search bar and searches for pages then renders them"""

	if request.method == 'GET':
		#here we check if the for is in the form of get. The difference between GET and POST is that in GET you are trying to read information and that's it, 
		#while in POST you try and change the state of the system. GET is good for search forms, while POST is sometimes good for passwords when coupled with the csrf token.
		input = request.GET.get('q')
		#we get the input and then we get the input by the name of the input.
		html = convert_to_HTML(input)
		#The entries are called from util and are later used to check if the entry exists or not
		entries = util.list_entries()
		#We define the list outside so that the list doesn't empty itself after each iteration. Forgot that initially
		search_pages = []

		for entry in entries:
			if input.upper() in entry.upper():
			#css.upper=CSS, CSS
			#Here if the entry is somewhat similar or is included in the the word of the entry, e.g. cs is included in css:
			#then we put the pages into this array and render a search page that contains this array.
				#By doing this the user knows what pages were similar.
				search_pages.append(entry)

		for entry in entries:
			#Here we check if the entry is already in entries by going through all of the entries in entries
			if input.upper() == entry.upper():
				#we make sure the function works for different kinds of capitalization
				return render(request, "encyclopedia/entry.html",{
					#we then render the page called encyclopedia/entry.html if the entry exists and give the page the variables such as the page in html form and the title.
					"entry": html,
					"entryTitle": input
				})
			elif search_pages != []:
				#somehow this won't work if you render during looping.
				return render(request, "encyclopedia/search.html",{
					"entries": search_pages
					})
			else:
				#in this case search_pages array will not have any pages and the query will not match any case
				#Here the nonExistingEntry.html is rendered and the input is given as the the thing in "____does not exist"
				#The user will then be asked to create that page.
				return render(request, "encyclopedia/nonExistingEntry.html",{
					"entryTitle": input
					})

		

def newPage(request):
	#Here ppl go to the form where they can create a new page.
	return render(request, "encyclopedia/newPage.html")

def save(request):
	#This function returns the information from the POST request on the Create new page template (a template is basically a page on the web)
	#This function will then use the util function to save this page
	if request.method == 'POST':
		#Request method is equal to POST because you are changing the system instead of just reading data. This means you need more security.
		input_title = request.POST['title']
		#This is grabbing the information from the form by using the name attribute in the form.
		input_text = request.POST['text']
		entries = util.list_entries()
		#getting the entries from util and util will help you create an array
		html = convert_to_HTML(input_title)
		#This uses a function previously written
		#You need to create the Already_exist_true variable before using it in two different functions because if you only use it in the function
		#it becomes local to the function and you will get a "local variable referenced before assignment error"
		Already_exist_true = "false"
		for entry in entries:
			if input_title.upper() == entry.upper():
				#upper rules out the possibility of the user using different capitalization and creating a page that already exists.
				Already_exist_true = "true"
				#We use this to show that the entry already exists but we needed to take this loop out or it would render and then delete itself when iterating.

		if Already_exist_true == "true":
			#This function renders the already existant page if the user tries to create an already existing page.
			return render(request, "encyclopedia/already_exist.html",{
				"entry":html,
				"entryTitle":input_title
				})

		else:
			#Use util to save the entry
			util.save_entry(input_title, input_text)
			#Then you want to render the page after you save it and you fetch the entry page
			"""You can do this by doing this:
			entryPage = util.get_entry(input_title)
			return render(request, "encyclopedia/entry.html", {
				"entry": markdowner.convert(entryPage),
				"entryTitle": input_title
			})
			but here is a simpler way:
			"""
			return render(request, "encyclopedia/entry.html", {
				"entry": convert_to_HTML(input_title),
				"entryTitle": input_title
			})


def randomPage(request):
	#This function generates a random page
	entries = util.list_entries()
	#Gets a list of entries
	randEntry = random.choice(entries)
	#We get a random entry from the random.choice function that chooses from an array
	html = convert_to_HTML(randEntry)
	#find the html and we render the page.
	return render(request, "encyclopedia/entry.html",{
		"entry": html,
		"entryTitle":randEntry
		})

def editPage(request): 
	#This function is called after we press the edit button on the template and renders a page with a form.
	#In order to know what we are editing, we first find the title of the page where editing was requested.
	if request.method == 'POST':
		#Because we are changing the state of the system, we use POST.
		input_title = request.POST['title']
		#Get the information by using request.POST['title'] from the hidden input named title.
		text = util.get_entry(input_title)
		#We want to initiate the form with the latest text that under this page and we pass it into the page as a variable.
		#We don't turn this into html because the user uses markdown to change it.

		return render(request, "encyclopedia/editPage.html",{
			"entry": text,
			"entryTitle": input_title
		})

def saveEdit(request):
	#After we edit, we want to save the edit made.
	if request.method == 'POST':
		#We check that the form is POST, and we retrieve the title and the text.
		entryTitle = request.POST['title']
		entry = request.POST['text']
		#We use the util function to save the entry.
		util.save_entry(entryTitle, entry)
		#We then render the page in html form.
		html = convert_to_HTML(entryTitle)
		return render (request, "encyclopedia/entry.html",{
			"entry": html,
			"entryTitle": entryTitle
			})
