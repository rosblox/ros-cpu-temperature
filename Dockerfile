ARG ROS_DISTRO

FROM ros:${ROS_DISTRO}-ros-core

RUN apt update && apt install -y --no-install-recommends python3-rpi.gpio python3-pip python3-colcon-common-extensions && rm -rf /var/lib/apt/lists/*

COPY ros_entrypoint.sh .


WORKDIR /colcon_ws
COPY ros_cpu_temperature src/ros_cpu_temperature

RUN . /opt/ros/${ROS_DISTRO}/setup.sh && colcon build --symlink-install


RUN echo 'alias build="colcon build --cmake-args --symlink-install  --event-handlers console_direct+"' >> ~/.bashrc
RUN echo 'alias run="ros2 run ros_cpu_temperature ros_cpu_temperature_publisher"' >> ~/.bashrc
