import re
#re stands for regular expressions.
from django.shortcuts import render
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.template import Context, loader

 

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.

    """
    _, filenames = default_storage.listdir("entries")


    return list(sorted(re.sub(r"\.md$", "", filename)

                for filename in filenames if filename.endswith(".md")))
    """
    The attibutes for the re.sub function are:
    re.sub(pattern, repl, string, count=0, flags=0)
    and it is used to replace the string ".md" with an empty string 
    for each filename to render a list of pure entry names.

    Pattern is basically what you're trying to find. Here we are trying to find all files that end with md.
    r'The backslash...' allows whatever follows to lose its initial meaning
    .md is the ending for the file name of all the entries
    $ is a special character that alows the function to find the match at the end of the string. 
    #For example, foo$ will match barfoo but not foobar.
    """

def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.

    . In Python source code, an f-string is a literal string, prefixed with 'f', 
    which contains expressions inside braces. 
    The expressions are replaced with their values. Some examples are:
    name = Anthea
    f"My name is {name}"
    """
    filename = f"entries/{title}.md"
    #Here the title is passed in as an argument and the filename is defined as being in the entires file under {title}
    if default_storage.exists(filename):
        #Here we verify if the file already exists or not.
        default_storage.delete(filename)
        #If it already exists we delete the file. This makes sure we don't have overlapping files.
    default_storage.save(filename, ContentFile(content))
    #Then we save the new file no matter if there is a file there or not already. We store the files with default_storage.save(filename, ConetentFile(content))
    """The content is passed in as markdown text without changing to HTML because there is no need to convert for the eyes of a viewer."""


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        #The try_except function allows you to try a function and then handle errors if there are any from that try function.
        f = default_storage.open(f"entries/{title}.md")
        #Here we get the entry through the default_storage function that opens the file entries/{title}.md from the entries file through the open function.
        return f.read().decode("utf-8")

    except FileNotFoundError:
        #However if the file is not found then it will return none and no file will be in get entry.
        return None

