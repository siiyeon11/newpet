const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch');
const path = require('path');

const app = express();
const PORT = 3000;
const API_BASE_URL = 'https://open.api.nexon.com';

// CORS 설정
app.use(cors());
app.use(express.json());
app.use(express.static('.'));

// 넥슨 API 프록시 엔드포인트
app.get('/api/maplestory/:endpoint', async (req, res) => {
    try {
        const { endpoint } = req.params;
        const apiKey = req.headers['x-nxopen-api-key'];
        
        if (!apiKey) {
            return res.status(400).json({ 
                error: 'API Key가 필요합니다.',
                message: 'x-nxopen-api-key 헤더를 포함해주세요.'
            });
        }

        // 쿼리 파라미터 구성
        const queryParams = new URLSearchParams(req.query).toString();
        const url = `${API_BASE_URL}/maplestory/v1/${endpoint}${queryParams ? '?' + queryParams : ''}`;

        console.log(`프록시 요청: ${url}`);

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'x-nxopen-api-key': apiKey
            }
        });

        const data = await response.json();
        
        if (!response.ok) {
            return res.status(response.status).json(data);
        }

        res.json(data);
    } catch (error) {
        console.error('프록시 오류:', error);
        res.status(500).json({ 
            error: '서버 오류가 발생했습니다.',
            message: error.message 
        });
    }
});

// 루트 경로에서 index.html 제공
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
    console.log(`서버가 http://localhost:${PORT} 에서 실행 중입니다.`);
    console.log('브라우저에서 http://localhost:3000 을 열어주세요.');
});


