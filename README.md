## How to Run the Script: `change_log.py`

To run the script, use the following command:

.\change_log.py [switches] [filters] <file>


### Switches:

- `--end-version "version"`: The script will parse all logs up to the given version.
- `--end-commit "commit"`: The script will parse all logs up to the given commit.
- `--similarity-value <0-100>`: Specifies the percentage of commit message similarity required for an artifact to be considered for log removal.

### Filters:

- `--author "name"`: The script will retain only commits created by the given author (name, surname, or email).
- `--date "Month DD YY"`: The script will retain only commits created on the specified date format (Month: Jan, Feb, Mar..., DD: 0-31, YY: 2021-2022).
- `--artf "artf"`: The script will retain only commits related to the given artifact.

### File:

`<file>` refers to the file containing the Git logs to parse.
