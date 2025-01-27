curl -X POST http://192.168.52.136:3000/display-text -H "Content-Type: application/json" -d "{\"R\": 255, \"G\": 0, \"B\": 0, \"text\": \"Score : 250 - 10\"}"
curl -X POST http://192.168.52.136:3000/display-text -H "Content-Type: application/json" -d "{\"R\": 5, \"G\": 0, \"B\": 0, \"text\": \"Score : 250 - 10\"}"
curl -X POST http://192.168.52.136:3000/display-text -H "Content-Type: application/json" -d "{\"R\": 255, \"G\": 0, \"B\": 0, \"text\": \"Score : 250 - 10\"}"
curl -X POST http://192.168.52.136:3000/display-text -H "Content-Type: application/json" -d "{\"R\": 5, \"G\": 0, \"B\": 0, \"text\": \"Score : 250 - 10\"}"
curl -X POST http://192.168.52.136:3000/display-text -H "Content-Type: application/json" -d "{\"R\": 255, \"G\": 0, \"B\": 0, \"text\": \"Score : 250 - 10\"}"
timeout /t 2
curl -X POST http://192.168.52.136:3000/display-text -H "Content-Type: application/json" -d "{\"R\": 255, \"G\": 100, \"B\": 50, \"text\": \"Score : 250\"}"
