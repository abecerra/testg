from flask import Flask
from flask import request

from dbhandler import suggestGeneNames

app = Flask(__name__)

@app.route('/gene_suggest')
def hello():
    query = request.args.get('query', default = 'BRCA', type = str)
    species = request.args.get('species', default = 'homo_sapiens', type = str)
    limit = request.args.get('limit', default = 10, type = int)
    return suggestGeneNames(query, species, limit)

if __name__ == '__main__':    
    app.run()
