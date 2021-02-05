from sqlalchemy import and_
from database import db, ITEMS_PER_PAGE
from covid19.blueprints.common.common_model import CommonDateReported, CommonRegion


class EuropeDateReported(CommonDateReported):
    __mapper_args__ = {'polymorphic_identity': 'europe'}


class EuropeContinent(CommonRegion):
    __mapper_args__ = {'polymorphic_identity': 'europe'}


class EuropeCountry(db.Model):
    __tablename__ = 'europe_country'

    id = db.Column(db.Integer, primary_key=True)
    countries_and_territories = db.Column(db.String(255), nullable=False)
    pop_data_2019 = db.Column(db.String(255), nullable=False)
    geo_id = db.Column(db.String(255), nullable=False)
    country_territory_code = db.Column(db.String(255), nullable=False)

    continent_id = db.Column(db.Integer, db.ForeignKey('common_region.id'), nullable=False)
    continent = db.relationship('CommonRegion', lazy='subquery', order_by='CommonRegion.region')

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__ + " cascade")
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).limit(500)

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one()

    @classmethod
    def find_by(cls, countries_and_territories, geo_id, country_territory_code):
        return db.session.query(cls).filter(and_(
            (cls.countries_and_territories == countries_and_territories),
            (cls.geo_id == geo_id),
            (cls.country_territory_code == country_territory_code)
        )).one()

    @classmethod
    def find_by_continent(cls, continent, page):
        return db.session.query(cls)\
            .filter(cls.continent_id == continent.id)\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_germany(cls):
        return db.session.query(cls) \
            .filter(cls.country_territory_code == 'DEU') \
            .one_or_none()


class EuropeData(db.Model):
    __tablename__ = 'europe_data'

    id = db.Column(db.Integer, primary_key=True)
    deaths_weekly = db.Column(db.Integer, nullable=False)
    cases_weekly = db.Column(db.Integer, nullable=False)
    notification_rate_per_100000_population_14days = db.Column(db.Float, nullable=False)

    europe_country_id = db.Column(db.Integer, db.ForeignKey('europe_country.id'), nullable=False)
    europe_country = db.relationship('EuropeCountry', lazy='joined')

    europe_date_reported_id = db.Column(db.Integer, db.ForeignKey('common_date_reported.id'), nullable=False)
    europe_date_reported = db.relationship('EuropeDateReported', lazy='joined')

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__ + " cascade")
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).limit(500)

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls).filter(cls.id == other_id).one()

    @classmethod
    def find_by_date_reported(cls, europe_date_reported, page):
        #TODO: * Issue #43 /europe/date_reported
        return db.session.query(cls).filter(
            cls.europe_date_reported_id == europe_date_reported.id)\
            .order_by(cls.notification_rate_per_100000_population_14days.desc())\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_notification_rate(cls, europe_date_reported, page):
        # TODO: * Issue #43 /europe/date_reported
        return db.session.query(cls).filter(
            cls.europe_date_reported_id == europe_date_reported.id) \
            .order_by(cls.notification_rate_per_100000_population_14days.desc()) \
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_deaths_weekly(cls, europe_date_reported, page):
        # TODO: * Issue #43 /europe/date_reported
        return db.session.query(cls).filter(
            cls.europe_date_reported_id == europe_date_reported.id) \
            .order_by(cls.deaths_weekly.desc()) \
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_date_reported_cases_weekly(cls, europe_date_reported, page):
        # TODO: * Issue #43 /europe/date_reported
        return db.session.query(cls).filter(
            cls.europe_date_reported_id == europe_date_reported.id) \
            .order_by(cls.cases_weekly.desc()) \
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def find_by_country(cls, europe_country, page):
        return db.session.query(cls).filter(
            cls.europe_country_id == europe_country.id).paginate(page, per_page=ITEMS_PER_PAGE)