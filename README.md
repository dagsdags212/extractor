# Extractor

A tool for extracting links and images from websites.

## Usage

Extractor requires `url` as the only required positional argument. The user
can pass in optional flag as listed below:

| Flag         | Alias | Description                                         |
| ------------ | ----- | --------------------------------------------------- |
| --abstract   | -a    | diplay the abstract                                 |
| --download   | -d    | download file to a specified directry               |
| --figures    | -f    | extract all figures and save to a directory         |
| --references | -r    | display a list of references used by the article    |

Display the abstract of an article:
```
extractor 'url' --abstract 
```

Display a list of references used in the article:
```
extractor 'url' --references
```

Download a copy of the article to a downloads directory in .pdf format:
```
DOWNLOAD_DIR=/home/downloads
extractor 'url' --download $DOWNLOAD_DIR
extractor 'url' -d $DOWNLOAD_DIR
```

Save all the figures used in the article to a image directory:
```
IMG_DIR=/home/images
extractor 'url' --figures $IMG_DIR
extractor 'url' -f $IMG_DIR
```
