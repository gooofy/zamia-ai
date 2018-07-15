from setuptools import setup
import os

df = []
for m in os.listdir('modules'):
    for f in os.listdir('modules/%s' % m):
        if f.endswith('.py') or f.endswith('.pl'):
            df.append(('share/zamia-ai/modules/%s' % m, ['modules/%s/%s' % (m, f)]))
 
# print repr(df)

setup(
    name                 = 'zamia-ai',
    version              = '0.1.1',
    description          = 'Free and open source A.I. system based on Python, TensorFlow and Prolog.',
    long_description     = open('README.md').read(),
    author               = 'Guenter Bartsch',
    author_email         = 'guenter@zamia.org',
    maintainer           = 'Guenter Bartsch',
    maintainer_email     = 'guenter@zamia.org',
    url                  = 'https://github.com/gooofy/zamia-ai',
    packages             = ['zamiaai'],
    install_requires     = [
                            'py-nltools', 'pyxsb', 'cmdln', 'pytz', 'tzlocal', 'six', 'sqlalchemy'
                           ],
    scripts              = [ 'zaicli' ],
    classifiers          = [
                               'Operating System :: POSIX :: Linux',
                               'License :: OSI Approved :: Apache Software License',
                               'Programming Language :: Python :: 2',
                               'Programming Language :: Python :: 2.7',
                               'Programming Language :: Python :: 3',
                               'Programming Language :: Python :: 3.5',
                               'Programming Language :: Cython',
                               'Programming Language :: C++',
                               'Intended Audience :: Developers',
                               'Topic :: Software Development :: Libraries :: Python Modules',
                               'Topic :: Multimedia :: Sound/Audio :: Speech'
                               'Topic :: Scientific/Engineering :: Artificial Intelligence'
                           ],
    license              = 'Apache',
    keywords             = 'natural language processing tokenizer nlp tts asr speech synthesis recognition tensorflow artificial-intelligence natural-language-processing prolog knowledgebase semantic-web',
    data_files           = df
    )

