#!/usr/bin/python3

import time
import psutil

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Temperature


class RosCpuTemperaturePublisher(Node):

    def __init__(self):
        super().__init__('ros_cpu_temperature_publisher')
        self.publisher_ = self.create_publisher(Temperature, 'cpu_temperature', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Temperature()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.temperature = self.get_cpu_temperature()
        self.publisher_.publish(msg)


    def get_cpu_temperature(self):
        system_temperatures = psutil.sensors_temperatures()

        if 'coretemp' in system_temperatures: 
            cpu_temperature = psutil.sensors_temperatures()['coretemp'][0].current
        elif 'cpu_thermal' in system_temperatures:
            cpu_temperature = psutil.sensors_temperatures()['cpu_thermal'][0].current
        else:
            cpu_temperature = float('NaN')
            self.get_logger().warn('No thermal sensor found')

        return cpu_temperature

def main(args=None):
    rclpy.init(args=args)

    ros_cpu_temperature_publisher = RosCpuTemperaturePublisher()

    rclpy.spin(ros_cpu_temperature_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    ros_cpu_temperature_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
