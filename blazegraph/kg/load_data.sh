upload_data(){
# Try to upload test data
while [ -z "$(curl -H "Content-Type:application/x-turtle" --data-binary "@/tmp/data/recipe_ontology_v2.0_small_extended.ttl" http://localhost:8080/bigdata/sparql )" ]
do
    sleep 60
done
echo "Data uploaded"
}

upload_data & # Run process in parallel
/bin/bash /var/lib/jetty/entrypoint.sh