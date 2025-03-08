import bddclass
import pandas

base= bddclass.DBLP() 

#base.print_features()

#base.download_latest_dump()
base.parse_all("dblp.xml","t2.json",)


#base.parse_by_year("2018","dblp.xml","2018.json")

"""The features that can be extracted from the DBLP dump are: address, author, booktitle, cdrom, chapter, cite
, crossref, editor, ee, isbn, journal, month, note, number, pages, publisher, publnr, school, series, title,
 url, volume, year.

              For more info, check on https://dblp.uni-trier.de/faq/index.html"""

