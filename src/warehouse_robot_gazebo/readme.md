# Warehouse Robot Gazebo Simulation

This package contains the Gazebo simulation environment, worlds, and models for the Warehouse Robot project.

## 1. Building the Package

Navigate to your workspace and build only the `warehouse_robot_gazebo` package using `colcon`. We recommend using `--symlink-install` so that you don't have to rebuild the package every time you tweak Python scripts or configuration files.

```bash
cd ~/warehouse_robot_ws_v1
colcon build --symlink-install --packages-select warehouse_robot_gazebo
source install/setup.bash
```

## 2. Verifying the Installation

After building, it is a good practice to verify that all necessary directories and models were installed correctly in the `share` directory.

Check the main package share directory:
```bash
ls install/warehouse_robot_gazebo/share/warehouse_robot_gazebo/
```
*Expected output should include:* `launch`, `worlds`, `config`, `models`, `package.xml`

Next, verify that the simulation models were successfully copied:
```bash
ls install/warehouse_robot_gazebo/share/warehouse_robot_gazebo/models
```
*Expected output should include:* `warehouse`, `shelf`, `aruco_markers`

## 3. Launching the Simulation

Once built and sourced, you can launch the Gazebo simulation using the provided launch file:

```bash
ros2 launch warehouse_robot_gazebo sim.launch.py
```