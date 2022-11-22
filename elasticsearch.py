# https://coralogix.com/blog/42-elasticsearch-query-examples-hands-on-tutorial/
# https://documenter.getpostman.com/view/7523144/SztK258g#4f058136-8be3-451f-bac2-e8979ef53a93
# https://elasticsearch-py.readthedocs.io/en/6.8.2/api.html#indices
# Elasticsearch Installation

 # Search Querys
 es = Elasticsearch([{'host': 'localhost'}])
 es.search(index="index_name", body=query)
 es.delete_by_query(index=indices, body={"query": {"match_all": {}}})
# 1. Delete single document using document id
curl -X DELETE "localhost:9200/document-index/_doc/1"
curl --location --request DELETE 'https://elasticsearch.careers360.de/qna'
# 2. Delete all documents from the index
POST document-index/_delete_by_query?conflicts=proceed
{
 "query": {
 "match_all": {}
 }
}
# 3. Delete documents based on the query or specific criteria
{
  "query": {
    "range" : {
        "id" : {
           "gte" : 1
        }
    }
  }
}

 
# POST employees/_search
# 1. match
{
  "query": {
    "match": {
      "phrase": {
        "query" : "heuristic roots help"
        "operator" : "AND" # optional (default => "OR")
        "minium_should_match": 3 # optional (all three words must appear in the document in order to be classified as a match.)
      }
    }
  }
}

# 1.1 Multi-Match Query
{
  "query": {
    "multi_match": {
        "query" : "research help"
        , "fields": ["position","phrase"]
    }
  }
}

# 1.2 Match Phrase
{
  "query": {
    "match_phrase": {
      "phrase": {
        "query": "roots heuristic coherent"
      }
    }
  }
}

{
  "query": {
    "match_phrase": {
      "phrase": {
        "query": "roots coherent",
        "slop": 1  # Optional (With slop=1, the query is indicating that it is okay to move one word for a match)
      }
    }
  }
}

{
  "query": {
    "match_phrase_prefix": {
      "phrase": {
        "query": "roots heuristic co"
        "slop": 1    # Optional
      }
    }
  }
}
# Note: “match_phrase_query” tries to match 50 expansions (by default) of the last provided keyword (co in our example). This can be increased or decreased by specifying the “max_expansions” parameter.

# 2. Term Level Queries
# Term level queries are used to query structured data, which would usually be the exact values.

# 2.1. Term Query/Terms Query
{
  "query": {
    "term": {
      "gender": "female" # Case Sensitive
    }
  }
}
{
  "query": {
    "terms": {
      "gender": [
        "female",
        "male" # To search both female and male in gender field.
      ]
    }
  }
}

# 2.2 Exists Queries
{
    "query": {
        "exists": {
            "field": "company"
        }
    }
}

{
  "query": {
    "bool": {
      "must_not": [
        {
          "exists": {
            "field": "company" # return all documents without company field.
          }
        }
      ]
    }
  }
}

# 2.3 Range Queries
{
    "query": {
        "range" : {
            "experience" : {
                "gte" : 5,
                "lte" : 10
            }
        }
    }
}

{
    "query": {
        "range" : {
            "date_of_birth" : {
                "gte" : "01/01/1986"
            }
        }
    }
}

# 2.4 Ids Queries
# GET indexname/typename/documentId
{
    "query": {
        "ids" : {
            "values" : ["1", "4"]
        }
    }
}

# 2.5 Prefix Queries
{
  "query": {
    "prefix": {
      "name": "al"  # Term query so it will return documents starting with the field_name al not AL
    }
  }
}

# 2.6 Wildcard Queries
{
    "query": {
        "wildcard": {
            "country": {
                "value": "c*a" # The above query will fetch all the documents with the “country” name starting with “c” and ending with “a” (eg: China, Canada, Cambodia, etc). Here the * operator can match zero or more characters.
            }
        }
    }
}

{
  "query": {
    "regexp": {
      "position": "res[a-z]*"
    }
  }
}

# 2.7 Regexp
{
  "query": {
    "regexp": {
      "position": "res[a-z]*"
    }
  }
}

# 2.8 Fuzzy
{
  "query": {
    "fuzzy": {
      "country": {
        "value": "Chnia", # Spelling Mistake
        "fuzziness": "2"  # Here fuzziness is the maximum edit distance allowed for matching
      }
    }
  }
}

{
    "query": {
        "multi_match" : {
            "query" : "heursitic reserch",
            "fields": ["phrase","position"],
            "fuzziness": 2
        }
    },
    "size": 10
}

# 3. Boosting
# While querying, it is often helpful to get the more favored results first. The simplest way of doing this is called boosting in Elasticsearch. And this comes in handy when we query multiple fields.
{
    "query": {
        "multi_match" : {
            "query" : "versatile Engineer",
            "fields": ["position^3", "phrase"]
        }
    }
}

# 4. Sorting
# 4.1 Default Sorting
{
	"query": {
		"match": {
			"country": "china"
		}
	}
}

{
    "query": {
        "bool" : {
            "filter" : {
            	"match": {
            		"country": "china"
            	}
            }
        }
    }
}

# 4.2 How to Sort by a Field
{
   "_source": ["name","experience","salary"], 
  "sort": [
    {
      "experience": {
        "order": "desc"
      }
    }
  ]
}

{
  "_source": [
    "name",
    "experience",
    "salary"
  ],
  "sort": [
    {
      "experience": {
        "order": "desc"
      }
    },
    {
      "salary": {
        "order": "desc"
      }
    }
  ]
}

# 5. Compound Queries
# 5.1. The Bool Query
{
  "query": {
    "bool" : {
      "must" : [],
      "filter": [],
      "must_not" : [],
      "should" : []
    }
  }
}

# Must (AND) (Score is considered)
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "position": "manager"
          }
        },
        {
          "range": {
            "experience": {
              "gte": 12
            }
          }
        }
      ]
    }
  }
}

# Filter (Score not Considered => 0), (when using the filter context, the score is not computed by Elasticsearch in order to make the search faster)
{
  "query": {
    "bool": {
      "filter": [
        {
          "match": {
            "position": "manager"
          }
        },
        {
          "range": {
            "experience": {
              "gte": 12
            }
          }
        }
      ]
    }
  }
}

# Should (OR)
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "position": "manager"
          }
        },
        {
          "range": {
            "experience": {
              "gte": 12
            }
          }
        }
      ],
    "should": [
      {
        "match": {
          "phrase": "versatile"
        }
      }
    ]
    }
  }
}

# Multiple Conditions
{
    "query": {
        "bool": {
            "must": [
              {
                "bool": {
                    "should": [{
                        "match": {
                            "company": "Talane"
                        }
                    }, {
                        "match": {
                            "company": "Yamaha"
                        }
                    }]
                }
            }, 
            {
                "bool": {
                    "should": [
                      {
                        "match": {
                            "position": "manager"
                        }
                    }, {
                        "match": {
                            "position": "Associate"
                        }
                    }
                    ]
                }
            }, {
                "bool": {
                    "must": [
                      {
                        "range": {
                          "salary": {
                            "gte": 100000
                          }
                        }
                      }
                      ]
                }
            }]
        }
    }
}










