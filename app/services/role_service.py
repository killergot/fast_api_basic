USER_ROLE: int = 0 # anyone
ADMIN_ROLE: int = 1 # 2^0

class RoleService:
    def is_admin(self, user) -> bool:
        return user.role & ADMIN_ROLE
