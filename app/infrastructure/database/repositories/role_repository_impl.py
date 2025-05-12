# from typing import List
# from sqlalchemy.orm import Session
# from ..models.role import Role


# class RoleRepository(IRoleRepository):

#     def __init__(self, session: Session):
#         self.session = session

#     def get_all(self) -> List[Role]:
#         list_role = self.session.query(Role).all()

#         return list_role
