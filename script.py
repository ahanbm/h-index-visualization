from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AuthorSearch
import citation.citation_historical as citation_historical
import citation.citation_documents as citation_documents
import plotting.plotter as plotter
import json
import sys
import os

def read_author_info(file_path):
    with open(file_path, 'r') as file:
        authors = json.load(file)
        author = authors[0]

        first_name = author.get('author_first_name', "")
        last_name = author.get('author_last_name', "")
        affiliation = author.get('author_affiliation', "")
    
    return [first_name, last_name, affiliation]


def read_config_info(file_path):
    while True:
      option = input("Would you like to use the options in config.json (y or n): ")

      if option == "n":
          return ["", "", ""]
      elif option == 'y':
          break
      else:
          print("Invalid input. Please enter a valid option (y or n).")

    with open(file_path, 'r') as file:
        configs = json.load(file)
        config = configs[0]

        use_author_json = config.get('use_author_json', "")
        author_number = config.get('author_number', "")
        use_historical_analysis = config.get('use_historical_analysis', "")
    
    return [use_author_json, author_number, use_historical_analysis]


def sanitize(s):
  if s:
    return s
  else:
    return "N/A"
  

def process(text, prefix):
  text = text.strip()
  
  if text:
    return prefix + "(" + text + ")"
  else:
    return None
  
  
def print_info(info, num):
  print("Author " + str(num))
  print("Name: " + (info[0] + " " + info[1]) + ", Affiliation: " + info[2])
  print("City: " + info[3] + ", Country: " + info[4] + ", Areas: " + info[5])
  print()


def get_search():
  print("On the three upcoming commands, enter to skip")

  first = input("First name of author: ")
  last = input("Last name of author: ")
  affiliation = input("Affiliation of author: ")

  return [first, last, affiliation]


def get_option_authors(use_author_json):
  if use_author_json == "y":
    return read_author_info("author.json")
  elif use_author_json == "n":
    return get_search()
  
  while True:
    option = input("Would you like to search authors through standard input (1) or author.json (2): ")

    if option == "1":
        return get_search()
    elif option == '2':
        return read_author_info("author.json")
    else:
        print("Invalid input. Please enter a valid option (1 or 2).")

def get_option_analysis(use_historical_analysis):
  if (use_historical_analysis == "y"):
    return citation_historical
  elif (use_historical_analysis == "n"):
    return citation_documents

  while True:
    option = input("Would use like to use historical (1) or document-based (2) analysis: ")

    if option == "1":
        return citation_historical
    elif option == '2':
        return citation_documents
    else:
        print("Invalid input. Please enter a valid option (1 or 2).")

  
def create_search(search_keys):
  search_string = ""
  previous = False

  for search_key in search_keys:
    if search_key:
      if previous:
        search_string += " and "
      else:
        previous = True

      search_string += search_key
  
  return search_string


def print_authors(authors):
  num = 1
  print()

  fields = ["givenname", "surname", "affiliation", "city", "country", "areas"]
  
  for author in authors:
    info = []

    for field in fields:
      info.append(sanitize(getattr(author, field)))
    
    print_info(info, num)
    num = num + 1


def s_to_u(s):
  return s.replace(" ", "_")


def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    

def get_index(authors, author_number):
  if is_integer(author_number):
    return author_number

  val = 0

  while True:
    index = input("Which number author would you like to select (type exit to stop): ")

    if index == "exit" or index == "stop":
      sys.exit(1)

    try:
      val = int(index)

      if val < 1 or val > len(authors):
        print("Please enter an index within the range.\n")
      else:
        break
    except ValueError:
      print("Invalid input. Please enter a valid integer.\n")
  
  return val


def file_write(data):
  with open('data.txt', 'w') as file:
    for tuple in data:
      (year, h, cites) = tuple

      file.write(str(year) + " ")
      file.write(str(h) + " ")
      file.write(str(cites) + "\n")
    
    file.write("Done\n\n")


def end_to_end():
  [use_author_json, author_number, use_historical_analysis] = read_config_info("config.json")

  search_keys = get_option_authors(use_author_json)
  search_texts = ["AUTHFIRST", "AUTHLAST", "AFFIL"]

  for i in range(len(search_keys)):
    search_keys[i] = process(search_keys[i], search_texts[i])

  search = AuthorSearch(create_search(search_keys))
  authors = search.authors

  if not authors:
    print("No authors were returned from this search, please change the search parameters. ")
    sys.exit(1)

  print_authors(authors)
  au = authors[int(get_index(authors, author_number)) - 1]

  auth = AuthorRetrieval(au.eid)

  analyzer = get_option_analysis(use_historical_analysis)
  data = analyzer.analyze(auth)

  file_write(data)

  author_name = sanitize(s_to_u(auth.given_name)) + "_" + sanitize(s_to_u(auth.surname))
  plotter.plot_data(data, author_name)
  os.system("open images/" + author_name + ".png")
  

if __name__ == "__main__":
  end_to_end()