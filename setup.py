from setuptools import setup, find_packages

setup(name='sms3',
      description='SMS sending and receiving with enfora gsm modems',
      long_description=open('README.txt').read(),
      author='Karolis Ryselis',
      author_email='djryse@gmail.com',
      url='https://github.com/ryselis/sms3',
      license='MIT',
      version='0.1',
      packages=find_packages(),
      package_data={'sms': ['*.txt']},
      zip_safe=False,
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Topic :: Communications :: Telephony'
      ],
      install_requires=['pyserial', 'setuptools'],
      )
