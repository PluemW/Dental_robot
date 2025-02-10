import os

from glob import glob
from setuptools import find_packages, setup

package_name = 'robot_node'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join("share", package_name, "launch"), glob("launch/*launch.py")),
        (os.path.join("share", package_name, "config_params"), glob("config_params/*.yaml")),
        (os.path.join("share", package_name, "program"), glob("program/*.py")),
        (os.path.join("share", package_name, "program/templates"), glob("program/templates/*.html")), 
        (os.path.join('share', package_name, 'program/static'), glob('program/static/*')),
        (os.path.join('share', package_name, 'program/image'), glob('program/image/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pw-wq',
    maintainer_email='jaroenwachiirasak@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "camera_node = robot_node.camera:main",
            "drive_node = robot_node.drive_node:main",
            "gripper_node = robot_node.gripper_node:main",
        ],
    },
)
