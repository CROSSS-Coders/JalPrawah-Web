from apiwrapper import APIWrapper
import datetime


class Cwcapi(APIWrapper):

    def fetch_stations_info(self, code):
        """
        @param: code
        @return: Response
        Uses Fetch dam info methos from url
        """
        url = 'http://ffs.tamcnhp.com/iam/api/layer-station/'+code
        return self.make_request(url, method='get', headers={'class-name': 'ForecastDetailLayerStationDto'}, data=None, callback=None).parsed

    def fetch_datatype_info(self, code,datatype):
        """
        @param: code
        @return: Response
        Uses Fetch dam hhs(Water level) info methos from url
        """
        url = "http://ffs.tamcnhp.com/iam/api/new-entry-data/specification/sorted?sort-criteria=%7B%22sortOrderDtos%22:%5B%7B%22sortDirection%22:%22ASC%22,%22field%22:%22id.dataTime%22%7D%5D%7D&specification=%7B%22where%22:%7B%22where%22:%7B%22where%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22id.stationCode%22,%22operator%22:%22eq%22,%22value%22:%22"+code+"%22%7D%7D,%22and%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22id.datatypeCode%22,%22operator%22:%22eq%22,%22value%22:%22"+datatype+"%22%7D%7D%7D,%22and%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22dataValue%22,%22operator%22:%22null%22,%22value%22:%22false%22%7D%7D%7D,%22and%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22id.dataTime%22,%22operator%22:%22btn%22,%22value%22:%222020-07-20T18:00:00.000,"+str(datetime.datetime.now().isoformat())+"%22%7D%7D%7D"
        return self.make_request(url, method='get', headers={'class-name': 'NewEntryDataDto'}, data=None, callback=None).parsed

    def fetch_location_info(self):
        """
        @return response
        Fetch location information
        """
        url = "http://ffs.tamcnhp.com/iam/api/layer-station-geo/specification/?specification=%7B%22where%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22layerStationStationCode.floodForecastStaticStationCode.type%22,%22operator%22:%22eq%22,%22value%22:%22Level%22%7D%7D,%22or%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22layerStationStationCode.floodForecastStaticStationCode.type%22,%22operator%22:%22eq%22,%22value%22:%22Inflow%22%7D%7D%7D"
        return self.make_request(url, method='get', headers={'class-name': 'LayerStationGeoDto'}, data=None, callback=None).parsed
