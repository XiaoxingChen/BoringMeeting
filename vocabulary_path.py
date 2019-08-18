class VocabularyPath():
    def __init__(self, root_folder):
        self.root = root_folder
    
    @property
    def glossary(self):
        return self.root + '/glossary.yaml'
    
    @property
    def cache_folder(self):
        return self.root + '/boring_cache'

    @property
    def audio_cache_folder(self):
        return self.cache_folder + '/audio'

    @classmethod 
    def FromWordList(cls, word_list_html):
        import os
        root_folder = os.path.dirname(word_list_html)
        return cls(root_folder)