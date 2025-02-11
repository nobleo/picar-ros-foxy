import rclpy
from rclpy.node import Node


from geometry_msgs.msg import Twist

from pibot_pycontrol.motor_control import Motor


class PiBotController(Node):
    """Simple Ackermann steering controller for the PiCar Pro"""

    def __init__(self):
        super().__init__("pibot_controller")
        self.cmd_subscriber = self.create_subscription(
            Twist, "~/cmd_vel", self.cmd_vel_callback, 10
        )
        self.motor = Motor()
        # self.cmd_out_publisher = self.create_publisher(Twist, "topic", 10)
        # timer_period = 0.5  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0

    def timer_callback(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.z = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        self.cmd_out_publisher.publish(twist)
        self.get_logger().info(f"Publishing message: {twist}")
        self.i += 1

    def cmd_vel_callback(self, msg):
        self.get_logger().info(f"Got cmd_vel msg: {msg}")
        # Simply extract the angular.z = theta
        self.theta = msg.angular.z
        # Simply extract the linear.x = speed
        self.speed = msg.linear.x
        self.get_logger().info(f"Received Twist msg: speed {self.speed}, theta: {self.theta}")
        self._set_vehicle_speed(self.speed)

    def _set_vehicle_speed(self, speed):
        self.motor.command(speed, 0)

    def _set_steering_angle(self, theta):
        pass

    def calculate_odometry(self):
        # TODO
        pass


def main(args=None):
    rclpy.init(args=args)
    pibot_controller = PiBotController()
    rclpy.spin(pibot_controller)
    pibot_controller.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
