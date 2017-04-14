#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def sort_remove_duplicates(old_list):
  new_list = list(set(old_list))
  return sorted(new_list)

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""

  #Opening the log file to read it's content
  ufile = urllib.urlopen(filename)
  file_read = ufile.read()

  #Creating a list with all the occurrences of the pattern we're looking for in the URLs
  urls = re.findall(r'[\S]*puzzle[\S]*', file_read)

  #Building a complete URL with server name from the filename + the path of the URL
  file_basename = os.path.basename(filename)
  path_separator = file_basename.find('_')
  url_path = file_basename[path_separator+1:]
  complete_url_path = [url_path + url for url in urls]
  
  #Calling a function that remove the duplicates in the list and sort the result
  return sort_remove_duplicates(complete_url_path)
  
  
def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  

def main():
  url_list = read_urls('/home/aiquis/google-python-class/google-python-exercises/logpuzzle/animal_code.google.com')
  print url_list

"""
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)
"""

if __name__ == '__main__':
  main()
