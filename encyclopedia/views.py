from django.shortcuts import render
from markdown2 import Markdown

from . import util

# step 7 helper function to convert markdown to html
def convert_md(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })
    
# run title through convert function, if content doesn't exist, return error page, else render entry page with title/content. 
def entry(request, title):
    html_content = convert_md(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": html_content,
            "title": title
        })
    

    

