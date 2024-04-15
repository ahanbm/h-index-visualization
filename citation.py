from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AuthorSearch
import bisect
import time

def timer(func, input):
  start_time = time.time()
  func(input)
  end_time = time.time()  

  return end_time - start_time

def full(auth):
  start_end = auth.publication_range

  start = start_end[0]
  end = start_end[1]

  docs = auth.get_documents()
  
  dates = []

  for doc in docs:
    dates.append(doc.coverDisplayDate)

  for i in range(len(dates)):
    dates[i] = int(dates[i][-4:])
  
  current_year = start
  index = len(dates) - 1

  current_cites = []
  current_h = 0

  h_indexes = []

  while current_year <= end:
    while index >= 0 and dates[index] == current_year:
      index = index - 1

    docs_year = docs[index + 1:]
    docs = docs[:index + 1]

    (current_cites, current_h) = h_index(docs_year, current_cites, current_h)

    h_indexes.append(current_h)
    current_year = current_year + 1

  return h_indexes

def h_index(docs, citations, h):
  vals = citations
  current_index = h

  for doc in docs:
    cites = doc.citedby_count

    if cites - current_index < 1:
      continue

    bisect.insort(vals, cites, key=lambda x: -1 * x)

    if vals[-1] > current_index:
      current_index = current_index + 1
    else:
      vals.pop()

  return (vals, current_index)

if __name__ == "__main__":
  s = AuthorSearch('AUTHLAST(Mishra) and AUTHFIRST(Ahan)')
  au = s.authors[0]

  id = au.eid
  auth = AuthorRetrieval(id)

  print(full(auth))