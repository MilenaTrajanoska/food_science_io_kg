from flask import Flask, request, jsonify
from rdflib import Graph


rdf_graph = Graph()
rdf_graph.parse("../ontology/recipe_ontology_v2.0_small.ttl", format="turtle") 


app = Flask(__name__)


@app.route('/api/v1/sparql', methods=['GET'])
def sparql_query():
    query = request.args.get('query')
    try:
        results = rdf_graph.query(query)
        bindings = [dict(result) for result in results.bindings]
        return jsonify({'results': bindings})
    except Exception as e:
        return jsonify({'error': 'Invalid SPARQL query provided'}), 400


if __name__ == "__main__":
    app.run(debug=True)