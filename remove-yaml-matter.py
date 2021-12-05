from win32_setctime import setctime
import datetime as dt
import time
import pytz
import os
import re

DEBUG = True

def delete_frontmatter(path, file_lines, num_lines):
    with open(path, 'w', encoding='utf-8') as f:
        for num, line in enumerate(file_lines):
            if num not in range(num_lines):
                f.write(line)
    f.close()

def get_date_created_from_frontmatter(path):
    f = open(path, "r", encoding='utf-8')
    file_lines = f.readlines()
    inside_frontmatter = False
    contains_complete_frontmatter = False
    frontmatter_num_lines = None
    found_date_created = True
    unix_time = None

    for line_num, line in enumerate(file_lines):
        # print(line_num, line, end='')
        line.strip()
        if line == "---\n":
            if inside_frontmatter:
                contains_complete_frontmatter = True
                frontmatter_num_lines = line_num + 2
                break
            inside_frontmatter = not inside_frontmatter

        if found_date_created:
            match_found = re.match('^created: [0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}Z\n$', line)
            if inside_frontmatter and match_found:  
                found_date_created = True       
                date_time = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}Z', line).group()
                date_time_obj = dt.datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ")
                utc_time = pytz.utc.localize(date_time_obj)
                date_time_zone = utc_time.astimezone(pytz.timezone('America/Vancouver'))
                unix_time = date_time_zone.timestamp()
                # print("TIME:", unix_time, date_time_zone)
    f.close()

    if contains_complete_frontmatter:
        delete_frontmatter(path, file_lines, frontmatter_num_lines)
        return unix_time

def iterate_files(path, number_ignored, ignored_list, exclude_list):
    if os.path.isfile(path):
        time = get_date_created_from_frontmatter(path)
        if time == None:
            number_ignored += 1
            ignored_list.append(path)
        else:
            if DEBUG: print(path, time)
            setctime(path, time)
        return number_ignored, ignored_list

    # iterate across all files in path
    for filename in os.listdir(path):
        if filename not in exclude_list:
            new_path = os.path.join(path, filename)
            number_ignored, ignored_list = iterate_files(new_path, number_ignored, ignored_list, exclude_list)
    
    return number_ignored, ignored_list

def main():
    number_ignored = 0
    ignored_list = []
    exclude_list = [".obsidian", ".stfolder"]
    path = "./notes/"
    print("Iterating across files...")
    number_ignored, ignored_list = iterate_files(path, number_ignored, ignored_list, exclude_list)
    print("number ignored:", number_ignored)
    print("ignored files: ", ignored_list)
    print("Done.")

if __name__ == "__main__":
    main()