import bisect

def date_docs(docs):
  dates = []

  for doc in docs:
    dates.append(doc.coverDate)

  for i in range(len(dates)):
    dates[i] = int(dates[i][:4])

  sorted_indexes = sorted(range(len(dates)), key=lambda x: -1 * dates[x])

  docs = [docs[i] for i in sorted_indexes]
  dates = [dates[i] for i in sorted_indexes]

  return (docs, dates)

def analyze(auth):
  (start, end) = auth.publication_range
  docs = auth.get_documents()

  (docs, dates) = date_docs(docs)
  
  current_year = start
  index = len(dates) - 1

  current_cites = []
  current_h = 0

  data = []
  current_tot_cites = 0

  while current_year <= end:
    while index >= 0 and dates[index] == current_year:
      index = index - 1

    docs_year = docs[index + 1:]
    docs = docs[:index + 1]

    (current_cites, current_h) = h_index(docs_year, current_cites, current_h)
    current_tot_cites = citations(docs_year, current_tot_cites)

    data.append((current_year, current_h, current_tot_cites))
    current_year = current_year + 1

  return data

def citations(docs, total_cites):
  current = total_cites

  for doc in docs:
    current = current + doc.citedby_count

  return current

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