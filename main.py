#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, glob, re, markdown
from flask import Flask, abort, request, render_template

# Creating the application.
app = Flask(__name__)
app.config.from_object("config")

@app.context_processor
def variables_def():
  return dict(
        websiteName=app.config["WEBSITENAME"],
        websiteDesc=app.config["WEBSITEDESC"],
        websiteUrl=request.url_root[:-1]
        )
        
# Reading the docs at the start of the application:
def readdocs():
  global bookpages
  docsfiles = glob.glob("docs/*.md")
  docsfiles = sorted(docsfiles)
  
  regexExtractTitle = re.compile("^#[^#\n]+")
  regexExtractSubHeading = re.compile("##[^#\n]+")
  bookpages = []
  
  for doc in docsfiles:
    currentdoc = open(doc, 'r')
    content = currentdoc.read()
    pagetitle = regexExtractTitle.findall(content)[0].split("# ")[1]
    pagesubheadings = []
    subheadings = regexExtractSubHeading.findall(content)
    if len(subheadings) > 0:
      for subheading in subheadings:
        pagesubheadings.append(subheading.split("## ")[1])
    pagehtml = markdown.markdown(text=content, extensions=['tables'])
    pagenumber = docsfiles.index(doc)+1
    bookpages.append([pagetitle, pagesubheadings, str(pagehtml), pagenumber])
      
  return bookpages

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html', bookpages=readdocs()), 404

@app.route('/')
def show_index():
  return render_template('index.html', bookpages=readdocs(), pagenumber=1)

@app.route('/bookpage/<int:pageurl>')
def show_page(pageurl):
  return render_template('bookpage.html', bookpages=readdocs(), pagenumber=pageurl)

if __name__ == "__main__":
  app.run(host='0.0.0.0')
