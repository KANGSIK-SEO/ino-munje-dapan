INSERT INTO member VALUES
(1, '김하나', 'hana@example.com'), (2, '이두리', 'duri@example.com'),
(3, '박세진', 'sejin@example.com'), (4, '최네모', 'nemo@example.com');

INSERT INTO category VALUES
(1, '소설'), (2, '과학'), (3, 'IT'), (4, '역사');

INSERT INTO book VALUES
(1, 1, '작은 이야기', 'A작가', 3), (2, 1, '긴 여행', 'B작가', 2),
(3, 2, '쉬운 과학', 'C작가', 5), (4, 2, '별과 우주', 'D작가', 1),
(5, 3, '처음 SQL', 'E작가', 4), (6, 3, '파이썬 기초', 'F작가', 2),
(7, 4, '한국사 입문', 'G작가', 3), (8, 4, '세계사 산책', 'H작가', 2);

INSERT INTO rental VALUES
(1, 1, 5, '2026-06-01', NULL), (2, 1, 6, '2026-06-02', '2026-06-05'),
(3, 2, 1, '2026-06-03', NULL), (4, 3, 3, '2026-06-04', NULL),
(5, 4, 7, '2026-06-05', '2026-06-06');
