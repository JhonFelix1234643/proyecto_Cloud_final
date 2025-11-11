from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.entities.user import User
from app.infrastructure.database.models import UserModel

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[User]:
        result = await self.session.execute(select(UserModel))
        users = result.scalars().all()
        return [User(id=user.id, name=user.name, email=user.email, age=user.age) for user in users]

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()
        if user:
            return User(id=user.id, name=user.name, email=user.email, age=user.age)
        return None

    async def create(self, user: User) -> User:
        db_user = UserModel(
            name=user.name,
            email=user.email,
            age=user.age
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return User(id=db_user.id, name=db_user.name, email=db_user.email, age=db_user.age)

    async def update(self, user_id: int, user_data: dict) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        db_user = result.scalar_one_or_none()
        if db_user:
            for key, value in user_data.items():
                setattr(db_user, key, value)
            await self.session.commit()
            await self.session.refresh(db_user)
            return User(id=db_user.id, name=db_user.name, email=db_user.email, age=db_user.age)
        return None

    async def delete(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        db_user = result.scalar_one_or_none()
        if db_user:
            await self.session.delete(db_user)
            await self.session.commit()
            return True
        return False