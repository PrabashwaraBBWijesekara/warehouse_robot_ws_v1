import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (AppendEnvironmentVariable, DeclareLaunchArgument,
                            IncludeLaunchDescription)
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution


def generate_launch_description():
    pkg = get_package_share_directory('warehouse_robot_gazebo')
    gz_launch = os.path.join(
        get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')

    world_arg = DeclareLaunchArgument(
        'world', default_value='warehouse.sdf',
        description='World file inside the package worlds/ folder')
    headless_arg = DeclareLaunchArgument(
        'headless', default_value='false',
        description='true = server only, no GUI')

    world_path = PathJoinSubstitution([pkg, 'worlds', LaunchConfiguration('world')])

    # Lets Gazebo resolve model://shelf, model://warehouse, model://aruco_markers.
    # Appends rather than overwrites, and only applies to this launch.
    resource_path = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH', os.path.join(pkg, 'models'))

    sim_with_gui = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch),
        launch_arguments={'gz_args': ['', world_path]}.items(),
        condition=UnlessCondition(LaunchConfiguration('headless')),
    )

    sim_headless = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gz_launch),
        launch_arguments={'gz_args': ['-r -s ', world_path]}.items(),
        condition=IfCondition(LaunchConfiguration('headless')),
    )

    return LaunchDescription([
        world_arg, headless_arg, resource_path, sim_with_gui, sim_headless,
    ])