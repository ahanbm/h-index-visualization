# *h*-index Visualization

## Dependencies

This project uses pybliometrics (https://github.com/pybliometrics-dev/pybliometrics). 

To go through the process of installing pybliometrics and dependencies, and to 
understand how pybliometrics connects with Elsevier's Scopus API, refer to the
documentation of the linked repository. 

You must have pybliometrics activated in order to run this project. This usually
requires an Elsevier API key and a network connection at an institution that
subscribes to Scopus (for more details refer to the documentation of the
pybliometrics repository).

This project has no other dependencies outside of the Python Standard Library.

## File Structure

To run the application, run script.py, which will provide interactive output. 
Images, once generated, will be placed in the images folder. Plotting logic is
in the plotting folder, and two types of citation analysis are in the citation
folder. 

author.json and config.json can be used to speed up the process of providing
information (explained further in next section). 

## Usage

config.json has 3 independent options, use_author_json, author_number, and 
use_historical_analysis.

use_author_json should be set to 'y' to use author.json (explained below), 'n'
to use standard input, and any other value to solicit the user's preference.

Similarly, use_historical_analysis should be set to 'y' to use historical
analysis (explained in next section), 'n' to use document analysis, and any
other value to solicit the user's preference.

When possible authors to be analyzed are printed, the user has an option to
select which one.

author_number should be set to a positive integer to pre-set which numbered author
should be chosen (e.g. author_number = 1 if you always want the most cited author 
of a search)

The options in config.json may or may not be activated based on the user's
response to the first question generated by script.py. 

author.json similarly has 3 fields, author_first_name, author_last_name, 
author_affiliation. Scopus searches will be generated based on these fields, 
searching for results that contain the values passed in. To not specify a search 
parameter, simply leave the corresponding field blank. 

The searches in author.json may or may not be activated based on config.json
and/or the user's responses to the questions generated by script.py.

## Historical vs Document Analysis

This project supports two modes of citation analysis - historical and document
based. The key difference is whether future citations count for a document. 

With historical analysis, the citation and *h*-index counts for a given year are
determined based on the number of citations that documents produced before or 
during that year received before or during that year. 

With document analysis, the citation and *h*-index counts for a given year are
determined based on the number of citations that documents produced before or
during that year ever received. 

For example, if an author only publishes 1 document, published in 2001
and receives 1 citation every year until 2020, then historical analysis would
show the number of citations increasing each year by 1 from 1 in 2001 to 20
in 2020. On the other hand, document analysis would put the number of citations
at 20 for every year between 2001 and 2020. 

Historical analysis can be viewed as an accurate historical snapshot of an 
author's *h*-index every year up to the present, while document analysis can be
viewed as analyzing an author's pattern of producing citation generating work. 

Document analysis tends to be much faster. 

Note that there may be slight discrepancies between the citation counts
generated by these two modes and the corresponding citations of an author
through an online Scopus Search; this is a result of inconsistencies/latency in 
Scopus' internal databases (https://blog.scopus.com/posts/enhancements-to-citation-overview-on-scopus).