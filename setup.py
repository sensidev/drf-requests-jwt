from setuptools import setup, find_packages

setup(name='drf_requests_jwt',
      version='0.2',
      description='Django Rest Framework Requests with JWT support',
      url='https://github.com/sensidev/drf-requests-jwt',
      author='Sensidev',
      author_email='lucian.corduneanu@sensidev.com',
      license='MIT',
      packages=find_packages(exclude=["tests*"]),
      zip_safe=False)
