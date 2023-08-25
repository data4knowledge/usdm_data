import argparse
from bs4 import BeautifulSoup

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog='HTML Tag Stripper',
    description='Will strip unwanted tags from a HTML file',
    epilog='Note: Not that sophisticated! :)'
  )
  parser.add_argument('filename', help="The name of the HTML file with path.") 
  parser.add_argument("tag", help = "The tag to clear")
  args = parser.parse_args()
  filename = args.filename
  tag = args.tag
  print (f"Processing {filename} to clear tag = '{tag}' ...")

  with open(filename, 'r') as f:
    html_doc = f.read()
    print(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser')
    for data in soup([tag]):
      data.unwrap()
    for data in soup('p', attrs={'class': 'p1'}):
      data.decompose()

  print(soup)

  with open("test.html", 'w') as f:
    f.write(str(soup))

  print ("... done")
