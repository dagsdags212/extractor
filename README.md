# Extractor

A tool for extracting links and images from websites.

## Installation

Run the following commands in sequence to install locally:
```
git clone https://github.com/dagsdags212/extractor.git
```

## Usage

### Initialization

A path pointing to the default download directories can be specified in `config.toml` file.

A minimal example config file is given below:
```
[downloads]
article = path/to/article/downloads
figures = path/to/figure/downloads 
```

### Arguments and Flags

Extractor requires `url` as the only required positional argument. The user
can pass in optional flag as listed below:

| Flag         | Alias | Description                                                |
| ------------ | ----- | :--------------------------------------------------------- |
| --abstract   | -s    | diplay the abstract                                        |
| --authors    | -a    | display the list of authors                                |
| --info       | -i    | display article info                                       |
| --references | -r    | display a list of references used by the article           |
: program parameters that require a value to be passed.

| Flag         | Description                                                |
| ------------ | :--------------------------------------------------------- |
| --download   | download file to path specified in config.toml file        |
| --figures    | download all figures to path specified in config.toml file |
: boolean flags.

Get a description of the article:
```
extractor 'url'

# verbosely pass in the --info flag
extractor 'url' --info 
```

Display the summary of an article:
```
extractor 'url' --abstract
extractor 'url' -s > summary.txt # save to file
```

Display the list of author:
```
extractor 'url' --authors
extractor 'url' -a > authors.txt # save to file
```

Display a list of references used in the article:
```
extractor 'url' --references
extractor 'url' --r > references.txt # save to file
```

Download a copy of the article in .pdf format:
```
extractor 'url' --download
```

Save all the figures used in the article to an image directory:
```
extractor 'url' --figures
```
