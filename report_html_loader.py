import jinja2
import os


class ReportHTML():

    def templateLoader(self, data_1, data_2, report_date, file_name):

        #working_path = os.getcwd()
        actual_path = '/home/deven/workspace/tripping-octo-wight/tripping-octo-wight/'
        #templateLoader = jinja2.FileSystemLoader(searchpath=working_path)
        templateLoader = jinja2.FileSystemLoader(searchpath=actual_path)
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "report_all_template.html"
        template = templateEnv.get_template(TEMPLATE_FILE)
        templateVars = {'title': 'NeCTAR Research Cloud Usage Report',
                        "description": "Report Gen", 'date': report_date,
                        'cell': data_1, 'rc': data_2}
        '''
        templateVars = {"title": "NeCTAR Research Cloud Usage Report",
                        "description": "Report Gen",
                        "report_date": data.get('report'), 
                        "cell": data.get('cell')}
        '''

        outputText = template.render(templateVars)
        with open(file_name, "wb") as fh:
            fh.write(outputText)


