import os

class VocabularyPath():
    def __init__(self, root_folder):
        self.root = root_folder
        os.makedirs(self.audio_cache_folder, exist_ok=True)

    @property
    def glossary(self):
        return self.cache_folder + os.sep + 'glossary.tmp'

    @property
    def sql_glossary(self):
        return self.cache_folder + os.sep + '.glossary'

    @property
    def cache_folder(self):
        return self.root + os.sep + '.glossary_cache'

    @property
    def audio_cache_folder(self):
        return self.cache_folder + os.sep + 'audio'

    def word_audio(self, word):
        return self.audio_cache_folder + os.sep + word + '.mp3'

    @classmethod
    def FromWordList(cls, word_list_html):
        import os
        root_folder = os.path.dirname(word_list_html)
        return cls(root_folder)