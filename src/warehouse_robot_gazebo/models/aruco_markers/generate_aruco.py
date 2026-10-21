import cv2
import os

# ArUco dictionary
# 6x6 markers, IDs 0-249
aruco_dict = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_6X6_250
)

# Output directory
output_dir = "textures"
os.makedirs(output_dir, exist_ok=True)

# Marker size in pixels
marker_size = 500

# Generate IDs 0 to 100
for marker_id in range(101):

    marker = cv2.aruco.generateImageMarker(
        aruco_dict,
        marker_id,
        marker_size
    )

    filename = os.path.join(
        output_dir,
        f"aruco_{marker_id}.png"
    )

    cv2.imwrite(filename, marker)

print("Successfully generated ArUco markers!")
print("IDs: 0 - 100")
print(f"Output directory: {output_dir}")
