from setuptools import setup

__version__ = '0.0.1'

setup(
    name="nslr_hmm",
    version=__version__,
    author='Jami Pekkanen',
    author_email='jami.pekkanen@gmail.com',
    url='https://gitlab.com/nslr/nslr-hmm',
    description='Python implementation of the NSLR-HMM eye movement identification algorithm.',
    long_description='',
    # install_requires=['nslr>0.0.5'], #TODO: Uncomment when this is merged https://gitlab.com/nslr/nslr/merge_requests/1
    packages=['nslr_hmm'],
    zip_safe=False,
    platforms=['any'],
)
