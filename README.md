**dupi** is a Python3 tool for finding duplicate files. It generates and stores
hashes for file contents as well as stats such as size and timestamps in an
index, and provides an interface for updating and querying the index for
duplicate file contents.

The motivation for an index-based file duplication detection tool is to persist
and reuse the results of potentially computationally intensive content hashing
for large numbers of large files across multiple comparisons.


## Usage

**dupi** consists of a number of subcommands, generally organized around either
index manipulation, or index querying. To get help on available options:

        dupi -h

To get help for any subcommand:

        dupi [subcommand] -h

### Index Manipulation

Update the index with hashes and stats from files within a directory tree:

        dupi update [dirs [dirs ...]]

Purge the entire index contents:

        dupi purge

Show statistics for the overall index:

        dupi stats

### Index Queries

List all duplicate files in the index:

         dupi list

List all files in the index, annotated with either 'o' if an original, or 'd'
if a duplicate:

        dupi report