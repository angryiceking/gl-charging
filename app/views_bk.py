from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views import View

import requests, json


class IndexView(View):
    app_id = 'yBGnCLxeEgCMLTKoGgieqkCGeBM8CnAE'
    app_secret = '363614f3b0db345466dd92c4646ff44e9d264e1b551171e2a7ee7f7d2228bb25'
    iterator = 1
    
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', None)
        at_source = ''

        if code:
            at_source = requests.post(
                'https://developer.globelabs.com.ph/oauth/access_token', 
                    data = {
                        'app_id':self.app_id,
                        'app_secret':self.app_secret,
                        'code':code
                    }
                )

            at_body = json.loads(at_source.content)
            access_token = at_body['access_token']
            subscriber = at_body['subscriber_number']

            ref_code_source = requests.get('https://devapi.globelabs.com.ph/payment/v1/transactions/getLastRefCode?app_id={}&app_secret={}'.format(
                self.app_id,
                self.app_secret
                )
            )
            ref_code_json = json.loads(ref_code_source.content)
            ref_code = ref_code_json['referenceCode']
            new_ref_code = int(ref_code) + self.iterator
            print(new_ref_code)
            charging = requests.post(
                'https://devapi.globelabs.com.ph/payment/v1/transactions/amount?access_token={}'.format(access_token),
                    data = {
                        'amount': '1.00',
                        'description':'My Application',
                        'endUserId':subscriber,
                        'referenceCode':new_ref_code,
                        'transactionOperationStatus':'Charged',
                        'duration':'0',
                    }
                )
            c = json.loads(charging.content)
            print(c)
            print(charging.url)
            print(charging.text)
            print(charging)

        return HttpResponse(at_source, status=200)

    def post(self, request, *args, **kwargs): 
        return HttpResponse('ok', status=200)


class CodeView(View):

    def get(self, request, *args, **kwargs):
        charging = requests.post(
            'https://devapi.globelabs.com.ph/payment/v1/transactions/amount?access_token=K1pi6mRXZAUFtAoSgSwxw4bLmS9c8375PUW1m_4H8II',
                data = {
                    'amount': '1.00',
                    'description':'My Application',
                    'endUserId':'9159250579',
                    'referenceCode':'07229200075',
                    'transactionOperationStatus':'Charged',
                    'duration':'0',
                }
            )
        print(charging.text)

        return HttpResponse('ok', status=200)

    def post(self, request, *args, **kwargs):
        return HttpResponse('ok', status=200)
