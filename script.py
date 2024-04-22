from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AuthorSearch
import citation
import sys

def sanitize(s):
  if s:
    return s
  else:
    return "N/A"

def process(text, prefix):
  if text == "n" or text == "'n'":
    return None
  else:
    return prefix + "(" + text + ")"
  
def print_info(info, num):
  print("Author " + str(num))
  print("Name: " + (info[0] + " " + info[1]) + ", Affiliation: " + info[2])
  print("City: " + info[3] + ", Country: " + info[4] + ", Areas: " + info[5])
  print()

def get_search():
  print("On the commands below, type 'n' to skip")

  first = input("First name of author: ")
  last = input("Last name of author: ")
  affiliation = input("Affiliation of author: ")

  return [first, last, affiliation]

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

def get_index():
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

if __name__ == "__main__":
  search_keys = get_search()
  search_texts = ["AUTHFIRST", "AUTHLAST", "AFFIL"]

  for i in range(len(search_keys)):
    search_keys[i] = process(search_keys[i], search_texts[i])

  search = AuthorSearch(create_search(search_keys))
  authors = search.authors

  if not authors:
    print("No authors were returned from this search, please change the search parameters. ")
    sys.exit(1)

  print_authors(authors)
  au = authors[int(get_index()) - 1]

  auth = AuthorRetrieval(au.eid)
  data = citation.analyze(auth)

  with open('output.txt', 'w') as file:
    for tuple in data:
      (year, h, cites) = tuple

      file.write(str(year) + " ")
      file.write(str(h) + " ")
      file.write(str(cites) + "\n")
    
    file.write("Done\n\n")

  print("\nFile Writing Complete")
  citation.plot_data(data, auth.given_name + " " + auth.surname)
  print("Plotting Complete")