from dataclasses import asdict

from sqlalchemy import select

from brain_agriculture.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='felipe', password='123456', email='felipe@test.com'
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'felipe'))

    assert asdict(user) == {
        'id': 1,
        'username': 'felipe',
        'password': '123456',
        'email': 'felipe@test.com',
    }
