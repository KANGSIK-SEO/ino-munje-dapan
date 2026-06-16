INSERT INTO client VALUES
(1, '김컬렉터', 'collector1@example.com', 'collector'),
(2, '서울갤러리', 'gallery@example.com', 'gallery'),
(3, '박소장', 'owner@example.com', 'basic'),
(4, '이큐레이터', 'curator@example.com', 'gallery'),
(5, '최아트', 'art@example.com', 'collector'),
(6, '정민수', 'minsu@example.com', 'basic'),
(7, '오민지', 'minji@example.com', 'collector'),
(8, '한서준', 'seojun@example.com', 'basic'),
(9, '윤갤러리', 'yoon-gallery@example.com', 'gallery'),
(10, '문아람', 'aram@example.com', 'collector');

INSERT INTO artist VALUES
(1, 'Vincent van Gogh', 1853, 'post-impressionism'),
(2, 'Pablo Picasso', 1881, 'cubism'),
(3, 'Claude Monet', 1840, 'impressionism'),
(4, 'Kim Whanki', 1913, 'abstract'),
(5, 'Lee Jung-seob', 1916, 'expressionism'),
(6, 'Park Soo-keun', 1914, 'modern korean'),
(7, 'Yayoi Kusama', 1929, 'contemporary'),
(8, 'Banksy', NULL, 'street art'),
(9, 'Henri Matisse', 1869, 'fauvism'),
(10, 'Joan Miro', 1893, 'surrealism');

INSERT INTO artwork VALUES
(1, 1, 'Sunflower Study', 1888, 'oil on canvas', 'private collection'),
(2, 2, 'Blue Guitar Fragment', 1903, 'oil on board', 'estate sale'),
(3, 3, 'Water Lily Morning', 1907, 'oil on canvas', 'gallery storage'),
(4, 4, 'Dot Composition', 1972, 'oil on cotton', 'collector note missing'),
(5, 5, 'Bull Family Sketch', 1954, 'paper and ink', 'inherited'),
(6, 6, 'Market Road', 1962, 'oil on panel', 'auction lot'),
(7, 7, 'Infinity Dot Trial', 1998, 'acrylic on canvas', 'certificate copy'),
(8, 8, 'Wall Rat Print', 2010, 'screen print', 'street edition'),
(9, 9, 'Red Room Variant', 1911, 'gouache', 'unknown provenance'),
(10, 10, 'Night Bird Draft', 1941, 'mixed media', 'dealer inventory');

INSERT INTO authentication_request VALUES
(1, 1, 1, '2026-06-01', 'paid_report_issued', 82, 49000),
(2, 2, 2, '2026-06-02', 'reviewed', 64, 89000),
(3, 3, 3, '2026-06-03', 'analyzing', 41, 49000),
(4, 4, 4, '2026-06-04', 'paid_report_issued', 27, 129000),
(5, 5, 5, '2026-06-05', 'submitted', 0, 49000),
(6, 6, 6, '2026-06-06', 'rejected', 93, 49000),
(7, 7, 7, '2026-06-07', 'paid_report_issued', 58, 89000),
(8, 8, 8, '2026-06-08', 'reviewed', 75, 49000),
(9, 9, 9, '2026-06-09', 'analyzing', 36, 129000),
(10, 10, 10, '2026-06-10', 'paid_report_issued', 21, 89000);

INSERT INTO paid_report VALUES
(1, 1, '2026-06-02', 'high_risk_fake', 49000, 'reports/EVR-0001.html'),
(2, 4, '2026-06-05', 'likely_authentic', 129000, 'reports/EVR-0004.html'),
(3, 7, '2026-06-08', 'needs_review', 89000, 'reports/EVR-0007.html'),
(4, 10, '2026-06-11', 'likely_authentic', 89000, 'reports/EVR-0010.html');
