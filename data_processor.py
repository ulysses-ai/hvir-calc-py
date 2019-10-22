import methods
import logging

def process_rows(raw_data,header,hvir_params,converters):
    surveys = []
    failed_rows = []
    key_fails = {}
    calculator = methods.hvir_calculator()
    for row_num, row in enumerate(raw_data):

        try:
            survey,key_fails = cast_row(row,header,converters,key_fails)
        except:
            print("Couldn't read in this row: %s" % row_num)
            failed_rows.append(row_num)
        survey,out_keys = calculator.method_logic(survey, hvir_params)
        surveys.append(survey)
        try:
            survey,out_keys = calculator.method_logic(survey, hvir_params)
            surveys.append(survey)

        except:
            logging.debug("couldn't calculate HVIR for this row: %s" % str(row_num))
            failed_rows.append(row_num)

    return key_fails,failed_rows,surveys,out_keys


def cast_row(row,header,converters,key_fails):
    survey = {'mass_limit': None,
              'length_limit': None,
              'sealed_shoulder_width': None,
              'seal_flag': None,
              'sealed_should_width': None,
              'form_width': None,
              'seal_width': None}
    cast_row = []
    for index, cell in enumerate(row):
        try:
            cast_row.append(converters[header[index]](cell))
            survey[header[index]] = cast_row[-1]
            # print('\t',header[index]+' '*(15-len(header[index])),'\t',index,'\t',cell+' '*(25-len(cell)),'\t',converters[header[index]](cell))
        except:
            # print('Failed to pass row %s, field %s, with value %s' % (row_num,header[index],cell))
            cast_row.append(None)
            survey[header[index]] = None
            if header[index] not in key_fails.keys():
                key_fails[header[index]] = 1
            else:
                key_fails[header[index]] += 1
    return survey,key_fails