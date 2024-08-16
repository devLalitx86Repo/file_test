import json
from utils.data_parser import DataParser
from utils.ppt_generator import PPTGenerator

class ChartBuilder:
    def __init__(self, data_parser: DataParser, chart_name, chart_config, data_sheet, client_id):
        self.data_parser = data_parser
        self.chart_name = chart_name
        self.parse_chart_data(chart_config, data_sheet, client_id)

    def parse_series_data(self, series_data):
        '''
        Parse the series data
        '''
        delimeter = series_data['properties']['value_delimiter']
        axis_series_data = series_data['field_value'].split(delimeter)
        return axis_series_data


    def populate_data(self, x_axis, y_axis, data_sheet, client_id):
        '''
        Populate the data for the chart
        '''
        # 3. resolve the data props
        self.x_axis = self.data_parser.field_parse(json.dumps(x_axis), data_sheet, client_id)
        self.x_axis['field_value'] = self.parse_series_data(self.x_axis)
        # now the y axis is a list of fields
        self.y_axis = []
        self.series_names = []
        for field_info in y_axis:
            # print(field_info)
            series_name = field_info['series_name'] if 'series_name' in field_info else None
            self.series_names.append(series_name)
            field_data_prop = self.data_parser.field_parse(json.dumps(field_info), data_sheet, client_id)
            field_data_prop['field_value'] = self.parse_series_data(field_data_prop)
            self.y_axis.append(field_data_prop)
            
        

    def parse_chart_data(self, chart_config, data_sheet, client_id):
        '''
        Parse the chart data from the configuration
        '''
        chart_config = json.loads(chart_config)
        # 1. Get the chart type
        self.chart_type = chart_config['chart_type']

        # 2. resolve the data props
        config_x_axis = chart_config['x_axis']
        config_y_axis = chart_config['y_axis']
        self.populate_data(config_x_axis, config_y_axis, data_sheet, client_id)


    def __str__(self):
        return f"ChartBuilder: {self.chart_type}, X-Axis: {self.x_axis}, Y-Axis: {self.y_axis}"


    def build(self, ppt_generator: PPTGenerator, slide):
        '''
        Build the chart
        '''
        categories = self.x_axis['field_value']
        series = [config['field_value'] for config in self.y_axis]
        ppt_generator.update_chart(slide, self.chart_name, categories, series, self.series_names)
        pass





