import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    # # тут можем получить None, в этом случае обращатся например к user.username нельзя (если выпаден None будет так же исключение)
    # # user: User | None = result.scalar_one_or_none()
    # в случае ниже мы должны быть готовы ловить исключение
    # user: User = result.scalar_one()
    user: User | None = await session.scalar(stmt)
    print("found user", username, user)
    return user


async def create_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None,
    last_name: str | None,
    bio: str | None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        bio=bio,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession) -> list[User]:
    pass


async def main():
    async with db_helper.session_factory() as session:
        pass
        # # await create_user(session=session, username="john")
        # # await create_user(session=session, username="sam")
        # user_sam = await get_user_by_username(session=session, username="sam")
        # user_john: User = await get_user_by_username(session=session, username="john")
        # profile_sam: Profile = await create_profile(
        #     session=session,
        #     user_id=user_sam.id,
        #     first_name="sam",
        #     last_name="males",
        #     bio="hi am gay!",
        # )
        # profile_john: Profile = await create_profile(
        #     session=session,
        #     user_id=user_john.id,
        #     first_name="john",
        #     last_name="boobs",
        #     bio="ABOBA",
        # )


if __name__ == "__main__":
    asyncio.run(main())
