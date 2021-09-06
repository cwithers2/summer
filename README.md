# summer.py
A command-line tool to summarize text.

Given a body of text, _summer_ attempts to find the most important sentences. The process involves finding the **TF-IDF** value for each term in the text, then creating a running total for each sentence. By default, the top five scoring sentences are printed.

**NOTE**: In an attempt to improve readability, the printed sentences are also sorted by their occurance in the original text.

## Dependencies
- `python3-nltk`

In addition to `python3-nltk` you need the `punkt` tokenizer they provide.

The following command installs the the tokenizer in the directory $HOME/nltk_data:

    $ python3 nltk.downloader punkt

Use these commands to install the tokenizer as an administrator:

|OS     |command                                                        |
|-------|---------------------------------------------------------------|
|Windows|`python -m nltk.downloader -d C:\nltk_data punkt`              |
|Mac    |`python -m nltk.downloader -d /usr/local/share/nltk_data punkt`|
|Unix   |`python -m nltk.downloader -d /usr/share/nltk_data punkt`      |

## Usage

    summer.py [-h] [-n NUM] [-s STOP] [filename]

<table>
  <tr>
    <th>Argument</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>filename</td>
    <td>A file with text to summarize (Optional).<br/>
        Input is read from stdin if `filename` is ommitted.</td>
  </tr>
  <tr>
    <td>-n NUM, --num NUM</td>
    <td>The number of sentences to print (Optional).<br/>
        Default is 5; 0 prints all.</td>
  </tr>
  <tr>
    <td>-s STOP, --stop STOP</td>
    <td>A file with stopwords to load (Optional).<br/>
        If ommitted, all terms are processed.</td>
  </tr>
</table>
