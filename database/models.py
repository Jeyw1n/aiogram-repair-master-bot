from datetime import datetime


class Order:
    def __init__(self, user_id, device_type, device_name, description, status=0, created_at=None, order_id=None):
        self.user_id = user_id
        self.device_type = device_type
        self.device_name = device_name
        self.description = description
        self.status = status 
        self.created_at = created_at or datetime.now().strftime("%m.%d.%Y %H:%M:%S")
        self.order_id = order_id