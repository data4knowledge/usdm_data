import argparse
from bs4 import BeautifulSoup
import yaml
import csv

section_num = -1000

def write_html_file(filename, contents):
  with open(f'{filename}_stripped.html', 'w', encoding='utf-8') as f:
    f.write(contents)

def read_html_file(filename):
  with open(f'{filename}.html', "r") as f:
    return f.read()

def read_yaml_file(filename):
  with open(f'{filename}_config.yaml', "r") as f:
    return yaml.safe_load(f)

def write_csv_file(filename, contents):
  with open(f'{filename}_sections.csv', "w") as f:
    writer = csv.DictWriter(f, fieldnames=['sectionNumber',	'name',	'sectionTitle',	'text'])
    writer.writeheader()
    writer.writerows(contents)

def write_yaml_file(filename, data):
  with open(f'{filename}_sections.yaml', "w") as f:
    return yaml.dump(data, f, default_flow_style=False)

def get_section_number(text):
  parts = text.split(' ')
  if parts[0][0].isdigit():
    section_number = parts[0]
    if len(parts) > 1 and parts[1].startswith('.'):
      section_number = f"{section_number}."
    return section_number
  elif parts[0].lower() == 'appendix':
    if len(parts) > 1: 
      section_number = f"{parts[0]} {parts[1]}"
      return section_number
  return None

def get_section_title(text):
  parts = text.split(' ')
  if parts[0][0].isdigit():
    if len(parts) > 1 and parts[1].startswith('.'):
      section_title = (' ').join(parts[2:])
    else:
      section_title = (' ').join(parts[1:])
    return section_title
  elif parts[0].lower() == 'appendix':
    if len(parts) > 2: 
      section_title = (' ').join(parts[2:])
      return section_title
  return None  

def find_by_path(root, items):
  tag_class = items[0]
  tags = root.findAll(tag_class['tag'], {"class": tag_class['class']})
  if len(items) > 1:
    results = []
    for tag in tags:
      inner = find_by_path_recurse(tag, items[1:])
      if inner:
        results.append(tag)
    return results
  else:
    return tags

def find_by_path_recurse(root, items):
  tag_class = items[0]
  tags = root.findAll(tag_class['tag'], {"class": tag_class['class']})
  if len(items) > 1:
    for tag in tags:
      return find_by_path_recurse(tag, items[1:])
  else:
    return tags

def section_number_key(section_number):
  text = section_number[:-1] if section_number.endswith('.') else section_number
  return text.replace('.', '-')

if __name__ == "__main__":

  parser = argparse.ArgumentParser(
    prog='HTML Tag Stripping Utility',
    description='Will strip unwanted tags from a HTML fil based on a configuration file',
    epilog='Note: Not that sophisticated! :)'
  )
  parser.add_argument('filename', help="The name of the HTML file with path without the file extension") 
  args = parser.parse_args()

  print (f"\n\nHTML Tag Stripping Utility\n\n")

  kill_list = []
  filename = args.filename
  doc = read_html_file(filename)
  actions = read_yaml_file(filename)

  soup = BeautifulSoup(doc, 'html.parser')

  # Replace tags
  for item in actions['replace_tag']:
    print(f"Replacing tags '{item['from']}' --> tag '{item['to']['tag']}'")
    tags = find_by_path(soup, item['from'])
    for tag in tags:
        tag.name = item['to']['tag']
        tag.attrs = {}
        if 'kill' in item['to']:
          for kill_item in tag.findAll(item['to']['kill']):
            kill_item.unwrap()
    
  # Manual delete of tags but keep content
  for item in actions['delete_tag_keep_content']:
    print(f"Removing tag '{item['tag']}', class '{item['class']}'")
    for match in soup.findAll(item['tag'], {"class": item['class']}):
      match.unwrap()

  # Manual delete of tags and content
  for item in actions['delete_tag_and_content']:
    print(f"Removing tag and content '{item['tag']}', class '{item['class']}'")
    for match in soup.findAll(item['tag'], {"class": item['class']}):
      match.extract()

  # Manual delete of tag attribute
  for item in actions['delete_attribute']:
    print(f"Removing attribute from tag '{item['tag']}', attribute '{item['attribute']}'")
    #for match in soup.findAll(item['tag'], {item['attribute']: True}):
    for match in soup.findAll(item['tag'], {item['attribute']: item['value']}):
      match.attrs = {key:value for key,value in match.attrs.items() if key != item['attribute']}

  # Clean out spans with no text, single space or line feeds
  print(f"Removing empty spans")
  for match in soup.findAll('span'):
    if not match.text:
      match.unwrap()
    elif match.text == ' ':
      match.unwrap()
    elif match.text == chr(10):
      match.unwrap()

  # Clean out paragraphs of line breaks
  print(f"Removing breaks and newlines from paragraphs")
  for tag in soup.findAll('p'):
    for br in soup.findAll('br'):
      br.replace_with(' ')
    tag.text.replace('\n', ' ')

  # Manual string replacements
  text = str(soup)
  for item in actions['replace_string']:
    print(f"Replacing text, '{item['from']}' --> '{item['to']}'")
    text = text.replace(item['from'], item['to'])

  soup = BeautifulSoup(text, 'html.parser')

  body = soup.find('body')  
  first_tag = body.find()
  new_h1 = soup.new_tag("h1")
  new_h1.append("0. Title Page")
  first_tag.insert_before(new_h1)

  for tag in soup.findAll('h1'):
    print(f"TAG: {tag.text}")
    section_number = get_section_number(tag.text)
    if section_number:
      continue
    tag.name = 'p'

  for tag in soup.findAll('h2'):
    section_number_title = tag.b.text
    section_text = tag.text.replace(section_number_title, '')
    new_h1 = soup.new_tag("h1")
    new_h1.append(section_number_title)
    new_p = soup.new_tag("p")
    new_p.append(section_text)
    tag.insert_after(new_h1)
    new_h1.insert_after(new_p)
    tag.extract()

  print("Saving HTML file\n\n")
  text = str(soup)
  write_html_file(f"{filename}", text)

  headings = {}
  sections = []
  soup = BeautifulSoup(text, 'html.parser')

  for match in soup.findAll('h1'):
    heading = match.text
    section_number = get_section_number(heading)
    if section_number:
      section_title = get_section_title(heading)
      headings[section_number_key(section_number)] = {'sectionNumber': section_number, 'name': '', 'sectionTitle': section_title, 'text': ''}
      sections.append(section_number)

  for match in soup.findAll("h1"):
    section_number = get_section_number(match.text)
    if section_number in sections:
      elements = []
      for tag in match.next_siblings:
        if tag.name == "h1":
          break
        else:
          if str(tag) != '\n':
            elements.append(str(tag))
      headings[section_number_key(section_number)]['text'] = ('\n').join(elements)
      print(f"Processing section '{section_number}'")

  print("\n\nSaving CSV file")
  write_csv_file(filename, list(headings.values()))
  print("\n\nSaving YAML file")
  write_yaml_file(filename, headings)

  print(f"\n\nDone\n\n")