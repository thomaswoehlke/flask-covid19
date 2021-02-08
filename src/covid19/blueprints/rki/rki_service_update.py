from database import db, app

from covid19.blueprints.rki.rki_model import RkiRegion, RkiDateReported, RkiCountry, RkiGermanyData
from covid19.blueprints.rki.rki_model import RkiGermanyDataImportTable


rki_service_update = None


class RkiServiceUpdate:
    def __init__(self, database):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Update [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.limit_nr = 20
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" RKI Service Update [ready]")

    def __update_who_date_reported(self):
        app.logger.info(" update who_date_reported [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for i_date_reported, in RkiGermanyDataImportTable.get_dates_reported():
            c = RkiDateReported.find_by_date_reported(i_date_reported)
            if c is None:
                o = RkiDateReported.create_new_object_factory(my_date_rep=i_date_reported)
                db.session.add(o)
                app.logger.info(" update who_date_reported "+i_date_reported+" added NEW")
            if i % 10 == 0:
                app.logger.info(" update who_date_reported "+i_date_reported+" not added")
                db.session.commit()
            i += 1
        db.session.commit()
        app.logger.info("")
        app.logger.info(" update who_date_reported [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_who_region(self):
        app.logger.info(" update who_region [begin]")
        app.logger.info("------------------------------------------------------------")
        i = 0
        for i_who_region, in db.session.query(RkiGermanyDataImportTable.who_region).distinct():
            c = db.session.query(RkiRegion).filter(RkiRegion.region == i_who_region).count()
            if c == 0:
                o = RkiRegion(region=i_who_region)
                db.session.add(o)
                app.logger.info(i_who_region +" added NEW ")
            else:
                app.logger.info(i_who_region +" not added ")
            if i % 10 == 0:
                db.session.commit()
            i += 1
        db.session.commit()
        app.logger.info("")
        app.logger.info(" update who_region [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_who_country(self):
        app.logger.info(" update who_country [begin]")
        app.logger.info("------------------------------------------------------------")
        sql_text = """
        select distinct 
            who_global_data_import.country_code,
            who_global_data_import.country,
            who_global_data_import.who_region
        from who_global_data_import
        """
        result = db.session.execute(sql_text).fetchall()
        for result_item in result:
            i_country_code = result_item.country_code
            i_country = result_item.country
            i_who_region = result_item.who_region
            output = i_country_code + " " + i_country + " " + i_who_region
            my_region = RkiRegion.find_by_region(i_who_region)
            my_country = RkiCountry.find_by_country_code_and_country_and_who_region_id(
                i_country_code, i_country, my_region
            )
            if my_country is None:
                o = RkiCountry(
                    country=i_country,
                    country_code=i_country_code,
                    region=my_region)
                db.session.add(o)
                db.session.commit()
                my_country = RkiCountry.find_by_country_code_and_country_and_who_region_id(
                    i_country_code, i_country, my_region
                )
                output += " added NEW "
            else:
                output += " not added "
            output += i_country_code + " id=" + str(my_country.id)
            app.logger.info(output)
        db.session.commit()
        app.logger.info("")
        app.logger.info(" update who_country [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_who_global_data(self):
        app.logger.info(" update WHO [begin]")
        app.logger.info("------------------------------------------------------------")
        dates_reported = RkiDateReported.get_all_as_dict()
        countries = RkiCountry.get_all_as_dict()
        #
        #
        i = 0
        result = RkiGermanyDataImportTable.get_all()
        for result_item in result:
            my_country = countries[result_item.country_code]
            my_date_reported = dates_reported[result_item.date_reported]
            result_who_global_data = RkiGermanyData.find_one_or_none_by_date_and_country(
                my_date_reported,
                my_country)
            if result_who_global_data is None:
                o = RkiGermanyData(
                    cases_new=int(result_item.new_cases),
                    cases_cumulative=int(result_item.cumulative_cases),
                    deaths_new=int(result_item.new_deaths),
                    deaths_cumulative=int(result_item.cumulative_deaths),
                    date_reported=my_date_reported,
                    country=my_country
                )
                db.session.add(o)
            if i % 2000 == 0:
                app.logger.info(" update WHO ... "+str(i)+" rows")
                db.session.commit()
            i += 1
        db.session.commit()
        app.logger.info(" update RKI :  "+str(i)+" total rows")
        app.logger.info(" update RKI [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_who_global_data_short(self):
        app.logger.info(" update RKI short [begin]")
        app.logger.info("------------------------------------------------------------")
        new_dates_reported_from_import = RkiGermanyDataImportTable.get_new_dates_as_array()
        i = 0
        for my_date_reported in new_dates_reported_from_import:
            my_date = RkiDateReported.find_by_date_reported(my_date_reported)
            for result_item in RkiGermanyDataImportTable.get_for_one_day(my_date_reported):
                my_country = RkiCountry.find_by_country_code(result_item.country_code)
                o = RkiGermanyData(
                    cases_new=int(result_item.new_cases),
                    cases_cumulative=int(result_item.cumulative_cases),
                    deaths_new=int(result_item.new_deaths),
                    deaths_cumulative=int(result_item.cumulative_deaths),
                    date_reported=my_date,
                    country=my_country
                )
                db.session.add(o)
                result_item.row_imported = True
                db.session.add(result_item)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" update WHO short ... "+str(i)+" rows")
                    db.session.commit()
            db.session.commit()
        app.logger.info(" update RKI short :  "+str(i)+" total rows")
        app.logger.info(" update RKI short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def __update_who_global_data_initial(self):
        app.logger.info(" update RKI initial [begin]")
        app.logger.info("------------------------------------------------------------")
        RkiGermanyData.remove_all()
        new_dates_reported_from_import = RkiGermanyDataImportTable.get_new_dates_as_array()
        i = 0
        for my_date_reported in new_dates_reported_from_import:
            my_date = RkiDateReported.find_by_date_reported(my_date_reported)
            for result_item in RkiGermanyDataImportTable.get_for_one_day(my_date_reported):
                my_country = RkiCountry.find_by_country_code(result_item.country_code)
                o = RkiGermanyData(
                    cases_new=int(result_item.new_cases),
                    cases_cumulative=int(result_item.cumulative_cases),
                    deaths_new=int(result_item.new_deaths),
                    deaths_cumulative=int(result_item.cumulative_deaths),
                    date_reported=my_date,
                    country=my_country
                )
                db.session.add(o)
                result_item.row_imported = True
                db.session.add(result_item)
                i += 1
                if i % 500 == 0:
                    app.logger.info(" update WHO initial ... "+str(i)+" rows")
                    db.session.commit()
            db.session.commit()
        app.logger.info(" update WHO initial :  "+str(i)+" total rows")
        app.logger.info(" update WHO initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_db(self):
        app.logger.info(" update db [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_who_date_reported()
        self.__update_who_region()
        self.__update_who_country()
        self.__update_who_global_data()
        app.logger.info(" update db [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_db_short(self):
        app.logger.info(" update db short [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_who_date_reported()
        self.__update_who_region()
        self.__update_who_country()
        self.__update_who_global_data_short()
        app.logger.info(" update db short [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_db_initial(self):
        app.logger.info(" update db initial [begin]")
        app.logger.info("------------------------------------------------------------")
        self.__update_who_date_reported()
        self.__update_who_region()
        self.__update_who_country()
        self.__update_who_global_data_initial()
        app.logger.info(" update db initial [done]")
        app.logger.info("------------------------------------------------------------")
        return self

    def update_who_country(self):
        self.__update_who_country()
        return self