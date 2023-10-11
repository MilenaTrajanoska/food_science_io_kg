FROM lyrasis/blazegraph:2.1.5

RUN mkdir /tmp/data
COPY kg /tmp/data

CMD ["/tmp/data/load_data.sh"]