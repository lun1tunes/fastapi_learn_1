import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload
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
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[Post]:
    posts = [Post(tittle=tittle, user_id=user_id) for tittle in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(
    session: AsyncSession,
):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    # users = await session.scalars(stmt)
    # for user in users.unique():
    #     print("*" * 20)
    #     print(user)
    #     for post in user.posts:
    #         print("-", post)

    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print("*" * 20)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:
        print("post", post)
        print("author", post.user)


async def get_users_with_posts_and_profiles(
    session: AsyncSession,
):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)

    for user in users:
        print("*" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        .order_by(Profile.id)
        .where(User.username == "john")
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def main_realations(session: AsyncSession):
    # # await create_user(session=session, username="john")
    # # await create_user(session=session, username="john")
    # await create_user(session=session, username="alice")
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
    # await show_users_with_profiles(session)
    # await create_posts(
    #     session,
    #     user_john.id,
    #     "SQLA 2.0",
    #     "SQLA Joins",
    # )
    # await create_posts(
    #     session,
    #     user_sam.id,
    #     "FastAPI intro",
    #     "FastAPI Advanced",
    #     "FastAPI more",
    # )
    await get_users_with_posts(session=session)
    await get_posts_with_authors(session=session)
    await get_users_with_posts_and_profiles(session=session)
    await get_profiles_with_users_and_users_with_posts(session=session)


async def demo_m2m(session: AsyncSession):
    pass


async def main():
    async with db_helper.session_factory() as session:
        pass
        # await main_realations(session=session)
        await demo_m2m(session=session)


if __name__ == "__main__":
    asyncio.run(main())
