'''
Created on 21-Oct-2020

@author: lsail
'''
from datetime import datetime
import json

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from pip._vendor import requests
import time


class PageInsights(object):
    '''
    classdocs
    '''

    def __init__(self, site, key):
        '''
        Constructor
        '''
        self.site = site
        self.key = key
        
    def getPageInsights(self):
        
        token = "THPa1hMyYsiLk1SfIZ_MFloSia4QwfdtSxY--kog96rs8VoiV03ZOk-Fv17WE3qn8sTJMzewlq7BEyvBKdwzow=="
        org = "gopi.y@shaftsoftwares.com"
        
        bucket = "insights"
        
        client = InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=token)
        try:
            targetURL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + str(self.site) + "&key=" + self.key + "&strategy=DESKTOP"
            
            req = requests.get(targetURL, timeout=30)
            
            res = json.loads(req.text)
            
            fetchTime = int(round(time.time() * 1000))
            fcp = str(res['lighthouseResult']['audits']['first-contentful-paint']['displayValue'])
            si = str(res['lighthouseResult']['audits']['speed-index']['displayValue'])
            toi = str(res['lighthouseResult']['audits']['interactive']['displayValue'])
            fmp = str(res['lighthouseResult']['audits']['first-meaningful-paint']['displayValue'])
            fci = str(res['lighthouseResult']['audits']['first-cpu-idle']['displayValue'])
            eil = str(res['lighthouseResult']['audits']['estimated-input-latency']['displayValue'])
            
            field_lcp = str(res['loadingExperience']['metrics']['LARGEST_CONTENTFUL_PAINT_MS']['percentile'])
            field_fcp = str(res['loadingExperience']['metrics']['FIRST_CONTENTFUL_PAINT_MS']['percentile'])
            field_fid = str(res['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']['percentile'])
            field_cls = str(res['loadingExperience']['metrics']['CUMULATIVE_LAYOUT_SHIFT_SCORE']['percentile'])
            
            write_api = client.write_api(write_options=SYNCHRONOUS)
            point = Point("mem").tag("host", "host1").field("URL", self.site).field("FETCH_TIME", fetchTime).field("FCP", fcp).field("TOI", toi).field("SI", si).field("FCI", fci).field("FMP", fmp).field("EIL", eil).field("FIRST_CONTENTFUL_PAINT_MS",field_fcp).field("FIRST_INPUT_DELAY_MS",field_fid).field("LARGEST_CONTENTFUL_PAINT_MS",field_lcp).field("CUMULATIVE_LAYOUT_SHIFT_SCORE",field_cls).time(datetime.utcnow(), WritePrecision.NS)

            write_api.write(bucket, org, point)

        except requests.exceptions.Timeout as e:
            print(e)
