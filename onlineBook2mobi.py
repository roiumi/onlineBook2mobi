import requests
import sys
import os
import re
from bs4 import BeautifulSoup


bookid = sys.argv[1]
base_url = "REMOVED"
url = "REMOVED"+bookid+"&p="
book_url = "REMOVED"+bookid
SAVE_FOLDER = 'img'
PHOTO_FOLDER = ''


"""GenerateFile Structure:
   -File Structure needed for images: /img/photo..
   
"""
def CreateImageFolders():
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    if not os.path.exists(PHOTO_FOLDER):
        os.mkdir(PHOTO_FOLDER)


"""Determine the number of pages for the book.
    The number of preges is selected on one of the divs from the page
    """
def PagesOfBook(soup):
        totalPages=0
        for a in soup.select('html body div#container div#main div#all div#out div#in div#content div.pageBook div.textBook div.navigation a'):
            if totalPages < int(a.text):
                totalPages=int(a.text)
        return totalPages


"""GatherText
    Description : Gather the Chapter name = h1 and write it to the HTML file.
    Then gather all the paragraph and write them to the HTML file
    
    Args:
        Takes the URL and puts it into the soup. The soup parses the content retrieved
    
    """
def GatherText(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')    
    for chapter in soup.find_all('div', attrs={'class':re.compile("take_h1")}):
        book.write("<h1>"+chapter.text+"</h1>")
        for p in soup.find_all('p', attrs={'class':re.compile("MsoNormal")}):
            book.write("<p>"+p.text+"</p>"+'\n')
        

"""GetCoverImageURL(soup) - Gets the cover image of the book. Parsing the content of the soup
*args: The soup wrapped around the request.


Returns: cover_image_url (string)
"""
       
def GetCoverImageURL(soup):
    for link in soup.findAll('img',attrs={'src':re.compile(bookid)}):
        cover_image_url = base_url+link['src']
        return cover_image_url

    """[convert_to_mobi] Converts the HTML to moby
    args: file type string. 
    type(file) string.
    file is format "file.html"
    mobiFile strips the .html from the name and replaces it with mobi
    
    cmd : ebook-convert file.html file.mobi
    """
def convert_to_mobi(file):
    print('Converting file to .mobi')
    mobiFile = os.path.splitext(file)[0]+".mobi"
    os.system("/usr/bin/ebook-convert %s %s 2>/dev/null" % (file, mobiFile))

 


#Creating file Structure
CreateImageFolders()    

#Accessing the URL    
response = requests.get(url)

#Making the Soup
soup=BeautifulSoup(response.text,'lxml')

#Parsing the Name of the book   
nume = soup.title.text.replace(' ','-')

#Downloading the image
imageName = PHOTO_FOLDER+'/'+nume+'.jpg'
downloadImage = requests.get(str(GetCoverImageURL(soup)))
with open(imageName,'wb') as image:
    image.write(downloadImage.content)

#Getting the number of pages of the book
Pages=PagesOfBook(soup)

#Writing to the file
#Adding Chapters and text
bookname = nume+".html"
with open(bookname,'+a') as book:
    
    book.write('<img align="center" src='+imageName+' style="margin:10px;"/>')
    for pageNumber in range(1,Pages+1):
        newurl = url+ str(pageNumber)
        GatherText(newurl)

#Making the conversion
convert_to_mobi(bookname)

os.remove(bookname)
os.remove(imageName)