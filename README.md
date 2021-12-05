# remove-yaml-matter

The purpose of this script is to update file creation date of all files in a directory based on the `created` tag in YAML front matter and remove front matter from Markdown file. Path to target directory is specified explicitly in the script.

Needed to be done after exporting notes from standardnotes application and using script from [standardnotes-to-markdown-yaml-export](https://github.com/hozza/standardnotes-to-markdown-yaml-export) tool to convert to markdown.

Could have created an export script of my own to keep creation date, not include a YAML front matter section, and move files to foldering structure (instead of all in one folder) used with tags in standardnotes. However, the creation date was already lost after exporting notes from standardnotes application and I had already sorted the notes manually so I decided to remedy existing exported files instead.

## Requirements

- Python 3.9

## Execution

```bash
pip install -r requirements.txt
python remove-yaml-matter.py >> output.log
```

## Resources
- https://stackoverflow.com/questions/4996405/how-do-i-change-the-file-creation-date-of-a-windows-file
- https://stackoverflow.com/questions/31531947/converting-timestamp-to-unix-date-python