import re
import flask

extensions = ({
    'co.uk': 'United Kingdom',
    'de': 'Germany',
    'fr': 'France',
    'com.au': 'Australia',
    'com.br': 'Brasil',
    'ca': 'Canada',
    'cn': 'China',
    'in': 'India',
    'it': 'Italy',
    'co.jp': 'Japan',
    'com.mx': 'Mexico',
    'nl': 'Netherlands',
    'es': 'Spain',
    'com': 'United States'
    })

def amazon_url_match(ProductURL):
    try:
        MatchURL = bool(re.match(r"^http(s|):\/\/(www.|)amazon.(co.uk|de|fr|com.au|com.br|ca|cn|in|it|co.jp|com.mx|nl|es|com)(\/[\s\S]*|)\/(dp|gp|deal)\/(product\/|)[A-Z0-9]{10}(\/|\?|\&|$)", ProductURL))
    except AttributeError:
        MatchURL = False
    return MatchURL

def minimize_url(ProductURL):
    try :
        MinimizedURL = re.search(r"http(s|):\/\/(www.|)amazon.(co.uk\/|de|fr|com.au\/|com.br\/|ca\/|cn\/|in\/|it\/|co.jp\/|com.mx\/|nl\/|es\/|com\/)([\s\S]*\/|)(dp|gp|deal)\/(product\/|)[A-Z0-9]{10}", ProductURL).group(0)
        MinimizedURL = re.sub(r"((?<=co.uk\/)|(?<=de\/)|(?<=fr\/)|(?<=com.au\/)|(?<=com.br\/)|(?<=ca\/)|(?<=cn\/)|(?<=in\/)|(?<=it\/)|(?<=co.jp\/)|(?<=com.mx\/)|(?<=nl\/)|(?<=es\/)|(?<=com\/)).*(?=(dp|gp|deal))", '', MinimizedURL)
    except AttributeError:
        MinimizedURL = '';
    return MinimizedURL

def parse_asin(ProductURL):
    try :
        ProductASIN = re.search(r"[A-Z0-9]{10}", ProductURL).group(0)
    except AttributeError:
        ProductASIN = ''
    return ProductASIN

def parse_region(ProductURL):
    try :
        AmazonRegion = extensions[re.search(r"(co.uk|de|fr|com.au|com.br|ca|cn|in|it|co.jp|com.mx|nl|es|com)", ProductURL).group(0)]
    except AttributeError:
        AmazonRegion = ''
    
    return AmazonRegion

app = flask.Flask(__name__)

@app.route('/api/v1/urls/amazon')
def Amazon_URL_check():
    try :
        ProductURL = str(flask.request.query_string)[1:].replace('\'', "")
        validURL = amazon_url_match(ProductURL);

        if validURL:
            MinimizedURL = minimize_url(ProductURL)
            ProductASIN = parse_asin(MinimizedURL)
            region = parse_region(MinimizedURL)
            
            url_result = {
                'ValidAmazonURL': validURL,
                'URL': ProductURL,
                'MinimalURL': MinimizedURL,
                'ASIN': ProductASIN,
                'Region': region
                }
        
        else :
            url_result = {
                'ValidAmazonURL': validURL,
                'URL': ProductURL
                }

        return flask.jsonify(url_result)
        
    except AttributeError as error:
        return "Error: " + error
        
if __name__ == "__main__":    
    app.run(host='0.0.0.0', port='80')