'''
Updated By: Lalit Gupta
Date: 2023-07-31
'''
import os
import time

from utils.data_parser import DataParser
from utils.ppt_generator import PPTGenerator
from utils.line_chart import LineChart
from utils.waterfall_chart import WaterfallChart

from chart_utils.chart_builder import ChartBuilder

# Performance Improvement
PERFORMANCE_SUBJECT = 500

TYPE_PLACEHOLDER = 'placeholder'
TYPE_LINE_CHART = 'line_chart'
TYPE_LINE_CHART_2 = 'line_chart_2'  # Multiple line chart in this case 2 lines
TYPE_WATERFALL_CHART = 'waterfall_chart'


def resolve_text_placeholder(ppt_generator: PPTGenerator, slide, field_name, data_props):
    '''
    Update the placeholder with the field data
    '''
    #Step 1: Fetch the value for the field
    field_value = data_props['field_value']
    # field_name = data_props['measure_key']

    #Step 2: Update the placeholder with the field value
    ppt_generator.update_placeholder(slide, field_name, field_value)



def build_chart(ppt_generator: PPTGenerator, data_parser: DataParser, slide, ppt_chart_name, chart_config, data_sheet, client_id):
    '''
    Build the chart
    '''
    # Step 1: Initialize the Chart
    chart = ChartBuilder(data_parser, ppt_chart_name, chart_config, data_sheet, client_id) 
    # chart = chart.build(ppt_generator, slide)
    # print(f"Chart built: {chart}")
    chart.build(ppt_generator, slide)


def resolve_chart(ppt_generator: PPTGenerator, data_parser: DataParser, slide, ppt_chart_name, chart_config, data_sheet, client_id):
    '''
    Update the chart with the field data
    '''
    # Testing: data from the chart
    # chart = ppt_generator.get_chart_data(slide, ppt_chart_name) 
    # print(f"Data from the chart: {chart}")

    # Step 1: Initialize the LineChart
    line_chart = LineChart(data_parser, chart_config, data_sheet, client_id)  # TODO: to be replace by it's factory method
    # print(line_chart)

    #Step 2: Custom logic for POC
    y_axis = [list(map(float, config['field_value'])) for config in line_chart.y_axis]
    # divide by 100
    y_axis = [[value/100 for value in values] for values in y_axis]
    #reverese the order of y_axis
    y_axis = list(reversed(y_axis))
    x_axis = line_chart.x_axis['field_value']
    # print(f"X-Axis: {x_axis}")
    # print(f"Y-Axis: {y_axis}")

    #Step 3: Update the chart with the data
    ppt_generator.update_chart(slide, ppt_chart_name, x_axis, y_axis)

def resolve_waterfall_chart(ppt_generator: PPTGenerator, data_parser: DataParser, slide, ppt_chart_name, chart_config, data_sheet, client_id):

    waterfall_chart = WaterfallChart(data_parser, chart_config, data_sheet, client_id)
    # print("\t",waterfall_chart)

    #Step 2: Custom logic for POC
    x_axis = waterfall_chart.x_axis['field_value']
    y_axis = [list(map(float, config['field_value'])) for config in waterfall_chart.y_axis]
    
    #Step 3: Update the chart with the data
    ppt_generator.update_chart(slide, ppt_chart_name, x_axis, y_axis)
    

def parse_row_data(row):
    '''
    Parse the row data
    '''
    slide_number = int(row['slide_number'])
    field_name = row['ppt_field_name']
    field_type = row['field_type']
    field_config = row['field_config']
    data_sheet = row['datasheet']
    return slide_number, field_name, field_type, field_config, data_sheet
    


def init_ppt(data_parser: DataParser, client_id, ppt_data, template_file):
    '''
    Initialize the PPT for the client
    '''

    # STEP 1: Load the template PPT
    ppt_generator = PPTGenerator(template_file)
    print(f"2. PPT loaded successfully for client: {client_id}")
    print("-- PPT Update Initiated...")
    for index, row in ppt_data.iterrows():
        # STEP 2: Parse the row data
        slide_number, field_name, field_type, field_config, datasheet = parse_row_data(row)
        # if slide_number == 10: continue # TODO: Skipping for the testing purpose
        # print(f"Data props for field: {field_name} and value: {data_props['field_value']}")
        slide = ppt_generator.add_slide(slide_number)
        
        # STEP 3: Update the field based on the type
        if field_type == TYPE_PLACEHOLDER:
            data_props = data_parser.get_data_props(field_config, datasheet, client_id)
            if data_props is None:
                print(f"Data props not found for field: {field_name}")
                continue
            print(f"\t{index}: Resolving placeholder for field: {field_name}")
            resolve_text_placeholder(ppt_generator, slide, field_name, data_props)
        elif field_type == TYPE_LINE_CHART:
            pass
        elif field_type == TYPE_LINE_CHART_2:
            print(f"\t{index}: Resolving chart for field: {field_name}")
            resolve_chart(ppt_generator, data_parser, slide, field_name, field_config, datasheet, client_id)
        # elif field_type == TYPE_WATERFALL_CHART:
        #     resolve_waterfall_chart(ppt_generator, data_parser, slide, field_name, field_config, datasheet, client_id)
        else:
            print(f"\t{index}: Resolving chart for field: {field_name}")
            build_chart(ppt_generator, data_parser, slide, field_name, field_config, datasheet, client_id)
            continue

    # STEP 4: Save the PPT
    output_file = f"output_ppt/{client_id}_visa.pptx"
    ppt_generator.save_ppt(output_file)
    print(f"PPT saved successfully: {output_file}")





if __name__ == "__main__":
    
    # Constants
    METADATA_FILE = "RIBS_DS.xlsx"
    TEMPLATE_FILE = "visa_template.pptx"
    
    # STEP 1: Parse the metadata file
    data_parser = DataParser(METADATA_FILE)
    ppt_data = data_parser.get_data()
    client_data = data_parser.get_client_data()

    # STEP 2: Start creating the PPT for each client
    for index, row in client_data.iterrows():
        client = row['ClientID']
        print(f"1. Initiating for client: {client}")
        # STEP 2.1: Initialize the PPT        
        init_ppt(data_parser, client, ppt_data, TEMPLATE_FILE)

        
        






