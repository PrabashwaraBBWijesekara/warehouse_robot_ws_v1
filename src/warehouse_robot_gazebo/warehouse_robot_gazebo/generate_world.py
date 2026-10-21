#!/usr/bin/env python3
"""Generate worlds/warehouse.sdf: empty warehouse + shelves + ArUco-marked boxes.

Reads  : config/layout.yaml, worlds/warehouse_empty.sdf
Writes : worlds/warehouse.sdf, config/box_manifest.yaml

Run from the package source tree:
    python3 warehouse_robot_gazebo/generate_world.py
"""
import math
from pathlib import Path

import yaml

# <pkg>/warehouse_robot_gazebo/generate_world.py -> parents[1] = <pkg>
PKG = Path(__file__).resolve().parents[1]
BOX_COLOR = "0.72 0.55 0.35 1"  # cardboard
MAX_MARKERS = 100               # aruco_0.png ... aruco_99.png


def box_sdf(idx, pose, size, mass, marker_size):
    """SDF for one box. The ArUco marker is on the box's local +X face."""
    sx, sy, sz = size
    ixx = mass / 12 * (sy**2 + sz**2)
    iyy = mass / 12 * (sx**2 + sz**2)
    izz = mass / 12 * (sx**2 + sy**2)
    x, y, z, yaw = pose
    tex = f"model://aruco_markers/textures/aruco_{idx:1d}.png"
    return f"""
    <model name="box_{idx:1d}">
      <pose>{x:.4f} {y:.4f} {z:.4f} 0 0 {yaw:.5f}</pose>
      <link name="link">
        <inertial>
          <mass>{mass}</mass>
          <inertia>
            <ixx>{ixx:.6f}</ixx><iyy>{iyy:.6f}</iyy><izz>{izz:.6f}</izz>
            <ixy>0</ixy><ixz>0</ixz><iyz>0</iyz>
          </inertia>
        </inertial>
        <collision name="collision">
          <geometry><box><size>{sx} {sy} {sz}</size></box></geometry>
          <surface>
            <friction><ode><mu>1.0</mu><mu2>1.0</mu2></ode></friction>
          </surface>
        </collision>
        <visual name="body">
          <geometry><box><size>{sx} {sy} {sz}</size></box></geometry>
          <material>
            <ambient>{BOX_COLOR}</ambient>
            <diffuse>{BOX_COLOR}</diffuse>
          </material>
        </visual>
        <visual name="marker">
          <pose>{sx / 2 + 0.0005:.4f} 0 0 0 0 0</pose>
          <geometry><box><size>0.001 {marker_size} {marker_size}</size></box></geometry>
          <material>
            <ambient>1 1 1 1</ambient>
            <diffuse>1 1 1 1</diffuse>
            <pbr><metal><albedo_map>{tex}</albedo_map></metal></pbr>
          </material>
        </visual>
      </link>
    </model>"""


def shelf_include(name, x, y, z, yaw):
    return f"""
    <include>
      <uri>model://shelf</uri>
      <name>{name}</name>
      <pose>{x} {y} {z} 0 0 {yaw}</pose>
    </include>"""


def main():
    cfg = yaml.safe_load((PKG / "config" / "layout.yaml").read_text())

    size = cfg["box_size"]
    mass = cfg["box_mass"]
    marker_size = cfg["marker_size"]
    front_offset = cfg["box_front_offset"]   # box centre along shelf-local Y
    levels = cfg["level_tops_z"]
    slots_x = cfg["slots_x"]
    first_id = cfg.get("marker_id_start", 0)

    idx = first_id
    out, manifest = [], []

    for shelf in cfg["shelves"]:
        sx, sy, sz, yaw = shelf["pose"]
        out.append(shelf_include(shelf["name"], sx, sy, sz, yaw))

        c, s = math.cos(yaw), math.sin(yaw)
        for top in levels:
            for lx in slots_x:
                if idx >= MAX_MARKERS:
                    raise SystemExit(
                        f"Out of markers (0-{MAX_MARKERS - 1}). "
                        "Reduce shelves, slots or levels."
                    )
                # shelf-local (lx, front_offset) -> world
                wx = sx + lx * c - front_offset * s
                wy = sy + lx * s + front_offset * c
                wz = sz + top + size[2] / 2 + 0.002  # 2 mm gap so boxes settle cleanly
                # Rotate box so its +X (marker face) points to shelf-local -Y (the aisle)
                box_yaw = yaw - math.pi / 2

                out.append(box_sdf(idx, (wx, wy, wz, box_yaw), size, mass, marker_size))
                manifest.append({
                    "id": idx,
                    "shelf": shelf["name"],
                    "x": round(wx, 3),
                    "y": round(wy, 3),
                    "z": round(wz, 3),
                    "yaw": round(box_yaw, 3),
                })
                idx += 1

    world_path = PKG / "worlds" / "warehouse_empty.sdf"
    world = world_path.read_text()
    if "</world>" not in world:
        raise SystemExit(f"No </world> tag found in {world_path}")

    block = "\n    <!-- GENERATED: shelves and boxes -->" + "".join(out) + "\n  "
    head, _, tail = world.rpartition("</world>")   # insert before the LAST </world>
    (PKG / "worlds" / "warehouse.sdf").write_text(head + block + "</world>" + tail)
    (PKG / "config" / "box_manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False))

    print(f"Wrote {idx - first_id} boxes (IDs {first_id}-{idx - 1}) "
          f"on {len(cfg['shelves'])} shelves -> worlds/warehouse.sdf")


if __name__ == "__main__":
    main()