import nltk

packages = ['maxent_ne_chunker', 'words', 'treebank', 'maxent_treebank_pos_tagger', 'punkt', 'averaged_perceptron_tagger']


def download_nltk_data():
    for package in packages:
        try:
            nltk.data.find(package)
        except LookupError:
            nltk.downloader.download(package, quiet=True)


download_nltk_data()
