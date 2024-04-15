from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AuthorSearch
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
    dates.append(doc.coverDate)

  for i in range(len(dates)):
    dates[i] = int(dates[i][:4])
  
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

def plot_data(data, name):
    plt.figure(name)
    x_values = [entry[0] for entry in data]
    y_values = [entry[1] for entry in data]
    z_values = [entry[2] for entry in data]

    fig = plt.figure(num=name, figsize=(20, 12))
    ax1 = fig.add_subplot()

    ax1.plot(x_values, y_values, 'bo', color='blue')
    ax1.plot(x_values, y_values, label='h-index', color='blue')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('h-index', color='blue')

    ax2 = ax1.twinx()
    ax2.plot(x_values, z_values, 'ro', color='red')
    ax2.plot(x_values, z_values, label='citations', color='red')
    ax2.set_ylabel('citations', color='red')

    ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='best')

    plt.title("Citations and H-index by Year")
    plt.subplots_adjust(right=0.85)
    plt.subplots_adjust(top=0.90)

    plt.grid(True)
    plt.show()

if __name__ == "__main__":
  s = AuthorSearch('AUTHFIRST(Ahan) and AUTHLAST(Mishra)')
  au = s.authors[0]

  id = au.eid
  auth = AuthorRetrieval(id)

  data = full(auth)

  with open('output.txt', 'w') as file:
    for tuple in data:
      (year, h, cites) = tuple

      file.write(str(year) + " ")
      file.write(str(h) + " ")
      file.write(str(cites) + "\n")
    
    file.write("Done\n\n")

  print("File Writing Complete")
  plot_data(data, auth.given_name + " " + auth.surname)