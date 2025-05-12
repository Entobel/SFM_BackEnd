from dataclasses import dataclass


@dataclass
class AccessPolicyContext:
    target_user_id: int
    target_role_id: int
    target_department_id: int
    actor_user_id: int
    actor_role_id: int
    actor_department_id: int
