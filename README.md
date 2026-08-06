# Drawing Robot Arm algorithm

### Caution: NO ROBOT RUNNING CODE IN THIS REPO. ONLY DRAWING ALGORITHM IS PRESENTED
1. Capture the image
2. Get edge information using Canny Edge Detection
3. Start from left bottom, sequentially search nearby edge pixel and save the path.
4. send bundle of line information to robot.
5. arguments.py is not available yet.

## Run code
``` bash
python main.py
```

## Path Verification

Run `get_path_video.py` to generate a simulation video showing the path that the robot will follow.

## Data Structure

```text
image/
├── test.jpg                  # Original input image
└── test/
    ├── test_edge.jpg         # Detected edges
    ├── test_final.jpg        # Final path after removing noise and short segments
    │                         # (the path the robot will actually follow)
    └── test_line.txt         # Path commands for the robot
```

## Demo video
https://www.youtube.com/shorts/O7QId9yMkKg
