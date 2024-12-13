from datetime import datetime


class Order:
    def __init__(self, user_id, device_type, device_name, description, created_at=None):
        self.user_id = user_id
        self.device_type = device_type
        self.device_name = device_name
        self.description = description
        self.created_at = created_at or datetime.now().strftime("%m.%d.%Y %H:%M:%S") # Автоматическое заполнение

    def __repr__(self):
        return f"Order(user_id={self.user_id}, device_type='{self.device_type}', device_name='{self.device_name}', description='{self.description}', created_at='{self.created_at}')"
