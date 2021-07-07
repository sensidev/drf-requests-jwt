from setuptools import setup, find_packages

requires = [
    'requests>=2.18.1',
    'python-slugify>=1.2.4'
]

setup(
    name='drf_requests_jwt',
    version='0.15',
    description='Django Rest Framework Requests with JWT support',
    long_description=open('README.rst').read(),
    url='https://github.com/sensidev/drf-requests-jwt',
    author='Sensidev',
    author_email='lucian.corduneanu@sensidev.com',
    license='MIT',
    packages=find_packages(exclude=["tests*"]),
    install_requires=requires,
    setup_requires=['pytest-runner', 'requests'],
    tests_require=['pytest', 'mock'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

)
