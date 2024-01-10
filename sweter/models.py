from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class CarInfo(Base):
    __tablename__ = 'car_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String, nullable=False)
    car_name = Column(String, nullable=False)
    announce_id = Column(String, nullable=False, unique=True)
    car_price_usd = Column(String)
    car_price_uah = Column(String)
    car_race = Column(String)
    car_location = Column(String)
    vin_code = Column(String, nullable=False, unique=True)
    bid_link = Column(String)
    message_id = Column(String, nullable=True, unique=True, default=None)

    def update(self, data):
        result = False

        if data['car_price_usd'] != self.car_price_usd:
            self.car_price_usd = data['car_price_usd']
            self.car_price_uah = data['car_price_uah']

            result = True

        return result

    @staticmethod
    def create_from_dict(data):
        new_car = CarInfo(
            link=data['link'],
            car_name=data['car_name'],
            announce_id=data['announce_id'],
            car_price_usd=data['car_price_usd'],
            car_price_uah=data['car_price_uah'],
            car_race=data['car_race'],
            car_location=data['car_location'],
            vin_code=data['vin_code'],
            bid_link=data['bid_link'],
        )

        return new_car


engine = create_engine('sqlite:///car_info.db')

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    engine = create_engine('sqlite:///car_info.db')  # замените 'sqlite:///car_info.db' на ваше подключение к базе данных

    Base.metadata.create_all(engine)

