import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
    vus: 50,              // usuários simultâneos
    duration: '30s',      // duração total do teste
    thresholds: {
        http_req_duration: ['p(95)<1000'], // 95% das requisições < 1s
        http_req_failed: ['rate<0.01'],    // menos de 1% de erros
    },
};

const headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NDg3Mjc4NDAsInN1YiI6ImFwaV9leHRlcm5hIn0.bZIqAbwjRadpb0caDbjshKUG8dsDinB6MGfL4cQSEJs',
};

const payload = JSON.stringify({
  "content": "YSwgYiA9IG1hcChpbnQsIGlucHV0KCkuc3BsaXQoKSkKcHJpbnQoYSArIGIp",
  "language_type": "py",
  "problem_id": "556be6cd-58e3-4a6c-8c29-a604b0993f92"
});

export default function () {
    let res = http.post('http://127.0.0.1:8000/v0/submissions', payload, { headers });

    check(res, {
        'status 201': (r) => r.status === 201,
    });

    sleep(1); // simula tempo entre ações do usuário
}