
# 			eventAPI

####  http://ec2-34-201-52-248.compute-1.amazonaws.com:5000

### INSTALL 

	docker-compose -f stack.yml up


## 		API Docs


###		RECORD AN EVENT USING JSON PAYLOAD

	url : /event

	method : POST 

	urlparams (required ) :
		
		JSON payload 

		example : {"key":"value","another_key":"another_value"}
	

####	Success response : 
	
		code: 200

		content: 'Ok'

####	Error response : 
	
		code: 400

		content: 'input data has to be in JSON-format'




##		FETCH RECORDED EVENT DATA

	url : /findevent

	method : GET

	urlparams (required ) :
	
		JSON query string 	

		example : {
						"city":[name of the city],
						 "st":[query time range start [%Y-%m-%d:%H.%M.%S] ],
						 "et":[query time range end [%Y-%m-%d:%H.%M.%S] ]]
 					}

		example : {
						"city":"paris",
						 "st":"2019-01-17:22.57.00",
						 "et":"2019-01-17:22.58.10"
 					}


####	Success response : 
	
		code: 200

		content: [JSON PAYLOAD]

####	Error response : 
	
		code: 400

		content: 'Bad Request'




