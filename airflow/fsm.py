from sqlalchemy import Column, String

from database import Base


class TicketSearchFSM(Base):
    __abstract__ = True

    state = Column(String(10), nullable=False, default='PENDING')

    def complete(self):
        if self.state != 'PENDING':
            raise ValueError('State is not in PENDING')
        self.state = 'COMPLETE'

    # Попытка заюзать sqlalchemy-fsm провалилась
