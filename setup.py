from setuptools import setup, find_packages

install_requires = [
    'lemur',
]

setup(
    name='lemur_manualissuer',
    version='0.1.0',
    author='Jose Plana',
    author_email='jplana@tuenti.com',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
    license='MIT',
    entry_points={
       'lemur.plugins': [
            'manualissuer = lemur_manualissuer.plugin:ManualIssuer'
        ],
    },
)
