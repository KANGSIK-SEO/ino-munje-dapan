-- 1. 전체 회원 조회
SELECT * FROM member;

-- 2. 도서와 카테고리 함께 보기
SELECT b.title, c.name AS category
FROM book b
JOIN category c ON b.category_id = c.id;

-- 3. 대여 중인 책 보기
SELECT m.name, b.title, r.rented_at
FROM rental r
JOIN member m ON r.member_id = m.id
JOIN book b ON r.book_id = b.id
WHERE r.returned_at IS NULL;

-- 4. 카테고리별 책 수
SELECT c.name, COUNT(*) AS book_count
FROM category c
LEFT JOIN book b ON b.category_id = c.id
GROUP BY c.id, c.name;

-- 5. 회원별 대여 횟수
SELECT m.name, COUNT(r.id) AS rental_count
FROM member m
LEFT JOIN rental r ON r.member_id = m.id
GROUP BY m.id, m.name
ORDER BY rental_count DESC;

-- 6. 평균 재고보다 재고가 많은 책
SELECT title, stock
FROM book
WHERE stock > (SELECT AVG(stock) FROM book);
