import math
import os
from typing import Optional, Iterable, Tuple, List

def loadMods() -> Optional[Iterable[Tuple[str, str, str]]]:
    levels_dir = os.path.abspath("./vanilla/levels/")  # Use forward slashes for cross-platform compatibility
    mod_files: List[Tuple[str, str, str]] = []

    # Loop through every folder in the levels directory
    for folder_name in os.listdir(levels_dir):
        folder_path = os.path.join(levels_dir, folder_name)

        # Ensure it is a directory
        if os.path.isdir(folder_path):
            csv_file = None
            ini_file = None
            wav_file = None

            # Find .csv, .ini, and .wav files in the folder
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if file_name.endswith(".csv"):
                    csv_file = file_path
                elif file_name.endswith(".ini"):
                    ini_file = file_path
                elif file_name.endswith(".wav"):
                    wav_file = file_path

            # Ensure both .csv and .ini are found before adding to list
            if csv_file and ini_file:
                mod_files.append((csv_file, ini_file, wav_file))

    return mod_files if mod_files else None

def look0At(b: Tuple[int, int]) -> float:
    """
    Calculates the angle in degrees from the origin (0, 0) to a target position *b*.
    
    This function returns the angle formed between the line from the origin (0, 0) to the point *b*
    and the positive X-axis. The angle is calculated using `atan2`, which gives the angle in radians,
    and it is then converted to degrees. The angle is normalized to be between 0 and 360 degrees.
    
    Args:
        b (Tuple[int, int]): The target position (x, y) to look at.
    
    Returns:
        float: The angle in degrees, between 0 and 360.
    
    Example:
        look0At((1, 1)) -> 45.0
    """
    # Use atan2 to calculate the angle in radians
    angle = math.atan2(b[1], b[0])
    
    # Convert the angle from radians to degrees
    angle_deg = math.degrees(angle)
    
    # Ensure the angle is between 0 and 360 degrees
    if angle_deg < 0:
        angle_deg += 360
    
    return angle_deg

def lookAt(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """
    Calculates the angle in degrees from position *a* to position *b*.
    
    This function computes the angle between the line from point *a* to point *b* and the positive X-axis.
    The difference in coordinates is calculated, and `atan2` is used to find the angle in radians.
    The angle is then converted to degrees and normalized to be between 0 and 360 degrees.
    
    Args:
        a (Tuple[int, int]): The starting position (x1, y1).
        b (Tuple[int, int]): The target position (x2, y2).
    
    Returns:
        float: The angle in degrees, between 0 and 360.
    
    Example:
        lookAt((1, 1), (2, 2)) -> 45.0
    """
    # Calculate the difference in coordinates
    dx = b[0] - a[0]
    dy = b[1] - a[1]

    # Use atan2 to calculate the angle in radians
    angle = math.atan2(dy, dx)

    # Convert the angle from radians to degrees
    angle_deg = math.degrees(angle)

    # Ensure the angle is between 0 and 360 degrees
    if angle_deg < 0:
        angle_deg += 360

    return angle_deg

def clamp(a: int, b: Tuple[int, int]) -> int:
    """
    Clamps the value 'a' to be within the range defined by the tuple 'b'.
    
    If 'a' is larger than the maximum of 'b', it returns the upper bound.
    If 'a' is smaller than the minimum of 'b', it returns the lower bound.
    Otherwise, it returns 'a'.
    
    Args:
        a (int): The value to clamp.
        b (Tuple[int, int]): A tuple containing the two bounds for clamping.
        
    Returns:
        int: The clamped value of 'a'.
    
    Examples:
        clamp(6, (1, 5)) -> 5
        clamp(-9, (15, 10)) -> 10
        clamp(6, (1, 10)) -> 6
    """
    if a > max(b[0], b[1]):
        return b[1]
    if a < min(b[0], b[1]):
        return b[0]
    return a

def clamp2D(a: Tuple[int, int], b: Tuple[Tuple[int, int], Tuple[int, int]]) -> Tuple[int, int]:
    """
    Clamps a 2D point 'a' within a 2D rectangular boundary defined by 'b'.
    
    It applies the 'clamp' function independently to both the X and Y coordinates.
    
    Args:
        a (Tuple[int, int]): The 2D point to clamp (x, y).
        b (Tuple[Tuple[int, int], Tuple[int, int]]): A tuple of two 2D points defining the clamping bounds.
        
    Returns:
        Tuple[int, int]: The clamped 2D point.
    
    Examples:
        clamp2D((7, 4), ((1, 8), (5, 9))) -> (7, 5)
    """
    return (clamp(a[0], b[0]), clamp(a[1], b[1]))

def clamp2DBox(apos: Tuple[int, int], asiz: Tuple[int, int], box: Tuple[int, int]) -> Tuple[int, int]:
    """
    Clamps a 2D object's position within a bounding box, ensuring the entire object fits inside.
    
    The object's position ('apos') is clamped so that it stays within the bounds defined by 'box'.
    The object has a size ('asiz'), and this ensures it doesn't extend outside the box.
    
    Args:
        apos (Tuple[int, int]): The position of the top-left corner of the object (x, y).
        asiz (Tuple[int, int]): The size of the object (width, height).
        box (Tuple[int, int]): The size of the bounding box (box width, box height).
        
    Returns:
        Tuple[int, int]: The clamped position of the object.
    
    Examples:
        clamp2DBox((4, 4), (2, 2), (5, 5)) -> (3, 4)
    """
    # Clamping the X coordinate so that the object stays within the box
    x_clamped = clamp(apos[0], (0, box[0] - asiz[0]))
    # Clamping the Y coordinate similarly
    y_clamped = clamp(apos[1], (0, box[1] - asiz[1]))
    return (x_clamped, y_clamped)

import math

def normalize(vector: Tuple[int, int]):
    """Normalize a 2D vector.

    Args:
        vector (Tuple[int, int]): A tuple representing the vector (x, y).

    Returns:
        tuple: A normalized vector (x, y) with length 1.
    """
    x, y = vector
    magnitude = math.sqrt(x ** 2 + y ** 2)

    if magnitude == 0:
        return (0, 0)  # Avoid division by zero; return a zero vector

    return (x / magnitude, y / magnitude)