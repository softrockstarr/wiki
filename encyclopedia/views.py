from django.shortcuts import render
from markdown2 import Markdown
from django import forms

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
        "entries": util.list_entries()
})
    
# run title through convert function, if content doesn't exist, return error page, else render entry page with title/content. 
def entry(request, title):
    html_content = convert_md(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry not found, please try another search."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": html_content,
            "title": title
        })

# if form is filled, save q to query variable, convert md to html and save to html_content. If this variable exists, render the entry page for query.      
def search(request):
    if request.method == "POST":
        query = request.POST['q']
        html_content = convert_md(query)
        if html_content is not None: 
            return render(request, "encyclopedia/entry.html", {
            "title": query,
            "content": html_content
        })
        # else create variable to save all entries, create a list for suggested entries, if the query is in the all_entries list, add it to a list of suggested searches. 
        else: 
            all_entries = util.list_entries()
            suggestion = []
            for entry in all_entries:
                if query.lower() in entry.lower():
                    suggestion.append(entry)
            return render(request, "encyclopedia/search.html", {
                "suggestion": suggestion
            })

def new(request):
    if request.method == "POST":
         title = request.POST['title']
         content = request.POST['content']
         title_entries = util.get_entry(title)
         if title_entries is not None:
             return render(request, "encyclopedia/error.html", {
                 "message": "This article already exists"
             })
         else: 
             util.save_entry(title, content)
             html_content = convert_md(title)
             return render(request, "encyclopedia/entry.html", {
                 "title": title,
                 "content": html_content
             })
    else:
        return render(request, "encyclopedia/new.html")





    

