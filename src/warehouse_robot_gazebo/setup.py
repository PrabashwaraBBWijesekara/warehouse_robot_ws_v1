import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'warehouse_robot_gazebo'


def tree(src):
    """Install every file under `src` (e.g. models/) keeping its folder structure."""
    return [
        (os.path.join('share', package_name, root),
         [os.path.join(root, f) for f in files])
        for root, _, files in os.walk(src) if files
    ]


setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ] + tree('models'),
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='prabashwara',
    maintainer_email='prabashwara21@gmail.com',
    description='Warehouse robot Gazebo simulation: world, shelves and ArUco boxes',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)