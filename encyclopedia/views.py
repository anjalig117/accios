from django.shortcuts import render

from markdown2 import Markdown
import random
import re
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect

from . import util 

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, entry):
	try:
		entryes = util.get_entry(entry)
		entries = markdowner.convert(entryes)
		print(entry)
		return render(request, "encyclopedia/entry.html", {
        "entries": entries,
        "entry": entry,
    	}) 	
	except:
		return render(request, "encyclopedia/error.html", {"message": 'Entry Not Found.'})

def random_entry(request):
	entries = util.list_entries()
	entry = random.choice(entries)
	print(entry)
	return HttpResponseRedirect(reverse('entry', args=(entry,)))

def search(request):
	try:
		search_entry = request.POST['q']
	except KeyError:
		return render(request, "encyclopedia/error.html", {"message": 'Invalid Search Entry.'})

	entry = util.list_entries()
	sub = search_entry
	print(sub)
	res = [x for x in entry if re.search(sub, x, re.IGNORECASE)]
	print(res)

	for reses in res:
		print(reses)
		if sub.lower() == reses.lower():
			return HttpResponseRedirect(reverse('entry', args=(search_entry,)))
		else:
			return render(request, 'encyclopedia/search.html', {"search": res})
	

	if len(res) == 0:
		return HttpResponseRedirect(reverse("index"))

def new(request):
	return render(request, "encyclopedia/new_entry.html")

def save_entry(request):
	try:
		entry_title = request.POST['title']
		entry_content = request.POST['content']
	except KeyError:
		return render(request, "encyclopedia/error.html", {"message": 'Invalid Data'})

	entry = util.list_entries()

	if entry_title in entry:
		return render(request, "encyclopedia/error.html", {"message": 'This encyclopedia entry already exists.'})

	else:
		new_entry = util.save_entry(entry_title, entry_content)
		print(new_entry)
		return HttpResponseRedirect(reverse("entry", args=(entry_title,)))

def edit_entry(request, entry):
	entry_content = util.get_entry(entry)
	print(entry_content)

	return render(request, "encyclopedia/edit_entry.html", {"entry_content": entry_content, "entry_title": entry})

def save_edit_entry(request, entry):
	try:
		entry_content = request.POST['content']
	except KeyError:
		return render(request, "encyclopedia/error.html", {"message": 'Invalid Data.'})

	new_editted_entry = util.save_entry(entry, entry_content)

	return HttpResponseRedirect(reverse("entry", args=(entry,)))