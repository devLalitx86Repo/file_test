import pandas as pd
import numpy as np
import json
import math


class DataParser:

    DOLLOR = '$'
    DOLLOR_VALUE_K = '$K'
    DOLLOR_VALUE_M = '$M'
    VALUE_K = '#K'
    VALUE_DECIMAL_K = '#.##K'
    VALUE_M = '#M'
    VALUE_PERCENT = '%'
    VALUE_DECIMAL = '#.##'


    def __init__(self, file_path):
        self.db_path = file_path
        self.metadata_df = pd.read_excel(file_path, sheet_name='Metadata')
        self.client_info_df = pd.read_excel(file_path, sheet_name='Clients')


    def get_data(self):
        return self.metadata_df


    def get_client_data(self):
        return self.client_info_df
    

    def resolve_value(self, measure_key, datasheet, client_id):
        '''
        Get the value for the field
        '''
        # Step 1: Get the datasheet
        datasheet = pd.read_excel(self.db_path, sheet_name=datasheet)
        
        # Step 2: Get the row for the client ID
        client_row = datasheet[datasheet['Issuers'] == client_id]
        if client_row.empty:
            print(f"Client ID '{client_id}' not found in the DataFrame.")
            return None
        
        # Step 3: Get the value for the measure key
        if measure_key not in datasheet.columns:
            print(f"Measure key '{measure_key}' not found in the DataFrame.")
            return None
        
        value = client_row[measure_key].values[0]
        return value
    
        
    def format_value(self, value, format):
        '''
        Format the value based on the format with no decimal
        '''
        if format == self.DOLLOR_VALUE_K:
            return f"${math.floor(value/1000)}K"
        elif format == self.DOLLOR_VALUE_M:
            return f"${math.floor(value/1000000)}M"
        elif format == self.VALUE_K:
            return f"{math.floor(value/1000)}K"
        elif format == self.VALUE_M:
            return f"{math.floor(value/1000000)}M"
        elif format == self.VALUE_PERCENT:
            return f"{value}%"
        elif format == self.VALUE_DECIMAL:
            return f"{value:.2f}"
        elif format == self.DOLLOR:
            return f"${value}"
        elif format == self.VALUE_DECIMAL_K:
            return f"{(value/1000):.1f}K"
        return value
        
        

    def field_parse(self, field_info, datasheet, client_id):
        '''
        Parse the field information
        '''
        # Step 1: Parse the field information
        info = json.loads(field_info)
        data_props = {}
        data_props['measure_key'] = info['key']
        data_props['is_group'] = info['is_group']
        data_props['properties'] = info['properties']
        data_props['field_agg_type'] = info['type']

        # check if the name is present
        if 'series_name' in info:
            data_props['series_name'] = info['series_name']
        else:
            data_props['series_name'] = None

        # Step 2: Resolve the value for the field
        
        field_value = self.resolve_value(data_props['measure_key'], datasheet, client_id)
        data_props['field_value'] = self.format_value(field_value, data_props['properties']['format'])
        return data_props


    def get_data_props(self, field_info, datasheet, client_id):
        '''
        Get the data properties for the field
        '''
        data_props = self.field_parse(field_info, datasheet, client_id)
        return data_props
        
        