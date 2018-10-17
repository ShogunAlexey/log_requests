#!/usr/bin/env python3

import requests
import logging
import logging.handlers
import time
import hashlib
import json
import pprint
#import urls_list

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from logging.handlers import SysLogHandler
syslogger = logging.getLogger(__name__)
syslogger.setLevel(logging.INFO)

sys_formatter = logging.Formatter("%(name)s %(funcName)-20s:%(lineno)-4d %(relativeCreated)-8d %(levelname)s - %(message)s")
sys_handler = SysLogHandler(address='/dev/log', facility=logging.handlers.SysLogHandler.LOG_USER)
sys_handler.setFormatter(sys_formatter)

syslogger.addHandler(sys_handler)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Section to be commented out or deleted
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s:%(name)s %(funcName)-20s:%(lineno)-4d %(relativeCreated)-8d %(levelname)s - %(message)s"
        )

file_handler = logging.FileHandler("Url_status_and_ssl.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# - - - - - - - - - - - - - - - - --  - - - - - - - - - - - - - - - - -- - - - - - - - - - - - -
urls_hashes = {
        'http://ivyaffiliates.com':'726a2a085e278dd1d6b1371393edf6f3',
        'https://londoncityfinance.com':'2a92e902e3cbc1b03db10307465eeb0b',
        'http://motorcyclefinancegroup.com':'726a2a085e278dd1d6b1371393edf6f3',
        'https://paydayloans.quiddicompare.co.uk':'e5c3419ee669e61344b0f8fdb481eaa4',
        'http://www.ivyaffiliates.co.uk':'726a2a085e278dd1d6b1371393edf6f3',
        'http://www.whitezip.com':'3b732c71b926410c3729f2af1efe8b96',
        'https://quiddicompare.co.uk':'988a1c8a73ae7fe13276128de6ad25e0',
        'https://thisIsNotAnWebsite-ThisISJustATest.abc':'TESTING HASH',
        'https://acceptloans.co.uk':'988a1c8a73ae7fe13276128de6ad25e0',
        'http://alienpayday.co.uk':'661ced1361c159f8accce6f40e9969bd',
        'http://amazedeal.co.uk':'3eadb9c1aa48dc3c7bc446a21c56de2d',
        'http://billboa.co.uk':'661ced1361c159f8accce6f40e9969bd',
        'https://cashcapital.co.uk':'f9ef2c66abdce9a82b48c8b7e2f6849a',
        'https://creditextracash.co.uk':'9aab7fb2d42d078387257fea591af34b',
        'http://creditextramoney.co.uk':'726a2a085e278dd1d6b1371393edf6f3',
        'https://flexikash.co.uk':'661ced1361c159f8accce6f40e9969bd',
        'http://flexikash.com':'661ced1361c159f8accce6f40e9969bd',
        'https://flexyfinance.co.uk':'a02b25ae69c5ed37b53b18fcf5e86b09',
        'https://www.youtube.com/results?sp=CAISBAgBEAE%253D&search_query=music':'09a027e38ab8886ace3a1b49f9698def',
    }

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Request( object ):
    
    def __init__( self,  syslogger ): 
        self.__syslogger = syslogger
        self.__session = requests.Session()
        self.__status_code = 410
        self.__name = 'http_request'
        self.__verify = True
        self.__location = None
        self.__headers = None
        self.__content = None
        self.__status = False
        self.__requested = None
        self.__completed = None
        self.__timeouts = { 'connection': 1, 'read': 3 } 
        self.__duration = -1
        self.__user_agent = None
        self.__extra_debug = False
        
        self.__hex = None
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    @property
    def name( self ):
        return self.__name
        
    @name.setter
    def name( self, value ):
        self.__name = value
            
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    @property
    def verify( self ):
        return self.__verify
                        
    @verify.setter
    def verify( self, value ):
        self.__verify = value                
                
    @property
    def connect_timeout( self ):
        return self.__timeouts['connection']
                                
    @connect_timeout.setter
    def connect_timeout( self, value ):
        self.__timeouts['connection'] = value
                                        
    @property
    def read_timeout( self ):
        return self.__timeouts['read']
                                        
    @read_timeout.setter
    def read_timeout( self, value ):
        self.__timeouts['read'] = value                        
                        
    @property
    def user_agent( self ):
        return self.__user_agent                        
                        
    @user_agent.setter
    def user_agent( self, value ):
        self.__user_agent = value
                                                        
    @property
    def extra_debug( self ):
        return self.__extra_debug
                            
    @extra_debug.setter
    def extra_debug( self, value ):
        self.__extra_debug = value

                                
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    @property
    def status_code( self ):
        return self.__status_code    
    
    @property
    def headers( self ):
        return self.__headers
                                                                
    @property
    def content( self ):
        return self.__content    
                                
    @property
    def location( self ):
        return self.__location
                                                                 
    @property
    def duration( self ):
        return self.__duration                                                                

    @property
    def hex( self ):
        return self.__hex
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    def request( self, url, method='GET', post_data=None, headers=None ):
        url=url.rstrip()
       
        self.__status_code = 500
        self.__requested = time.time()        


        ##headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        print("headers before:", headers)
        if not headers.get( 'User-Agent' ):
            headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'   #self.user_agent
  #          headers['User-Agent'] = self.user_agent

            print("headers after:", headers['User-Agent'])
                 
        try:
            response = self.__session.request(
                method = method,
                url = url,
                data = post_data,
                headers = headers,
                timeout = (self.connect_timeout, self.read_timeout),
                verify = self.verify
            )
            syslogger.info(url)

            self.__status_code = response.status_code
            self.__content = response.content
            self.__headers = dict(response.headers)
            self.__location = response.url
            self.__status = True

            if response.history != []:
                print(response.history, "Redirect to: ", response.url)

            print("Response.headers: ",response.headers)
                
            def hash_md5():
                x = response.content
            
                hashed = hashlib.md5(x)
                hexed = hashed.hexdigest()
            
                syslogger.info(hexed)
                return hexed
           
            self.__hex = hash_md5()
             
        except requests.exceptions.SSLError as e:
             self.__content = 'timed out reading %s after %s seconds' % ( url , str(e))
             self.__headers = { 'X-Error-Type': 'SSL Validation Error' }
             #self.__logger.debug( self.headers )
             self.__syslogger.debug(self.headers)
   
             syslogger.info(url)
                          
        except requests.exceptions.ConnectionError as e:
            self.__status_code = 503
            self.__content = "connection error to %s, Reason: %s" % (self.name, str(e))
            self.__headers = {"X-Error-Type": "Connection Error"}
            #self.__logger.debug(self.headers)
            self.__syslogger.debug(self.headers)
            #logger.info(url)
            syslogger.info(url)
                        
        except requests.exceptions.Timeout as e:
            self.__status_code = 522
            self.__content = "connection error to %s timed out after %d seconds" % (url, self.connect_timeout)
            self.__headers = {"X-Error-Type":"Connect Timeout"}
            #self.__logger.debug(self.headers)
            self.__syslogger.debug(self.headers)
            #logger.info(url)
            syslogger.info(url)
                                    
        except requests.exceptions.ReadTimeout as e:
            self.__status_code = 408
            self.__content = 'timed out reading %s after %s seconds' % ( url, self.read_timeout )
            self.__headers = { 'X-Error-Type': 'Read Timeout' }
            #self.__logger.debug( self.headers )
            self.__syslogger.debug(self.headers)
            #logger.info(url)
            syslogger.info(url)                        
            
        except Exception as e:
            self.__status_code = 520
            self.__content = 'Error occured with %s, Reason: %s' % ( url, str(e)) # e.message )
            self.__headers = { 'X-Error-Type': 'Other Error' }
            #self.__logger.debug( self.headers )
            self.__syslogger.debug(self.headers)
            #logger.info(url)
            syslogger.info(url)
                                    
        self.__completed = time.time()
        self.__duration = self.__completed - self.__requested

        self.__syslogger.info( "{} response status code: {}".format( self.name, self.status_code ) )
        self.__syslogger.info( "{} response duration: {}".format( self.name, self.duration ) )
        
        if self.extra_debug:
            self.__syslogger.debug( "{} response headers: {}".format( self.name, pprint.pformat( self.headers ) ) )
            self.__syslogger.debug( "{} response payload: {}".format( self.name, pprint.pformat( self.content ) ) )  
            
            return self.__status

#----------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    
    myRequest = Request(syslogger) #logger
                
    for k,v in urls_hashes.items():
        print("-"*60)
        myRequest.request(url = k, headers={})
        w = myRequest.hex
        if v == w:
            print("Hashes are unchanged:",myRequest.hex)
        elif v == '':
            print("There is no stored hash")
            print(myRequest.hex, "-current hash")
        else:
            print(v,"-stored hash")
            print(myRequest.hex,"-current hash")
 
#CHECK IF SESSION STATUS CODE IS EQUAL TO THE requests.get STATUS CODE
        if k == "http://motorcyclefinancegroup.com" or k == "https://quiddicompare.co.uk" or k == "https://thisIsNotAnWebsite-ThisISJustATest.abc" or k == "http://billboa.co.uk" or k == "http://creditextramoney.co.uk":
            pass
        else:
            r = requests.get(k) #, timeout=(1,3))
            print("Requests.get():",r.status_code)
            print("Requests.get() headers: ",r.headers)
