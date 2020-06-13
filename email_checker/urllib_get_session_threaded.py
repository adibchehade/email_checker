import urllib
import time
import json
from request_mods import add_request_headers


def get_session_id(req):
    response = [None]
    web_id = request_www_westernunion_com(req, response)
    return web_id
    # if(request_www_westernunion_com(response)):
    #     response[0].close()


def request_www_westernunion_com(req, response):
    response[0] = None

    try:
        body = b"{\"device\":{\"id\":\"\",\"type\":\"WEB\"},\"channel\":{\"name\":\"Western Union\",\"type\":\"WEB\",\"version\":\"9Z00\",\"device_identifier\":\"RESPONSIVE_WEB\",\"is_responsive\":\"true\"},\"external_reference_no\":\"1\",\"locale\":{\"country_code\":\"us\",\"language_code\":\"en\"},\"security\":{\"black_box_data\":{\"data\":\"0400CIfeAe15Cx8Nf94lis1ztjXGwoPOvePAXyx2B+S3GHv4zk88XIRRraRLunIct8bff+0OYje9QG3QyfTeh05zWmOBOa6UBu99tJnG7aBZufFTM+276GxRfLnYpgrFwByeqHV8lCsVIFbWfvi2lw6riEVfH5Uu1Pa6eRLHB1R9v2d8MjlSDtQj+Jtpu4sEMnf8VWodMUtjVJMS2ITlncEvFXsdUywEcm1K+F9+VNHlcz2VwAGEd3H4L952RAUPKwCzLQAfZaA7jSiwHHrDW3HSYxnPse2ZJCsq4e3f1u/ETzp5VpgkQXTQzZ2bCkUkx/iDf2bn3Sw5z10y0BqqmpPWK5eIIfzGRmuyVIAW7uDQjXP1CYi+TBqr3g2vHHGOZYr7JaKI7U4dmdRZBrj3LMq6iXlL9ZZMAKELmgn6CSbaXfRSaQNEG0FLiAWeQwVS3/hrPOYe85lXFCRN2krK3MiK1aItlVfahFwAQkjj/Bf3sgBpWZmpMPu3J+3HIgrXK7aMtUplBKI7zAe5LqBNk4kdSgpA2sdPp297uf8vNtTCr7/8HBzsKudZ5X1CE/Fgu0JWx7yacWI+PSKq5dbmqXWqTFN9ILpoIeXbhWKXcVtbrPCixPMqjFULp9I8UWAJoym9T+HoQVdeZcQIrULZXTBjG6UIdAMpjc1v/zE8byqzj+BO44oNAQPdfLI+vS3zO1UWOjx45x9ZlwMJdmNWP4mnL4jqdQ4rX1XOyAfUMZ5LKFqFl81CC76WZKXakoCa7XCW4IhJrOz08Pzf+x4pw6W9esbGEpq7CoRYvFQ3SxgXyvTx/y4JwLTE4Nxv4KowoTq90t/25gxtwQokB0ojkm20iUzI+mPNi65X5WFPYlDG9N0Lbh5nOj3u3DXqRCiKCUrsEkMt8z9fxO9pLLGVQUKIYR2wTw53CiWK96FOpPevDWtH2XR0QkfOd02D73n81x6hEMCy0s3hRLn08Th9FlNHDMJBqLj+Tz8r0O/E9ABp/9e7Ass1MT2qnLUp3jXsoo0BtaQs3aTWzAj/ypZq/h+ZaTb+e2ERnQvcpeWgW0V2eQpdgS6+ebIBT9vO/g2GqbAcLd4t9XvVSBPuppttgqi/0yfOq1vG2COf7bsfFYzAaFLxVajijX/olA2vHHGOZYr7JaKI7U4dmdRZBrj3LMq6iXlL9ZZMAKELmgn6CSbaXfRSaQNEG0FLiAihm4Lf/K7HlU99UoH2xklR3N/aeGt5EB/svVUJi7EGUSnZsY8TL9w0j8/lZ9+74sNpkoqaTrmhoW0aLFYgm2YxWGZYhQabfSN8veAtIY6ioVg6fdSBnYKijDqHtCq29GqemMBz8q5Len0BJTgLAg0K0EGZNc9EzZa3c3jVldoE\",\"length\":1380},\"client_ip\":\"103082043065\"},\"bashPath\":\"/us/en\"}"

        response[0] = urllib.request.urlopen(req, body)
        json_data = response[0].fp.read()
        web_id = json.loads(json_data.decode('utf-8'))['security']['session']['id']
        return web_id

    except urllib.error.URLError as e:
        if not hasattr(e, "code"):
            return False
        response[0] = e
    except:
        return False

    return True
    
if __name__ == "__main__":
    get_session_id()