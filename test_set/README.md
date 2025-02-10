This folder contains a set of examples to run the project.

To run the examples, simply do:
```shell
curl --request POST \
  --url http://localhost:8000/api/v1/files \
  --header 'Content-Type: multipart/form-data' \
  --form file=@provided_example.txt
```
Use the id returned by the previous call, until the status is `"SUCCESS"`
```shell
curl --request GET \
  --url http://localhost:8000/api/v1/files/${file_id}
```
Finally, query the file using:
```shell
curl --request GET \
  --url 'http://localhost:8000/api/v1/query/${file_id}?limit=5'
```
