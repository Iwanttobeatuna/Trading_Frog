# Implementation of the project
First, I break the project into parts that need to be done, extracting the code out and testing it externally before incorporating it back to the main file.
Those parts are:

## 1. Static webpage
Template: New Age from Bootstrap
Redesign the page with different color scheme.
Design images on Canva and incorporate it to the template


## 2. Login/logout/register (the web app main skeleton)
Copied the code from CS50's finance, cleaning up and deleting unwanted portions.
Incorporate it with the static template

## 3. News_scrapper for index
From here onwards, that's where the difficult task really begin. I extracted every part out to code and test before incorporating into the web app.
I start to learn about news scrapping online and with the help from the communities, I figure out how to code a functional newscrapper with Python BeautifulSoup from rss web feed
The code for news_scrapper can be found here: https://github.com/Iwanttobeatuna/news-scrapper.git
From there, I incorporate the code into my Flask application. Bootstrap "card" is a specific CSS feature I found interesting for the design.
Note: There is still room for improvement with incorporating it to the website instead of using specific array like I do. I am super confused about the usage of for loop in Flask.

## 4. World Index info for index
I used investpy to scrap for index info, and implement it with Boostrap "card" in the index page. This was relatively okay.

## 5. Stock result for searched stock
Similar to the search for index, investpy is super helpful in doing this. For better design, I tried to search for better looking Bootstrap cards design online.
https://codepen.io/lesliesamafful/pen/oNXgmBG
This website provided fantastic design of bootstrap card, hence I referenced from there while building the page.


## 6. Stock graph for searched stock
This is probably the most difficult section throughout my CS50 final project. The goal is to plot with plotly a graph with the csv from investpy and incorporate it with Flask.
At first, I successfully plot a graph with my google colab, which can be found here: https://colab.research.google.com/drive/1H6Jz5CID-rpzS0LZE-CxNqvDxprcd6Yy?usp=sharing
However, when I tried to implement it on Flask, the graph just wouldn't show. I got help from Professor Malan on Ed about the issue and solved it!

## 7. Piecing it together
That's it! CS50 final is done!

# Miscellaneous: Things I have leanrt via this CS50 final project:
1. Understanding the problem and goal is important before the start of a project
2. Pseudocode before coding helps a lot!
3. Breaking into smaller part before implementing it with the larger framework works!
4. Print function is super useful when trying to understand and debug, especially if you don't have check50!
5. Asking question is key! CS open source community and CS50's supportive community are just awesome! Got a lot of inspiration from ED and my section leader!
