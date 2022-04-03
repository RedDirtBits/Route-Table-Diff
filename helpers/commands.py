
class RunCommand():
    """
    RunCommand A simple class similar to the one used for credentials.  Static methods to return commands
    to be run on Cisco devices

    Returns:
        str: show ip route
        str: show ip route | b Gateway
        str: show ip interface brief
        str: show ip interface brief | i up
    """

    @staticmethod
    def show_routes():
        return "show ip route"

    @staticmethod
    def show_routes_minimal():
        return "show ip route | b Gateway"

    @staticmethod
    def show_interfaces_all():
        return "show ip interface brief"

    @staticmethod
    def show_up_interfaces():
        return "show ip interface brief | i up"