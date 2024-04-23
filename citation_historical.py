from pybliometrics.scopus import ScopusSearch

def citations(overall_cites, year, total_cites):
  current = total_cites

  for cites in overall_cites:
    current = current + cites[year]

  return current


def h_index(overall_cites, year, citations):
  for i in range(len(overall_cites)):
    cites_item = overall_cites[i]
    cites = cites_item[year]
    citations[i] = citations[i] + cites
  
  vals = sorted(citations, reverse=True)

  h_index = 0
  
  for i, citation_count in enumerate(vals, start=1):
      if citation_count >= i:
          h_index = i
  
  return (citations, h_index)


def get_cites(docs): 
  overall_cites = []

  for doc in docs:    
    search_results = ScopusSearch(f"ref({doc.eid})")
    cites = []

    if not search_results.results:
      overall_cites.append(cites)
      continue

    for result in search_results.results:
      cites.append(result.coverDate)
    
    overall_cites.append(cites)
  
  return overall_cites


def date_docs(docs, overall_cites):
  dates = []

  for doc in docs:
    dates.append(doc.coverDate)

  return date_cites(dates, overall_cites)


def date_cites(dates, cites):
  for i in range(len(dates)):
    dates[i] = int(dates[i][:4])

  sorted_indexes = sorted(range(len(dates)), key=lambda x: -1 * dates[x])

  cites = [cites[i] for i in sorted_indexes]
  dates = [dates[i] for i in sorted_indexes]

  return cites


def process_cites(years_list, min_year, max_year):
    year_counts = {year: 0 for year in range(min_year, max_year + 1)}
    
    for year in reversed(years_list): 
        if year in year_counts:
            year_counts[year] += 1 
    
    return year_counts


def compute(range_pubs, overall_cites):
  (start, end) = range_pubs
  ordered_cites = []

  for cites in overall_cites:
    cites = date_cites(cites, cites)
    cites = process_cites(cites, start, end)
    ordered_cites.append(cites)
  
  current_year = start

  current_cites = [0 for _ in range(len(overall_cites))]
  current_h = 0

  data = []
  current_tot_cites = 0

  while current_year <= end:
    (current_cites, current_h) = h_index(ordered_cites, current_year, current_cites)
    current_tot_cites = citations(ordered_cites, current_year, current_tot_cites)

    data.append((current_year, current_h, current_tot_cites))
    current_year = current_year + 1
  
  return data


def analyze(auth):
  overall_cites = get_cites(auth.get_documents())
  return compute(auth.publication_range, overall_cites)