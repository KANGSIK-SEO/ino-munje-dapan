-- 1. 전체 고객 조회
SELECT id, name, email, tier FROM client;

-- 2. 전체 작가 조회
SELECT id, name, style FROM artist ORDER BY name;

-- 3. 전체 작품 조회
SELECT id, title, medium, produced_year FROM artwork;

-- 4. 진행 중인 감정 요청 조회
SELECT id, submitted_at, status, risk_score
FROM authentication_request
WHERE status IN ('submitted', 'analyzing', 'reviewed');

-- 5. 작품과 작가 INNER JOIN
SELECT aw.title, ar.name AS artist, ar.style
FROM artwork aw
INNER JOIN artist ar ON ar.id = aw.artist_id;

-- 6. 감정 요청과 고객 INNER JOIN
SELECT req.id, c.name AS client, req.status, req.fee
FROM authentication_request req
INNER JOIN client c ON c.id = req.client_id;

-- 7. 감정 요청, 작품, 작가 3중 JOIN
SELECT req.id, c.name AS client, aw.title, ar.name AS artist, req.risk_score
FROM authentication_request req
INNER JOIN client c ON c.id = req.client_id
INNER JOIN artwork aw ON aw.id = req.artwork_id
INNER JOIN artist ar ON ar.id = aw.artist_id;

-- 8. 유료 리포트가 없는 요청 LEFT JOIN
SELECT req.id, aw.title, req.status
FROM authentication_request req
LEFT JOIN paid_report report ON report.request_id = req.id
JOIN artwork aw ON aw.id = req.artwork_id
WHERE report.id IS NULL;

-- 9. 상태별 요청 수
SELECT status, COUNT(*) AS request_count
FROM authentication_request
GROUP BY status;

-- 10. 고객 등급별 예상 감정 수수료 합계
SELECT c.tier, SUM(req.fee) AS fee_total
FROM authentication_request req
JOIN client c ON c.id = req.client_id
GROUP BY c.tier;

-- 11. 리포트 판정별 평균 위험도
SELECT report.verdict, AVG(req.risk_score) AS avg_risk
FROM paid_report report
JOIN authentication_request req ON req.id = report.request_id
GROUP BY report.verdict;

-- 12. 유료 리포트 매출 합계
SELECT SUM(price) AS paid_report_revenue
FROM paid_report;

-- 13. 평균 위험도보다 높은 요청
SELECT id, status, risk_score
FROM authentication_request
WHERE risk_score > (SELECT AVG(risk_score) FROM authentication_request);

-- 14. 고위험 미술품 검토 상태 업데이트
UPDATE authentication_request
SET status = 'reviewed'
WHERE risk_score >= 80 AND status = 'analyzing';

-- 15. 제출만 하고 위험도 0인 테스트 요청 삭제
DELETE FROM authentication_request
WHERE status = 'submitted' AND risk_score = 0;

-- 16. 인덱스 확인용 상태 검색
SELECT id, status, submitted_at
FROM authentication_request
WHERE status = 'paid_report_issued';
