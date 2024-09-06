pip3 install --no-cache-dir --default-timeout=1000 -r ./requirements.txt

curl --location --request POST '
https://ray-server.sigma-cd3.aws.itsma-ng.net/opus-mt-zh-en'
\
--header 'Content-Type: application/json' \
--data-raw '{
    "inputs": [
        "怎么连接打印机?",
        "你好吗?"
    ]
}'

curl --location --request POST '
https://ray-server.sigma-cd3.aws.itsma-ng.net/opus-mt-en-zh'
\
--header 'Content-Type: application/json' \
--data-raw '{
    "inputs": [
        ">>cmn_Hans<<How do you connect the printer?",
        ">>cmn_Hans<<How are you?"
    ]
}'