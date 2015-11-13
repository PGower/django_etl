class ETLPipeLine(object):
    def __init__(self, stdout, stderr):
        self.stdout = stdout
        self.stderr = stderr

    def setup(self):
        '''
        Perform any setup actions required to extract the data
        '''
        pass

    def extract(self):
        '''
        Extract the data from the source
        '''
        pass

    def transform(self):
        '''
        Perform any data transformations required
        '''
        pass

    def load(self):
        '''
        Load the transformed data into the destination
        '''
        pass

    def teardown(self):
        '''
        Perform cleanup actions required as a counterpart to setup
        '''
        pass

