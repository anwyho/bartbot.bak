curl -H "Content-Type:application/json" -X POST "localhost:5000/webhook" -d '{"object":"page","entry":[{"id":"1816383528408275","time":1458692752478,"messaging":[{"sender":{"id":"2153980617965043"},"recipient":{"id":"1816383528408275"},"timestamp":1535668107322,"message":{"mid":"BPz5ur9Btq7j4COCe1mCzYkLKYgxzkzkA1c5Qo1fAeHwydq7QZl3h2_9tJsh7t1yWpu-vCymEb1Scci-RVgOkg","seq":1560439,"text":"What will the weather be like saturday at dberk [note: simple message with wit]","nlp":{"entities":{"datetime":[{"confidence":0.96243,"values":[{"value":"2018-08-25T00:00:00.000-07:00","grain":"day","type":"value"},{"value":"2018-09-01T00:00:00.000-07:00","grain":"day","type":"value"},{"value":"2018-09-08T00:00:00.000-07:00","grain":"day","type":"value"}],"value":"2018-08-25T00:00:00.000-07:00","grain":"day","type":"value","_entity":"datetime","_body":"saturday","_start":30,"_end":38}],"station":[{"confidence":1,"value":"DBRK","type":"value","_entity":"station","_body":"dberk","_start":42,"_end":47}],"intent":[{"confidence":0.94982186799528,"value":"weather","_entity":"intent"},{"confidence":0.00056112378288034,"value":"travel","_entity":"intent"},{"confidence":0.000029564727499213,"value":"cost","_entity":"intent"}],"greetings":[{"confidence":0.00057287785703837,"value":"true","_entity":"greetings"}],"bye":[{"confidence":0.000099909333908896,"value":"true","_entity":"bye"}],"thanks":[{"confidence":0.000036381962049978,"value":"true","_entity":"thanks"}]}}}}]}]}'