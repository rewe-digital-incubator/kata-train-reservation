from setuptools import setup, find_packages

setup(
    name='train-reservation',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        train_data_service=train_reservation.cli:train_data_service
        booking_reference_service=train_reservation.cli:booking_reference_service
    ''',
    url='https://github.com/rewe-digital-incubator/kata-train-reservation',
    license='MIT License',
    author='',
    author_email='',
    description=''
)
